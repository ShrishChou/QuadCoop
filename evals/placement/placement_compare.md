# Start placements: PARENT = `place-ten-ippo-it4000`, IPPO = `place-nwA-ippo-it5000`, MAPPO = `place-nwB-mappo-it5000`

## PARENT

### Success by formation (unswapped and swapped pooled)

| formation | objects | n | success | falls | precise | success change vs standard [95% CI] |
|---|---|---|---|---|---|---|
| standard | all ten | 960 | 613/960 (64%) | 128/960 (13%) | 553/960 (58%) |  |
| standard | arch | 96 | 27/96 (28%) | 34/96 (35%) | 23/96 (24%) |  |
| standard | cylinder | 96 | 43/96 (45%) | 16/96 (17%) | 35/96 (36%) |  |
| standard | long | 96 | 73/96 (76%) | 4/96 (4%) | 69/96 (72%) |  |
| standard | sphere | 96 | 90/96 (94%) | 6/96 (6%) | 91/96 (95%) |  |
| flank | all ten | 960 | 620/960 (65%) | 133/960 (14%) | 573/960 (60%) | +0.7 [-2.2, +3.6] pts |
| flank | arch | 96 | 35/96 (36%) | 17/96 (18%) | 33/96 (34%) | +8.3 [-3.1, +19.8] pts |
| flank | cylinder | 96 | 43/96 (45%) | 22/96 (23%) | 37/96 (39%) | +0.0 [-8.3, +8.3] pts |
| flank | long | 96 | 73/96 (76%) | 7/96 (7%) | 69/96 (72%) | +0.0 [-9.4, +9.4] pts |
| flank | sphere | 96 | 93/96 (97%) | 3/96 (3%) | 93/96 (97%) | +3.1 [-1.0, +8.3] pts |
| goal_behind | all ten | 960 | 604/960 (63%) | 128/960 (13%) | 549/960 (57%) | -0.9 [-3.9, +1.9] pts |
| goal_behind | arch | 96 | 27/96 (28%) | 32/96 (33%) | 22/96 (23%) | +0.0 [-11.5, +10.4] pts |
| goal_behind | cylinder | 96 | 39/96 (41%) | 15/96 (16%) | 31/96 (32%) | -4.2 [-13.5, +5.2] pts |
| goal_behind | long | 96 | 72/96 (75%) | 7/96 (7%) | 65/96 (68%) | -1.0 [-11.5, +8.3] pts |
| goal_behind | sphere | 96 | 95/96 (99%) | 1/96 (1%) | 95/96 (99%) | +5.2 [+0.0, +10.4] pts |

### Success by formation and mass (all ten)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 90% | 78% | 60% | 28% |
| flank | 90% | 85% | 57% | 27% |
| goal_behind | 87% | 81% | 59% | 25% |

### Timing (seconds from the start)

| formation | first push, median | never pushed | first 0.25 m progress, median | never progressed |
|---|---|---|---|---|
| standard | 1.4 | 0/960 (0%) | 3.0 | 18/960 (2%) |
| flank | 1.1 | 0/960 (0%) | 3.3 | 18/960 (2%) |
| goal_behind | 1.2 | 11/960 (1%) | 3.9 | 40/960 (4%) |

### Roles: who leads (more push time) and who pushes first

| formation | half | n | leader = anymal1 | leader by start role | first pusher = anymal1 | first pusher by start role | success |
|---|---|---|---|---|---|---|---|
| standard | unswapped | 480 | 306/478 (64%) | behind_left 64%, behind_right 36% | 292/480 (61%) | behind_left 61%, behind_right 39% | 312/480 (65%) |
| standard | swapped | 480 | 235/480 (49%) | behind_left 51%, behind_right 49% | 260/480 (54%) | behind_left 46%, behind_right 54% | 301/480 (63%) |
| flank | unswapped | 480 | 265/476 (56%) | left 44%, right 56% | 300/480 (62%) | left 38%, right 62% | 312/480 (65%) |
| flank | swapped | 480 | 276/480 (57%) | left 57%, right 42% | 180/480 (38%) | left 38%, right 62% | 308/480 (64%) |
| goal_behind | unswapped | 480 | 402/476 (84%) | behind 84%, goal_side 16% | 449/476 (94%) | behind 94%, goal_side 6% | 311/480 (65%) |
| goal_behind | swapped | 480 | 125/472 (26%) | behind 74%, goal_side 26% | 27/473 (6%) | behind 94%, goal_side 6% | 293/480 (61%) |

### Swap: same task, start places exchanged

| formation | matched pairs | success unswapped / swapped | outcome differs | leader follows the start place | leader follows identity |
|---|---|---|---|---|---|
| standard | 480 | 312 / 301 | 111 | 299/478 (63%) | 179/478 (37%) |
| flank | 480 | 312 / 308 | 106 | 292/476 (61%) | 184/476 (39%) |
| goal_behind | 480 | 311 / 293 | 98 | 346/470 (74%) | 124/470 (26%) |

