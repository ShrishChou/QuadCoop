# Spot-arm turn pilot: sa-sweep-s2-t0.1_0.47-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_14-26-35_push_ft_s2_posture/model_2999.pt. Torso: 0.1,0.47 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 77.5% | 5.0% | 18.2 | 0.089 | 2.2 | +4.4 |
| both | straight | 40 | 82.5% | 2.5% | 25.6 | 0.085 | 1.9 | +0.4 |
| both | right | 40 | 70.0% | 0.0% | 23.9 | 0.103 | 1.6 | +0.0 |
| both | all | 120 | 76.7% | 2.5% | 21.5 | 0.094 | 1.9 | +1.6 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 70.0% | 85.0% | 2.3% | 4.4% | 33.8% | 26.3% |
| both | straight | 70.0% | 95.0% | 2.7% | 4.9% | 20.1% | 31.6% |
| both | right | 65.0% | 75.0% | 4.0% | 5.3% | 19.7% | 27.7% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 92 | 64.1% | 0.000 | 2.2 | 1.1% |
