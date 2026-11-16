# Spot-arm turn pilot: sa-heavy-mo_am_mappo_stowed_s0-long-60kg-2m

logs/marl2/mo_am_mappo_stowed_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 60 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 0.0% | 0.0% | - | 0.859 | 12.6 | -6.8 |
| stowed | straight | 40 | 0.0% | 5.0% | - | 0.840 | 20.1 | -19.4 |
| stowed | right | 40 | 0.0% | 5.0% | - | 0.708 | 25.4 | -5.5 |
| stowed | all | 120 | 0.0% | 3.3% | - | 0.798 | 18.2 | -10.6 |
| solo_1 | left | 40 | 0.0% | 2.5% | - | 1.825 | 44.6 | +46.0 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.395 | 48.6 | -47.8 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.525 | 80.7 | +73.2 |
| solo_1 | all | 120 | 0.0% | 0.8% | - | 1.563 | 56.3 | +23.8 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | +60.2 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 2.000 | 0.0 | +0.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 2.000 | 60.0 | -60.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 2.000 | 60.0 | +0.1 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +36.8 [+32.7, +40.9] |
| solo_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +18.4 [+12.4, +24.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 0.0% | 0.0% | 0.0% | 20.1% | 13.5% |
| stowed | straight | 0.0% | 0.0% | 0.0% | 0.6% | 20.0% | 14.6% |
| stowed | right | 0.0% | 0.0% | 0.0% | 0.4% | 15.3% | 26.3% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
