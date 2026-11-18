# Spot-arm turn pilot: sa-sweep-s3-t0_0.47-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: 0,0.47 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 95.0% | 5.0% | 17.4 | 0.098 | 1.8 | +1.2 |
| both | straight | 40 | 97.5% | 0.0% | 14.4 | 0.099 | 1.8 | +1.4 |
| both | right | 40 | 95.0% | 5.0% | 10.9 | 0.097 | 2.2 | +1.5 |
| both | all | 120 | 95.8% | 3.3% | 14.9 | 0.097 | 2.0 | +1.4 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 90.0% | 100.0% | 0.6% | 0.8% | 22.9% | 18.5% |
| both | straight | 95.0% | 100.0% | 0.5% | 1.2% | 18.9% | 23.1% |
| both | right | 100.0% | 90.0% | 0.3% | 1.4% | 19.4% | 23.1% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 115 | 48.7% | nan | nan | 1.7% |
