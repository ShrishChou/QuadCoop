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
