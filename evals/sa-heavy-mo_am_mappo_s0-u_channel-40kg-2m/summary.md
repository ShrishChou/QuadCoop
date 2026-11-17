# Spot-arm turn pilot: sa-heavy-mo_am_mappo_s0-u_channel-40kg-2m

logs/marl2/mo_am_mappo_s0/model_4000.pt, iteration 4000, mappo, arms learned. u_channel 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 12 | 0.0% | 0.0% | - | 0.724 | 14.1 | +7.1 |
| both | straight | 12 | 0.0% | 0.0% | - | 0.887 | 26.2 | -25.2 |
| both | right | 12 | 0.0% | 0.0% | - | 0.753 | 70.7 | -53.8 |
| both | all | 36 | 0.0% | 0.0% | - | 0.744 | 18.9 | -24.0 |
| none | left | 12 | 0.0% | 8.3% | - | 0.778 | 15.6 | +6.5 |
| none | straight | 12 | 0.0% | 0.0% | - | 0.837 | 26.1 | -23.6 |
| none | right | 12 | 0.0% | 0.0% | - | 1.303 | 25.4 | -35.8 |
| none | all | 36 | 0.0% | 2.8% | - | 0.778 | 16.5 | -17.7 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.966 | 33.9 | +7.5 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.948 | 51.0 | -55.0 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.922 | 108.9 | -79.4 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.922 | 59.9 | -42.3 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.857 | 66.3 | +59.8 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.831 | 10.2 | +17.3 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.453 | 34.0 | -25.6 |
| solo_2 | all | 36 | 0.0% | 2.8% | - | 1.814 | 42.4 | +17.2 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| none | +0.0 [+0.0, +0.0] pts | 0 | 0 | -3.3 [-10.3, +3.2] |
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +35.2 [+18.8, +52.1] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +6.7 [-8.3, +21.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 0.0% | 0.0% | 0.0% | 0.3% | 0.9% | 25.6% |
| both | straight | 0.0% | 0.0% | 0.0% | 0.1% | 1.3% | 30.2% |
| both | right | 0.0% | 0.0% | 0.0% | 0.5% | 9.8% | 22.8% |
| none | left | 0.0% | 0.0% | 0.0% | 1.3% | 5.8% | 20.9% |
| none | straight | 0.0% | 0.0% | 0.0% | 0.0% | 12.0% | 3.8% |
| none | right | 0.0% | 0.0% | 0.0% | 0.0% | 19.8% | 1.9% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.3% | 0.3% | 35.3% | 2.9% |
| solo_2 | straight | 0.0% | 0.0% | 0.1% | 0.0% | 6.9% | 17.3% |
| solo_2 | right | 0.0% | 0.0% | 0.1% | 0.0% | 11.6% | 1.0% |
