# Start placements: A = `place-nwA-ippo-it5000`, F = `place-nwF-ippo-mixstart-it5000`

## A

### Success by formation (unswapped and swapped pooled)

| formation | objects | n | success | falls | precise | success change vs standard [95% CI] |
|---|---|---|---|---|---|---|
| standard | all ten | 960 | 635/960 (66%) | 122/960 (13%) | 577/960 (60%) |  |
| standard | arch | 96 | 39/96 (41%) | 16/96 (17%) | 32/96 (33%) |  |
| standard | cylinder | 96 | 42/96 (44%) | 26/96 (27%) | 35/96 (36%) |  |
| standard | long | 96 | 69/96 (72%) | 5/96 (5%) | 62/96 (65%) |  |
| standard | sphere | 96 | 91/96 (95%) | 5/96 (5%) | 91/96 (95%) |  |
| flank | all ten | 960 | 607/960 (63%) | 133/960 (14%) | 546/960 (57%) | -2.9 [-6.1, +0.2] pts |
| flank | arch | 96 | 32/96 (33%) | 17/96 (18%) | 27/96 (28%) | -7.3 [-18.8, +4.2] pts |
| flank | cylinder | 96 | 34/96 (35%) | 28/96 (29%) | 22/96 (23%) | -8.3 [-17.7, +1.0] pts |
| flank | long | 96 | 71/96 (74%) | 4/96 (4%) | 68/96 (71%) | +2.1 [-8.3, +12.5] pts |
| flank | sphere | 96 | 92/96 (96%) | 3/96 (3%) | 92/96 (96%) | +1.0 [-4.2, +6.2] pts |
| goal_behind | all ten | 960 | 606/960 (63%) | 114/960 (12%) | 544/960 (57%) | -3.0 [-5.9, +0.0] pts |
| goal_behind | arch | 96 | 32/96 (33%) | 20/96 (21%) | 31/96 (32%) | -7.3 [-18.8, +4.2] pts |
| goal_behind | cylinder | 96 | 35/96 (36%) | 17/96 (18%) | 30/96 (31%) | -7.3 [-16.7, +2.1] pts |
| goal_behind | long | 96 | 75/96 (78%) | 7/96 (7%) | 68/96 (71%) | +6.2 [-3.1, +15.6] pts |
| goal_behind | sphere | 96 | 95/96 (99%) | 1/96 (1%) | 95/96 (99%) | +4.2 [+0.0, +9.4] pts |

### Success by formation and mass (all ten)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 90% | 84% | 62% | 28% |
| flank | 87% | 82% | 58% | 27% |
| goal_behind | 88% | 80% | 57% | 28% |

### Timing (seconds from the start)

| formation | first push, median | never pushed | first 0.25 m progress, median | never progressed |
|---|---|---|---|---|
| standard | 1.3 | 0/960 (0%) | 3.0 | 17/960 (2%) |
| flank | 1.1 | 0/960 (0%) | 3.3 | 24/960 (2%) |
| goal_behind | 1.2 | 5/960 (1%) | 3.9 | 30/960 (3%) |

### Roles: who leads (more push time) and who pushes first

| formation | half | n | leader = anymal1 | leader by start role | first pusher = anymal1 | first pusher by start role | success |
|---|---|---|---|---|---|---|---|
| standard | unswapped | 480 | 295/479 (62%) | behind_left 62%, behind_right 38% | 267/480 (56%) | behind_left 56%, behind_right 44% | 324/480 (68%) |
| standard | swapped | 480 | 209/480 (44%) | behind_left 56%, behind_right 44% | 200/480 (42%) | behind_left 58%, behind_right 42% | 311/480 (65%) |
| flank | unswapped | 480 | 281/479 (59%) | left 41%, right 59% | 304/480 (63%) | left 37%, right 63% | 307/480 (64%) |
| flank | swapped | 480 | 230/480 (48%) | left 48%, right 52% | 182/480 (38%) | left 38%, right 62% | 300/480 (62%) |
| goal_behind | unswapped | 480 | 377/476 (79%) | behind 79%, goal_side 21% | 465/477 (97%) | behind 97%, goal_side 3% | 309/480 (64%) |
| goal_behind | swapped | 480 | 114/475 (24%) | behind 76%, goal_side 24% | 37/478 (8%) | behind 92%, goal_side 8% | 297/480 (62%) |

