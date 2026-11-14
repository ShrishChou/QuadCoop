# Start placements: do the trained pairs coordinate from unfamiliar relative positions?

Status (2026-11-14): evaluation submitted, no training.
- Smoke test: job 29106329 (arch, 20 kg, one rep, 8 s).
- Then arm A (IPPO, iteration 5000): job 29106338.
- Arm B (MAPPO, iteration 5000): job 29106339.
- Parent (IPPO, iteration 4000): job 29106340, after arm A.

**Why.**
- Training at level 4 already places the robots around much of the circle:
  - the "behind" direction is offset by up to ±180°;
  - each robot is spread ±90° around it;
  - the robots are at least 60° apart, with gaps of 0.3–0.9 m.
- The standard evaluation uses one narrow formation: both robots at 180° ± 35° in a fixed world frame, ±10° jitter,
  while the goal direction varies.
- So we don't yet know whether the policies handle other relative starts: opposite faces, or one robot well placed
  and the other not. Answer that with the existing checkpoints before training a mixed-start arm.

**Run** (`eval_coop2.py --formations standard,flank,goal_behind --swap`, launcher
`slurm/submit_placement_eval.sh`).
- Tasks: the 480 seed-7100 benchmark tasks, 10 objects × 4 masses × 4 scenarios × 3 reps.
- Each task is run in each formation, once as drawn and once with the two robots' start places exchanged.
  That is 2,880 episodes per checkpoint.
- What stays the same across formations and swaps: object, mass, goal, gaps and jitter (one draw per task).
- What changes: only the robots' bearings around the object.

| formation | anymal1 | anymal2 |
|---|---|---|
| standard (the benchmark) | 180° − 35°, world frame (behind left) | 180° + 35° (behind right) |
| flank: opposite faces across the goal axis | goal direction − 90° (right) | goal direction + 90° (left) |
| goal_behind: one placed well, one not | goal direction + 180° (behind) | goal direction (goal side, between the object and the goal) |

The unswapped standard rows are the benchmark placements, so they should match `nw-A`/`nw-B` up to rerun noise.
On every build the evaluator prints the largest difference between each robot's placed and intended bearing.

**Per episode, besides success and falls:**
- each robot's first push: its front within 8 cm of the object and behind it relative to the goal;
- the first time the object is 0.25 m closer to the goal;
- the first pusher;
- takeover: the time the other robot pushed while the first pusher did not, and the object's progress meanwhile.

**Analysis.** `scripts/placement_compare.py --runs=IPPO:place-nwA-ippo-it5000,MAPPO:place-nwB-mappo-it5000,PARENT:place-ten-ippo-it4000`.
- Success and falls per formation, paired against standard, overall and for arch, cylinder, long and sphere.
- Time to the first push and to the first progress.
- Roles: who leads (more push time) and who pushes first. Each is reported by start role and by robot identity,
  unswapped and swapped.
- The swap test, on matched pairs:
  - if leading follows the start place, the pair is switching roles;
  - if leading follows the identity, one actor is the fixed leader.
- Takeover episodes and their success.
- Differences between policies per formation, on the same tasks.

**Reading rules.**
- A rerun of one checkpoint flips about 15% of outcomes (`docs/ten_restart.md`). Only gaps well outside that are
  findings.
- A mixed-start training arm is warranted only if one formation shows a repeatable deficit, for example on more than
  one object or in both algorithms. That arm would be:
  - from iteration 4000;
  - 75% existing placements and 25% the failing formation;
  - reward, budget and sampler unchanged;
  - judged against arm A or B on the benchmark and on fresh placements.
- **The new starts must be built into a new task bank.** Replay restores the bank's saved bearings, so changing the
  start rule while reusing `bank_ten_s0_k16.pt` would not change any start.

## Results (2026-11-14; full tables in `evals/placement/placement_compare.md`)

Runs:
- Arms A and B: two evaluation runs each (`place-nwA-ippo-it5000[-r2]`, `place-nwB-mappo-it5000[-r2]`).
- Parent: one run so far (`place-ten-ippo-it4000`). Its rerun, `-r2`, is job 29119422.

Fidelity:
- Placed bearings matched the intended ones to 0.00° in every build.
- Unswapped standard rows: 312, 324 and 313 successes, against the benchmark's 315, 315 and 316. That is rerun level.
- A rerun flips 140–170 of 960 outcomes per formation.

**Success change vs standard, two-run mean per task** (points [95% CI]; ** = excludes 0):

| | IPPO flank | IPPO goal_behind | MAPPO flank | MAPPO goal_behind |
|---|---|---|---|---|
| all ten | −2.6 [−5.1, −0.1] ** | −2.0 [−4.4, +0.4] | −1.9 [−4.4, +0.5] | −4.1 [−6.6, −1.6] ** |
| cylinder | −8.9 [−16.7, −1.6] ** | −8.3 [−16.7, +0.0] | −12.5 [−19.8, −5.7] ** | −13.5 [−21.9, −5.2] ** |
| long | −4.7 | +2.6 | −11.5 [−19.8, −3.1] ** | −7.8 [−15.1, −0.5] ** |
| arch | −1.0 | +0.0 | +6.8 [−1.6, +15.1] | +1.0 |
| sphere | −2.6 | +1.0 | −0.5 | +0.5 |

Parent, single run: flank +0.7, goal_behind −0.9 overall; cylinder +0.0 and −4.2.

**Reading:**
- **The pairs mostly coordinate from unfamiliar relative starts.**
  - Overall cost: 2–4 points.
  - The first push comes as fast as from the standard start (median 1.1–1.3 s).
  - Mass still dominates: about 27% success at 80 kg in every formation.
- **Role switching follows the start place.**
  - In goal_behind, the robot that starts behind pushes first in 92–98% of episodes and leads (more push time) in
    74–84%, in both halves of the swap.
  - Success holds under the swap: 309/297 for IPPO, 303/298 for MAPPO, 311/293 for the parent.
  - On matched swap pairs, the leader follows the start place 71–74% of the time and the robot identity 26–29%.
  - A small identity bias remains: anymal1 leads about 5 points more often than its start place predicts.
- **Takeovers are common.** The second robot pushes alone while the object still progresses in 38–57% of episodes.
  Those episodes succeed more often (67–74% vs 52–63%).
- **Repeatable deficit: cylinder.**
  - It loses 8–14 points in both new formations, in both algorithms, pooled over two runs.
  - MAPPO also loses on long.
  - The parent's single run does not show it (0 and −4). If its rerun agrees, the deficit appeared during the
    next-wave 1000 iterations.
- **Arch is not placement-limited.** Flank does no worse, perhaps better, and the parent's arch falls halve in flank
  (34 → 17). Arch fails under load, not from the starting arrangement.

**Decision:**
- No mixed-start training is launched yet.
- The only repeatable deficit is one object, with a small overall cost.
- The parent rerun decides whether the deficit is inherited or new:
  - **Inherited:** a mixed-start arm from iteration 4000 (75% existing, 25% flank and goal_behind, built into a new
    bank) is the test.
  - **New:** the arms' 1000 uniform-bank iterations narrowed what they handle, and the mixed-start arm should be
    compared directly with arm A.
