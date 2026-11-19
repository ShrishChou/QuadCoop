# Spot-arm turn pilot: sa-mech-s3-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: on. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 90.0% | 7.5% | 17.6 | 0.074 | 2.2 | +0.9 |
| both | straight | 40 | 97.5% | 0.0% | 14.3 | 0.068 | 1.7 | +0.0 |
| both | right | 40 | 97.5% | 0.0% | 10.6 | 0.080 | 1.1 | +0.5 |
| both | all | 120 | 95.0% | 2.5% | 14.0 | 0.074 | 1.6 | +0.5 |
| only_1 | left | 40 | 92.5% | 5.0% | 18.1 | 0.062 | 1.6 | +2.0 |
| only_1 | straight | 40 | 90.0% | 7.5% | 14.4 | 0.071 | 1.7 | +2.3 |
| only_1 | right | 40 | 95.0% | 2.5% | 13.9 | 0.067 | 1.5 | +0.4 |
| only_1 | all | 120 | 92.5% | 5.0% | 15.8 | 0.069 | 1.5 | +1.6 |
| only_2 | left | 40 | 90.0% | 5.0% | 17.7 | 0.074 | 1.5 | +4.7 |
| only_2 | straight | 40 | 100.0% | 0.0% | 12.1 | 0.072 | 1.2 | +0.5 |
| only_2 | right | 40 | 97.5% | 0.0% | 11.1 | 0.061 | 1.8 | +1.3 |
| only_2 | all | 120 | 95.8% | 1.7% | 12.9 | 0.071 | 1.5 | +2.2 |
| none | left | 40 | 82.5% | 10.0% | 15.1 | 0.067 | 1.7 | +10.4 |
| none | straight | 40 | 97.5% | 2.5% | 13.7 | 0.070 | 1.4 | +0.1 |
| none | right | 40 | 92.5% | 2.5% | 10.8 | 0.063 | 1.6 | +0.2 |
| none | all | 120 | 90.8% | 5.0% | 13.2 | 0.067 | 1.6 | +3.6 |
| hold_out | left | 40 | 0.0% | 0.0% | - | 1.290 | 17.5 | +3.6 |
| hold_out | straight | 40 | 0.0% | 0.0% | - | 0.876 | 16.3 | +3.0 |
| hold_out | right | 40 | 2.5% | 0.0% | 21.8 | 1.107 | 6.8 | -11.0 |
| hold_out | all | 120 | 0.8% | 0.0% | 21.8 | 1.051 | 14.4 | -1.5 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | -2.5 [-9.2, +3.3] pts | 9 | 6 | +1.0 [-0.3, +2.7] |
| only_2 | +0.8 [-4.2, +5.8] pts | 4 | 5 | +0.9 [-0.4, +2.5] |
| none | -4.2 [-10.8, +2.5] pts | 11 | 6 | +3.3 [+0.7, +6.3] |
| hold_out | -94.2 [-98.3, -90.0] pts | 113 | 0 | +18.2 [+14.8, +21.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 90.0% | 90.0% | 0.1% | 0.1% | 26.0% | 22.5% |
| both | straight | 95.0% | 100.0% | 0.3% | 0.3% | 24.6% | 27.2% |
| both | right | 95.0% | 100.0% | 0.1% | 0.3% | 28.9% | 30.7% |
| only_1 | left | 95.0% | 90.0% | 0.0% | 0.0% | 19.1% | 36.1% |
| only_1 | straight | 95.0% | 85.0% | 0.0% | 0.1% | 28.3% | 24.7% |
| only_1 | right | 95.0% | 95.0% | 0.1% | 0.0% | 21.7% | 33.2% |
| only_2 | left | 95.0% | 85.0% | 0.1% | 0.4% | 29.2% | 23.4% |
| only_2 | straight | 100.0% | 100.0% | 0.5% | 0.1% | 24.5% | 25.5% |
| only_2 | right | 95.0% | 100.0% | 0.0% | 0.4% | 26.9% | 29.2% |
| none | left | 90.0% | 75.0% | 0.0% | 0.1% | 20.7% | 30.9% |
| none | straight | 100.0% | 95.0% | 0.0% | 0.1% | 24.3% | 26.2% |
| none | right | 95.0% | 90.0% | 0.0% | 0.0% | 25.5% | 34.4% |
| hold_out | left | 0.0% | 0.0% | 33.9% | 27.3% | 12.7% | 2.2% |
| hold_out | straight | 0.0% | 0.0% | 42.6% | 45.8% | 29.0% | 6.2% |
| hold_out | right | 0.0% | 5.0% | 32.0% | 48.1% | 7.3% | 16.8% |
