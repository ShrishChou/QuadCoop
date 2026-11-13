"""Train ANYmal C + Spot to push one Stage 2 object together, with IPPO or MAPPO (Stages 3-4).

    python train_coop2.py --algo mappo --seed 0                  # new run logs/marl2/mappo_s0
    python train_coop2.py --algo ippo  --seed 0
    python train_coop2.py --algo mappo --seed 0 --resume         # continue it
    python train_coop2.py --algo mappo --check                   # build, warm start, a few steps, exit
    python train_coop2.py --algo mappo --partner-map --reward r5 --mean-clip 1.1 --bound-coef 0.01 \
        --entropy-coef 0.003 --run-name mappo_r6_s0                # r6: r5 + exploration fixes
    python train_coop2.py --algo mappo --scratch --partner-map --reward r5 --mean-clip 1.1 \
        --bound-coef 0.01 --entropy-coef 0.003 --run-name mappo_scratch_s0   # from the walkers only
    python train_coop2.py --algo mappo --pair anymal --partner-map --reward r7 ...   # two ANYmal C
    python train_coop2.py --algo mappo --pair anymal --partner-map --reward r7 --kl-ref 0.05 \
        --critic-warmup 500 --max-actor-lr 1e-4 --run-name mappo_aa_kl_s0   # anchored to Stage 2b
    python train_coop2.py --algo mappo --pair anymal --partner-map --reward r7 --contacts \
        --kl-ref 0.05 --kl-ramp 1000 --need-frac 0.5 --critic-warmup 500 --max-actor-lr 1e-4 \
        --run-name s4_aa_s0                                       # Stage 4: push from assigned contacts
    python train_coop2.py --algo mappo --pair anymal --partner-map --reward r7 --contacts \
        --reselect-s 3,6 --random-start 0.3 --need-frac 0.5 --resume --run-name s4b_aa_s0 ...
                                                                  # Stage 4b: contacts re-chosen as it goes
    (Stage 4c = the same with --off-contact soft, now the default: no deadlines, no ending for being off
    contact; a pull to the assigned contact and a cost per second off it; --off-contact terminate = 4/4b)

Stage 4 (--contacts): each episode both robots get a contact pair (quadcoop/contacts.py candidates;
spread / adjacent / random pair, --contact-mix) and start at it; the contacts are part of their
input; leaving a contact (> 0.5 m for 1 s) ends the episode as a failure. The success tolerance
follows its own curriculum (--tol-levels, loose -> 10 cm / 3 deg; the task levels wait for it).

The models come from evals/models.yaml (the roles walker_anymal, walker_spot, push2b_anymal,
push2b_spot; push2ctrl_* for --variant ctrl), resolved through evals/registry.yaml: each robot's
walker checkpoint and the env vars it was trained with (Spot's joint gains and history length),
and each robot's Stage 2 policy, whose registered walker must be the same one. What was used is
written to logs/marl2/<run>/inputs.yaml and into every checkpoint.
Checkpoints: logs/marl2/<run>/model_<iter>.pt; model_0.pt = the warm-started pair before any
update (the frozen-pair baseline).
"""

from __future__ import annotations

import argparse
import os
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))


