# Spot-arm turn pilot: sa-sweep-s2-t0_0.43-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_14-26-35_push_ft_s2_posture/model_2999.pt. Torso: 0,0.43 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 92.5% | 2.5% | 18.8 | 0.077 | 1.9 | +1.0 |
| both | straight | 40 | 95.0% | 2.5% | 22.7 | 0.091 | 2.4 | -1.8 |
| both | right | 40 | 87.5% | 7.5% | 20.6 | 0.099 | 2.4 | -1.1 |
| both | all | 120 | 91.7% | 4.2% | 20.6 | 0.086 | 2.2 | -0.6 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 90.0% | 95.0% | 1.6% | 6.0% | 29.5% | 23.5% |
| both | straight | 95.0% | 95.0% | 3.3% | 3.4% | 18.9% | 31.1% |
| both | right | 90.0% | 85.0% | 3.3% | 5.2% | 21.9% | 30.1% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 110 | 60.9% | 0.080 | 2.1 | 1.8% |
