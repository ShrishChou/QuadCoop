# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-arch-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. arch 40 kg, 2 m, 6 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 12 | 25.0% | 0.0% | 22.7 | 0.216 | 8.2 | +8.6 |
| stowed | straight | 12 | 41.7% | 0.0% | 8.5 | 0.237 | 5.1 | +4.4 |
| stowed | right | 12 | 58.3% | 0.0% | 15.5 | 0.085 | 5.5 | +3.2 |
| stowed | all | 36 | 41.7% | 0.0% | 14.8 | 0.210 | 5.5 | +5.4 |
| solo_1 | left | 12 | 0.0% | 50.0% | - | 1.849 | 64.8 | +40.5 |
| solo_1 | straight | 12 | 0.0% | 8.3% | - | 1.905 | 8.8 | -7.1 |
| solo_1 | right | 12 | 0.0% | 16.7% | - | 1.883 | 65.1 | -62.1 |
| solo_1 | all | 36 | 0.0% | 25.0% | - | 1.849 | 55.1 | -9.6 |
| solo_2 | left | 12 | 0.0% | 8.3% | - | 1.987 | 60.0 | +61.2 |
| solo_2 | straight | 12 | 0.0% | 0.0% | - | 1.999 | 0.1 | -1.8 |
| solo_2 | right | 12 | 0.0% | 0.0% | - | 1.987 | 60.3 | -60.9 |
| solo_2 | all | 36 | 0.0% | 2.8% | - | 1.988 | 59.6 | -0.5 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -41.7 [-58.3, -25.0] pts | 15 | 0 | +35.4 [+26.4, +44.9] |
| solo_2 | -41.7 [-58.3, -25.0] pts | 15 | 0 | +34.6 [+26.1, +43.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 0.0% | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 33.3% | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 50.0% | 66.7% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
