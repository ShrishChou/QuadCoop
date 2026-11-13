# Request-tracking pilot: teach the executor to follow feasible pushing requests

Status: preflight passed; training `track_beam_s0` (job 28988820, 300 iterations) running. Written 2026-11-13, before any preflight or training result. Changes after
results go under "Amendments", with a reason.

**Why.** `docs/planner_feedback.md` found that the frozen executor (turn_debug) barely responds to the planner's
share request.
- A 0.4 share swing moves its forward command by about 0.02 m/s.
- Its forward output is past the ±1 clip on about 60% of samples.

The planner therefore has no usable control channel. This pilot trains one isolated skill: deliver what is requested.
- Push harder when more is asked.
- Push less when less is asked.
- Stop when stopping is asked.
- Keep making progress throughout.

**Unchanged:**
- walker, physics, contact candidates, replanning rules;
- the frozen base executor and its input layout;
- the reference planner, with feedback off (`fb_on=0`, `share_adapt=0`).

## Design (the review's four amendments)

**1. Slowing and stopping are representable.**
- The correction's bound is per axis (`--resid-scale-axes 1.2,0.3,0.3`, vx / vy / wz).
- It is composed on the clipped base as before: mean = clip(base) + gate × bound × tanh(MLP).
- With the forward bound at 1.2, a saturated base (action 1, 0.8 m/s) can be brought to action −0.2, a forward
  command of −0.04 m/s, which is a stop.
- At initialisation the correction is exactly 0, so the applied command is the base's.
- The walker is unchanged.
- Preflight check ("express", in `check_residual`), on gated env states with the base's forward output saturated,
  forcing only the forward correction:
  - tanh 0 must give exactly the base's command (maintain);
  - tanh −0.5 must give 0.2–0.6 m/s (reduce);
  - tanh → −1 must give ≤ 0.02 m/s (stop).

**2. Planner requests are task-consistent proposals, not proof of feasibility.**
- Requests come from the reference planner on short engaged tasks (`--short-tasks`):
  - 1–2 m goals, beam broadside within ±15°, goal turn up to ±30°, 25 s episodes;
  - robots start at their contacts (`--contact-start-at 1 --random-start 0`);
  - beam only, 40–60 kg, friction drawn from 0.4–0.6.
- Straight goals give balanced requests. Turning goals give unequal shares, which covers reducing one robot's
  contribution. The approach to a goal gives settling and stopping.
- **Force targets** (`CoopPush2Command._update_track`):
  - Total push F_need = μ m g (`tr_margin` 1.0, not the effort rule's 1.2). It is an initial scale, not a measured
    threshold.
  - Each robot's target is its sent share × F_need.
  - If a target exceeds the planner's per-robot `robot_push_force` (250 N), both robots' targets are scaled by the
    same factor, so the split is kept. That is recorded (`tr_limited`).
  - Conditions with μ m g > 320 N are marked marginal (`tr_marginal`). This covers 60 kg at friction ≥ 0.55,
    beyond the demonstrated sustained delivery.
- **Tolerance band:** in transport, delivery within 0.8–1.25 × the target is on target.
- **Correction inputs:** the correction (not the base) sees its own and its partner's target band, its phase, its
  delivered force, and the marginal and limited flags (`track_obs`, 11 inputs in `resid_<robot>`).

**3. Stopping and contact loss are handled explicitly.** The phases, per robot:

| phase | when | target |
|---|---|---|
| 0 transition | not yet engaged on its (newly) assigned contact | not scored |
| 1 transport | motion wanted, pose error ≥ 0.3 m, share ≥ 0.05 | band [0.8, 1.25] × target |
| 2 settle | motion wanted, pose error < 0.3 m | upper limit only: 1.25 × target, tapered with pose error to 0.3 of it |
| 3 stop / withdraw | nothing wanted, or share < 0.05 | upper limit 20 N |

- In settling, pushing less to settle is fine.
- Delivery is the robot's 1 s gait-filtered force along its push direction.
- Once a robot is engaged, losing touch is not an exemption: delivery decays and is scored as missing.
  Reassignment is a transition: it isn't scored until the robot reaches its new contact.
- **Cost:** `track_<robot>` = −0.5 × the normalised error (0..1, normalised by max(target, 50 N)) per second. It is
  a cost only: being inside the band pays nothing, so the term never pays for standing and pressing.
- **The rest of the reward is unchanged `rmin`:** pose progress, precise progress, the goal bonus (success requires
  the beam at rest inside the tolerance), the failure and fall costs, the contact approach potential, and
  `contact_work` (force × beam motion in the wanted direction).
- Per-episode statistics are logged to wandb as `Metrics/goal/track_*`.

**4. Training.**
- A fresh correction on turn_debug `model_15000.pt`, gated to the beam, with a 0.6 m contact gate.
- Fixed difficulty, finest tolerance, replanning 3–6 s.
- One run of 300 iterations; checkpoint 300 is chosen in advance. Logged to wandb.

```
ALGO=mappo SEED=0 RUN_NAME=track_beam_s0 ITERS=300 EXTRA="--pair anymal --partner-map --contacts --guide \
  --push-cmd --contact-mix expert:1 --reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 \
  --reselect-s 3,6 --contact-start-at 1 --random-start 0 --reward rmin --turn-frac 0 \
  --residual logs/keep/marl2/turn_debug/model_15000.pt --resid-scale-axes 1.2,0.3,0.3 --resid-std 0.15 \
  --min-std 0.05 --resid-objects beam --resid-gate-dist 0.6 --train-shapes beam --train-mass 40,60 \
  --fixed-difficulty --fixed-level 0 --short-tasks --track --track-w 0.5 --actor-lr 3e-4 --max-actor-lr 3e-4 \
  --critic-warmup 50" sbatch -p mit_normal_gpu -t 02:00:00 slurm/train_coop2.sbatch
```

## Preflight (before training)

- `--resid-check 400` with 512 envs: the existing checks, now with the per-axis bound, plus "express".
- A 2-iteration `--check` run with the tracking metrics logged, to confirm phases, targets and the marginal and
  limited flags are populated under the base policy.

## Evaluation and pass criteria (declared before training)

**Arms**
- **A:** the frozen executor, rerun with the current code, `--set track_on=1` for measurement only (no effect on
  actions).
- **T:** checkpoint 300.

Both use the same tasks as `docs/planner_feedback.md`: seed 4200, beam, S_straight and S_moveturn,
`--start contact`, 20 s horizon, 5 s settling window, 8 reps.

| condition | role |
|---|---|
| 40 + 60 kg, friction 0.5 (32 tasks) | main |
| 60 kg, friction 0.6 (16 tasks) | marginal stress, reported separately, not a pass criterion |

**Responsiveness (held out)**
- Training never perturbs requests. The test uses P1's protocol on T: contacts fixed, `share_perturb` −0.2 / +0.2,
  seed 4100, 3 reps, 40 and 60 kg at friction 0.5.
- R1 (pass): the paired change in robot 1's (anymal1's) delivered share is ≥ +0.10 (≥ 0.25 of the requested
  change), with a 95% CI excluding 0, at 40 kg and at 60 kg separately.

