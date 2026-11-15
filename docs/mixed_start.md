# Mixed-start IPPO arm (F) against arm A

Status (2026-11-14): submitted.
- Mixed-start bank build and check: job 29122899.
- Arm F training: `nwF_ippo_uniform_mixstart_s0`, job 29122903, afterok on the bank check.
- Evaluations below.

**Why.** Placement tests (`docs/placement_eval.md`) found one repeatable weakness:
- cylinder loses 6–14 points when the robots start on opposite faces (flank) or with one on the goal side
  (goal_behind);
- it shows in the parent, IPPO A and MAPPO B, and pooled over two runs;
- it falls below the 40% floor.

Changing the critic (MAPPO) did not fix it. Broader starts are a plausible fix for cylinder. Arch does not lose
success with formation, so this is not expected to fix heavy arch.

**The one deliberate difference from A is the starting arrangement.**
- **F's bank:** `logs/next_wave/bank_ten_s0_k16_mix.pt`, a copy of A's `bank_ten_s0_k16.pt`
  (`task_bank.remix`, `train_coop2.py --bank-remix`).
- **What changes:** on each of the 4096 slots, 2 of 16 tasks get flank bearings and 2 get goal_behind bearings.
  - Flank: goal direction ∓ 90°.
  - Goal_behind: anymal1 behind, anymal2 on the goal side.
  - The angles are relative to that task's own object-to-goal direction, ±10° per robot, as in the evaluation.
  - That is 75% original starts, 12.5% flank and 12.5% goal_behind.
  - On every slot, one task of each formation has the robots exchanged, so each actor takes each place equally often.
- **What stays the same:**
  - each task's object, pose, mass, friction, size, goal, turn and heavy-pair flags, gaps and yaw noise;
  - the reward (r7), the uniform sampler, seed 0, 4096 envs;
  - the parent's actors (iteration 4000), fresh critics with a 100-iteration warm-up;
  - 1000 iterations, to 5000.
- **Bank check before training** (`slurm/mixed_start_bank.sbatch`, under the arm's env build):
  - every column is re-recorded on every slot;
  - placed robots must be within 0.5° of the remixed bearing;
  - nothing but the robot poses may change (≤ 1e-4);
  - all 16 columns are replay-checked twice (≤ 1e-4).
  - Report: `logs/next_wave/bank_ten_s0_k16_mix.check.json`.

## Judging F

**Evaluations** (each with all three formations, swap, all ten objects, 2,880 episodes; two runs each):

| | seed 7100 (development tasks, includes the benchmark) | seed 7300 (fresh placements) |
|---|---|---|
| A | `place-nwA-ippo-it5000[-r2]`, already run | `place-nwA-ippo-it5000-fresh7300[-r2]`: jobs 29122908, 29122909 |
| F | `place-nwF-ippo-mixstart-it5000[-r2]`: jobs 29122910, 29122911 | `place-nwF-ippo-mixstart-it5000-fresh7300[-r2]`: jobs 29122912, 29122913 |

The unswapped standard rows at seed 7100 are the original 480-task benchmark.

**Analysis:**
`scripts/placement_compare.py --runs=A:<run1>+<run2>,F:<run1>+<run2> --pairs=F-A --diag=cylinder`, once per seed.
- **Primary question:** is cylinder back above 40% in both flank and goal_behind, and better than A on matched tasks
  (F − A per base task, interval excluding 0)?
- **Cost check:** standard cylinder, overall success, falls, and the strong objects (sphere, long), so that a gain
  bought by losing standard performance is visible.
- **Mechanism:** cylinder's time to the first 0.25 m of progress and its final distance to the goal. Both cylinder
  failure modes are now near misses: the object moves, but the pair doesn't finish.

**Scope.** 10 points on cylinder is 1 point on the ten-object average. Reaching 70% overall needs gains on heavy loads
and on the long move-and-turn.

## Results (2026-11-14): no fix for cylinder, no cost elsewhere; F is not adopted

**Delivered as designed.** From `bank_5000.pt`, F's 42,895 training episodes:
- 75.0% original starts, 12.6% flank and 12.4% goal_behind;
- about 1,000 cylinder episodes in the new formations.

In training the new formations were not harder than the original starts: 63% and 61% success, against 61%. The
level-4 training starts already cover most of the circle.

**Cylinder** (two runs per arm and seed, swaps pooled; full reports in `evals/mixed_start/F_vs_A_seed{7100,7300}.md`):

| | standard | flank | goal_behind |
|---|---|---|---|
| A, seed 7100 | 44.3% | 35.4% | 35.9% |
| F, seed 7100 | 46.4% | 35.4% | 35.9% |
| F − A, seed 7100 | +2.1 [−3.6, +7.8] | +0.0 [−5.7, +5.7] | +0.0 [−5.2, +4.7] |
| A, seed 7300 (fresh) | 45.3% | 41.7% | 34.4% |
| F, seed 7300 (fresh) | 47.9% | 39.6% | 37.5% |
| F − A, seed 7300 | +2.6 [−4.2, +9.9] | −2.1 [−7.3, +2.6] | +3.1 [−1.6, +7.8] |

- **Primary question: no.** Cylinder stays below 40% in both new formations on both seeds, and F matches A on
  matched tasks.
- **Cylinder mechanism, unchanged:**
  - the push starts in nearly every episode, with the first 0.25 m at 2.5–3.1 s in the new formations;
  - failures end a median 0.15–0.36 m from the goal;
  - falls are 16–28%.

**Everything else, F − A:**
- **Overall, standard formation:** +0.2 points on both seeds.
- **Overall, flank:** +0.3 and +0.4.
- **Overall, goal_behind:** −1.3 [−3.2, +0.6] at seed 7100, +2.3 [+0.5, +4.2] at seed 7300. Not consistent across
  seeds.
- **Falls:** 13.1% against 12.8% at seed 7100, 12.3% against 13.4% at seed 7300.
- **Sphere, standard:** −4.7 [−9.4, −0.5] and −3.6 [−8.3, +0.5]. A small cost, still at 93–95%.
- **Arch, standard:** −4.2 and −6.2, both intervals including 0.

**Reading:**
- Adding 25% opposite-face and goal-side starts for 1000 iterations changed neither the cylinder weakness nor
  overall success.
- The weakness is not a lack of exposure to those relative positions: training already contains them, and the
  policy does as well there as from its other training starts.
- What remains for cylinder is finishing: a near miss with the object moving, plus falls.
  - The next look is at cylinder failure videos and traces from the new formations: overshoot, rolling or the hold,
    and who falls.
  - Changing the start distribution further is not the next step.
- **Parent stays iteration 4000; control stays arm A.** F is not adopted.
- **The course result stands:** in the swap test, the leader follows the start place (`docs/placement_eval.md`).
- For performance, the larger gaps are still heavy loads (about 27% at 80 kg; see the contribution analysis in
  `docs/recovery_eval.md`) and the long move-and-turn.
