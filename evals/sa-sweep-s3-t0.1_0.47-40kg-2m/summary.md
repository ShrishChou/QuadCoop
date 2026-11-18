# Spot-arm turn pilot: sa-sweep-s3-t0.1_0.47-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: 0.1,0.47 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 87.5% | 5.0% | 21.9 | 0.118 | 2.0 | +4.3 |
| both | straight | 40 | 90.0% | 5.0% | 9.9 | 0.113 | 1.9 | +1.7 |
| both | right | 40 | 92.5% | 5.0% | 15.5 | 0.109 | 2.8 | +2.2 |
| both | all | 120 | 90.0% | 5.0% | 15.5 | 0.109 | 2.2 | +2.7 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 95.0% | 80.0% | 2.1% | 2.2% | 23.6% | 17.2% |
| both | straight | 85.0% | 95.0% | 1.5% | 3.9% | 18.9% | 20.3% |
| both | right | 90.0% | 95.0% | 2.0% | 2.9% | 18.3% | 24.6% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 108 | 33.3% | 0.034 | 0.2 | 2.8% |