**Force** (main condition; trace columns `tr_*`)
- F1 (sufficient for requested transport): over tasks, the median of mean transport-phase delivered / target is
  ≥ 0.8, and the mean transport error is ≤ A's.
- F2 (reduce when requested): the mean settle and stop error (force above the limit) is ≤ A's + 0.02.

**Progress and stability** (main condition, paired against A)
- P1: success change ≥ 0 points, and the lower 95% CI bound > −12.5 points (−4 of 32 tasks).
- P2: falls increase by at most 2 tasks (+6.25 points).
- P3: mean final position error worse than A by at most 0.05 m.

**Pass:** R1, F1, F2, P1, P2 and P3 together.
- Reported separately for straight transport (S_straight), turning (S_moveturn) and finishing (success, settled,
  settle errors).
- This small suite can screen the pilot. It cannot establish preservation across objects. Other objects keep the
  frozen executor (beam gate).

**Only if it passes:**
1. Retest the planner feedback (B, then C) on the same tasks.
2. Then ordinary starts with the existing replanning.
3. Then other objects.

## Preflight results (2026-11-13, `evals/request_tracking/`)

**`--resid-check 400`: passed** (`preflight_resid_check.json`)
- About 409k rows per pass. Every equality check was 0.0:
  - sent vs walker term;
  - base history vs the base's own output;
  - wrapper base vs an independently loaded plain base;
  - ungated rows unchanged;
  - zero correction vs the plain base, and its applied command unchanged.
- ±0.2 changed every in-range gated component and every pulled-back saturated component (≥ 0.99999).
- Draw: 589 episodes, all beam, all inside 40–60 kg.
- Base output past ±1.3 on gated rows: 35% overall, 53% of forward components.
- Forward expressiveness, on 45,428 gated rows with the base's forward output saturated:
  - maintain gives exactly the base's 0.80 m/s;
  - reduce gives 0.38 m/s;
  - stop gives −0.04 m/s.

**2-iteration check**
- The tracking inputs (11 per robot) and the costs `track_anymal1` / `track_anymal2` (weight −0.5) are wired up.
- No episode finished in 2 iterations (25 s episodes), so the tracking state was checked on arm A's traces instead.

**Arm A with `track_on=1`** (`trkA-f05`, `trkA-f06`, measurement only)

| | main (friction 0.5) | stress (60 kg, friction 0.6) |
|---|---|---|
| phase share: transition / transport / settle / stop | 14 / 57 / 14 / 15% | 3 / 96 / 1 / 0% |
| mean error: transport / settle / stop | 0.29 / 0.09 / 0.38 | 0.23 / 0.25 / — |
| transport target, median (p10–p90) | 141 N (84–196) | 177 N (141–212) |
| delivered / target, median (p10–p90) | 0.60 (0.07–1.06) | 0.61 (0.31–0.95) |
| targets limited | 9.5% | 5.6% |
| marked marginal | 0% | 100% |

- The frozen executor under-delivers in transport (median 0.6 of target).
- It over-delivers when asked to stop or withdraw (stop error 0.38).
