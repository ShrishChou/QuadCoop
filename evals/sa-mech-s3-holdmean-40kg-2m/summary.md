# Spot-arm turn pilot: sa-mech-s3-holdmean-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: logs/rsl_rl/walker_spot_arm/2026-11-17_18-10-15_push_ft_s3_handload/model_2999.pt. Torso: default (interface False, expanded []). Arm-object collisions: on. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| hold_mean | left | 40 | 90.0% | 5.0% | 18.6 | 0.082 | 2.0 | +5.6 |
| hold_mean | straight | 40 | 100.0% | 0.0% | 10.7 | 0.058 | 1.8 | +1.6 |
| hold_mean | right | 40 | 90.0% | 0.0% | 9.5 | 0.081 | 2.6 | +1.6 |
| hold_mean | all | 120 | 93.3% | 1.7% | 12.1 | 0.074 | 2.2 | +3.0 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| hold_mean | left | 90.0% | 90.0% | 0.0% | 0.0% | 31.4% | 19.6% |
| hold_mean | straight | 100.0% | 100.0% | 0.0% | 0.0% | 23.2% | 25.6% |
| hold_mean | right | 90.0% | 90.0% | 0.0% | 0.0% | 28.9% | 25.2% |
