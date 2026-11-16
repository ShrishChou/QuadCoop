# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-long-40kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 20.0% | 0.0% | 15.2 | 0.395 | 5.8 | +7.8 |
| stowed | straight | 40 | 25.0% | 0.0% | 15.1 | 0.292 | 4.0 | +3.8 |
| stowed | right | 40 | 27.5% | 0.0% | 8.5 | 0.214 | 2.0 | +0.4 |
| stowed | all | 120 | 24.2% | 0.0% | 10.3 | 0.244 | 3.5 | +4.0 |
| solo_1 | left | 40 | 0.0% | 5.0% | - | 1.600 | 64.7 | -15.5 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 1.871 | 51.6 | +1.0 |
| solo_1 | right | 40 | 0.0% | 2.5% | - | 1.832 | 50.9 | -24.3 |
| solo_1 | all | 120 | 0.0% | 2.5% | - | 1.693 | 51.6 | -13.0 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.836 | 46.2 | +35.9 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.814 | 30.8 | -30.2 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.642 | 67.1 | -16.0 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.776 | 47.4 | -3.4 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -24.2 [-32.5, -16.7] pts | 29 | 0 | +38.4 [+33.4, +43.3] |
| solo_2 | -24.2 [-32.5, -16.7] pts | 29 | 0 | +39.9 [+35.0, +44.6] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 40.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 50.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 35.0% | 20.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
