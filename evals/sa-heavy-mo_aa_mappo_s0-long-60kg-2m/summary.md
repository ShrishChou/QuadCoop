# Spot-arm turn pilot: sa-heavy-mo_aa_mappo_s0-long-60kg-2m

logs/marl2/mo_aa_mappo_s0/model_4000.pt, iteration 4000, mappo, arms stowed. long 60 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 20.0% | 10.0% | 29.9 | 0.701 | 5.6 | +9.0 |
| stowed | straight | 40 | 10.0% | 2.5% | 23.3 | 0.585 | 4.0 | +1.4 |
| stowed | right | 40 | 37.5% | 5.0% | 14.7 | 0.147 | 3.6 | -8.7 |
| stowed | all | 120 | 22.5% | 5.8% | 18.6 | 0.351 | 4.4 | +0.6 |
| solo_1 | left | 40 | 0.0% | 22.5% | - | 1.861 | 60.0 | +36.7 |
| solo_1 | straight | 40 | 0.0% | 17.5% | - | 1.831 | 36.2 | -23.7 |
| solo_1 | right | 40 | 0.0% | 7.5% | - | 1.909 | 55.8 | -28.5 |
| solo_1 | all | 120 | 0.0% | 15.8% | - | 1.874 | 54.7 | -5.2 |
| solo_2 | left | 40 | 0.0% | 10.0% | - | 1.915 | 53.9 | +52.0 |
| solo_2 | straight | 40 | 0.0% | 5.0% | - | 1.878 | 11.2 | -18.9 |
| solo_2 | right | 40 | 0.0% | 10.0% | - | 1.766 | 67.6 | -12.3 |
| solo_2 | all | 120 | 0.0% | 8.3% | - | 1.878 | 54.0 | +6.9 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -22.5 [-30.0, -15.0] pts | 27 | 0 | +35.6 [+30.2, +40.8] |
| solo_2 | -22.5 [-30.0, -15.0] pts | 27 | 0 | +37.4 [+32.3, +42.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 40.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | straight | 20.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| stowed | right | 30.0% | 45.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
