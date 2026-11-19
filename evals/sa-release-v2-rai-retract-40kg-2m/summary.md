# Spot-arm turn pilot: sa-release-v2-rai-retract-40kg-2m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 40 kg, 2 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 67.5% | 12.5% | 18.9 | 0.086 | 1.5 | +0.6 |
| both | straight | 40 | 77.5% | 0.0% | 14.7 | 0.076 | 2.0 | +0.8 |
| both | right | 40 | 47.5% | 0.0% | 14.0 | 0.097 | 1.0 | -1.0 |
| both | all | 120 | 64.2% | 4.2% | 16.1 | 0.084 | 1.5 | +0.1 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 45.0% | 90.0% | 0.0% | 0.3% | 39.2% | 19.9% |
| both | straight | 80.0% | 75.0% | 0.0% | 0.1% | 35.1% | 41.2% |
| both | right | 50.0% | 45.0% | 0.0% | 0.3% | 33.8% | 43.5% |

Release (retract), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 77 | 77 | 100.0% | 100.0% | 0.002 | 0.1 | 0.0% |
