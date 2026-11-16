# Spot-arm turn pilot: sa-team-sa_ippo_stowed60_s0

logs/marl2/sa_ippo_stowed60_s0/model_2000.pt, iteration 2000, ippo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 82.5% | 0.0% | 4.8 | 0.065 | 1.9 | +0.5 |
| stowed | straight | 40 | 97.5% | 0.0% | 4.1 | 0.065 | 1.6 | -1.2 |
| stowed | right | 40 | 90.0% | 0.0% | 6.2 | 0.062 | 3.3 | +2.0 |
| stowed | all | 120 | 90.0% | 0.0% | 4.4 | 0.065 | 2.4 | +0.5 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.753 | 34.1 | +14.7 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.593 | 50.5 | -42.4 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.591 | 87.2 | +10.4 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.632 | 51.1 | -5.8 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | +58.7 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 21.2 | -27.8 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -24.8 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 1.000 | 60.0 | +2.0 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -90.0 [-95.0, -84.2] pts | 108 | 0 | +51.0 [+46.4, +55.7] |
| solo_2 | -90.0 [-95.0, -84.2] pts | 108 | 0 | +40.4 [+35.7, +45.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 80.0% | 85.0% | 0.0% | 0.0% | 15.8% | 20.4% |
| stowed | straight | 100.0% | 95.0% | 0.0% | 0.0% | 21.3% | 21.2% |
| stowed | right | 100.0% | 80.0% | 0.0% | 0.0% | 12.7% | 15.7% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 11.1% | 14.1% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 1.4% | 0.7% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 11.6% | 7.5% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.2% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
