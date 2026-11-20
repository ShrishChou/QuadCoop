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
import json
import math
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
        if robot == "spot_arm":  # RAI's released walker (quadcoop/robots/spot_arm.py); no Stage 2 policy for this body
            out["selection"]["walker_spot_arm"] = "RAI judo spot_locomotion.onnx (frozen; QUADCOOP_JUDO)"
            continue
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


def _obs_study_selfcheck(env, trainer) -> None:
    """--check with --geom-obs / --hist-obs (docs/obs_study.md): the nearest surface point lies on the true shape
    (its signed distance ~0), the normal is a unit vector pointing away from the object, the new inputs are finite,
    and the history fills at 10 Hz with its validity mask; then 12 steps of zero action."""
    import torch
    from quadcoop.coop2 import mdp
    from quadcoop.stage2 import profiles as pf
    g = env.command_manager.get_term("goal")
    parts, kinds, rest = g.active()
    for r in mdp.AGENTS:
        dist, s_w, n_w, s_o, p_w = g.surface_geometry(r)
        on = pf.point_distance(parts, kinds, rest, s_o).abs()
        near = dist < 1.5
        out = ((p_w - s_w) * n_w).sum(-1) * dist.sign()  # bumper on the outward side when outside (>= 0)
        print(f"[obs-check] {r}: |sd(nearest point)| median {on[near].median():.4f} m, p95 {on[near].quantile(0.95):.4f} "
              f"(n {int(near.sum())}); |normal| {torch.linalg.norm(n_w, dim=-1).min():.3f}-"
              f"{torch.linalg.norm(n_w, dim=-1).max():.3f}; outward frac {(out >= -1e-3).float().mean():.3f}; "
              f"distance {dist.min():.2f}..{dist.max():.2f} m", flush=True)
    n = env.num_envs
    act = torch.zeros(n, env.action_manager.total_action_dim, device=env.device)
    for _ in range(12):
        env.step(act)
    ob = env.observation_manager.compute()
    for k_, v in ob.items():
        if k_.startswith(("actor_", "state_")):
            print(f"[obs-check] {k_}: {tuple(v.shape)} finite {bool(torch.isfinite(v).all())}", flush=True)
    if g.cfg.hist_obs:
        vm = g.ihist_valid.mean(0)
        print(f"[obs-check] history valid fraction per slot (newest first): {[round(float(x), 2) for x in vm]}", flush=True)
        h = mdp.interaction_history_obs(env, mdp.AGENTS[0])
        print(f"[obs-check] history input {tuple(h.shape)}, |max| {h.abs().max():.2f}", flush=True)
    if g.cfg.hist_obs or True:
        c = mdp.contact_geom_obs(env, mdp.AGENTS[0]) if "contact_geom" in env.observation_manager.active_terms[f"actor_{mdp.AGENTS[0]}"] else None
        if c is not None:
            print(f"[obs-check] contact geometry input {tuple(c.shape)}, first env {[round(float(x), 2) for x in c[0]]}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--algo", choices=("ippo", "mappo"), required=True)
    ap.add_argument("--variant", choices=("b", "ctrl"), default="b")
    ap.add_argument("--bc-data", default="", help="demonstrations (scripts/spot_arm/collect_demos.py): actors cloned, "
                    "then an imitation loss during PPO")
    ap.add_argument("--bc-coef", type=float, default=0.0, help="imitation loss weight at iteration 0")
    ap.add_argument("--bc-iters", type=int, default=0, help="the imitation weight fades linearly to 0 by this iteration")
    ap.add_argument("--bc-pretrain-steps", type=int, default=0, help="behaviour-cloning steps before PPO")
    ap.add_argument("--bc-keep-norm", action="store_true",
                    help="keep the warm-started actors' observation normalizers (do not fit them to the demonstrations)")
    ap.add_argument("--turn-signs", action="store_true",
                    help="goal heading change -1 or +1 x the --pilot-level value (turn in place)")
    ap.add_argument("--start-opposite", action="store_true",
                    help="one robot starts behind the object, one in front (turn in place)")
    ap.add_argument("--arm-hold-steps", type=int, default=0, help="--arm hand_rate: latch the arm actions this many steps")
    ap.add_argument("--hand-obs", action="store_true",
                    help="--pair spot_arm: actors also read the hand point (measured, commanded) and the extension")
    ap.add_argument("--arm", choices=("stowed", "learned", "hand", "hand_rate"), default="stowed",
                    help="--pair spot_arm: each robot's arm held stowed (3 actions per robot) or policy-controlled "
                         "(learned: 9, + six rate-limited arm joint targets; hand: 7, + hand point and extension)")
    ap.add_argument("--pilot-level", default="",
                    help="one level row replacing the level table, 11 comma-separated values: d_lo, d_hi, robot "
                         "spread deg, behind offset deg, object start yaw deg, goal yaw change deg, pos tol m, yaw tol "
                         "deg, hold s, max mass, min mass (use with --fixed-difficulty --fixed-level 0)")
    ap.add_argument("--extra-levels", default="",
                    help="further level rows after --pilot-level, ';'-separated (same 11 columns); used by --level-mix")
    ap.add_argument("--level-mix", default="",
                    help="fixed level-mix schedule over the levels, e.g. 0:0.5,0.5,0;600:0.25,0.45,0.3 (start iteration: "
                         "weights); each phase reassigns every env a level and redraws object masses in its window")
    ap.add_argument("--solo-agent", type=int, default=-1,
                    help="solo control: train only robot k (0/1); the other is parked 40 m away with zero actions")
    ap.add_argument("--pilot-episode-s", type=float, default=0.0, help="episode length with --pilot-level")
    ap.add_argument("--dyaw-choices", action="store_true",
                    help="goal heading change is -1, 0 or +1 x the level's value, equally often (left / straight / right)")
    ap.add_argument("--pair", choices=("mixed", "anymal", "spot", "spot_arm", "anymal_arm", "anymal3"), default="mixed",
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
    ap.add_argument("--goal-credit", action="store_true",
                    help="r7: replace push_credit (trunk front on the object) with goal_motion_credit: the object's "
                         "motion toward its goal pose (travel + turning), paid while any part (arm included) touches it")
    ap.add_argument("--align-bonus", type=float, default=1.0,
                    help="--goal-credit: pay x (1 + this x cos(object motion, wanted motion))")
    ap.add_argument("--arm-bonus", type=float, default=0.0,
                    help="--goal-credit: pay x (1 + this) while the arm touches the object (Spot-arm)")
    ap.add_argument("--roll-ratio", type=float, default=0.0,
                    help="contact planner's rolling model for lying cylinders (goal command roll_ratio; 0 = isotropic, "
                         "docs/planner_cylinder.md)")
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
    ap.add_argument("--std-cap", type=float, default=0.0,
                    help="> 0: action noise never above this (applied after any warm start / init, current noise clamped)")
    ap.add_argument("--geom-obs", action="store_true",
                    help="pair inputs: explicit contact geometry for self and partner (docs/obs_study.md)")
    ap.add_argument("--hist-obs", action="store_true",
                    help="pair inputs: 1 s of interaction history at 10 Hz with a validity mask (docs/obs_study.md)")
    ap.add_argument("--yaw-gate", type=float, default=1.5,
                    help="yaw_progress (signed heading progress) only within this many m of the goal; 0 = everywhere")
    ap.add_argument("--yaw-w", type=float, default=0.0, help="> 0: yaw_progress weight (default 1 for r5/r7/r8, else 0.5)")
    ap.add_argument("--action-rate-w", type=float, default=0.05, help="penalty weight on the change of each robot's actions")
    ap.add_argument("--action-limit-w", type=float, default=0.02, help="penalty weight on actions past their range")
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
    # -- next wave (docs/next_wave.md): matched IPPO / MAPPO arms, fixed task bank --------------------------------
    ap.add_argument("--init-actors", default=None,
                    help="both actors (weights, normalizers, action noise) from this trainer checkpoint of either "
                         "algorithm; critics and optimizers fresh (pair with --critic-warmup-resume)")
    # -- actor schedules and shared actor (docs/actor_schedule.md) ------------------------------------------------
    ap.add_argument("--actor-schedule", default="",
                    help="joint (both actors learn: the matched control) | alt:<N> (one actor at a time, N-iteration "
                         "blocks, first robot first) | only:<agent> (the other stays exactly as initialised)")
    ap.add_argument("--shared-actor", action="store_true",
                    help="one actor for both robots (needs a checkpoint with identical actors, "
                         "scripts/make_shared_ckpt.py): parameters tied, both robots' samples pooled, one optimizer")
    ap.add_argument("--schedule-check", type=int, default=0, metavar="N",
                    help="run N iterations and check after each that exactly the scheduled actors changed (weights, "
                         "normalizer, noise, optimizer state, lr) and, with --shared-actor, that the robots' actors "
                         "stay identical; writes schedule_check.json, exit 0 / 1")
    ap.add_argument("--oppose-cost", type=float, default=0.0,
                    help="opposing-force arm (docs/opposing_force.md): per robot, weight of the cost of pushing "
                         "against the wanted object motion (mdp.opposing_power)")
    ap.add_argument("--cancel-cost", type=float, default=0.0,
                    help="opposing-force arm: team weight of the cost of the robots' forces cancelling "
                         "(mdp.force_cancellation)")
    ap.add_argument("--swap-starts", action="store_true",
                    help="exchange the two robots' start tuples (bearing, gap, yaw noise) with probability 0.5 at "
                         "every reset, after any task-bank replay")
    ap.add_argument("--transfer-check", default=None, metavar="OBS_FILE",
                    help="with --init-actors: compare the actors with the source on the observations saved in "
                         "OBS_FILE (collected under the source policy if missing), before any update; exit 0 / 1")
    ap.add_argument("--task-bank", choices=("uniform", "sgs"), default=None,
                    help="resets draw from the fixed bank --task-bank-file: uniformly or success-guided")
    ap.add_argument("--task-bank-file", default=None, help="the bank (written by --bank-make)")
    ap.add_argument("--bank-make", action="store_true",
                    help="draw the bank with the training rule (this run's env and seed), save --task-bank-file, "
                         "check its replay, exit")
    ap.add_argument("--bank-check", action="store_true", help="replay-check --task-bank-file on this env, exit")
    ap.add_argument("--bank-per-env", type=int, default=16, help="--bank-make: tasks per env slot")
    ap.add_argument("--bank-seed", type=int, default=9100, help="--bank-make: draw seed (not an evaluation seed)")
    ap.add_argument("--bank-remix", default=None, metavar="SRC_BANK",
                    help="write --task-bank-file as a copy of SRC_BANK with some tasks' robot bearings set to the "
                         "--bank-mix formations (docs/mixed_start.md), re-record and replay-check every column, exit")
    ap.add_argument("--bank-mix", default="flank:2,goal_behind:2",
                    help="--bank-remix: columns per slot per formation (even: half with the robots exchanged)")
    ap.add_argument("--bank-mix-seed", type=int, default=9200, help="--bank-remix: which columns, jitter")
    ap.add_argument("--drop-rewards", default="",
                    help="reward terms removed after the reward set is built, by name prefix (each robot's), e.g. "
                         "push_credit: team return only for pushing")
    ap.add_argument("--sgs-floor", type=float, default=0.05, help="SGS: lowest weight 4p(1-p) may take")
    ap.add_argument("--sgs-ema", type=float, default=0.3, help="SGS: per-task success estimate update rate")
    a = ap.parse_args()

    if a.kl_ref > 0 and a.scratch:
        raise SystemExit("--kl-ref anchors to the Stage 2 policies: it does not apply with --scratch")
    if a.init_actors and (a.init_from or a.scratch or a.residual):
        raise SystemExit("--init-actors replaces --init-from / --scratch / --residual")
    if a.actor_schedule and not (a.actor_schedule == "joint" or a.actor_schedule.startswith(("alt:", "only:"))):
        raise SystemExit(f"--actor-schedule {a.actor_schedule}: joint, alt:<N> or only:<agent>")
    if a.shared_actor and (a.residual or a.actor_schedule.startswith("only:")):
        raise SystemExit("--shared-actor: plain actors, and both robots use the one actor (no only:<agent>)")
    if a.transfer_check and not a.init_actors:
        raise SystemExit("--transfer-check checks an --init-actors transfer")
    if (a.task_bank or a.bank_make or a.bank_check or a.bank_remix) and not a.task_bank_file:
        raise SystemExit("--task-bank / --bank-make / --bank-check / --bank-remix need --task-bank-file")
    if (a.bank_make or a.bank_remix) and Path(a.task_bank_file).exists():
        raise SystemExit(f"{a.task_bank_file} exists: a bank is written once")
    if (a.task_bank or a.bank_make or a.bank_check or a.bank_remix) and (a.contacts or not a.fixed_difficulty):
        raise SystemExit("the task bank is for planner-free runs at fixed difficulty (--fixed-difficulty)")
    if a.bank_make and Path(a.task_bank_file).exists():
        raise SystemExit(f"{a.task_bank_file} exists: a bank is drawn once and shared by the arms")
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
    if a.pair in _pairs().ARM_PAIRS and not (a.scratch or a.resume or a.init_from or a.init_actors):
        raise SystemExit(f"--pair {a.pair}: a Spot-arm slot has no Stage 2 policies to start from: pass --scratch (or --resume / --init-from)")
    pilot_level = tuple(float(x) for x in a.pilot_level.split(",")) if a.pilot_level else ()
    extra_levels = tuple(tuple(float(x) for x in r.split(",")) for r in a.extra_levels.split(";")) if a.extra_levels else ()
    level_mix = tuple((int(ph.split(":")[0]), tuple(float(x) for x in ph.split(":")[1].split(",")))
                      for ph in a.level_mix.split(";")) if a.level_mix else ()
    if level_mix and (not a.fixed_difficulty or len(level_mix[0][1]) != 1 + len(extra_levels) or level_mix[0][0] != 0):
        raise SystemExit("--level-mix: needs --fixed-difficulty, a first phase at 0, one weight per level")
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
                                 start_mode="around" if a.start_around else "opposite" if a.start_opposite else "behind",
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
                                 short_tasks=a.short_tasks, arm=a.arm, pilot_level=pilot_level,
                                 oppose_cost=a.oppose_cost, cancel_cost=a.cancel_cost,
                                 pilot_episode_s=a.pilot_episode_s, dyaw_choices=a.dyaw_choices,
                                 hand_obs=a.hand_obs, goal_credit=a.goal_credit, align_bonus=a.align_bonus, arm_bonus=a.arm_bonus, action_rate_w=a.action_rate_w, action_limit_w=a.action_limit_w, yaw_gate=a.yaw_gate, yaw_w=a.yaw_w, geom_obs=a.geom_obs, hist_obs=a.hist_obs, turn_signs=a.turn_signs, arm_hold_steps=a.arm_hold_steps,
                                 extra_levels=extra_levels, level_mix=level_mix, solo_agent=a.solo_agent)
    env_cfg.scene.num_envs = a.num_envs
    if a.swap_starts:
        env_cfg.commands["goal"].swap_starts = True
    env_cfg.seed = a.seed
    drop_rewards = tuple(x.strip() for x in a.drop_rewards.split(",") if x.strip())
    for pre in drop_rewards:
        gone = [nm for nm in list(env_cfg.rewards) if nm == pre or nm.startswith(pre + "_")]
        if not gone:
            raise SystemExit(f"--drop-rewards {pre}: no such term in {sorted(env_cfg.rewards)}")
        for nm in gone:
            del env_cfg.rewards[nm]
        print(f"[marl2] rewards dropped: {gone}")
    env_cfg.commands["goal"].start_level = a.start_level
    env_cfg.commands["goal"].turn_frac = a.turn_frac
    if a.roll_ratio > 0:
        env_cfg.commands["goal"].roll_ratio = a.roll_ratio
        print(f"[marl2] planner rolling model: roll_ratio {a.roll_ratio:g}")
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
                  kl_partner_scale=a.kl_partner_scale, start_mode="around" if a.start_around else "opposite" if a.start_opposite else "behind",
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
                  arm=a.arm if a.pair in _pairs().ARM_PAIRS else "", pilot_level=pilot_level,
                  pilot_episode_s=a.pilot_episode_s, dyaw_choices=a.dyaw_choices, hand_obs=a.hand_obs, goal_credit=a.goal_credit, align_bonus=a.align_bonus,
                  arm_bonus=a.arm_bonus, roll_ratio=a.roll_ratio, action_rate_w=a.action_rate_w,
                  action_limit_w=a.action_limit_w, std_cap=a.std_cap, yaw_gate=a.yaw_gate, yaw_w=a.yaw_w, geom_obs=a.geom_obs, hist_obs=a.hist_obs,
                  turn_signs=a.turn_signs, arm_hold_steps=a.arm_hold_steps, extra_levels=extra_levels, level_mix=level_mix,
                  solo_agent=a.solo_agent, bc_data=a.bc_data, bc_keep_norm=a.bc_keep_norm, bc_coef=a.bc_coef,
                  bc_iters=a.bc_iters, bc_pretrain_steps=a.bc_pretrain_steps,
                  video_interval=0 if a.check else a.video_interval, video_length=a.video_length,
                  inputs=models["selection"], residual=a.residual or "", resid_scale=a.resid_scale,
                  resid_std=a.resid_std, resid_objects=resid_objects, shape_bias=shape_bias, min_std=a.min_std,
                  resid_compose=a.resid_compose, resid_gate_dist=a.resid_gate_dist, train_shapes=train_shapes,
                  train_mass=train_mass, fixed_difficulty=a.fixed_difficulty,
                  resid_scale_axes=tuple(float(x) for x in a.resid_scale_axes.split(",")) if a.resid_scale_axes else (),
                  track=a.track, track_w=a.track_w, short_tasks=a.short_tasks,
                  drop_rewards=drop_rewards, init_actors=a.init_actors or "", task_bank=a.task_bank or "", task_bank_file=a.task_bank_file or "",
                  actor_schedule=a.actor_schedule, shared_actor=a.shared_actor, swap_starts=a.swap_starts,
                  oppose_cost=a.oppose_cost, cancel_cost=a.cancel_cost)
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
        elif a.init_actors:
            trainer.init_actors(a.init_actors)
        elif a.init_from:
            trainer.init_from(a.init_from)
        else:
            trainer.warm_start(models["policy"])
    trainer.apply_std_cap()
    if a.check and (a.geom_obs or a.hist_obs):
        _obs_study_selfcheck(env, trainer)
    if a.check and trainer.it > 0:  # a check from a later checkpoint (--init-from / --resume): 2 more iterations
        trainer.cfg.max_iterations = trainer.it + 2
    if a.fixed_difficulty:  # re-apply the declared settings after any warm start / resume, and check the
        g_ = env.command_manager.get_term("goal")  # episodes already running were drawn with them
        g_.level = a.fixed_level
        if level_mix:  # after the startup mass event and any resume (the step counter sets the phase): draw now
            g_.mix_phase = -1
            g_._apply_level_mix()
        if getattr(g_, "tol_table", None) is not None:
            g_.tol_level = len(g_.cfg.tol_levels) - 1
            assert bool((g_.env_tol_level == g_.tol_level).all()), "fixed difficulty: episodes at another tolerance"
        assert level_mix or bool((g_.env_level == a.fixed_level).all()), "fixed difficulty: episodes at another level"
        print(f"[marl2] fixed difficulty: level {g_.level}, tolerance level {getattr(g_, 'tol_level', 0)} (finest), "
              f"mass window {train_mass or 'the level'}, shapes {train_shapes or 'Stage 2 split'}")
    if a.transfer_check:
        raise SystemExit(transfer_check(trainer, env, a, device))
    if a.bank_remix:
        from quadcoop.coop2 import task_bank as tbm
        per = {k: int(v) for k, v in (x.split(":") for x in a.bank_mix.split(","))}
        src = torch.load(a.bank_remix, map_location="cpu", weights_only=False)
        mix = tbm.remix(src, per, a.bank_mix_seed)
        tb = tbm.TaskBank(mix, "uniform", device)
        tb.check_physics(env)
        g_ = env.command_manager.get_term("goal")
        g_.scenario = tb
        moved = tbm.resnap(env, tb)
        # placed robots against the remixed bearings, on every task (from the re-recorded snapshot)
        oxy = tb.snap["obj_xy"]
        berr = 0.0
        for k_, ag_ in enumerate(("anymal1", "anymal2")):
            v_ = tb.snap[f"xy_{ag_}"] - oxy
            dd = torch.atan2(v_[..., 1], v_[..., 0]) - tb.t["bearings"][..., k_]
            berr = max(berr, float(torch.atan2(torch.sin(dd), torch.cos(dd)).abs().max()))
        fixed_keys = [k_ for k_ in moved if not k_.startswith(("xy_", "yaw_"))]
        drift = max(moved[k_] for k_ in fixed_keys)
        out_ = {"tasks": {k_: v_.cpu() for k_, v_ in tb.t.items()}, "snap": {k_: v_.cpu() for k_, v_ in tb.snap.items()},
                "meta": mix["meta"], "mix": mix["mix"]}
        Path(a.task_bank_file).parent.mkdir(parents=True, exist_ok=True)
        torch.save(out_, a.task_bank_file)
        rep_ = tbm.replay_check(env, tb, columns=tuple(range(tb.K)))
        g_.scenario = None
        rep_.update(source=a.bank_remix, mix=mix["meta"]["mix"], resnap_change=moved, non_robot_drift=drift,
                    bearing_err_deg=math.degrees(berr))
        rep_["pass"] = bool(rep_["pass"] and drift <= 1e-4 and math.degrees(berr) <= 0.5)
        f_ = mix["mix"]["formation"]
        print(f"[bank] remix {a.bank_remix} -> {a.task_bank_file}: per slot {per}; tasks original "
              f"{int((f_ < 0).sum())}, " + ", ".join(f"{nm} {int((f_ == i).sum())}" for i, nm in enumerate(mix['mix']['names']))
              + f"; robot poses moved up to {max(moved[k_] for k_ in moved if k_ not in fixed_keys):.2f}, other keys "
              f"{drift:.2e}; placed vs remixed bearing {math.degrees(berr):.3f} deg; replay (all {tb.K} columns, twice) "
              f"worst {rep_['worst']:.2e} -> {'PASS' if rep_['pass'] else 'FAIL'}")
        (Path(a.task_bank_file).with_suffix(".check.json")).write_text(json.dumps(rep_, indent=1))
        raise SystemExit(0 if rep_["pass"] else 1)
    if a.bank_make or a.bank_check or a.task_bank:
        from quadcoop.coop2 import task_bank as tbm
        if a.bank_make:
            bank = tbm.generate(env, a.bank_per_env, a.bank_seed)
            Path(a.task_bank_file).parent.mkdir(parents=True, exist_ok=True)
            torch.save(bank, a.task_bank_file)
            print(f"[bank] {a.task_bank_file}: {env.num_envs} slots x {a.bank_per_env} tasks, seed {a.bank_seed}, "
                  f"level {bank['meta']['level']}; shapes drawn " + ", ".join(
                      f"{nm} {int((bank['tasks']['shape'] == i).sum())}" for i, nm in enumerate(bank["meta"]["shapes"])
                      if int((bank['tasks']['shape'] == i).sum())))
        bank = torch.load(a.task_bank_file, map_location="cpu", weights_only=False)
        tb = tbm.TaskBank(bank, a.task_bank or "uniform", device, ema=a.sgs_ema, floor=a.sgs_floor)
        tb.check_physics(env)
        if a.bank_make or a.bank_check:
            g_ = env.command_manager.get_term("goal")
            g_.scenario = tb
            rep_ = tbm.replay_check(env, tb)
            g_.scenario = None
            bad = {k: v for k, v in rep_.items() if isinstance(v, float) and v > 1e-4}
            print(f"[bank] replay check (columns 0 and {tb.K - 1}, every slot, twice): worst {rep_['worst']:.2e} "
                  f"-> {'PASS' if rep_['pass'] else 'FAIL'}" + (f"; over tolerance: {bad}" if bad else ""))
            if a.swap_starts:  # the replay with exchanged starts: its own record (the bank's own check stays)
                sh_ = [x for k_, v_ in rep_.items() if k_.endswith("swap_share") for x in v_]
                print(f"[bank] swap_starts: share of slots exchanged per replay {[round(x, 3) for x in sh_]}")
                rep_["pass"] = bool(rep_["pass"] and all(0.45 <= x <= 0.55 for x in sh_))
            (Path(a.task_bank_file).with_suffix(".swap.check.json" if a.swap_starts else ".check.json")).write_text(
                json.dumps(rep_, indent=1))
            raise SystemExit(0 if rep_["pass"] else 1)
        trainer.attach_bank(tb)
        print(f"[bank] training resets draw from {a.task_bank_file} ({tb.n} slots x {tb.K} tasks, "
              f"{a.task_bank}{f', floor {a.sgs_floor:g}, ema {a.sgs_ema:g}' if a.task_bank == 'sgs' else ''})")
    if a.resid_check:
        if not a.residual:
            raise SystemExit("--resid-check needs --residual")
        rep = trainer.check_residual(steps=a.resid_check)
        raise SystemExit(0 if rep["pass"] else 1)
    if a.check:
        cfg.max_iterations = trainer.it + 2  # a check always runs 2 iterations, wherever it starts
    if a.schedule_check:
        cfg.max_iterations = trainer.it + a.schedule_check
        trainer.iter_hook = schedule_hook(log_dir / "schedule_check.json", cfg)
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
    if trainer.iter_hook is not None and hasattr(trainer.iter_hook, "prime"):
        trainer.iter_hook.prime(trainer)
    trainer.learn()
    env.close()
    return 0


