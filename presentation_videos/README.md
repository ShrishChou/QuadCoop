# QuadCoop presentation videos

42 clips in 9 folders, in presentation order. Each file name is `<system>_<object>_<mass>__<outcome>`.

Outcomes:
- `success`: within 10 cm and 6° of the goal for 1 s;
- `fail_timeout`: the horizon ran out;
- `fail_fell`: a robot fell.

Captions are burned into each clip. Unless noted, tasks are the 480-task benchmark: the object at the origin, both robots
behind it, the goal 3 m ahead; `far_turn` means 5 m ahead with a 90° turn.

| folder | what it shows | the number behind it |
|---|---|---|
| 01_individual_walkers | ANYmal and Spot walking policies alone: velocity tracking, resisting pushes, walking into a 30 kg cube | the frozen walkers every team uses |
| 02_single_robot_baseline | one robot with its single-robot push policy, partner parked | ANYmal alone 52.4%, Spot alone 40.7% |
| 03_frozen_pair_untrained | two single-robot policies side by side, never trained together | 46.2%, worse than one ANYmal |
| 04_ippo_mappo_kl_anchor_near_walker | IPPO and MAPPO trained with a KL anchor to the single-robot policy, so behaviour stays close to it; plus MAPPO without the anchor, which drifts (timeouts, a fall) | ANYmal pair, 60 kg, iteration 3000 |
| 05_ippo_mappo_final_trained | the final ten-object IPPO and MAPPO teams at 40 and 80 kg | IPPO 65.6%, MAPPO 64.6% (ANYmal + ANYmal) |
| 06_contact_planner | the contact planner + executor: three successes, two timeouts, one fall | – |
| 07_spot_arm_transport | two Spots with arms, 20 kg long object, 1 m, straight or ±60° | arms active 99.2%, arms locked 99.2%, partner parked 0%; stowed-trained pair 81.7% |
| 08_spot_arm_hand_reach | one Spot reaching left, right or stowed, then walking into the object | left turns it clockwise, right counter-clockwise, stowed barely turns |
| 09_turn_in_place | 20 kg long object, centre held at the goal, turned 40° counter-clockwise (`ccw`) or clockwise (`cw`); scripted maneuver with both hands or trunk only, and the behaviour clone | scripted: both hands 78%, trunk only 25%, one robot alone 0%; clone 11/16 |

In folder 09, all three filmed clockwise episodes failed. The clone is much weaker clockwise (38% vs 100% counter-clockwise).

The source runs live in `logs/evals/<name>/` and `evals/spot_arm/` on the cluster.

Pending, to be added after their evaluations:
- learned turn-in-place T1–T3;
- the hardware comparison (Spot-arm pair vs armless Spot pair vs ANYmal + Spot).