### Swap: same task, start places exchanged

| formation | matched pairs | success unswapped / swapped | outcome differs | leader follows the start place | leader follows identity |
|---|---|---|---|---|---|
| standard | 480 | 324 / 311 | 103 | 311/479 (65%) | 168/479 (35%) |
| flank | 480 | 307 / 300 | 111 | 310/479 (65%) | 169/479 (35%) |
| goal_behind | 480 | 309 / 297 | 108 | 338/471 (72%) | 133/471 (28%) |

### Takeover: the second robot pushes alone while the object moves >= 0.2 m toward the goal

| formation | episodes with a takeover | their success | success of the rest |
|---|---|---|---|
| standard | 461/960 (48%) | 340/461 (74%) | 295/499 (59%) |
| flank | 547/960 (57%) | 391/547 (71%) | 216/413 (52%) |
| goal_behind | 415/960 (43%) | 296/415 (71%) | 310/545 (57%) |

## F

### Success by formation (unswapped and swapped pooled)

| formation | objects | n | success | falls | precise | success change vs standard [95% CI] |
|---|---|---|---|---|---|---|
| standard | all ten | 960 | 621/960 (65%) | 116/960 (12%) | 561/960 (58%) |  |
| standard | arch | 96 | 26/96 (27%) | 21/96 (22%) | 24/96 (25%) |  |
| standard | cylinder | 96 | 41/96 (43%) | 18/96 (19%) | 30/96 (31%) |  |
| standard | long | 96 | 74/96 (77%) | 4/96 (4%) | 68/96 (71%) |  |
| standard | sphere | 96 | 91/96 (95%) | 4/96 (4%) | 92/96 (96%) |  |
| flank | all ten | 960 | 603/960 (63%) | 134/960 (14%) | 537/960 (56%) | -1.9 [-4.9, +1.1] pts |
| flank | arch | 96 | 35/96 (36%) | 15/96 (16%) | 29/96 (30%) | +9.4 [-2.1, +20.8] pts |
| flank | cylinder | 96 | 35/96 (36%) | 29/96 (30%) | 28/96 (29%) | -6.2 [-15.6, +3.1] pts |
| flank | long | 96 | 68/96 (71%) | 8/96 (8%) | 65/96 (68%) | -6.2 [-15.6, +3.1] pts |
| flank | sphere | 96 | 91/96 (95%) | 3/96 (3%) | 91/96 (95%) | +0.0 [-6.2, +6.2] pts |
| goal_behind | all ten | 960 | 593/960 (62%) | 136/960 (14%) | 537/960 (56%) | -2.9 [-6.0, +0.3] pts |
| goal_behind | arch | 96 | 29/96 (30%) | 24/96 (25%) | 21/96 (22%) | +3.1 [-7.3, +14.6] pts |
| goal_behind | cylinder | 96 | 35/96 (36%) | 16/96 (17%) | 28/96 (29%) | -6.2 [-16.7, +4.2] pts |
| goal_behind | long | 96 | 69/96 (72%) | 10/96 (10%) | 61/96 (64%) | -5.2 [-15.6, +5.2] pts |
| goal_behind | sphere | 96 | 96/96 (100%) | 0/96 (0%) | 96/96 (100%) | +5.2 [+1.0, +10.4] pts |

### Success by formation and mass (all ten)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 87% | 83% | 58% | 30% |
| flank | 85% | 82% | 59% | 25% |
| goal_behind | 86% | 77% | 57% | 28% |

### Timing (seconds from the start)

| formation | first push, median | never pushed | first 0.25 m progress, median | never progressed |
|---|---|---|---|---|
| standard | 1.3 | 0/960 (0%) | 3.0 | 15/960 (2%) |
| flank | 1.1 | 0/960 (0%) | 3.3 | 13/960 (1%) |
| goal_behind | 1.2 | 8/960 (1%) | 4.0 | 38/960 (4%) |

### Roles: who leads (more push time) and who pushes first