def schedule_hook(out_file, cfg):
    """--schedule-check: after every iteration, which actors changed against the previous iteration."""
    import re

    import torch

    from quadcoop.coop2.pairs import AGENTS

    def snap(tr):
        st = {}
        for ag in AGENTS:
            sd = {re.sub(rf"(?<=_){ag}(?=\.)", "X", k): v.detach().clone() for k, v in tr.actors[ag].state_dict().items()}
            opt = tr.actor_opt[ag if not cfg.shared_actor else AGENTS[0]].state_dict()["state"]
            steps = sum(float(v["step"]) for v in opt.values()) if opt else 0.0
            st[ag] = (sd, steps, float(tr.lr[ag]))
        return st

    rows, prev, ok = [], {}, [True]

    def hook(tr, active, warm):
        cur = snap(tr)
        if "s" in prev:
            row = {"iter": tr.it, "warm": warm, "active": [] if warm else list(active), "changed": {}, "ok": True}
            for ag in AGENTS:
                sd0, st0, lr0 = prev["s"][ag]
                sd1, st1, lr1 = cur[ag]
                w = [k for k in sd1 if not torch.equal(sd1[k], sd0[k])]
                row["changed"][ag] = {"tensors": len(w), "opt_steps": st1 - st0, "lr_changed": lr1 != lr0,
                                      "normalizer": any("normalizer" in k for k in w), "noise": any("std" in k for k in w)}
                should = (not warm) and ag in active
                changed = bool(w) or st1 != st0
                frozen_ok = should or (not w and st1 == st0 and lr1 == lr0)
                if (should and not changed) or not frozen_ok:
                    row["ok"] = False
            if cfg.shared_actor:
                a0 = AGENTS[0]
                same = all(torch.equal(cur[a0][0][k], cur[ag][0][k]) for ag in AGENTS[1:] for k in cur[a0][0])
                row["shared_identical"] = same
                row["ok"] &= same
            ok[0] &= row["ok"]
            rows.append(row)
            print(f"[schedule-check] iteration {tr.it}: warm {warm} active {row['active']} changed "
                  f"{ {k: v['tensors'] for k, v in row['changed'].items()} } -> {'ok' if row['ok'] else 'FAIL'}", flush=True)
        prev["s"] = cur
        if tr.it >= cfg.max_iterations:
            import json
            Path(out_file).write_text(json.dumps({"pass": ok[0], "schedule": cfg.actor_schedule,
                                                  "shared": cfg.shared_actor, "rows": rows}, indent=1))
            print(f"[schedule-check] {'PASS' if ok[0] else 'FAIL'} -> {out_file}", flush=True)
            if not ok[0]:
                raise SystemExit(1)
    hook.prime = lambda tr: prev.__setitem__("s", snap(tr))  # the state before the first iteration
    return hook


