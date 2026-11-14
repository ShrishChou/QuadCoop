# Contact loss and recovery: planner-free IPPO, iterations 3000 and 4000

Status (2026-11-14): done for iterations 3000 and 4000; results below. No recovery training change is warranted yet.

**Why.** The planner-free policy has no assigned contact point. It can walk back to the same face, choose another, or
stay off while its partner pushes. The existing evaluation columns can't tell these apart:
- `touch_frac` is robot-to-robot contact;
- `push_frac` is geometric: the front within 8 cm of the object and behind it.

**Run.**
- `eval_coop2.py --recovery`, on the same 480 seed-7100 tasks. The robot–object contact sensors are switched on for
  logging only; the policy, observations and outcome rules are unchanged.
- Each episode gets a 10 Hz trace: each robot's contact fraction and force, its front point in the object frame,
  the push rule, the object's position and heading error, and falls.
- Output: `logs/evals/<name>/pair/recovery_<mass>kg.npz`.
- The pass writes the usual episodes file too. It should reproduce the matched evaluation's outcomes, up to GPU
  nondeterminism.

**Analysis.** `scripts/recovery_analysis.py`, on CPU; definitions in its docstring.

| question | measure |
|---|---|
| Did the robot disengage? | Sustained contact (1 s trailing contact fraction ≥ 0.3 for ≥ 1 s), then ≥ 1 s with no contact at all. A dip inside one gait cycle doesn't count. |
| Did it recover? | Re-engagement (the start of 1 s at contact fraction ≥ 0.3) within 1, 3 and 5 s after the loss is confirmed. Also reported: time to re-engage, and whether it came back to the same place (front point within 0.3 m in the object frame) or a different part. Episodes that end first are censored by how they ended: success, own fall, partner fall, other. |
| Did leaving hurt? | During the separation: the share of time the partner was engaged and behind the object, and the change in the object's position and heading error. Each separation is classed as stall, productive repositioning, modest, or release near the goal (≤ 0.3 m at the loss). Episodes with a prolonged (≥ 3 s) stalled separation are compared with the rest on success. |

**Rule for a training change.** Change training only if prolonged contact loss repeatedly coincides with stalled
progress and failed placement.
- The first experiment would then start a robot a short distance off the object while its partner is already
  engaged, and train with the existing goal reward. That gives practice at recovering and leaves the face free to
  choose.
- Productive repositioning would not be forced back to the old point: that is the coordination behaviour under study.

**Jobs.**
- 29057447: iteration 3000.
- 29057448: iteration 4000, after training succeeds and the 480-task evaluation ends.

At most two GPUs are in use at once.

## Results (`evals/recovery/summary.md`; every event in `evals/recovery/*_events.csv`)

**Fidelity.**
- The logging passes matched the main evaluations on 398/480 tasks (iteration 3000) and 412/480 (iteration 4000).
  That is the rerun noise of GPU simulation, not an effect of the sensors.
- Totals: 309 vs 303 successes at iteration 3000, 311 vs 315 at iteration 4000.

| | iteration 3000 | iteration 4000 |
|---|---|---|
| disengagements | 802 (1.67 per episode; 315 episodes) | 774 (1.61; 322 episodes) |
| re-engaged within 1 / 3 / 5 s of confirmation (share of decided) | 34% / 56% / 69% | 33% / 57% / 71% |
| time to re-engage after confirmation, median (p90) | 1.6 s (10.4 s) | 1.7 s (9.2 s) |
| re-engaged at the same place / a different place | 276 / 375 | 246 / 376 |
| productive repositioning: n, partner pushing share, object moved (median), episode success | 287, 0.56, 0.36 m, 54% | 282, 0.57, 0.42 m, 63% |
| release near the goal: n, episode success | 283, 63% | 285, 68% |
| stall: n, partner pushing share, episode success | 165, 0.29, 29% | 165, 0.29, 23% |
| prolonged (≥ 3 s) separations: productive / near goal / stall / modest | 215 / 122 / 46 / 29 | 214 / 123 / 38 / 14 |
| episodes with a prolonged stalled separation, and their success | 37 (19%) | 27 (11%) |
| success of the other episodes | 68% | 68% |

**Reading:**
- **Disengaging is common, and mostly useful or harmless.**
  - About a third of separations are productive: the partner keeps pushing more than half the time, and the object
    moves about 0.4 m.
  - Another third are releases near the goal.
  - Most robots come back: 70% within 5 s. Nearly 60% return to a different place.
  - This is the planner-free policy choosing its face, which a "return to your point" rule would suppress.
- **Prolonged stalls do predict failure, but they are not the main failure mode.**
  - They occur in 37 (iteration 3000) and 27 (iteration 4000) of 480 episodes, which succeed 19% and 11% of the time.
  - That is about 17% and 15% of all failures.
  - Causation could also run the other way: an object that jams makes a robot leave.
  - They concentrate on arch (8 failed episodes at iteration 4000) and dumbbell (6).
- **Decision (the rule set above):**
  - Prolonged loss coincides with stalls and failure in a minority of episodes, so it is not repeated across the
    benchmark.
  - Don't train a recovery change now.
  - Look at arch's stalled separations in the next-wave arms. That is where the off-contact start experiment would
    be tried first if the pattern grows.
