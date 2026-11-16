# Spot-arm turn pilot: sa-hand-sa_mappo_stowed60_s0

logs/marl2/sa_mappo_stowed60_s0/model_2000.pt, iteration 2000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +60.0 to +60.0 deg, straight +0.0 to +0.0 deg, right -60.0 to -60.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 60.0% | 0.0% | 4.0 | 0.081 | 2.8 | +0.5 |
| stowed | straight | 40 | 90.0% | 0.0% | 6.5 | 0.071 | 3.0 | +0.6 |
| stowed | right | 40 | 95.0% | 0.0% | 4.4 | 0.057 | 2.1 | +0.5 |
| stowed | all | 120 | 81.7% | 0.0% | 4.5 | 0.063 | 2.6 | +0.5 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 85.0% | 35.0% | 0.0% | 0.0% | 19.0% | 15.8% |
| stowed | straight | 90.0% | 90.0% | 0.0% | 0.0% | 15.9% | 15.2% |
| stowed | right | 100.0% | 90.0% | 0.0% | 0.0% | 18.3% | 29.0% |
