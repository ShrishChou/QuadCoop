# Spot-arm turn pilot: sa-sweep-s3ctrl-t0.1_0.47-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_22-18-34_push_ft_s3_ctrl/model_2999.pt. Torso: 0.1,0.47 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 72.5% | 2.5% | 22.4 | 0.098 | 2.4 | +3.8 |
| both | straight | 40 | 75.0% | 5.0% | 14.6 | 0.122 | 2.5 | +0.3 |
| both | right | 40 | 50.0% | 2.5% | 24.7 | 0.130 | 2.7 | -2.8 |
| both | all | 120 | 65.8% | 3.3% | 19.6 | 0.110 | 2.5 | +0.4 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 50.0% | 95.0% | 2.1% | 3.8% | 29.1% | 20.0% |
| both | straight | 50.0% | 100.0% | 2.5% | 6.4% | 23.9% | 25.2% |
| both | right | 50.0% | 50.0% | 4.6% | 7.2% | 17.5% | 28.7% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 79 | 58.2% | 0.009 | 2.0 | 0.0% |
