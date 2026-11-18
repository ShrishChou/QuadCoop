# Spot-arm turn pilot: smoke-mech-b

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 1 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: 0.1,0.45 (interface True, expanded ['spotarm1', 'spotarm2']). Arm-object collisions: off. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| hold_out | left | 2 | 0.0% | 0.0% | - | 1.030 | 3.7 | +2.1 |
| hold_out | straight | 2 | 0.0% | 0.0% | - | 1.234 | 6.9 | -4.4 |
| hold_out | right | 2 | 0.0% | 0.0% | - | 1.815 | 64.3 | -52.6 |
| hold_out | all | 6 | 0.0% | 0.0% | - | 1.234 | 6.9 | -18.3 |
| hold_mean | left | 2 | 100.0% | 0.0% | 35.2 | 0.080 | 4.7 | +3.8 |
| hold_mean | straight | 2 | 50.0% | 0.0% | 18.8 | 0.415 | 3.9 | +3.0 |
| hold_mean | right | 2 | 50.0% | 0.0% | 9.2 | 0.441 | 30.9 | -14.2 |
| hold_mean | all | 6 | 66.7% | 0.0% | 31.7 | 0.080 | 3.9 | -2.5 |

Ablation, paired per task against hold_out (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| hold_mean | +66.7 [+33.3, +100.0] pts | 0 | 4 | -11.9 [-32.7, +1.0] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| hold_out | left | 0.0% | 0.0% | 0.0% | 0.0% | 20.0% | 6.6% |
| hold_out | straight | 0.0% | 0.0% | 0.0% | 0.0% | 8.2% | 18.2% |
| hold_out | right | 0.0% | 0.0% | 0.0% | 0.0% | 13.6% | 28.2% |
| hold_mean | left | 100.0% | 100.0% | 0.0% | 0.0% | 35.8% | 13.1% |
| hold_mean | straight | 0.0% | 100.0% | 0.0% | 0.0% | 54.2% | 56.4% |
| hold_mean | right | 0.0% | 100.0% | 0.0% | 0.0% | 36.6% | 50.6% |

Release (retract), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| hold_out | 0 | - | - | - | - |
| hold_mean | 4 | 75.0% | 0.008 | 0.6 | 0.0% |
