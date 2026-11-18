# Spot-arm turn pilot: sa-sweep-s3-t0_0.43-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: 0,0.43 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 92.5% | 5.0% | 18.1 | 0.120 | 2.4 | +3.4 |
| both | straight | 40 | 100.0% | 0.0% | 11.6 | 0.104 | 2.0 | +1.0 |
| both | right | 40 | 95.0% | 2.5% | 11.4 | 0.093 | 2.4 | +1.3 |
| both | all | 120 | 95.8% | 2.5% | 14.6 | 0.101 | 2.2 | +1.9 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 90.0% | 95.0% | 1.5% | 2.0% | 21.8% | 18.6% |
| both | straight | 100.0% | 100.0% | 1.8% | 3.1% | 17.7% | 20.7% |
| both | right | 95.0% | 95.0% | 1.8% | 2.0% | 18.3% | 27.7% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 115 | 47.0% | 0.104 | 2.0 | 0.9% |