### Takeover: the second robot pushes alone while the object moves >= 0.2 m toward the goal

| formation | episodes with a takeover | their success | success of the rest |
|---|---|---|---|
| standard | 487/960 (51%) | 331/487 (68%) | 282/473 (60%) |
| flank | 539/960 (56%) | 388/539 (72%) | 232/421 (55%) |
| goal_behind | 368/960 (38%) | 255/368 (69%) | 349/592 (59%) |

## IPPO

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

## MAPPO

### Success by formation (unswapped and swapped pooled)

| formation | objects | n | success | falls | precise | success change vs standard [95% CI] |
|---|---|---|---|---|---|---|
| standard | all ten | 960 | 646/960 (67%) | 109/960 (11%) | 594/960 (62%) |  |
| standard | arch | 96 | 32/96 (33%) | 25/96 (26%) | 26/96 (27%) |  |
| standard | cylinder | 96 | 48/96 (50%) | 13/96 (14%) | 38/96 (40%) |  |
| standard | long | 96 | 79/96 (82%) | 2/96 (2%) | 77/96 (80%) |  |
| standard | sphere | 96 | 93/96 (97%) | 2/96 (2%) | 93/96 (97%) |  |
| flank | all ten | 960 | 615/960 (64%) | 133/960 (14%) | 548/960 (57%) | -3.2 [-6.2, -0.1] pts |
| flank | arch | 96 | 40/96 (42%) | 16/96 (17%) | 34/96 (35%) | +8.3 [-3.1, +19.8] pts |
| flank | cylinder | 96 | 31/96 (32%) | 28/96 (29%) | 24/96 (25%) | -17.7 [-27.1, -8.3] pts |
| flank | long | 96 | 66/96 (69%) | 4/96 (4%) | 63/96 (66%) | -13.5 [-22.9, -4.2] pts |
| flank | sphere | 96 | 93/96 (97%) | 2/96 (2%) | 93/96 (97%) | +0.0 [-5.2, +5.2] pts |
| goal_behind | all ten | 960 | 601/960 (63%) | 130/960 (14%) | 531/960 (55%) | -4.7 [-7.9, -1.5] pts |
| goal_behind | arch | 96 | 33/96 (34%) | 22/96 (23%) | 29/96 (30%) | +1.0 [-11.5, +12.5] pts |
| goal_behind | cylinder | 96 | 40/96 (42%) | 16/96 (17%) | 29/96 (30%) | -8.3 [-17.7, +2.1] pts |
| goal_behind | long | 96 | 69/96 (72%) | 6/96 (6%) | 67/96 (70%) | -10.4 [-19.8, -2.1] pts |
| goal_behind | sphere | 96 | 93/96 (97%) | 0/96 (0%) | 94/96 (98%) | +0.0 [-5.2, +5.2] pts |

### Success by formation and mass (all ten)

| formation | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| standard | 91% | 84% | 64% | 30% |
| flank | 88% | 85% | 58% | 25% |
| goal_behind | 85% | 83% | 57% | 26% |

### Timing (seconds from the start)

| formation | first push, median | never pushed | first 0.25 m progress, median | never progressed |
|---|---|---|---|---|
| standard | 1.3 | 0/960 (0%) | 3.0 | 14/960 (1%) |
| flank | 1.1 | 0/960 (0%) | 3.3 | 16/960 (2%) |
| goal_behind | 1.1 | 6/960 (1%) | 4.0 | 32/960 (3%) |

### Roles: who leads (more push time) and who pushes first

| formation | half | n | leader = anymal1 | leader by start role | first pusher = anymal1 | first pusher by start role | success |
|---|---|---|---|---|---|---|---|
| standard | unswapped | 480 | 303/478 (63%) | behind_left 63%, behind_right 37% | 277/480 (58%) | behind_left 58%, behind_right 42% | 313/480 (65%) |
| standard | swapped | 480 | 235/479 (49%) | behind_left 51%, behind_right 49% | 205/480 (43%) | behind_left 57%, behind_right 43% | 333/480 (69%) |
| flank | unswapped | 480 | 282/480 (59%) | left 41%, right 59% | 329/480 (69%) | left 31%, right 69% | 308/480 (64%) |
| flank | swapped | 480 | 239/479 (50%) | left 50%, right 50% | 193/480 (40%) | left 40%, right 60% | 307/480 (64%) |
| goal_behind | unswapped | 480 | 380/476 (80%) | behind 80%, goal_side 20% | 467/477 (98%) | behind 98%, goal_side 2% | 303/480 (63%) |
| goal_behind | swapped | 480 | 126/476 (26%) | behind 74%, goal_side 26% | 22/477 (5%) | behind 95%, goal_side 5% | 298/480 (62%) |

### Swap: same task, start places exchanged