| formation | half | n | leader = anymal1 | leader by start role | first pusher = anymal1 | first pusher by start role | success |
|---|---|---|---|---|---|---|---|
| standard | unswapped | 480 | 303/480 (63%) | behind_left 63%, behind_right 37% | 286/480 (60%) | behind_left 60%, behind_right 40% | 304/480 (63%) |
| standard | swapped | 480 | 208/480 (43%) | behind_left 57%, behind_right 43% | 207/480 (43%) | behind_left 57%, behind_right 43% | 317/480 (66%) |
| flank | unswapped | 480 | 262/479 (55%) | left 45%, right 55% | 304/480 (63%) | left 37%, right 63% | 308/480 (64%) |
| flank | swapped | 480 | 258/478 (54%) | left 54%, right 46% | 165/480 (34%) | left 34%, right 66% | 295/480 (61%) |
| goal_behind | unswapped | 480 | 368/475 (77%) | behind 77%, goal_side 23% | 441/475 (93%) | behind 93%, goal_side 7% | 306/480 (64%) |
| goal_behind | swapped | 480 | 123/477 (26%) | behind 74%, goal_side 26% | 30/477 (6%) | behind 94%, goal_side 6% | 287/480 (60%) |

### Swap: same task, start places exchanged

| formation | matched pairs | success unswapped / swapped | outcome differs | leader follows the start place | leader follows identity |
|---|---|---|---|---|---|
| standard | 480 | 304 / 317 | 91 | 323/480 (67%) | 157/480 (33%) |
| flank | 480 | 308 / 295 | 109 | 307/477 (64%) | 170/477 (36%) |
| goal_behind | 480 | 306 / 287 | 105 | 350/472 (74%) | 122/472 (26%) |

### Takeover: the second robot pushes alone while the object moves >= 0.2 m toward the goal

| formation | episodes with a takeover | their success | success of the rest |
|---|---|---|---|
| standard | 463/960 (48%) | 326/463 (70%) | 295/497 (59%) |
| flank | 572/960 (60%) | 396/572 (69%) | 207/388 (53%) |
| goal_behind | 395/960 (41%) | 274/395 (69%) | 319/565 (56%) |

## Policies compared (paired, same tasks; single runs)

| formation | F - A success [95% CI] |
|---|---|
| standard | -1.5 [-4.1, +1.2] pts |
| flank | -0.4 [-3.1, +2.3] pts |
| goal_behind | -1.4 [-4.0, +1.2] pts |

## Pooled over swaps and runs (per base task; ** = interval excludes 0)

- A: rerun flips (of 960 per formation): standard 156, flank 142, goal_behind 147
- F: rerun flips (of 960 per formation): standard 156, flank 137, goal_behind 152

### Success rate

| object | A (2 runs) standard | A (2 runs) flank | A (2 runs) goal_behind | F (2 runs) standard | F (2 runs) flank | F (2 runs) goal_behind |
|---|---|---|---|---|---|---|
| all ten | 65.2% | 62.6% | 63.2% | 65.4% | 62.9% | 61.9% |
| arch | 33.3% | 32.3% | 33.3% | 29.2% | 34.4% | 29.2% |
| cube | 66.1% | 65.6% | 64.1% | 65.1% | 63.0% | 64.1% |
| cylinder | 44.3% | 35.4% | 35.9% | 46.4% | 35.4% | 35.9% |
| dumbbell | 61.5% | 57.8% | 56.8% | 58.9% | 52.6% | 55.2% |
| l_shape | 79.2% | 74.5% | 71.9% | 81.2% | 73.4% | 75.5% |
| long | 75.0% | 70.3% | 77.6% | 76.6% | 69.8% | 72.9% |
| plus | 53.6% | 61.5% | 54.7% | 55.2% | 61.5% | 54.2% |
| sphere | 97.4% | 94.8% | 98.4% | 92.7% | 94.8% | 99.5% |
| t_shape | 71.9% | 63.5% | 70.8% | 76.6% | 70.3% | 65.1% |
| u_channel | 69.8% | 70.3% | 68.2% | 72.4% | 73.4% | 67.2% |

### Change vs standard (points [95% CI])

