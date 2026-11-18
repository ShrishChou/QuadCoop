# Spot-arm turn pilot: sa-mech-rai-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 77.5% | 12.5% | 17.1 | 0.080 | 1.4 | +2.6 |
| both | straight | 40 | 85.0% | 0.0% | 12.7 | 0.064 | 1.4 | +0.2 |
| both | right | 40 | 57.5% | 0.0% | 13.5 | 0.091 | 2.3 | -2.1 |
| both | all | 120 | 73.3% | 4.2% | 14.8 | 0.080 | 1.6 | +0.2 |
| only_1 | left | 40 | 47.5% | 0.0% | 21.8 | 0.143 | 2.4 | +9.7 |
| only_1 | straight | 40 | 45.0% | 0.0% | 13.8 | 0.147 | 1.8 | -0.9 |
| only_1 | right | 40 | 52.5% | 0.0% | 20.3 | 0.096 | 2.4 | -0.2 |
| only_1 | all | 120 | 48.3% | 0.0% | 18.5 | 0.100 | 2.2 | +2.9 |
| only_2 | left | 40 | 70.0% | 12.5% | 22.0 | 0.082 | 1.9 | +2.5 |
| only_2 | straight | 40 | 85.0% | 0.0% | 18.9 | 0.079 | 1.9 | -1.3 |
| only_2 | right | 40 | 57.5% | 0.0% | 20.2 | 0.094 | 2.3 | -1.0 |
| only_2 | all | 120 | 70.8% | 4.2% | 21.0 | 0.082 | 1.9 | +0.0 |
| none | left | 40 | 45.0% | 5.0% | 31.3 | 0.132 | 1.9 | +10.1 |
| none | straight | 40 | 47.5% | 0.0% | 18.3 | 0.088 | 1.4 | -1.0 |
| none | right | 40 | 27.5% | 0.0% | 21.1 | 0.326 | 4.8 | -0.5 |
| none | all | 120 | 40.0% | 1.7% | 22.7 | 0.177 | 1.9 | +2.9 |
| hold_out | left | 40 | 0.0% | 10.0% | - | 1.353 | 12.1 | +19.0 |
| hold_out | straight | 40 | 0.0% | 0.0% | - | 1.546 | 10.5 | -4.1 |
| hold_out | right | 40 | 0.0% | 0.0% | - | 1.615 | 52.4 | -41.5 |
| hold_out | all | 120 | 0.0% | 3.3% | - | 1.533 | 16.8 | -8.9 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -25.0 [-36.7, -13.3] pts | 43 | 13 | +3.3 [+1.0, +5.7] |
| only_2 | -2.5 [-12.5, +7.5] pts | 21 | 18 | +0.3 [-1.6, +2.1] |
| none | -33.3 [-45.0, -21.7] pts | 53 | 13 | +4.1 [+1.7, +6.7] |
| hold_out | -73.3 [-80.8, -65.8] pts | 88 | 0 | +23.4 [+19.7, +27.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 60.0% | 95.0% | 0.0% | 0.4% | 47.3% | 24.5% |
| both | straight | 90.0% | 80.0% | 0.1% | 0.3% | 45.6% | 49.8% |
| both | right | 55.0% | 60.0% | 0.1% | 0.2% | 38.2% | 46.5% |
| only_1 | left | 40.0% | 55.0% | 0.0% | 0.0% | 48.3% | 47.2% |
| only_1 | straight | 40.0% | 50.0% | 0.0% | 0.1% | 41.9% | 54.9% |
| only_1 | right | 50.0% | 55.0% | 0.0% | 0.2% | 34.4% | 45.3% |
| only_2 | left | 60.0% | 80.0% | 0.0% | 0.5% | 47.3% | 20.1% |
| only_2 | straight | 85.0% | 85.0% | 0.1% | 0.2% | 41.3% | 48.9% |
| only_2 | right | 40.0% | 75.0% | 0.0% | 0.2% | 41.4% | 45.2% |
| none | left | 45.0% | 45.0% | 0.0% | 0.3% | 45.6% | 38.2% |
| none | straight | 45.0% | 50.0% | 0.0% | 0.0% | 41.4% | 54.1% |
| none | right | 40.0% | 15.0% | 0.0% | 0.0% | 42.2% | 49.7% |
| hold_out | left | 0.0% | 0.0% | 46.9% | 36.9% | 33.2% | 7.9% |
| hold_out | straight | 0.0% | 0.0% | 36.7% | 33.7% | 14.6% | 11.9% |
| hold_out | right | 0.0% | 0.0% | 35.7% | 36.6% | 11.3% | 20.0% |
