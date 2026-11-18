# Opposing-force costs (two ANYmals, IPPO and MAPPO)

Status (2026-11-17): queued after the S0-S4 trainings (`slurm/submit_opposing_force.sh`; check job first).

**Why.** r7 has no per-robot cost for negative work: `push_credit` is clamped at 0 and the object-progress terms
are shared, so a robot that loses contact and comes back pushing the wrong way, or two robots squeezing the object
against each other, cost both robots the same slower progress and neither specifically. r8's `work_credit` (pay
each robot for its force along the goal direction) cut idling but lowered success (55-59% vs 63%): it paid
pushing even when yielding or steering was better. These costs pay nothing for pushing; they only charge
working against the motion the task wants.

**Terms** (`mdp.py`):
- Wanted motion: the command's own rule (`_wanted`): toward the goal position and heading, each saturating
  (0.3 m/s, 0.4 rad/s) and slowing near the goal; as a unit twist (v, rho w) / |(v, rho w)|, rho = the object's
  bounding radius. Off within 0.1 m of the goal.
- `oppose_<robot>` (per robot, weight `--oppose-cost`, 0.5): max(0, -(F . v_hat + (tau / rho) w_hat) / 200 N),
  capped at 2; F = the robot's contact force on the object (`push_<robot>` sensor), tau about the object from the
  robot's front point. A turning couple helps the wanted yaw, so it is not "against"; braking an overshoot helps the
  wanted motion back to the goal.
- `force_cancellation` (team, weight `--cancel-cost`, 0.25): (|F1| + |F2| - |F1 + F2|) / 200 N x (1 - turning share
  of the wanted motion), capped at 2: squeezing while only translation is wanted.
- Scale: a robot pushing 100 N straight against the wanted motion pays 0.25 per second, about the goal-error
  cost's rate at the start of a task.

**Arms** (S0's settings, `docs/actor_schedule.md`: the ten-object parent's actors, fresh critics, 100 critic-only
iterations, 2000 actor iterations to 6100, uniform bank, start swaps, joint updates):

| arm | algorithm | costs | compared with |
|---|---|---|---|
| OFi `ofI_ippo_oppose_s0` | IPPO | yes | S0 `asS0_joint_s0` |
| OFm `ofM_mappo_oppose_s0` | MAPPO | yes | OFm0 |
| OFm0 `ofM0_mappo_joint_s0` | MAPPO | no | (the MAPPO control under these settings) |

Evaluation: the 480 benchmark tasks x standard / flank / goal-behind x starts exchanged. Read: success and its
per-object minimum, 60-80 kg success, idle share (both robots' work, `--recovery` traces), opposing-power and
cancellation rates in evaluation, falls. Risk to watch: robots avoiding contact to avoid the cost (idle share up).