| object | A flank | A goal_behind | F flank | F goal_behind |
|---|---|---|---|---|
| all ten | -2.6 [-5.2, -0.2] ** | -2.0 [-4.6, +0.5] | -2.6 [-5.2, -0.2] ** | -3.5 [-6.2, -0.8] ** |
| arch | -1.0 [-9.9, +7.8] | +0.0 [-8.3, +8.9] | +5.2 [-3.1, +14.1] | +0.0 [-8.9, +8.9] |
| cube | -0.5 [-6.2, +5.7] | -2.1 [-8.3, +4.7] | -2.1 [-8.3, +3.6] | -1.0 [-7.8, +6.2] |
| cylinder | -8.9 [-18.2, +0.0] | -8.3 [-19.3, +1.6] | -10.9 [-20.8, -2.6] ** | -10.4 [-22.4, +1.0] |
| dumbbell | -3.6 [-10.9, +3.6] | -4.7 [-14.1, +4.7] | -6.2 [-12.5, +0.0] | -3.6 [-12.5, +4.7] |
| l_shape | -4.7 [-11.5, +2.1] | -7.3 [-14.1, -0.5] ** | -7.8 [-16.7, +0.0] | -5.7 [-13.0, +2.6] |
| long | -4.7 [-13.0, +3.1] | +2.6 [-4.7, +10.4] | -6.8 [-15.6, +2.1] | -3.6 [-12.0, +4.7] |
| plus | +7.8 [-3.1, +18.8] | +1.0 [-10.4, +12.5] | +6.2 [-4.2, +17.2] | -1.0 [-12.0, +9.9] |
| sphere | -2.6 [-6.8, +1.0] | +1.0 [-2.6, +4.2] | +2.1 [-3.6, +7.8] | +6.8 [+2.6, +11.5] ** |
| t_shape | -8.3 [-16.1, -1.0] ** | -1.0 [-7.3, +5.2] | -6.2 [-11.5, -1.0] ** | -11.5 [-19.8, -3.6] ** |
| u_channel | +0.5 [-9.4, +9.9] | -1.6 [-9.4, +6.2] | +1.0 [-6.2, +8.3] | -5.2 [-14.1, +4.2] |

### F - A, success per formation (per base task; points [95% CI])

| object | standard | flank | goal_behind |
|---|---|---|---|
| all ten | +0.2 [-1.7, +2.1] | +0.3 [-1.8, +2.3] | -1.3 [-3.2, +0.6] |
| arch | -4.2 [-13.0, +4.2] | +2.1 [-5.7, +9.4] | -4.2 [-11.5, +3.6] |
| cube | -1.0 [-5.2, +3.1] | -2.6 [-9.9, +4.2] | +0.0 [-4.2, +4.2] |
| cylinder | +2.1 [-3.6, +7.8] | +0.0 [-5.7, +5.7] | +0.0 [-5.2, +4.7] |
| dumbbell | -2.6 [-8.9, +3.6] | -5.2 [-13.0, +2.1] | -1.6 [-9.9, +6.2] |
| l_shape | +2.1 [-3.1, +7.8] | -1.0 [-7.3, +5.2] | +3.6 [-3.1, +10.9] |
| long | +1.6 [-3.6, +7.3] | -0.5 [-4.7, +3.6] | -4.7 [-11.5, +2.1] |
| plus | +1.6 [-7.3, +10.4] | +0.0 [-6.2, +6.2] | -0.5 [-6.8, +5.2] |
| sphere | -4.7 [-9.4, -0.5] ** | +0.0 [-5.7, +5.7] | +1.0 [-1.0, +3.6] |
| t_shape | +4.7 [+1.6, +8.3] ** | +6.8 [+0.0, +13.5] | -5.7 [-13.5, +1.0] |
| u_channel | +2.6 [-3.1, +8.9] | +3.1 [-2.6, +8.9] | -1.0 [-5.7, +3.6] |

### cylinder: getting the push going vs finishing it (all runs and swaps)

| policy | formation | n | success | falls | first 0.25 m progress, median s | never progressed | final distance to goal, median m | final distance, failures, median m |
|---|---|---|---|---|---|---|---|---|
| A | standard | 192 | 44.3% | 24.5% | 2.0 | 1.0% | 0.09 | 0.27 |
| A | flank | 192 | 35.4% | 25.0% | 2.6 | 0.0% | 0.12 | 0.21 |
| A | goal_behind | 192 | 35.9% | 16.1% | 3.0 | 0.5% | 0.11 | 0.17 |
| F | standard | 192 | 46.4% | 17.2% | 2.0 | 1.0% | 0.09 | 0.20 |
| F | flank | 192 | 35.4% | 26.0% | 2.5 | 0.0% | 0.11 | 0.24 |
| F | goal_behind | 192 | 35.9% | 15.6% | 3.1 | 0.0% | 0.09 | 0.15 |
