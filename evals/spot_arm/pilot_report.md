# Spot-arm turn pilot: systems on the same held-out tasks

| system | arm mode | success | falls | abs heading error left / straight / right, median deg |
|---|---|---|---|---|
| sa-pilot-sa_ippo_stowed_s0 | stowed | 93.3% | 0.0% | 1.1 / 1.1 / 1.8 |
| sa-pilot-sa_ippo_learned_s0 | both | 100.0% | 0.0% | 1.3 / 1.2 / 1.6 |
| sa-pilot-sa_ippo_learned_s0 | only_1 | 100.0% | 0.0% | 1.5 / 2.0 / 2.5 |
| sa-pilot-sa_ippo_learned_s0 | only_2 | 100.0% | 0.0% | 1.8 / 1.9 / 1.4 |
| sa-pilot-sa_ippo_learned_s0 | none | 99.2% | 0.0% | 1.9 / 1.7 / 2.1 |
| sa-pilot-sa_mappo_stowed_s0 | stowed | 93.3% | 0.8% | 1.2 / 1.7 / 0.9 |
| sa-pilot-sa_mappo_learned_s0 | both | 96.7% | 0.8% | 2.4 / 1.8 / 0.8 |
| sa-pilot-sa_mappo_learned_s0 | only_1 | 99.2% | 0.0% | 1.4 / 1.9 / 1.6 |
| sa-pilot-sa_mappo_learned_s0 | only_2 | 95.8% | 0.8% | 2.0 / 1.3 / 1.8 |
| sa-pilot-sa_mappo_learned_s0 | none | 99.2% | 0.0% | 0.9 / 1.5 / 1.0 |

Paired per task, each system as trained (learned arms: both active), against the first:

| system | change in success [95% CI] | tasks gained | tasks lost |
|---|---|---|---|
| sa-pilot-sa_ippo_learned_s0 vs sa-pilot-sa_ippo_stowed_s0 | +6.7 [+2.5, +11.7] pts | 8 | 0 |
| sa-pilot-sa_mappo_stowed_s0 vs sa-pilot-sa_ippo_stowed_s0 | +0.0 [-6.7, +6.7] pts | 8 | 8 |
| sa-pilot-sa_mappo_learned_s0 vs sa-pilot-sa_ippo_stowed_s0 | +3.3 [-2.5, +9.2] pts | 8 | 4 |

## sa-pilot-sa_ippo_stowed_s0

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 87.5% | 0.0% | 4.2 | 0.070 | 1.1 | +0.7 |
| stowed | straight | 40 | 95.0% | 0.0% | 4.1 | 0.053 | 1.1 | +1.3 |
| stowed | right | 40 | 97.5% | 0.0% | 4.3 | 0.050 | 1.8 | +0.5 |
| stowed | all | 120 | 93.3% | 0.0% | 4.2 | 0.053 | 1.4 | +0.8 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 100.0% | 75.0% | 0.0% | 0.0% | 16.8% | 16.7% |
| stowed | straight | 100.0% | 90.0% | 0.0% | 0.0% | 19.1% | 21.2% |
| stowed | right | 100.0% | 95.0% | 0.0% | 0.0% | 23.5% | 21.5% |

## sa-pilot-sa_ippo_learned_s0

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 3.9 | 0.038 | 1.3 | -1.2 |
| both | straight | 40 | 100.0% | 0.0% | 3.9 | 0.039 | 1.2 | -0.0 |
| both | right | 40 | 100.0% | 0.0% | 4.1 | 0.045 | 1.6 | +1.7 |
| both | all | 120 | 100.0% | 0.0% | 4.0 | 0.040 | 1.4 | +0.1 |
| only_1 | left | 40 | 100.0% | 0.0% | 4.3 | 0.058 | 1.5 | +0.5 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.4 | 0.054 | 2.0 | +0.9 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.7 | 0.062 | 2.5 | +1.6 |
| only_1 | all | 120 | 100.0% | 0.0% | 4.4 | 0.058 | 2.0 | +1.0 |
| only_2 | left | 40 | 100.0% | 0.0% | 4.2 | 0.055 | 1.8 | -1.8 |
| only_2 | straight | 40 | 100.0% | 0.0% | 4.1 | 0.059 | 1.9 | -1.3 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.2 | 0.050 | 1.4 | +1.2 |
| only_2 | all | 120 | 100.0% | 0.0% | 4.2 | 0.053 | 1.7 | -0.6 |
| none | left | 40 | 100.0% | 0.0% | 4.7 | 0.065 | 1.9 | +0.1 |
| none | straight | 40 | 100.0% | 0.0% | 4.6 | 0.060 | 1.7 | -0.0 |
| none | right | 40 | 97.5% | 0.0% | 4.6 | 0.054 | 2.1 | +1.3 |
| none | all | 120 | 99.2% | 0.0% | 4.6 | 0.060 | 1.9 | +0.5 |

