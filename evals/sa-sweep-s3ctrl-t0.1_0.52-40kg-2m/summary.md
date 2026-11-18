# Spot-arm turn pilot: sa-sweep-s3ctrl-t0.1_0.52-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_22-18-34_push_ft_s3_ctrl/model_2999.pt. Torso: 0.1,0.52 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 67.5% | 0.0% | 23.9 | 0.106 | 2.2 | +2.9 |
| both | straight | 40 | 65.0% | 0.0% | 23.8 | 0.155 | 3.1 | +1.9 |
| both | right | 40 | 37.5% | 0.0% | 27.8 | 0.321 | 3.3 | -5.1 |
| both | all | 120 | 56.7% | 0.0% | 25.1 | 0.133 | 2.9 | -0.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 40.0% | 95.0% | 1.7% | 1.8% | 35.1% | 25.1% |
| both | straight | 30.0% | 100.0% | 1.0% | 0.9% | 22.9% | 29.4% |
| both | right | 30.0% | 45.0% | 1.2% | 1.3% | 19.2% | 30.8% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 68 | 58.8% | 0.018 | 1.8 | 0.0% |