def _pairs():
    """quadcoop/coop2/pairs.py, loaded as a plain file (importing the quadcoop package would read
    robot settings from the environment before set_env has set them)."""
    import importlib.util

    spec = importlib.util.spec_from_file_location("_qc_pairs", ROOT / "src" / "quadcoop" / "coop2" / "pairs.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def robot_of(pair: str | None = None) -> dict[str, str]:
    """slot -> robot type ("anymal_c" / "spot") for the pair (default: QUADCOOP_PAIR or mixed)."""
    return dict(_pairs().slots(pair))


ROBOT_OF = robot_of("mixed")  # the default pair (older callers)


def resolve_models(variant: str, pair: str = "mixed") -> dict:
    """The models from evals/models.yaml (a walker and a Stage 2 policy per robot type in the
    pair) + everything needed to rebuild their envs. policy is keyed by slot, walker_* by robot
    type."""
    import yaml

    from methods import EVALS, load, resolve

    role_of = _pairs().ROLE
    sel = yaml.safe_load((EVALS / "models.yaml").read_text()) or {}
    reg = load()
    out = {"selection": {}, "walker_ckpt": {}, "walker_env": {}, "policy": {}, "pair": pair}
    for a, robot in robot_of(pair).items():
        role = role_of[robot]
        w_role, p_role = f"walker_{role}", f"push2{variant}_{role}"
        if w_role not in sel or p_role not in sel:
            raise SystemExit(f"evals/models.yaml needs {w_role} and {p_role} "
                             f"(python scripts/select_models.py --set {p_role}=<id>)")
        w, p = resolve(sel[w_role], reg), resolve(sel[p_role], reg)
        if reg[sel[p_role]].get("walker") != sel[w_role]:
            raise SystemExit(f"{sel[p_role]} was trained on walker {reg[sel[p_role]].get('walker')}, but "
                             f"evals/models.yaml has {w_role}: {sel[w_role]}")
        for path in (w["checkpoint_abs"], p["checkpoint_abs"]):
            if not Path(path).exists():
                raise SystemExit(f"{path} not found (registered models live in logs/evals/<id>/)")
        out["selection"][w_role], out["selection"][p_role] = sel[w_role], sel[p_role]
        out["walker_ckpt"][robot] = w["checkpoint_abs"]
        out["walker_env"][robot] = dict(w["env_all"])
        out["policy"][a] = p["checkpoint_abs"]
    return out


def set_env(models: dict) -> None:
    """Env vars the two-robot env reads at import / build time."""
    os.environ["QUADCOOP_SHAPES"] = "v2"
    os.environ["QUADCOOP_PAIR"] = models.get("pair", "mixed")
    for k in ("QUADCOOP_WALKER_CKPT", "QUADCOOP_WALKER_HISTORY", "QUADCOOP_PUSH_FORCE", "QUADCOOP_SUCCESS_MODE"):
        os.environ.pop(k, None)
    for robot, path in models["walker_ckpt"].items():
        os.environ[f"QUADCOOP_WALKER_CKPT_{robot.upper()}"] = path
        env = models["walker_env"][robot]
        os.environ[f"QUADCOOP_WALKER_HISTORY_{robot.upper()}"] = str(env.get("QUADCOOP_WALKER_HISTORY", "0"))
        if robot == "spot":
            os.environ["QUADCOOP_SPOT_PROFILE"] = env.get("QUADCOOP_SPOT_PROFILE", "v1")
        override = os.environ.get(f"QUADCOOP_WALKER_OVERRIDE_{robot.upper()}", "")
        if override:  # a different walker for a test (e.g. a compliant walker under a v1-trained executor)
            if not Path(override).exists():
                raise SystemExit(f"QUADCOOP_WALKER_OVERRIDE_{robot.upper()}={override}: not found")
            os.environ[f"QUADCOOP_WALKER_CKPT_{robot.upper()}"] = str(Path(override).resolve())
            os.environ[f"QUADCOOP_WALKER_HISTORY_{robot.upper()}"] = os.environ.get(
                f"QUADCOOP_WALKER_OVERRIDE_HISTORY_{robot.upper()}", "0")
            models["walker_ckpt"][robot] = str(Path(override).resolve())
            models.setdefault("walker_override", {})[robot] = str(Path(override).resolve())
            print(f"[walker] {robot}: OVERRIDE {override} (the policies above it were trained on "
                  f"{models['selection'].get('walker_' + ('anymal' if robot == 'anymal_c' else robot), '?')})")


RULES = ("spread", "adjacent", "random", "wrench", "expert")


def parse_contact_mix(txt: str) -> tuple[float, ...]:
    """'1,1,1' / '1,1,1,2' (spread, adjacent, random[, wrench]) or 'wrench:2,spread:1' -> weights."""
    parts = [x.strip() for x in txt.split(",") if x.strip()]
    if all(":" in x for x in parts):
        w = dict.fromkeys(RULES, 0.0)
        for x in parts:
            k, v = x.split(":")
            if k not in w:
                raise SystemExit(f"--contact-mix: unknown rule {k!r} (rules: {', '.join(RULES)})")
            w[k] = float(v)
        out = tuple(w[r] for r in RULES)
        return out if out[4] > 0 else (out[:4] if out[3] > 0 else out[:3])
    out = tuple(float(x) for x in parts)
    if len(out) not in (3, 4, 5):
        raise SystemExit("--contact-mix needs 3-5 weights (spread, adjacent, random[, wrench[, expert]]) or name:weight pairs")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--algo", choices=("ippo", "mappo"), required=True)
    ap.add_argument("--variant", choices=("b", "ctrl"), default="b")
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot"), default="mixed",
                    help="which two robots: ANYmal C + Spot (mixed), two ANYmal C, two Spot "
                         "(quadcoop/coop2/pairs.py); both start from that type's Stage 2 policy")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--num-envs", type=int, default=4096)
    ap.add_argument("--max-iterations", type=int, default=6000, help="total (a resumed run stops here too)")
    ap.add_argument("--run-name", default=None, help="default <algo>[_ctrl]_s<seed>")
    ap.add_argument("--resume", action="store_true", help="continue the newest checkpoint of this run")
    ap.add_argument("--critic-warmup", type=int, default=None, help="default 100 (warm start), 0 (--scratch)")
    ap.add_argument("--scratch", action="store_true",
                    help="no Stage 2 warm start: random actors and critics on the frozen walkers")
    ap.add_argument("--kl-ref", type=float, default=0.0,
                    help="beta: penalty beta * KL(policy || its frozen Stage 2b policy) in the actor loss "
                         "(KL-regularized fine-tuning; 0 = off; not with --scratch)")
    ap.add_argument("--kl-partner-scale", type=float, default=1.0,
                    help="< 1: the KL anchor is multiplied by this while the partner is within 1.5 m, back to "
                         "full beyond 3 m (partner-aware anchor: stay 2b alone, free to change together)")
    ap.add_argument("--start-around", action="store_true",
                    help="robots start anywhere around the object (>= 60 deg apart) instead of behind it")
    ap.add_argument("--effort", action="store_true",
                    help="force_track: each robot observes an absolute push target (its share of what slides the object) "
                         "and the contact force it applies; the minimal reward's contact work is paid only up to the "
                         "target (needs --reward rmin --push-cmd --contacts)")
    ap.add_argument("--contact-sense", action="store_true",
                    help="contact curriculum: each robot observes the contact force it applies to the object, that force "
                         "along its push direction, touching, and the object motion the planner wants (7 inputs, last)")
    ap.add_argument("--acq-bonus", type=float, default=0.0,
                    help="bonus for reaching real contact: on contact, 30 N+ along the push direction for 0.5 s; once per "
                         "assignment, re-armed by a new assignment only after 0.1 m of pose progress; 0 = off")
    ap.add_argument("--time-cost", type=float, default=0.0, help="team cost per second (0 = off)")
    ap.add_argument("--touch-cost", type=float, default=0.0,
                    help="team cost per second while any part of one robot touches the other (the minimal reward has "
                         "none: nothing stopped a robot shoving its partner aside); 0 = off")
    ap.add_argument("--over-push-w", type=float, default=1.0,
                    help="--effort: weight of the cost for pushing past 1.5 x the push target (per second, per robot)")
    ap.add_argument("--turn-frac", type=float, default=0.0,
                    help="turn practice: share of training episodes that are a turn in place (the goal within 0.3 m, "
                         "heading off 15-90 deg either way, capped by symmetry); evaluations unchanged")
    ap.add_argument("--need-frac", type=float, default=0.0,
                    help="share of training episodes with a wide object (long, arch, dumbbell, T) above "
                         "--need-mass kg, i.e. one robot alone cannot do it (evaluations unchanged)")
    ap.add_argument("--need-mass", type=float, default=45.0)
    ap.add_argument("--contacts", action="store_true",
                    help="Stage 4: assigned contact pairs as inputs, robots start at them, leaving one fails")
    ap.add_argument("--contact-mix", default="1,1,1",
                    help="weights of the contact rules: 3 or 4 numbers (spread, adjacent, random[, wrench]) or "
                         "name:weight pairs, e.g. wrench:2,spread:1,random:1")
    ap.add_argument("--contact-start-at", type=float, default=0.7,
                    help="share of robots starting at their contact (the rest at its approach point)")
    ap.add_argument("--drift-dist", type=float, default=0.35,
                    help="on contact = the front within this many m of the contact point ...")
    ap.add_argument("--drift-heading", type=float, default=45.0,
                    help="... and facing the contact's push direction within this many deg (another face is off contact)")
    ap.add_argument("--reselect-s", default="0",
                    help="Stage 4b: re-apply the contact rule every so many seconds, 'lo,hi' (uniform) or one value; "
                         "0 = contacts fixed for the episode")
    ap.add_argument("--random-start", type=float, default=0.0,
                    help="share of robots starting anywhere around the object (they walk to their contact)")
    ap.add_argument("--off-contact", choices=("soft", "terminate"), default="soft",
                    help="soft: no deadlines and no ending for being off contact; pulled to the contact (potential) "
                         "and a cost per second off a reached contact; terminate: Stage 4 / 4b rules")
    ap.add_argument("--off-contact-cost", type=float, default=1.0, help="soft: per second off a reached contact")
    ap.add_argument("--contact-approach", type=float, default=1.0, help="soft: weight of the pull to the assigned contact")
    ap.add_argument("--critic-warmup-resume", type=int, default=0,
                    help="critic-only iterations after --resume (use when the rewards changed, e.g. 100)")
    ap.add_argument("--guide", action="store_true",
                    help="Stage 4d: a route to the contact as 6 more inputs, the pull pays for shortening the route, "
                         "touching the object off the contact costs --bump-cost per second (needs --contacts, soft)")
    ap.add_argument("--bump-cost", type=float, default=1.0)
    ap.add_argument("--disturb-frac", type=float, default=0.0,
                    help="share of training episodes in which the object is moved and turned by script for a few seconds")
    ap.add_argument("--push-cmd", action="store_true",
                    help="Stage 4e (needs --guide): each robot's push direction recomputed every step from the "
                         "remaining error (4 more inputs), on-contact judged against it, pose_progress / "
                         "motion_credit / walk_cost rewards, partner-aware route")
    ap.add_argument("--walk-cost", type=float, default=0.3, help="--push-cmd: per second on the way to a new contact")
    ap.add_argument("--exec-v2", action="store_true",
                    help="Phase 2 executor (needs --push-cmd): a phase command (walk / hold / push) and the team-ready "
                         "flag as 4 more inputs, motion credit only when told to push, hold_cost while told to hold")
    ap.add_argument("--hold-rand", type=float, default=0.3,
                    help="--exec-v2: share of contact arrivals told to hold 0.5-4 s whatever the partner does")
    ap.add_argument("--hold-cost", type=float, default=1.0, help="--exec-v2: hold_cost weight")
    ap.add_argument("--credit-press", type=float, default=0.0,
                    help="--push-cmd, r7: motion_credit only while the robot touches the object with at least this many N "
                         "(0 = a front within 8 cm is enough, as Stage 4e)")
    ap.add_argument("--work-w", type=float, default=3.0, help="--reward rmin: contact_work weight")
    ap.add_argument("--reselect-min-dist", type=float, default=0.15,
                    help="no contact re-choice with the object this close to its goal (m); 0 = re-choose anywhere")
    ap.add_argument("--init-from", default=None,
                    help="start from this trainer checkpoint, expanding its networks for new inputs (e.g. a Stage 4b/4c "
                         "model for --guide); ignored once the run has its own checkpoints (then --resume continues it)")
    ap.add_argument("--tol-levels", default=None,
                    help="success-tolerance curriculum 'pos_m:yaw_deg,...' loose -> fine; 'none' = fixed "
                         "10 cm / 3 deg; default with --contacts: 0.30:15,0.20:10,0.15:6,0.12:4,0.10:3")
    ap.add_argument("--kl-ramp", type=int, default=0,
                    help="> 0: the KL anchor's beta falls linearly to 0 over this many iterations")
    ap.add_argument("--actor-lr", type=float, default=None,
                    help="starting actor learning rate (adapted to the KL target); default 1e-4, 3e-4 with --scratch")
    ap.add_argument("--max-actor-lr", type=float, default=None,
                    help="cap on the adapted actor learning rate; default 3e-4, 1e-3 with --scratch")
    ap.add_argument("--partner-map", action="store_true", help="partner footprint as a 2nd map channel")
    ap.add_argument("--reward", choices=("r3", "r4", "r5", "r7", "r8", "rmin"), default="r3",
                    help="r4: no per-robot behind-the-object term, exponential proximity penalty below 0.6 m; "
                         "r5: r4 + approach reward only for getting closer, team time cost, stronger "
                         "push_along and yaw_progress; r7: outcome-based: goal-error cost per second, "
                         "failure pays the time left, push_credit, proximity on the body gap; "
                         "r8: r7 with work_credit (contact force x object speed) and touch-only penalty "
                         "(quadcoop/coop2/env_cfg.py)")
    ap.add_argument("--entropy-coef", type=float, default=0.0)
    ap.add_argument("--residual", default=None,
                    help="residual execution pilot (docs/residual_pilot.md): this executor checkpoint is the frozen base; "
                         "each actor learns a bounded correction (zero at the start) from extra force / motion inputs; "
                         "critic and curriculum state carried over")
    ap.add_argument("--resid-scale", type=float, default=0.3, help="--residual: correction bound (command units)")
    ap.add_argument("--resid-scale-axes", default="",
                    help="--residual: per-axis correction bound 'vx,vy,wz' (overrides --resid-scale), e.g. 1.2,0.3,0.3 "
                         "so the forward correction can bring a saturated forward command to a stop")
    ap.add_argument("--track", action="store_true",
                    help="--residual: request-tracking pilot (docs/request_tracking.md): per-robot force-target band "
                         "cost and the targets as correction inputs")
    ap.add_argument("--track-w", type=float, default=0.5, help="--track: weight of the tracking cost (per second)")
    ap.add_argument("--short-tasks", action="store_true",
                    help="one level of 1-2 m segments, goal turn up to +-30 deg, 25 s episodes (with --fixed-level 0)")
    ap.add_argument("--resid-std", type=float, default=0.15, help="--residual: initial exploration std")
    ap.add_argument("--resid-objects", default="", help="--residual: shapes with the correction enabled (default all)")
    ap.add_argument("--resid-gate-dist", type=float, default=0.0,
                    help="--residual: also gate the correction per robot to contact distance <= this (m; 0 = object "
                         "gate only)")
    ap.add_argument("--resid-compose", choices=("clipped", "raw"), default="clipped",
                    help="--residual: correction added to the clipped base command (default) or the raw base output")
    ap.add_argument("--resid-check", type=int, default=0,
                    help="--residual: run the command-interface check for this many steps per pass, then exit")
    ap.add_argument("--shape-bias", default="",
                    help="training shape mix weights, e.g. beam:8,cylinder:1.5,asym:0 (others 1; 0 = never drawn). "
                         "Applied after eligibility: a held-out shape needs --train-shapes")
    ap.add_argument("--train-shapes", default="",
                    help="shapes eligible in training, e.g. beam (default: the Stage 2 split, which holds out beam, "
                         "l_shape, asym, u_channel, plus)")
    ap.add_argument("--train-mass", default="", help="fixed training mass window lo,hi kg (default: the level's)")
    ap.add_argument("--fixed-difficulty", action="store_true",
                    help="hold the curriculum: level and tolerance fixed, uniform shape weights, no replayed levels")
    ap.add_argument("--fixed-level", type=int, default=None,
                    help="--fixed-difficulty: the level to hold (default: the one the warm start carries)")
    ap.add_argument("--min-std", type=float, default=0.2, help="action noise floor")
    ap.add_argument("--max-std-factor", type=float, default=1.0,
                    help="action noise may not rise above this x its warm-start value")
    ap.add_argument("--mean-clip", type=float, default=0.0,
                    help="> 0: sample actions around the policy mean clamped to +-this, gradient passed "
                         "straight through, so noise acts on saturated outputs (r6: 1.1; 0 = off)")
    ap.add_argument("--bound-coef", type=float, default=0.0,
                    help="penalty on the raw policy mean past +-mean-clip (r6: 0.01; 0 = off)")
    ap.add_argument("--start-level", type=int, default=0)
    ap.add_argument("--video-interval", type=int, default=500, help="training video every N iterations (0 = off)")
    ap.add_argument("--video-length", type=int, default=1000, help="steps per training video (50 per second)")
    ap.add_argument("--logger", choices=("wandb", "tensorboard"), default="tensorboard")
    ap.add_argument("--wandb-project", default="quadcoop")
    ap.add_argument("--device", default=None)
    ap.add_argument("--check", action="store_true", help="build, warm start, run 2 iterations, exit")
    a = ap.parse_args()

    if a.kl_ref > 0 and a.scratch:
        raise SystemExit("--kl-ref anchors to the Stage 2 policies: it does not apply with --scratch")
    if a.tol_levels is None:
        a.tol_levels = "0.30:15,0.20:10,0.15:6,0.12:4,0.10:3" if a.contacts else "none"
    tol_levels = () if a.tol_levels == "none" else tuple(tuple(float(v) for v in x.split(":"))
                                                        for x in a.tol_levels.split(","))
    contact_mix = parse_contact_mix(a.contact_mix)
    resid_objects = tuple(x.strip() for x in a.resid_objects.split(",") if x.strip())
    shape_bias = tuple((x.split(":")[0].strip(), float(x.split(":")[1])) for x in a.shape_bias.split(",") if x.strip())
    train_shapes = tuple(x.strip() for x in a.train_shapes.split(",") if x.strip())
    train_mass = tuple(float(x) for x in a.train_mass.split(",")) if a.train_mass else ()
    if train_mass and len(train_mass) != 2:
        raise SystemExit("--train-mass lo,hi")
    if (a.fixed_level is not None) != a.fixed_difficulty:
        raise SystemExit("--fixed-difficulty and --fixed-level go together (the level is declared, not inherited)")
    if a.residual and not (a.contacts and a.push_cmd and a.guide):
        raise SystemExit("--residual builds on the Stage 4e executor (--contacts --guide --push-cmd)")
    rs = [float(x) for x in a.reselect_s.split(",")]
    reselect_s = (rs[0], rs[-1])
    if a.push_cmd and not a.guide:
        raise SystemExit("--push-cmd builds on --guide (Stage 4d)")
    if a.exec_v2 and not a.push_cmd:
        raise SystemExit("--exec-v2 builds on --push-cmd (Stage 4e)")
    if a.effort and a.reward != "rmin":
        raise SystemExit("--effort needs --reward rmin (with --push-cmd --contacts)")
    if a.reward == "rmin" and not (a.push_cmd and a.contacts):
        raise SystemExit("--reward rmin builds on Stage 4e (--contacts --guide --push-cmd)")
    if a.critic_warmup is None:
        a.critic_warmup = 0 if a.scratch else 100
    if a.actor_lr is None:
        a.actor_lr = 3e-4 if a.scratch else 1e-4
    if a.max_actor_lr is None:
        a.max_actor_lr = 1e-3 if a.scratch else 3e-4
    models = resolve_models(a.variant, a.pair)
    set_env(models)
    import torch
    import yaml

    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    contact_txt = ""
    if a.contacts:
        resel = f"{reselect_s[0]:g}-{reselect_s[1]:g} s" if reselect_s[1] > 0 else "never"
        soft_txt = f" (cost {a.off_contact_cost:g}/s, pull {a.contact_approach:g})" if a.off_contact == "soft" else ""
        if a.guide:
            soft_txt += f", GUIDED (bump cost {a.bump_cost:g}/s, disturbed episodes {a.disturb_frac:g})"
        if a.push_cmd:
            soft_txt += f", PUSH DIRECTIONS (walk cost {a.walk_cost:g}/s)"
        if a.exec_v2:
            soft_txt += f", EXECUTOR V2 (random holds {a.hold_rand:g}, hold cost {a.hold_cost:g}/s)"
        if a.credit_press > 0:
            soft_txt += f", MOTION CREDIT ONLY WHILE PRESSING ({a.credit_press:g} N+)"
        if a.reward == "rmin":
            soft_txt += f", MINIMAL REWARD (progress, success, failure, falls, contact approach, contact work x{a.work_w:g})"
        if a.turn_frac > 0:
            soft_txt += f", TURN PRACTICE ({a.turn_frac:g} of episodes turn in place)"
        if a.contact_sense:
            soft_txt += ", CONTACT SENSE (contact force, touching, wanted object motion: 7 inputs)"
        if a.acq_bonus > 0 or a.time_cost > 0:
            soft_txt += f", contact-acquired bonus {a.acq_bonus:g}, time cost {a.time_cost:g}/s"
        if a.touch_cost > 0:
            soft_txt += f", robot-robot touch cost {a.touch_cost:g}/s"
        if a.effort:
            soft_txt += f", PUSH EFFORT (absolute push targets + force feedback; work paid up to the target, over-push cost {a.over_push_w:g})"
        if a.reselect_min_dist != 0.15:
            soft_txt += f", re-choice down to {a.reselect_min_dist:g} m from the goal"
        contact_txt = (f"CONTACTS (mix {contact_mix}, start at {a.contact_start_at:g}, on contact = {a.drift_dist:g} m / "
                       f"{a.drift_heading:g} deg, re-select {resel}, random start {a.random_start:g}, off contact "
                       f"{a.off_contact}{soft_txt})  ")
    run = a.run_name or f"{a.algo}{'_ctrl' if a.variant == 'ctrl' else ''}_s{a.seed}"
    log_dir = ROOT / "logs" / "marl2" / (run + ("_check" if a.check else ""))
    print(f"run {run}  algo {a.algo}  pair {a.pair}  variant {a.variant}  seed {a.seed}  device {device}  "
          f"partner map {a.partner_map}  rewards {a.reward}  entropy {a.entropy_coef:g}  mean clip {a.mean_clip:g}  "
          f"bound {a.bound_coef:g}  kl_ref {a.kl_ref:g} (partner scale {a.kl_partner_scale:g})  "
          f"start {'around' if a.start_around else 'behind'}  need_frac {a.need_frac:g}  "
          f"{contact_txt}"
          f"{f'tolerance curriculum {tol_levels}  ' if tol_levels else ''}{f'kl ramp {a.kl_ramp}  ' if a.kl_ramp else ''}"
          f"{'FROM SCRATCH' if a.scratch else 'warm start from Stage 2b'}")
    for k, v in models["selection"].items():
        print(f"  {k:15s} {v}")

    if a.track and not a.residual:
        raise SystemExit("--track needs --residual")
    if a.resid_scale_axes and len(a.resid_scale_axes.split(",")) != 3:
        raise SystemExit("--resid-scale-axes takes three values: vx,vy,wz")
    random.seed(a.seed)
    torch.manual_seed(a.seed)
    import quadcoop  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv

    from quadcoop.coop2.env_cfg import make_coop2_env_cfg
    from quadcoop.coop2.marl import MarlCfg, MarlTrainer

    env_cfg = make_coop2_env_cfg(a.variant, partner_map=a.partner_map, reward_set=a.reward,
                                 start_mode="around" if a.start_around else "behind",
                                 need_frac=a.need_frac, need_mass=a.need_mass, contacts=a.contacts,
                                 tol_levels=tol_levels, contact_mix=contact_mix, contact_start_at=a.contact_start_at,
                                 drift_dist=a.drift_dist, drift_heading_deg=a.drift_heading,
                                 reselect_s=reselect_s, random_start=a.random_start, off_contact=a.off_contact,
                                 off_contact_cost=a.off_contact_cost, contact_approach=a.contact_approach,
                                 guide=a.guide, bump_cost=a.bump_cost, disturb_frac=a.disturb_frac,
                                 push_cmd=a.push_cmd, walk_cost=a.walk_cost, reselect_min_dist=a.reselect_min_dist,
                                 exec_v2=a.exec_v2, hold_rand=a.hold_rand, hold_cost_w=a.hold_cost,
                                 credit_press=a.credit_press, work_w=a.work_w, effort=a.effort,
                                 over_push_w=a.over_push_w, contact_sense=a.contact_sense,
                                 acq_bonus=a.acq_bonus, time_cost=a.time_cost, touch_cost=a.touch_cost,
                                 resid=bool(a.residual), resid_objects=resid_objects, shape_bias=shape_bias,
                                 resid_gate_dist=a.resid_gate_dist, train_shapes=train_shapes, train_mass=train_mass,
                                 fixed_difficulty=a.fixed_difficulty, track=a.track, track_w=a.track_w,
                                 short_tasks=a.short_tasks)
    env_cfg.scene.num_envs = a.num_envs
    env_cfg.seed = a.seed
    env_cfg.commands["goal"].start_level = a.start_level
    env_cfg.commands["goal"].turn_frac = a.turn_frac
    if a.fixed_difficulty:  # the very first episodes (drawn at construction, before the warm start) match too
        env_cfg.commands["goal"].start_level = a.fixed_level
        env_cfg.commands["goal"].tol_start_finest = True
    env = ManagerBasedRlEnv(cfg=env_cfg, device=device)
    cfg = MarlCfg(algo=a.algo, variant=a.variant, num_envs=a.num_envs, seed=a.seed,
                  max_iterations=2 if a.check else a.max_iterations,
                  critic_warmup=1 if a.check else a.critic_warmup, init={} if a.scratch else dict(models["policy"]),
                  scratch=a.scratch, actor_learning_rate=a.actor_lr, max_actor_learning_rate=a.max_actor_lr,
                  entropy_coef=a.entropy_coef, max_std_factor=a.max_std_factor,
                  mean_clip=a.mean_clip, bound_coef=a.bound_coef, kl_ref=a.kl_ref,
                  kl_partner_scale=a.kl_partner_scale, start_mode="around" if a.start_around else "behind",
                  need_frac=a.need_frac, contacts=a.contacts, contact_mix=contact_mix,
                  contact_start_at=a.contact_start_at, tol_levels=tol_levels, kl_ramp=a.kl_ramp,
                  drift_dist=a.drift_dist, drift_heading_deg=a.drift_heading,
                  reselect_s=reselect_s, random_start=a.random_start, off_contact=a.off_contact,
                  off_contact_cost=a.off_contact_cost, contact_approach=a.contact_approach,
                  critic_warmup_resume=a.critic_warmup_resume, guide=a.guide, bump_cost=a.bump_cost,
                  disturb_frac=a.disturb_frac, init_from=a.init_from or "", push_cmd=a.push_cmd,
                  walk_cost=a.walk_cost, reselect_min_dist=a.reselect_min_dist,
                  exec_v2=a.exec_v2, hold_rand=a.hold_rand if a.exec_v2 else 0.0, hold_cost_w=a.hold_cost,
                  credit_press=a.credit_press, work_w=a.work_w, turn_frac=a.turn_frac, effort=a.effort,
                  over_push_w=a.over_push_w if a.effort else 0.0,
                  contact_sense=a.contact_sense, acq_bonus=a.acq_bonus, time_cost=a.time_cost, touch_cost=a.touch_cost,
                  partner_map=a.partner_map, reward_set=a.reward, pair=a.pair,
                  video_interval=0 if a.check else a.video_interval, video_length=a.video_length,
                  inputs=models["selection"], residual=a.residual or "", resid_scale=a.resid_scale,
                  resid_std=a.resid_std, resid_objects=resid_objects, shape_bias=shape_bias, min_std=a.min_std,
                  resid_compose=a.resid_compose, resid_gate_dist=a.resid_gate_dist, train_shapes=train_shapes,
                  train_mass=train_mass, fixed_difficulty=a.fixed_difficulty,
                  resid_scale_axes=tuple(float(x) for x in a.resid_scale_axes.split(",")) if a.resid_scale_axes else (),
                  track=a.track, track_w=a.track_w, short_tasks=a.short_tasks)
    trainer = MarlTrainer(env, cfg, log_dir, device, logger="tensorboard" if a.check else a.logger,
                          wandb_project=a.wandb_project)
    last = MarlTrainer.newest(log_dir)
    if a.resume and last is not None:
        trainer.load(last)
    else:
        if last is not None and not a.check:
            raise SystemExit(f"{log_dir} already has checkpoints: pass --resume, or another --run-name")
        if a.scratch:
            trainer.init_scratch()
        elif a.residual:
            trainer.init_residual(a.residual)
        elif a.init_from:
            trainer.init_from(a.init_from)
        else:
            trainer.warm_start(models["policy"])
    if a.fixed_difficulty:  # re-apply the declared settings after any warm start / resume, and check the
        g_ = env.command_manager.get_term("goal")  # episodes already running were drawn with them
        g_.level = a.fixed_level
        if getattr(g_, "tol_table", None) is not None:
            g_.tol_level = len(g_.cfg.tol_levels) - 1
            assert bool((g_.env_tol_level == g_.tol_level).all()), "fixed difficulty: episodes at another tolerance"
        assert bool((g_.env_level == a.fixed_level).all()), "fixed difficulty: episodes at another level"
        print(f"[marl2] fixed difficulty: level {g_.level}, tolerance level {getattr(g_, 'tol_level', 0)} (finest), "
              f"mass window {train_mass or 'the level'}, shapes {train_shapes or 'Stage 2 split'}")
    if a.resid_check:
        if not a.residual:
            raise SystemExit("--resid-check needs --residual")
        rep = trainer.check_residual(steps=a.resid_check)
        raise SystemExit(0 if rep["pass"] else 1)
    if a.check:
        cfg.max_iterations = trainer.it + 2  # a check always runs 2 iterations, wherever it starts
    if a.kl_ref > 0:
        trainer.build_refs(models["policy"])
    (log_dir / "inputs.yaml").write_text(yaml.safe_dump({"run": run, "algo": a.algo, "variant": a.variant,
                                                         "partner_map": a.partner_map, "reward_set": a.reward,
                                                         "scratch": a.scratch, "contacts": a.contacts,
                                                         "tol_levels": [list(x) for x in tol_levels],
                                                         "seed": a.seed, **models}, sort_keys=False, width=120))
    print(f"[marl2] reward terms: team {[trainer.term_names[i] for i in trainer.team_idx]}")
    for ag, ix in trainer.own_idx.items():
        print(f"[marl2]               {ag} {[trainer.term_names[i] for i in ix]}")
    if trainer.it >= cfg.max_iterations:
        print(f"{log_dir} is already at iteration {trainer.it} (target {cfg.max_iterations})")
        return 0
    trainer.learn()
    env.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