| formation | matched pairs | success unswapped / swapped | outcome differs | leader follows the start place | leader follows identity |
|---|---|---|---|---|---|
| standard | 480 | 313 / 333 | 102 | 320/477 (67%) | 157/477 (33%) |
| flank | 480 | 308 / 307 | 97 | 308/479 (64%) | 171/479 (36%) |
| goal_behind | 480 | 303 / 298 | 107 | 333/472 (71%) | 139/472 (29%) |

### Takeover: the second robot pushes alone while the object moves >= 0.2 m toward the goal

| formation | episodes with a takeover | their success | success of the rest |
|---|---|---|---|
| standard | 449/960 (47%) | 324/449 (72%) | 322/511 (63%) |
| flank | 552/960 (57%) | 399/552 (72%) | 216/408 (53%) |
| goal_behind | 389/960 (41%) | 259/389 (67%) | 342/571 (60%) |

## Policies compared (paired, same tasks; single runs)

| formation | IPPO - PARENT success [95% CI] | MAPPO - PARENT success [95% CI] | MAPPO - IPPO success [95% CI] |
|---|---|---|---|
| standard | +2.3 [-0.5, +5.0] pts | +3.4 [+0.7, +6.0] pts | +1.1 [-1.5, +3.9] pts |
| flank | -1.4 [-3.9, +1.2] pts | -0.5 [-3.0, +2.0] pts | +0.8 [-1.7, +3.4] pts |
| goal_behind | +0.2 [-2.3, +2.8] pts | -0.3 [-2.9, +2.3] pts | -0.5 [-3.0, +2.0] pts |

## Two runs per checkpoint: rerun noise and pooled change vs standard

### IPPO (`place-nwA-ippo-it5000-r2` as the second run)

Same checkpoint, same tasks, second run: outcome flips (1 -> 0 / 0 -> 1) per formation: standard 87 / 69; flank 77 / 65; goal_behind 73 / 74 (of 960).

| object | standard (2 runs) | flank change [95% CI] | goal_behind change [95% CI] |
|---|---|---|---|
| all ten | 65% | -2.6 [-5.1, -0.1] ** | -2.0 [-4.4, +0.4] |
| arch | 33% | -1.0 [-8.9, +7.3] | +0.0 [-8.9, +9.4] |
| cube | 66% | -0.5 [-8.3, +7.3] | -2.1 [-8.3, +4.2] |
| cylinder | 44% | -8.9 [-16.7, -1.6] ** | -8.3 [-16.7, +0.0] |
| dumbbell | 61% | -3.6 [-11.5, +4.2] | -4.7 [-12.5, +3.1] |
| l_shape | 79% | -4.7 [-12.0, +2.6] | -7.3 [-14.6, +0.0] |
| long | 75% | -4.7 [-13.5, +4.2] | +2.6 [-5.7, +10.9] |
| plus | 54% | +7.8 [-1.6, +16.7] | +1.0 [-8.9, +10.9] |
| sphere | 97% | -2.6 [-6.8, +1.6] | +1.0 [-2.1, +4.2] |
| t_shape | 72% | -8.3 [-16.1, -0.5] ** | -1.0 [-7.3, +5.7] |
| u_channel | 70% | +0.5 [-7.8, +8.9] | -1.6 [-9.4, +5.7] |

** = interval excludes 0.

### MAPPO (`place-nwB-mappo-it5000-r2` as the second run)

Same checkpoint, same tasks, second run: outcome flips (1 -> 0 / 0 -> 1) per formation: standard 83 / 58; flank 70 / 70; goal_behind 92 / 78 (of 960).

| object | standard (2 runs) | flank change [95% CI] | goal_behind change [95% CI] |
|---|---|---|---|
| all ten | 66% | -1.9 [-4.4, +0.5] | -4.1 [-6.6, -1.6] ** |
| arch | 32% | +6.8 [-1.6, +15.1] | +1.0 [-7.8, +10.4] |
| cube | 68% | -2.1 [-8.9, +4.7] | -5.2 [-12.0, +1.6] |
| cylinder | 49% | -12.5 [-19.8, -5.7] ** | -13.5 [-21.9, -5.2] ** |
| dumbbell | 61% | -6.8 [-14.1, +1.0] | -6.2 [-14.1, +2.1] |
| l_shape | 79% | -5.2 [-11.5, +1.0] | -4.2 [-10.4, +2.1] |
| long | 80% | -11.5 [-19.8, -3.1] ** | -7.8 [-15.1, -0.5] ** |
| plus | 54% | +6.8 [-3.1, +16.1] | -2.6 [-11.5, +6.2] |
| sphere | 97% | -0.5 [-4.2, +3.1] | +0.5 [-3.1, +4.2] |
| t_shape | 70% | +1.6 [-6.2, +8.9] | -4.2 [-13.0, +4.2] |
| u_channel | 69% | +4.2 [-2.6, +10.4] | +1.0 [-7.3, +8.9] |

** = interval excludes 0.