Arm ablation, paired per task against both arms active (the same policy; a locked arm stays stowed):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.4 [+0.1, +0.7] |
| only_2 | +0.0 [+0.0, +0.0] pts | 0 | 0 | +0.2 [-0.0, +0.5] |
| none | -0.8 [-2.5, +0.0] pts | 1 | 0 | +0.5 [+0.1, +0.9] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 1.3% | 0.2% | 16.9% | 21.9% |
| both | straight | 100.0% | 100.0% | 0.4% | 0.4% | 24.3% | 22.8% |
| both | right | 100.0% | 100.0% | 0.9% | 0.1% | 27.3% | 24.9% |
| only_1 | left | 100.0% | 100.0% | 0.0% | 0.4% | 19.7% | 22.7% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.4% | 20.1% | 25.6% |
| only_1 | right | 100.0% | 100.0% | 0.1% | 0.0% | 26.4% | 23.7% |
| only_2 | left | 100.0% | 100.0% | 0.2% | 0.7% | 13.6% | 21.5% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 0.3% | 20.6% | 26.1% |
| only_2 | right | 100.0% | 100.0% | 1.3% | 0.0% | 27.3% | 26.0% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 17.5% | 21.5% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 17.7% | 26.6% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 24.7% | 25.1% |

## sa-pilot-sa_mappo_stowed_s0

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 92.5% | 2.5% | 3.8 | 0.056 | 1.2 | +0.1 |
| stowed | straight | 40 | 90.0% | 0.0% | 4.1 | 0.053 | 1.7 | +0.9 |
| stowed | right | 40 | 97.5% | 0.0% | 4.2 | 0.063 | 0.9 | +0.7 |
| stowed | all | 120 | 93.3% | 0.8% | 4.1 | 0.056 | 1.4 | +0.6 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 90.0% | 95.0% | 0.4% | 0.0% | 23.8% | 21.6% |
| stowed | straight | 80.0% | 100.0% | 0.0% | 0.0% | 25.0% | 25.5% |
| stowed | right | 100.0% | 95.0% | 0.0% | 0.0% | 25.6% | 23.2% |

## sa-pilot-sa_mappo_learned_s0

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 97.5% | 0.0% | 3.6 | 0.056 | 2.4 | -2.2 |
| both | straight | 40 | 97.5% | 2.5% | 3.8 | 0.057 | 1.8 | -1.3 |
| both | right | 40 | 95.0% | 0.0% | 3.9 | 0.041 | 0.8 | -0.7 |
| both | all | 120 | 96.7% | 0.8% | 3.8 | 0.052 | 1.6 | -1.4 |
| only_1 | left | 40 | 97.5% | 0.0% | 3.8 | 0.065 | 1.4 | -0.4 |
| only_1 | straight | 40 | 100.0% | 0.0% | 4.0 | 0.057 | 1.9 | -1.0 |
| only_1 | right | 40 | 100.0% | 0.0% | 4.2 | 0.063 | 1.6 | +0.5 |
| only_1 | all | 120 | 99.2% | 0.0% | 4.0 | 0.062 | 1.7 | -0.3 |
| only_2 | left | 40 | 95.0% | 0.0% | 3.9 | 0.058 | 2.0 | -0.3 |
| only_2 | straight | 40 | 92.5% | 2.5% | 4.1 | 0.040 | 1.3 | +0.2 |
| only_2 | right | 40 | 100.0% | 0.0% | 4.2 | 0.049 | 1.8 | -1.0 |
| only_2 | all | 120 | 95.8% | 0.8% | 4.0 | 0.049 | 1.7 | -0.3 |
| none | left | 40 | 100.0% | 0.0% | 4.0 | 0.067 | 0.9 | +0.8 |
| none | straight | 40 | 100.0% | 0.0% | 4.7 | 0.055 | 1.5 | +0.4 |
| none | right | 40 | 97.5% | 0.0% | 4.6 | 0.065 | 1.0 | +0.5 |
| none | all | 120 | 99.2% | 0.0% | 4.3 | 0.062 | 1.1 | +0.6 |

Arm ablation, paired per task against both arms active (the same policy; a locked arm stays stowed):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +2.5 [-0.8, +6.7] pts | 1 | 4 | -0.0 [-0.4, +0.4] |
| only_2 | -0.8 [-5.8, +4.2] pts | 5 | 4 | -0.0 [-0.4, +0.3] |
| none | +2.5 [-0.8, +6.7] pts | 1 | 4 | -0.4 [-0.8, -0.1] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 95.0% | 100.0% | 0.2% | 0.4% | 20.7% | 15.8% |
| both | straight | 95.0% | 100.0% | 0.3% | 0.1% | 18.7% | 13.2% |
| both | right | 90.0% | 100.0% | 0.0% | 0.1% | 19.8% | 23.3% |
| only_1 | left | 95.0% | 100.0% | 0.0% | 0.0% | 20.9% | 19.1% |
| only_1 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 16.6% | 13.7% |
| only_1 | right | 100.0% | 100.0% | 0.0% | 0.0% | 18.3% | 21.6% |
| only_2 | left | 90.0% | 100.0% | 0.0% | 0.0% | 23.0% | 17.3% |
| only_2 | straight | 85.0% | 100.0% | 0.0% | 0.0% | 16.0% | 16.5% |
| only_2 | right | 100.0% | 100.0% | 0.0% | 0.0% | 21.8% | 25.4% |
| none | left | 100.0% | 100.0% | 0.0% | 0.0% | 22.9% | 15.0% |
| none | straight | 100.0% | 100.0% | 0.0% | 0.0% | 13.4% | 12.6% |
| none | right | 100.0% | 95.0% | 0.0% | 0.0% | 18.8% | 22.7% |
