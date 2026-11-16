# Spot-arm turn pilot: sa-team-sa_mappo_learned60_s0

logs/marl2/sa_mappo_learned60_s0/model_2000.pt, iteration 2000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 97.5% | 0.0% | 4.2 | 0.053 | 1.4 | -0.6 |
| both | straight | 40 | 100.0% | 0.0% | 3.8 | 0.034 | 0.9 | -0.6 |
| both | right | 40 | 100.0% | 0.0% | 4.1 | 0.048 | 3.1 | -0.1 |
| both | all | 120 | 99.2% | 0.0% | 4.0 | 0.044 | 1.8 | -0.4 |
| only_1 | left | 40 | 97.5% | 0.0% | 4.3 | 0.061 | 1.2 | -0.4 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.1 | 0.044 | 1.7 | -1.2 |
| only_1 | right | 40 | 100.0% | 0.0% | 5.3 | 0.065 | 1.4 | -0.8 |
| only_1 | all | 120 | 99.2% | 0.0% | 4.3 | 0.053 | 1.4 | -0.8 |
| only_2 | left | 40 | 90.0% | 0.0% | 5.0 | 0.071 | 2.2 | +2.9 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.2 | 0.072 | 1.1 | -0.1 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.3 | 0.050 | 1.9 | -0.2 |
| only_2 | all | 120 | 96.7% | 0.0% | 4.3 | 0.063 | 1.4 | +0.9 |
| none | left | 40 | 97.5% | 2.5% | 4.7 | 0.060 | 1.3 | +2.3 |
| none | straight | 40 | 100.0% | 0.0% | 4.7 | 0.056 | 1.6 | -1.5 |
| none | right | 40 | 100.0% | 0.0% | 5.3 | 0.043 | 2.7 | -0.9 |
| none | all | 120 | 99.2% | 0.8% | 4.8 | 0.055 | 1.6 | -0.1 |
| solo_1 | left | 40 | 0.0% | 0.0% | - | 0.761 | 39.3 | +40.1 |
| solo_1 | straight | 40 | 0.0% | 0.0% | - | 0.988 | 38.1 | +1.4 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.983 | 41.9 | -11.4 |
| solo_1 | all | 120 | 0.0% | 0.0% | - | 0.898 | 38.8 | +10.0 |
| solo_2 | left | 40 | 0.0% | 7.5% | - | 0.818 | 24.8 | +14.3 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 0.723 | 17.9 | +0.8 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 1.000 | 60.0 | -46.0 |
| solo_2 | all | 120 | 0.0% | 2.5% | - | 0.798 | 32.9 | -10.3 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [-2.5, +2.5] pts | 1 | 1 | -0.1 [-0.4, +0.3] |
| only_2 | -2.5 [-5.8, +0.8] pts | 4 | 1 | +0.4 [-0.5, +1.7] |
| none | +0.0 [-2.5, +2.5] pts | 1 | 1 | +0.2 [-0.4, +1.2] |
| solo_1 | -99.2 [-100.0, -97.5] pts | 119 | 0 | +35.7 [+32.8, +38.7] |
| solo_2 | -99.2 [-100.0, -97.5] pts | 119 | 0 | +33.7 [+29.7, +37.6] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 95.0% | 0.1% | 0.7% | 30.0% | 14.1% |
| both | straight | 100.0% | 100.0% | 0.1% | 6.1% | 20.7% | 14.4% |
| both | right | 100.0% | 100.0% | 0.1% | 0.5% | 12.0% | 26.6% |
| only_1 | left | 95.0% | 100.0% | 0.0% | 0.0% | 32.0% | 19.4% |
| only_1 | straight | 100.0% | 100.0% | 0.1% | 0.0% | 27.5% | 17.0% |
| only_1 | right | 100.0% | 100.0% | 0.1% | 0.0% | 17.4% | 32.2% |
| only_2 | left | 80.0% | 100.0% | 0.1% | 1.3% | 27.4% | 19.3% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 5.4% | 17.7% | 13.1% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.3% | 13.2% | 28.7% |
| none | left | 95.0% | 100.0% | 0.0% | 0.0% | 33.3% | 22.2% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 20.1% | 14.2% |
| none | right | 100.0% | 100.0% | 0.0% | 0.0% | 17.9% | 33.4% |
| solo_1 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_1 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 8.8% | 1.6% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.2% | 2.2% | 7.4% |
| solo_2 | left | 0.0% | 0.0% | 3.6% | 3.2% | 3.9% | 0.3% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.5% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.1% | 2.4% |
