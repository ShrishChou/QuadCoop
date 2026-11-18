# Spot-arm turn pilot: sa-sweep-s3ctrl-t0_0.47-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_22-18-34_push_ft_s3_ctrl/model_2999.pt. Torso: 0,0.47 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 85.0% | 2.5% | 22.7 | 0.097 | 3.0 | +1.2 |
| both | straight | 40 | 87.5% | 0.0% | 17.4 | 0.099 | 2.1 | +0.3 |
| both | right | 40 | 82.5% | 0.0% | 27.4 | 0.094 | 2.6 | -1.0 |
| both | all | 120 | 85.0% | 0.8% | 22.4 | 0.094 | 2.6 | +0.2 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 75.0% | 95.0% | 0.8% | 1.7% | 29.7% | 19.5% |
| both | straight | 75.0% | 100.0% | 0.5% | 1.4% | 20.8% | 23.1% |
| both | right | 75.0% | 90.0% | 1.1% | 1.3% | 18.0% | 25.5% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 102 | 57.8% | 0.013 | 0.1 | 1.0% |
