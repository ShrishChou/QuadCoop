# Spot-arm turn pilot: sa-pilot-sa_mappo_stowed_s0

logs/marl2/sa_mappo_stowed_s0/model_2000.pt, iteration 2000, mappo, arms stowed. long 20 kg, 1 m, 20 placements per turn x swap, horizon 20 s, seed 7100. Goal heading change as placed: left +30.0 to +30.0 deg, straight +0.0 to +0.0 deg, right -30.0 to -30.0 deg.

##

| arm mode | turn | episodes | success | falls | time to success, median s | final position error, median m | final heading error, median abs deg | signed heading error, mean deg |
|---|---|---|---|---|---|---|---|---|
| stowed | left | 40 | 92.5% | 2.5% | 3.8 | 0.056 | 1.2 | +0.1 |
| stowed | straight | 40 | 90.0% | 0.0% | 4.1 | 0.053 | 1.7 | +0.9 |
| stowed | right | 40 | 97.5% | 0.0% | 4.2 | 0.063 | 0.9 | +0.7 |
| stowed | all | 120 | 93.3% | 0.8% | 4.1 | 0.056 | 1.4 | +0.6 |

Start places exchanged (swap) and who uses its arm. Left / right = the robot's start side seen along the push direction; arm contact = share of the episode with that robot's arm on the object.

| arm mode | turn | success unswapped | success swapped | arm contact, robot starting left | arm contact, robot starting right | trunk contact left | trunk contact right |
|---|---|---|---|---|---|---|---|
| stowed | left | 90.0% | 95.0% | 0.4% | 0.0% | 23.8% | 21.6% |
| stowed | straight | 80.0% | 100.0% | 0.0% | 0.0% | 25.0% | 25.5% |
| stowed | right | 100.0% | 95.0% | 0.0% | 0.0% | 25.6% | 23.2% |
