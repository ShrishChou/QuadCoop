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
