# Planner feedback extension: object-motion feedback and adaptive force shares

Status: **done (2026-11-13). Do not adopt.** P0 passed; P1 failed (the executor does not follow share requests), so arm C was not run. Motion feedback (B) gave no gain over A. Recommendation at the end. Written 2026-11-13, before any preflight or development
result. Changes after results go under "Amendments", with a reason.

**Question.** Can the frozen executor respond to corrected planner requests, and does that improve controlled
transport? The loop under test is:

request → measured delivery → measured object motion → corrected request.

**Unchanged:**
- walker, executor (turn_debug `model_15000.pt`), physics, rewards;
- contact candidates, tolerances, replanning rules.

No corner ban and no retraining.

## What changed (`src/quadcoop/coop2/mdp.py`, CoopPush2CommandCfg; all off by default)

The planner's per-step `_update_push` now keeps three things separate.

**Nominal wanted motion**
- `c_vdes` / `c_wdes`, computed from the remaining pose error as before (`_wanted`).
- Everything else in the env keeps seeing the nominal motion: rewards, observations of the wanted motion,
  replanning scores and the success logic.

**Measured motion** (`fb_on`)
- `fb_vmeas` / `fb_wmeas`: object velocity and yaw rate, low-passed over `fb_tau`.

**Feedback-adjusted motion** (`fb_vcmd` / `fb_wcmd`), handed only to the existing force split (`_split`):
- Velocity: v = v_nom + kv (v_nom − v_meas), correction bounded by `fb_vmax`.
- Yaw rate: w = w_nom + kw (w_nom − w_meas), correction bounded by `fb_wmax`. This damps unwanted rotation.
- Speed limits: the result is capped at the planner's `push_vmax` / `push_wmax`.
- Fading: the correction is scaled by the nominal request's size, max(|v_nom| / push_vmax, |w_nom| / push_wmax),
  so it vanishes as the nominal request does.
- Stopping: where nothing is wanted nominally (|v| ≤ 0.02 and |w| ≤ 0.02) the motion is the nominal one, and
  directions and shares are held as before. Feedback never restarts pushing at a reached goal.
- Smoothing: the existing low-pass of push directions (`push_tau`) is unchanged.

**Adaptive share** (`share_adapt`)
- Force filtering, kept separate from the faster pose feedback:
  - each robot's contact force on the object (force sensor) and its touching are low-passed over `fs_tau`;
  - force along each robot's push direction gives robot 0's delivered share, `fs_meas`.
- Sample conditions. A step counts (`fs_valid`) only when:
  - motion is wanted;
  - both robots are engaged on their contacts and physically touching (filtered touch ≥ 0.5);
  - total filtered force along the push directions is ≥ `fs_fmin`;
  - the requested shares are interior;
  - neither robot is tilted past the fall limit;
  - `fs_hold_s` has passed since the last reassignment or large push-direction change.
- Estimate (`fs_bias`): delivered − requested share for robot 0 (the share sent last step).
  - It is an exponential average over `fs_est_tau`, bounded by `fs_bias_max`.
  - A new assignment resets it to 0.
  - A push direction turning by more than `fs_dir_deg` multiplies it by `fs_dir_decay`.
- Correction: the share sent is nominal − `fs_gain` × estimate, bounded by `fs_corr_max`, then clipped to
  [`fs_min_share`, 1 − `fs_min_share`]. Only interior nominal shares are corrected; zero and withdraw requests
  pass unchanged.
