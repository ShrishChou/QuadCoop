# Spot-arm turn pilot: sa-sweep-s2-t0.1_0.52-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_14-26-35_push_ft_s2_posture/model_2999.pt. Torso: 0.1,0.52 (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 82.5% | 5.0% | 20.7 | 0.091 | 2.8 | +2.3 |
| both | straight | 40 | 82.5% | 2.5% | 20.3 | 0.089 | 2.0 | +0.8 |
| both | right | 40 | 62.5% | 0.0% | 18.5 | 0.109 | 2.8 | +0.3 |
| both | all | 120 | 75.8% | 2.5% | 19.9 | 0.098 | 2.6 | +1.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 75.0% | 90.0% | 1.1% | 2.5% | 35.8% | 28.3% |
| both | straight | 65.0% | 100.0% | 0.7% | 2.0% | 24.5% | 33.2% |
| both | right | 60.0% | 65.0% | 1.2% | 1.6% | 21.6% | 30.5% |

Release (policy), episodes that succeeded: retained = still within tolerance at the end of the release; displacement = object travel during it.

| arm mode | successes | retained | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|
| both | 91 | 58.2% | nan | nan | 0.0% |
