# Spot-arm turn pilot: sa-release-v2-rai-policy-20kg-1m

logs/marl2/sa_heavy_learned_s0/model_4000.pt, iteration 4000, mappo, arms learned. long 20 kg, 1 m, 20 placements per turn x swap, horizon 40 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

Walker: RAI (spot_locomotion.onnx). Torso: default (interface False, expanded []). Arm-object collisions: on. Release: policy for 5 s.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| both | left | 40 | 100.0% | 0.0% | 4.2 | 0.100 | 2.9 | -0.2 |
| both | straight | 40 | 100.0% | 0.0% | 4.2 | 0.154 | 1.3 | +0.5 |
| both | right | 40 | 97.5% | 0.0% | 4.3 | 0.161 | 1.9 | +1.3 |
| both | all | 120 | 99.2% | 0.0% | 4.2 | 0.120 | 1.9 | +0.6 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| both | left | 100.0% | 100.0% | 0.5% | 0.6% | 23.2% | 20.6% |
| both | straight | 100.0% | 100.0% | 0.1% | 0.1% | 19.3% | 19.2% |
| both | right | 95.0% | 100.0% | 0.3% | 0.1% | 17.1% | 21.1% |

Release (policy), episodes that succeeded (success only inside the task horizon; the simulation continues for the release window): complete = the follow-up window finished (or a fall ended it); rates over complete episodes. Inside at end = within tolerance at the end of the window; inside throughout = within tolerance at every step of it; displacement = object travel during it.

| arm mode | successes | complete | inside at end | inside throughout | object displacement, median m | heading change, median abs deg | falls in release |
|---|---|---|---|---|---|---|---|
| both | 119 | 119 | 30.3% | 3.4% | 0.136 | 2.2 | 0.0% |