- Records: `push_share_nom` (the split's shares) and `push_share` (sent to the executor).
- The force-along-push measurements are used only as shares. No force level is treated as a capacity, and
  nothing assumes a higher speed command gives more force.

**`share_perturb`** (preflight only) adds a fixed offset to robot 0's requested share, for interior shares.

**Settings, frozen after the preflight**

| setting | value |
|---|---|
| `fb_kv` | 1.0 |
| `fb_kw` | 2.0 |
| `fb_vmax` | 0.15 m/s |
| `fb_wmax` | 0.3 rad/s |
| `fb_tau` | 0.2 s |
| `fs_tau` | 1.0 s |
| `fs_est_tau` | 3.0 s |
| `fs_fmin` | 60 N |
| `fs_min_share` | 0.15 |
| `fs_hold_s` | 1.0 s |
| `fs_dir_deg` | 20° |
| `fs_dir_decay` | 0.5 |
| `fs_gain` | 1.0 |
| `fs_corr_max` | 0.15 |
| `fs_bias_max` | 0.5 |

Every eval records the full goal config in `provenance.json`.

**Eval tooling (`scripts/contact_test.py`)**
- `--friction`: fixed object friction, recorded as applied.
- `--scenarios`: a subset of a task set.
- `--planner-check`: every step runs the reference `_update_push` (7a8b7c6) and the current one on the same state.
  It records the largest output difference in `summary.json`.
- New trace columns: nominal and corrected motion, measured motion, nominal and sent shares, `fs_meas`, `fs_bias`,
  `fs_valid`.

## Preflight (before the comparison)

**P0: equivalence**
- Setup: flags off, `--planner-check`, on the comparison's tasks.
- Pass: largest difference of every planner output (push directions, shares, residual, nominal motion) = 0.
- Also run with `fb_on=1`, to show the check sees a change.

**P1: does the executor follow share requests?**
- Setup:
  - contacts fixed (`--reselect-s 0`), feedback and adaptation off;
  - `share_perturb` = −0.2 / 0 / +0.2 on identical tasks;
  - beam S_straight and S_moveturn, 40 and 60 kg, friction 0.5, 3 reps.
- Measured: robot 1's (anymal1's) delivered share of force along the push directions, 1 s filtered. It is taken
  on samples where both robots are requested (engaged, interior shares) and touching (1 s), with total force along
  the push ≥ 60 N.
- Pass:
  - the paired task-level difference in delivered share (+0.2 arm − −0.2 arm) is > 0 with a 95% bootstrap interval
    excluding 0, at 40 kg and at 60 kg;
  - the response is at least 0.25 of the requested change (≥ 0.10 of the 0.4 difference).
- Otherwise the adaptive-share branch stops (arm C is not run) and that result is reported.
- Sign, frame, filtering and initialisation errors may be fixed here; settings are frozen after it.

## Development comparison (only after the preflight)

**Tasks**
- Beam only. Short engaged segments from `--tasks segment --start contact`:
  - `S_straight`: 1.5 m straight;
  - `S_moveturn`: 1.5 m with a 30° turn.
- Main: 40 and 60 kg at friction 0.5, 8 reps → 32 tasks per arm.
- Stress: 60 kg at friction 0.6, 8 reps → 16 tasks per arm, reported separately.
- Fixed across arms: seed 4100, 20 s horizon, 5 s settling window, expert replanning `auto`. Initial assignments
  are identical (chosen at reset, before any feedback).
- Later assignments may diverge; contact switches are logged per episode.

**Arms**
- A: unchanged planner.
- B: `fb_on=1`.
- C: `fb_on=1, share_adapt=1`, only if P1 passes.

**Budget:** 3 arms × 2 runs, about 10 minutes each.

**Report**, per arm and paired against A (bootstrap 95% CI over tasks, plus individual task outcomes):
- goal-pose success;
- final position and heading error;
- unintended yaw during straight transport;
- falls and completion time;
- requested vs delivered force share;
- desired vs measured object motion;
- physical contact duty;
- contact switches;
- tasks gained and lost.

## Preflight results (2026-11-13, `evals/planner_feedback/`)

**P0: passed** (`p0_equivalence.json`)
- Flags off: every planner output was identical to the reference (largest difference 0.0) over 2,368 checked steps
  at 40 and 60 kg.
- `fb_on=1`, checked on the same tasks:
  - nominal motion unchanged (difference 0.0);
  - push directions differ by up to 0.037;
  - sent shares by up to 1.0;
  - the pair residual by up to 0.88.
- So the check sees the change. Note that the residual feeds the replanner's "residual too high" timer, so
  feedback can change when replans happen, under unchanged rules.

**P1: failed, the executor does not follow share requests** (`p1_share_response.md`)
- Setup: 12 matched tasks, contacts fixed.
- Requested share for robot 1 (anymal1) was 0.300 / 0.482 / 0.683 in the three arms. Its delivered share was
  0.488 / 0.515 / 0.488.
- Paired change from −0.2 to +0.2: requested +0.383, delivered +0.000 [−0.039, +0.031].
  - 40 kg: −0.009 [−0.069, +0.042].
  - 60 kg: +0.009 [−0.027, +0.046].
- Ruled out:
  - the share is in the executor's observation (`push_obs`, in turn_debug's actor input since it was trained with
    `--push-cmd`), and the traces show the perturbed shares were sent;
  - the perturbation was constant through each episode, so response delay can't explain it;
  - the requested change dwarfs the noise of a 1 s filtered measurement.
