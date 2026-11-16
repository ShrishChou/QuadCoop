# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-long-20kg-1m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 15.0% | 0.0% | 9.4 | 0.255 | 4.6 | +3.4 |
| stowed | straight | 40 | 25.0% | 0.0% | 6.8 | 0.492 | 6.5 | +5.5 |
| stowed | right | 40 | 27.5% | 0.0% | 5.3 | 0.247 | 2.7 | +0.6 |
| stowed | all | 120 | 22.5% | 0.0% | 6.2 | 0.270 | 3.6 | +3.2 |
| solo_1 | left | 40 | 0.0% | 7.5% | - | 0.633 | 72.2 | -38.3 |
| solo_1 | straight | 40 | 0.0% | 2.5% | - | 1.000 | 27.9 | +24.9 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 1.000 | 32.5 | -34.3 |
| solo_1 | all | 120 | 0.0% | 3.3% | - | 0.987 | 47.1 | -15.9 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.929 | 31.2 | +25.6 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.846 | 33.6 | -32.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.950 | 60.1 | -20.2 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.883 | 42.8 | -8.9 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -22.5 [-30.0, -15.0] pts | 27 | 0 | +38.7 [+33.7, +43.6] |
| solo_2 | -22.5 [-30.0, -15.0] pts | 27 | 0 | +40.5 [+35.6, +45.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 25.0% | 5.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 40.0% | 10.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 55.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
