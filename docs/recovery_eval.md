# Contact loss and recovery: planner-free IPPO, iterations 3000 and 4000

Status (2026-11-14): measurement built and queued. This is a separate pass, and the 480-task comparison runs as
submitted.

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
