# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-cylinder-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. cylinder 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 8.3% | 8.3% | 28.4 | 0.263 | 8.3 | +6.3 |
| stowed | straight | 12 | 50.0% | 8.3% | 6.5 | 0.087 | 2.5 | +0.1 |
| stowed | right | 12 | 0.0% | 0.0% | - | 0.250 | 23.3 | -22.2 |
| stowed | all | 36 | 19.4% | 5.6% | 6.5 | 0.238 | 8.3 | -5.3 |
| solo_1 | left | 12 | 0.0% | 16.7% | - | 1.047 | 65.3 | +65.8 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.247 | 5.4 | +1.6 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 1.287 | 51.3 | -51.7 |
| solo_1 | all | 36 | 0.0% | 5.6% | - | 1.132 | 51.3 | +5.2 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.361 | 54.0 | +52.8 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.565 | 4.7 | -6.4 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 0.598 | 63.2 | -65.9 |
| solo_2 | all | 36 | 0.0% | 2.8% | - | 1.035 | 54.0 | -6.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -19.4 [-33.3, -8.3] pts | 7 | 0 | +28.7 [+21.0, +36.6] |
| solo_2 | -19.4 [-33.3, -8.3] pts | 7 | 0 | +29.7 [+22.6, +36.8] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 16.7% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 33.3% | 66.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
