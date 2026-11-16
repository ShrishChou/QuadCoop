# Spot-arm turn pilot: sa-heavy-sa_heavy_solo_s0-40kg-2m

logs/marl2/sa_heavy_solo_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 0.0% | 17.5% | - | 1.673 | 47.8 | +11.3 |
| both | straight | 40 | 0.0% | 22.5% | - | 1.712 | 20.1 | -19.7 |
| both | right | 40 | 0.0% | 22.5% | - | 1.605 | 72.9 | -18.3 |
| both | all | 120 | 0.0% | 20.8% | - | 1.668 | 47.1 | -8.9 |
| only_1 | left | 40 | 0.0% | 2.5% | - | 1.890 | 44.3 | +39.7 |
| only_1 | straight | 40 | 0.0% | 5.0% | - | 1.960 | 18.0 | -23.5 |
| only_1 | right | 40 | 0.0% | 0.0% | - | 2.011 | 72.0 | -15.2 |
| only_1 | all | 120 | 0.0% | 2.5% | - | 1.940 | 55.2 | +0.3 |
| only_2 | left | 40 | 0.0% | 30.0% | - | 1.593 | 49.2 | +34.3 |
| only_2 | straight | 40 | 0.0% | 20.0% | - | 1.624 | 26.7 | -19.5 |
| only_2 | right | 40 | 0.0% | 27.5% | - | 1.617 | 67.0 | -27.7 |
| only_2 | all | 120 | 0.0% | 25.8% | - | 1.614 | 47.5 | -4.3 |
| none | left | 40 | 0.0% | 0.0% | - | 1.775 | 34.6 | +35.7 |
| none | straight | 40 | 0.0% | 7.5% | - | 1.719 | 31.8 | -33.1 |
| none | right | 40 | 0.0% | 0.0% | - | 1.868 | 73.1 | -48.2 |
| none | all | 120 | 0.0% | 2.5% | - | 1.821 | 54.8 | -15.2 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 1.309 | 13.8 | +24.8 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.306 | 14.1 | -14.8 |
| solo_1 | right | 40 | 0.0% | 5.0% | - | 1.303 | 38.0 | -9.5 |
| solo_1 | all | 120 | 0.0% | 1.7% | - | 1.303 | 18.0 | +0.2 |
| solo_2 | left | 40 | 0.0% | 5.0% | - | 1.957 | 55.8 | +55.7 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.960 | 4.7 | -4.7 |
| solo_2 | right | 40 | 0.0% | 2.5% | - | 1.972 | 64.4 | -63.6 |
| solo_2 | all | 120 | 0.0% | 2.5% | - | 1.957 | 55.8 | -4.2 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.8 [-3.9, +5.6] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -0.8 [-4.9, +3.1] |
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | +3.7 [-1.3, +8.3] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -18.8 [-24.1, -13.6] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.3 [-7.2, +0.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 22.2% | 12.2% | 14.5% | 8.3% |
| both | straight | 0.0% | 0.0% | 7.1% | 0.4% | 6.4% | 1.5% |
| both | right | 0.0% | 0.0% | 8.9% | 1.5% | 8.3% | 2.9% |
| only_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 14.2% | 0.3% |
| only_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 13.2% | 1.4% |
| only_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 22.4% | 10.7% |
| only_2 | left | 0.0% | 0.0% | 0.2% | 0.2% | 32.4% | 16.8% |
| only_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 21.6% | 5.2% |
| only_2 | right | 0.0% | 0.0% | 0.0% | 0.5% | 28.9% | 6.3% |
| none | left | 0.0% | 0.0% | 0.0% | 0.0% | 12.9% | 0.4% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 28.2% | 2.7% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 42.2% | 1.7% |
| solo_1 | left | 0.0% | 0.0% | 0.1% | 0.0% | 16.0% | 14.4% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 26.5% | 16.6% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 34.2% | 23.5% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.4% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.3% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.5% |
