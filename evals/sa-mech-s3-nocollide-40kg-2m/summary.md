# Spot-arm turn pilot: sa-mech-s3-nocollide-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: off. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 92.5% | 0.0% | 20.3 | 0.079 | 2.7 | +1.8 |
| both | straight | 40 | 97.5% | 0.0% | 12.3 | 0.074 | 1.6 | +0.9 |
| both | right | 40 | 100.0% | 0.0% | 11.5 | 0.085 | 1.3 | -0.0 |
| both | all | 120 | 96.7% | 0.0% | 16.1 | 0.078 | 1.6 | +0.9 |
| only_1 | left | 40 | 95.0% | 5.0% | 18.0 | 0.076 | 1.4 | +1.6 |
| only_1 | straight | 40 | 97.5% | 2.5% | 17.8 | 0.079 | 1.8 | +0.1 |
| only_1 | right | 40 | 97.5% | 2.5% | 13.8 | 0.068 | 1.8 | +0.5 |
| only_1 | all | 120 | 96.7% | 3.3% | 16.3 | 0.074 | 1.8 | +0.7 |
| only_2 | left | 40 | 90.0% | 7.5% | 17.3 | 0.077 | 2.2 | +2.2 |
| only_2 | straight | 40 | 100.0% | 0.0% | 11.1 | 0.066 | 1.8 | +1.2 |
| only_2 | right | 40 | 97.5% | 0.0% | 11.2 | 0.075 | 2.3 | +1.0 |
| only_2 | all | 120 | 95.8% | 2.5% | 12.7 | 0.072 | 2.0 | +1.5 |

Ablation, paired per task against both (the same policy; a locked arm stays stowed; solo_k: only robot k, the other parked 40 m away):

| arm mode | change in success [95% CI] | tasks lost | tasks gained | change in abs heading error, deg [95% CI] |
|---|---|---|---|---|
| only_1 | +0.0 [-4.2, +4.2] pts | 4 | 4 | +0.4 [-1.1, +2.3] |
| only_2 | -0.8 [-5.8, +4.2] pts | 5 | 4 | +0.1 [-1.1, +1.5] |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 95.0% | 90.0% | 0.0% | 0.0% | 28.2% | 21.0% |
| both | straight | 95.0% | 100.0% | 0.0% | 0.0% | 23.7% | 27.6% |
| both | right | 100.0% | 100.0% | 0.0% | 0.0% | 27.5% | 31.4% |
| only_1 | left | 95.0% | 95.0% | 0.0% | 0.0% | 19.5% | 36.5% |
| only_1 | straight | 100.0% | 95.0% | 0.0% | 0.0% | 26.2% | 24.2% |
| only_1 | right | 95.0% | 100.0% | 0.0% | 0.0% | 22.6% | 34.1% |
| only_2 | left | 100.0% | 80.0% | 0.0% | 0.0% | 28.6% | 21.2% |
| only_2 | straight | 100.0% | 100.0% | 0.0% | 0.0% | 27.0% | 27.0% |
| only_2 | right | 100.0% | 95.0% | 0.0% | 0.0% | 28.5% | 30.1% |
