# Spot-arm turn pilot: sa-sweep-s2-tdefault-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_14-26-35_push_ft_s2_posture/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 75.0% | 10.0% | 19.6 | 0.098 | 2.0 | +0.6 |
| both | straight | 40 | 87.5% | 5.0% | 21.7 | 0.086 | 2.9 | -1.2 |
| both | right | 40 | 72.5% | 5.0% | 23.1 | 0.087 | 2.8 | +0.4 |
| both | all | 120 | 78.3% | 6.7% | 21.7 | 0.088 | 2.4 | -0.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 75.0% | 75.0% | 0.1% | 0.8% | 30.6% | 28.0% |
| both | straight | 80.0% | 95.0% | 0.5% | 0.7% | 24.9% | 28.8% |
| both | right | 75.0% | 70.0% | 0.3% | 0.4% | 25.1% | 27.4% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 94 | 66.0% | 0.006 | 0.3 | 3.2% |
