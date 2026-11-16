# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-cylinder-40kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. cylinder 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 0.0% | 8.3% | - | 0.150 | 34.5 | +34.9 |
| stowed | straight | 12 | 16.7% | 0.0% | 7.1 | 0.190 | 5.1 | +1.2 |
| stowed | right | 12 | 0.0% | 16.7% | - | 0.253 | 48.2 | -45.5 |
| stowed | all | 36 | 5.6% | 8.3% | 7.1 | 0.222 | 27.8 | -3.1 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.021 | 53.1 | +53.4 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 0.839 | 19.5 | -19.4 |
| solo_1 | right | 12 | 0.0% | 8.3% | - | 1.627 | 67.7 | -68.3 |
| solo_1 | all | 36 | 0.0% | 2.8% | - | 1.097 | 53.1 | -11.4 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | +60.0 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 60.0 | +0.0 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +18.4 [+14.9, +22.4] |
| solo_2 | -5.6 [-13.9, +0.0] pts | 2 | 0 | +11.4 [+5.9, +17.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 3.3% | 19.3% |
| stowed | straight | 0.0% | 33.3% | 0.0% | 0.0% | 16.7% | 18.3% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 26.4% | 13.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
