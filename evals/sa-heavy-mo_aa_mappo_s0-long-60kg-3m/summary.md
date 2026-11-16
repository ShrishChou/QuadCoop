# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-long-60kg-3m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 60 kg, 3 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 7.5% | 7.5% | 39.0 | 1.104 | 7.3 | +5.7 |
| stowed | straight | 40 | 2.5% | 2.5% | 23.3 | 1.236 | 5.9 | -5.0 |
| stowed | right | 40 | 10.0% | 5.0% | 22.3 | 0.556 | 7.6 | -18.2 |
| stowed | all | 120 | 6.7% | 5.0% | 38.1 | 1.088 | 6.2 | -5.8 |
| solo_1 | left | 40 | 0.0% | 20.0% | - | 2.858 | 60.0 | +33.8 |
| solo_1 | straight | 40 | 0.0% | 22.5% | - | 2.849 | 16.6 | -26.8 |
| solo_1 | right | 40 | 0.0% | 12.5% | - | 2.885 | 57.2 | -26.8 |
| solo_1 | all | 120 | 0.0% | 18.3% | - | 2.861 | 55.5 | -6.6 |
| solo_2 | left | 40 | 0.0% | 15.0% | - | 2.922 | 54.3 | +48.5 |
| solo_2 | straight | 40 | 0.0% | 2.5% | - | 2.872 | 14.2 | -15.2 |
| solo_2 | right | 40 | 0.0% | 7.5% | - | 2.844 | 69.6 | -14.3 |
| solo_2 | all | 120 | 0.0% | 8.3% | - | 2.872 | 55.2 | +6.4 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -6.7 [-11.7, -2.5] pts | 8 | 0 | +29.1 [+23.1, +34.9] |
| solo_2 | -6.7 [-11.7, -2.5] pts | 8 | 0 | +31.8 [+26.4, +37.2] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 10.0% | 5.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 5.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 10.0% | 10.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