- So this isn't a sign, frame or filtering error: the trained executor ignores the share request. No settings were
  changed. As declared, the adaptive-share branch stops and arm C is not run; the gains were not increased.

## Amendments

- 2026-11-13, after the preflight and before any comparison result: the comparison uses seed 4200, not 4100.
  The preflights ran on seed 4100, and their first 2–3 reps would have been the comparison's tasks. Nothing else
  changed.

## Comparison results (`evals/planner_feedback/compare_f05.md`, `compare_f06.md`)

Seed 4200, beam, short engaged segments, 8 reps, 20 s horizon. Jobs 28974900 (A) and 28974901 (B). The deltas
are paired, B − A, with 95% CIs.

**Main condition (friction 0.5, 40 + 60 kg, 32 tasks per arm)**

| metric | A | B | B − A [95% CI] |
|---|---|---|---|
| success | 7/32 (22%) | 7/32 (22%) | +0.0 pts [−15.6, +15.6] |
| 40 kg success | 4/16 | 7/16 | +18.8 [0.0, +37.5] |
| 60 kg success | 3/16 | 0/16 | −18.8 [−37.5, 0.0] |
| S_straight success | 7/16 | 7/16 | — |
| S_moveturn success | 0/16 | 0/16 | — |
| falls | 3/32 | 7/32 | +12.5 pts [−3.1, +28.1] |
| final position error (m) | 0.34 | 0.43 | +0.09 [−0.03, +0.20] |
| final heading error (deg) | 6.6 | 6.5 | −0.1 [−2.0, +2.0] |
| unintended yaw, S_straight (deg) | 9.0 | 8.7 | −0.3 [−1.4, +0.8] |
| measured − wanted velocity (m/s) | 0.224 | 0.224 | +0.00 [−0.02, +0.02] |
| measured − wanted yaw rate (deg/s) | 7.2 | 7.1 | −0.05 [−1.1, +1.2] |
| delivered − sent share error | 0.17 | 0.22 | +0.05 [+0.02, +0.08] |
| both robots touching (duty) | 33% | 30% | −3.1 pts [−6.7, +0.6] |
| contact switches per episode | 1.7 | 1.9 | +0.2 [−0.3, +0.8] |

- B gained 3 tasks (all S_straight 40 kg) and lost 3 (all S_straight 60 kg, one to a fall).
- Correction did happen: the corrected velocity differed from the nominal by 0.038 m/s on average.

**Stress condition (60 kg, friction 0.6, 16 tasks per arm)**
- No successes in either arm.
- Falls 5 → 2; final position error 0.80 → 0.71 m.
- Unintended yaw 6.0 → 8.7°.

**Reading**
- Motion feedback didn't change measured object motion: velocity and yaw-rate tracking error are unchanged. It
  didn't improve controlled transport either: no success change, more falls at friction 0.5, gains at 40 kg offset
  by losses at 60 kg.
- That is consistent with P1. Feedback can only act through the push directions and shares sent to the executor.
  The executor ignores shares, and the direction changes are small after the existing low-pass.
- Delivered-vs-sent share error rose only because B sends different shares that the executor doesn't follow.
- The reference itself does poorly on these short engaged tasks: 22% success, 0% on the 1.5 m + 30° segment. Of its 25
  failures, 22 are time-outs (13 ending within 0.25 m of the goal, 9 at 0.4–1.4 m) and 3 are falls.

## Recommendation

Decision rule applied: "if share requests are not followed, propose a short execution-training task specifically
for tracking feasible requests."

- **Planner extension:** keep it in the code, off by default; P0 shows it is inert when off. Adopt neither arm.
  Motion feedback isn't retained as a candidate, because the executor gives it nothing to act through.
- **Proposed next step:** a bounded engaged-start request-tracking task for the executor, gated to the beam, at
  40–60 kg, friction 0.4–0.6.
  - The planner's requests (push direction and share, from the nominal planner) are perturbed within the feasible
    range, as in P1.
  - The executor is rewarded for the delivered share and push direction matching the request: gait-filtered
    measurement, only while both robots are requested and touching.
  - Team goal progress stays in the reward, so tracking isn't learned at the expense of motion. Force level and
    contact duration are not objectives.
  - Success is measured by the P1 response test (delivered/requested slope ≥ 0.25, CI excluding 0) and by
    no-regression on the A tasks above.
  - Only after that would the planner feedback (B, then C) be re-tested, on the same tasks and seed.
- No training has been started.
