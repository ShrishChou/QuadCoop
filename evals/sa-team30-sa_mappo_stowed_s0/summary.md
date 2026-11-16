# Spot-arm turn pilot: sa-team30-sa_mappo_stowed_s0

logs/marl2/sa_mappo_stowed_s0/model_2000.pt, iteration 2000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 92.5% | 0.0% | 3.9 | 0.060 | 0.9 | +0.3 |
| stowed | straight | 40 | 92.5% | 0.0% | 4.1 | 0.053 | 1.4 | +0.9 |
| stowed | right | 40 | 97.5% | 0.0% | 4.3 | 0.057 | 1.2 | +0.5 |
| stowed | all | 120 | 94.2% | 0.0% | 4.1 | 0.056 | 1.3 | +0.6 |
| solo_1 | left | 40 | 0.0% | 12.5% | - | 0.789 | 15.7 | +16.8 |
| solo_1 | straight | 40 | 0.0% | 12.5% | - | 0.759 | 21.6 | -24.0 |
| solo_1 | right | 40 | 0.0% | 0.0% | - | 0.865 | 55.8 | -38.8 |
| solo_1 | all | 120 | 0.0% | 8.3% | - | 0.775 | 20.0 | -15.3 |
| solo_2 | left | 40 | 0.0% | 0.0% | - | 0.999 | 30.1 | +30.4 |
| solo_2 | straight | 40 | 0.0% | 0.0% | - | 1.000 | 2.3 | +8.0 |
| solo_2 | right | 40 | 0.0% | 0.0% | - | 0.984 | 29.5 | -14.4 |
| solo_2 | all | 120 | 0.0% | 0.0% | - | 0.995 | 29.8 | +8.0 |

Ablation, paired per task against stowed (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| solo_1 | -94.2 [-97.5, -90.0] pts | 113 | 0 | +26.5 [+22.8, +30.6] |
| solo_2 | -94.2 [-97.5, -90.0] pts | 113 | 0 | +19.8 [+17.2, +22.4] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 85.0% | 100.0% | 0.0% | 0.0% | 22.6% | 20.9% |
| stowed | straight | 85.0% | 100.0% | 0.0% | 0.0% | 22.0% | 24.5% |
| stowed | right | 100.0% | 95.0% | 0.0% | 0.0% | 24.8% | 22.7% |
| solo_1 | left | 0.0% | 0.0% | 1.9% | 0.0% | 1.8% | 0.3% |
| solo_1 | straight | 0.0% | 0.0% | 1.8% | 0.0% | 6.0% | 0.3% |
| solo_1 | right | 0.0% | 0.0% | 0.0% | 0.0% | 17.7% | 0.4% |
| solo_2 | left | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% |
| solo_2 | straight | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 1.4% |
| solo_2 | right | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | 2.8% |
