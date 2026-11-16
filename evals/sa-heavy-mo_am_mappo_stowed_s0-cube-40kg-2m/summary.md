# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-cube-40kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. cube 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left -30.0 to -30.0 deg, straight +0.0 to +0.0 deg, right +30.0 to +30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 16.7% | 8.3% | 9.3 | 0.289 | 3.7 | -2.6 |
| stowed | straight | 12 | 58.3% | 0.0% | 8.7 | 0.094 | 2.8 | -1.3 |
| stowed | right | 12 | 8.3% | 0.0% | 10.5 | 0.423 | 1.7 | -0.8 |
| stowed | all | 36 | 27.8% | 2.8% | 8.9 | 0.281 | 2.8 | -1.6 |
| solo_1 | left | 12 | 0.0% | 0.0% | - | 1.584 | 41.0 | +40.3 |
| solo_1 | straight | 12 | 0.0% | 0.0% | - | 1.448 | 41.9 | -4.5 |
| solo_1 | right | 12 | 0.0% | 0.0% | - | 2.000 | 30.0 | +26.9 |
| solo_1 | all | 36 | 0.0% | 0.0% | - | 1.584 | 38.6 | +20.9 |
| solo_2 | left | 12 | 0.0% | 0.0% | - | 2.000 | 30.0 | -29.8 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 2.000 | 30.0 | +31.2 |
| solo_2 | all | 36 | 0.0% | 0.0% | - | 2.000 | 30.0 | +0.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -27.8 [-41.7, -13.9] pts | 10 | 0 | +31.7 [+28.7, +34.4] |
| solo_2 | -27.8 [-41.7, -13.9] pts | 10 | 0 | +16.5 [+11.8, +21.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 33.3% | 0.0% | 0.0% | 24.1% | 30.7% |
| stowed | straight | 50.0% | 66.7% | 0.0% | 0.0% | 27.1% | 15.3% |
| stowed | right | 0.0% | 16.7% | 0.0% | 0.0% | 34.6% | 3.9% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