def transfer_check(trainer, env, a, device) -> int:
    """--transfer-check: the observations are collected once (under the source policy: at the start, then
    after 50 and 200 steps) and reused by every arm's check, so IPPO and MAPPO are compared on the same inputs."""
    from quadcoop.coop2.marl import PairPolicy
    import torch

    obs_file = Path(a.transfer_check)
    if not obs_file.exists():
        src = PairPolicy(trainer.obs, device, a.variant, checkpoint=a.init_actors)
        snaps, obs = {"t0": trainer.obs.clone()}, trainer.obs
        with torch.inference_mode():
            for t in range(1, 201):
                o, *_ = env.step(src(obs))
                obs = trainer._td(o)
                if t in (50, 200):
                    snaps[f"t{t}"] = obs.clone()
        obs_file.parent.mkdir(parents=True, exist_ok=True)
        torch.save(snaps, obs_file)
        print(f"[transfer] saved {len(snaps)} observation batches x {env.num_envs} envs to {obs_file}")
    rep = trainer.check_actor_transfer(a.init_actors, obs_file)
    print(f"[transfer] {a.init_actors} -> {a.algo} actors, before any update, on {obs_file}:")
    for k, v in rep.items():
        if isinstance(v, dict):
            print(f"[transfer]   {k}: {v}")
    print(f"[transfer] worst difference {rep['worst']:.2e} -> {'PASS' if rep['pass'] else 'FAIL'}; critics "
          f"{list(trainer.critics)} fresh, critic-only iterations {trainer.cfg.critic_warmup_resume}")
    out = obs_file.with_name(f"{obs_file.stem}.{a.algo}.json")
    out.write_text(json.dumps(rep, indent=1, default=str))
    return 0 if rep["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
