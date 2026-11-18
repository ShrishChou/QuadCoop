# Spot-arm turn pilot: sa-mech-rai-holdmean-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: none.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| hold_mean | left | 40 | 90.0% | 2.5% | 21.1 | 0.072 | 2.3 | +3.1 |
| hold_mean | straight | 40 | 87.5% | 0.0% | 12.8 | 0.071 | 2.1 | +1.0 |
| hold_mean | right | 40 | 57.5% | 2.5% | 11.8 | 0.084 | 2.8 | -3.2 |
| hold_mean | all | 120 | 78.3% | 1.7% | 14.7 | 0.074 | 2.4 | +0.3 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| hold_mean | left | 80.0% | 100.0% | 0.0% | 0.0% | 43.8% | 19.8% |
| hold_mean | straight | 90.0% | 85.0% | 0.0% | 0.0% | 45.9% | 49.6% |
| hold_mean | right | 55.0% | 60.0% | 0.0% | 0.0% | 40.2% | 44.7% |
