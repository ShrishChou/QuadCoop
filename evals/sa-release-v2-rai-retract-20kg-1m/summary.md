# Spot-arm turn pilot: sa-release-v2-rai-retract-20kg-1m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: retract for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.2 | 0.049 | 1.1 | +0.4 |
| both | straight | 40 | 97.5% | 0.0% | 4.2 | 0.057 | 0.9 | -0.1 |
| both | right | 40 | 100.0% | 0.0% | 4.3 | 0.058 | 1.7 | +0.5 |
| both | all | 120 | 99.2% | 0.0% | 4.2 | 0.053 | 1.2 | +0.3 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.3% | 0.6% | 10.5% | 11.5% |
| both | straight | 100.0% | 95.0% | 0.1% | 0.0% | 13.3% | 10.7% |
| both | right | 100.0% | 100.0% | 0.0% | 0.0% | 10.2% | 14.9% |

Release (retract), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 119 | 119 | 96.6% | 96.6% | 0.008 | 0.3 | 0.0% |
