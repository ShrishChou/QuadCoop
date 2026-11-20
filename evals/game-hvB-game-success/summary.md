# Contact game: game-hvB

payoff: success; 2000 rounds x 20 seeds per task; sweep game-hvB-allpairs

## summary

| | tasks | optimum | worst pure Nash | share with a trap (worst NE < optimum - 0.1) | pure NE per task | random usable pair | spread rule | adjacent rule | regret matching (found optimum) | rm plus (found optimum) | hedge (found optimum) | exp3 (found optimum) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all tasks | 60 | 0.17 | 0.08 | 0.30 | 13.03 | 0.07 | 0.08 | 0.06 | 0.17 (0.99) | 0.17 (1.00) | 0.17 (1.00) | 0.09 (0.92) |
| tasks with 4+ contacts per robot | 54 | 0.14 | 0.04 | 0.33 | 14.26 | 0.03 | 0.03 | 0.01 | 0.14 (0.99) | 0.14 (1.00) | 0.14 (1.00) | 0.06 (0.91) |

Learner columns: expected team payoff of the joint play over the last 100 rounds (and the share of runs whose most played pair is the optimum). All values here are read off the sweep itself, so the optimum is optimistic (the best of noisy cells); see the holdout table.

learned chooser (leave-one-object-out ridge regression on pair features), on the sweep: all tasks: 0.06; tasks with 4+ contacts per robot: 0.02

## how much the pair matters vs noise

Within a task, the true payoffs of different pairs spread by about 0.05 (sd), while one episode of the same pair varies by 0.19. With 4 episodes per pair a pair's estimate has reliability 0.22 (share of its variance that is real differences between pairs); 12 episodes: 0.45, 24 episodes: 0.62, 48 episodes: 0.77.

## choices scored on fresh placements (holdout)

| | sweep's optimum pair | learned chooser (unseen object) | spread rule | adjacent rule | random usable pair | regret matching's final pair | rm plus's final pair | hedge's final pair | exp3's final pair | holdout's own best (optimistic) |
|---|---|---|---|---|---|---|---|---|---|---|
| all tasks | 0.12 | 0.03 | 0.04 | 0.04 | 0.04 | 0.12 | 0.11 | 0.11 | 0.12 | 0.16 |
| tasks with 4+ contacts per robot | 0.13 | 0.02 | 0.03 | 0.03 | 0.03 | 0.12 | 0.12 | 0.12 | 0.12 | 0.17 |

## per task

| object | scenario | mass | contacts | optimum (pair) | pure NE | worst NE | random | spread | adjacent | regret matching | rm plus | hedge | exp3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | A_straight | 40 | 6 | 0.50 (part 3 corner -x+y + part 2 -x) | 6 | 0.25 | 0.12 | 0.00 | 0.00 | 0.40 | 0.49 | 0.50 | 0.21 |
| arch | A_straight | 80 | 6 | 0.25 (part 3 corner -x+y + part 2 -x) | 12 | 0.00 | 0.03 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.04 |
| arch | B_left | 40 | 8 | 0.25 (part 3 -x + part 2 corner -x-y) | 20 | 0.00 | 0.02 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.05 |
| arch | B_left | 80 | 8 | 0.50 (part 3 corner -x-y + part 2 corner -x-y) | 28 | 0.00 | 0.02 | 0.00 | 0.00 | 0.50 | 0.50 | 0.50 | 0.13 |
| arch | C_backright | 40 | 6 | 0.00 (part 3 +y + part 3 +x) | 22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | C_backright | 80 | 6 | 0.00 (part 3 +y + part 3 +x) | 22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| arch | D_far_turn | 40 | 6 | 0.25 (part 3 -x + part 2 corner -x+y) | 10 | 0.00 | 0.03 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.04 |
| arch | D_far_turn | 80 | 6 | 0.25 (part 3 -x + part 2 corner -x+y) | 10 | 0.00 | 0.03 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.05 |
| asym | A_straight | 80 | 4 | 0.00 (part 1 -x + part 0 corner -x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| asym | B_left | 80 | 5 | 0.00 (part 1 -x + part 1 -y) | 12 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| asym | C_backright | 80 | 4 | 0.00 (part 1 +x + part 0 corner +x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| asym | D_far_turn | 80 | 4 | 0.00 (part 1 -x + part 0 corner -x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| beam | A_straight | 80 | 7 | 0.00 (part 0 -x seg 3/5 + part 0 -x seg 1/5) | 30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam | B_left | 80 | 8 | 0.00 (part 0 -x seg 3/5 + part 0 -x seg 1/5) | 42 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam | C_backright | 80 | 7 | 0.00 (part 0 +x seg 1/5 + part 0 +x seg 3/5) | 30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| beam | D_far_turn | 80 | 7 | 0.00 (part 0 -x seg 3/5 + part 0 -x seg 1/5) | 30 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| cube | A_straight | 40 | 2 | 0.00 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| cube | B_left | 40 | 4 | 0.25 (part 0 -x + part 0 -y) | 4 | 0.00 | 0.08 |  |  | 0.25 | 0.25 | 0.25 | 0.10 |
| cube | C_backright | 40 | 2 | 0.75 (part 0 +x + part 0 +y) | 2 | 0.75 | 0.75 |  |  | 0.75 | 0.75 | 0.75 | 0.73 |
| cube | D_far_turn | 40 | 2 | 0.00 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | A_straight | 40 | 4 | 0.25 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.25 | 0.08 |  |  | 0.25 | 0.25 | 0.25 | 0.09 |
| cylinder | A_straight | 80 | 4 | 0.75 (part 0 -x seg 1/2 + part 0 corner -x+y) | 4 | 0.75 | 0.50 |  |  | 0.75 | 0.75 | 0.75 | 0.71 |
| cylinder | B_left | 40 | 5 | 0.00 (part 0 -x seg 1/2 + part 0 -y) | 12 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | B_left | 80 | 5 | 0.25 (part 0 -y + part 0 -x seg 2/2) | 6 | 0.00 | 0.04 |  |  | 0.25 | 0.25 | 0.25 | 0.07 |
| cylinder | C_backright | 40 | 4 | 0.00 (part 0 +x seg 1/2 + part 0 corner +x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | C_backright | 80 | 4 | 0.00 (part 0 +x seg 1/2 + part 0 corner +x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | D_far_turn | 40 | 4 | 0.00 (part 0 -x seg 1/2 + part 0 corner -x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| cylinder | D_far_turn | 80 | 4 | 0.00 (part 0 -x seg 1/2 + part 0 corner -x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | A_straight | 40 | 7 | 0.50 (part 1 -x + part 0 corner -x+y) | 8 | 0.00 | 0.07 | 0.00 | 0.00 | 0.50 | 0.50 | 0.50 | 0.29 |
| dumbbell | A_straight | 80 | 7 | 0.25 (part 1 -x + part 0 corner -x+y) | 6 | 0.25 | 0.05 | 0.25 | 0.00 | 0.25 | 0.24 | 0.25 | 0.07 |
| dumbbell | B_left | 40 | 8 | 0.50 (part 1 corner +x-y + part 2 -x seg 2/3) | 26 | 0.00 | 0.02 | 0.00 | 0.00 | 0.50 | 0.50 | 0.50 | 0.14 |
| dumbbell | B_left | 80 | 8 | 0.25 (part 1 -y + part 2 -x seg 2/3) | 28 | 0.00 | 0.01 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.02 |
| dumbbell | C_backright | 40 | 6 | 0.00 (part 1 +x + part 2 +x seg 2/3) | 22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | C_backright | 80 | 6 | 0.00 (part 1 +x + part 2 +x seg 2/3) | 22 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | D_far_turn | 40 | 7 | 0.00 (part 1 corner -x+y + part 1 corner -x-y) | 28 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | D_far_turn | 80 | 7 | 0.00 (part 1 corner -x+y + part 1 corner -x-y) | 28 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape | A_straight | 80 | 6 | 0.00 (part 0 -x seg 1/2 + part 0 corner -x+y) | 12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape | B_left | 80 | 7 | 0.00 (part 0 -x seg 1/2 + part 0 -y) | 30 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape | C_backright | 80 | 6 | 0.00 (part 0 +x seg 1/2 + part 1 +x) | 20 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| l_shape | D_far_turn | 80 | 6 | 0.00 (part 0 -x seg 1/2 + part 0 corner -x+y) | 12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| long | A_straight | 40 | 4 | 0.25 (part 0 -x seg 1/2 + part 0 corner -x+y) | 4 | 0.25 | 0.17 | 0.25 | 0.25 | 0.25 | 0.25 | 0.25 | 0.14 |
| long | B_left | 40 | 5 | 0.50 (part 0 corner +x-y + part 0 -x seg 2/2) | 4 | 0.00 | 0.08 | 0.00 | 0.00 | 0.50 | 0.50 | 0.50 | 0.34 |
| long | C_backright | 40 | 4 | 0.00 (part 0 +x seg 1/2 + part 0 corner +x+y) | 6 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| long | D_far_turn | 40 | 4 | 0.00 (part 0 -x seg 1/2 + part 0 corner -x+y) | 6 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| plus | A_straight | 80 | 5 | 0.00 (part 1 -x + part 0 corner -x-y) | 12 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| plus | B_left | 80 | 6 | 0.25 (part 1 corner -x-y + part 0 corner +x-y) | 12 | 0.00 | 0.03 |  |  | 0.25 | 0.25 | 0.25 | 0.04 |
| plus | C_backright | 80 | 4 | 0.00 (part 1 +x + part 0 corner +x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| plus | D_far_turn | 80 | 5 | 0.00 (part 1 -x + part 0 corner -x-y) | 12 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| sphere | A_straight | 40 | 2 | 1.00 (sector 225 + sector 135) | 2 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 1.00 | 0.98 |
| sphere | B_left | 40 | 4 | 0.25 (sector 315 + sector 180) | 2 | 0.25 | 0.08 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.10 |
| sphere | C_backright | 40 | 2 | 0.50 (sector 0 + sector 90) | 2 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.46 |
| sphere | D_far_turn | 40 | 2 | 0.50 (sector 225 + sector 135) | 2 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.50 | 0.45 |
| t_shape | A_straight | 80 | 5 | 0.25 (part 0 -x seg 1/3 + part 0 corner -x+y) | 6 | 0.00 | 0.04 |  |  | 0.25 | 0.25 | 0.25 | 0.07 |
| t_shape | B_left | 80 | 8 | 0.25 (part 0 -x seg 1/3 + part 0 -y) | 26 | 0.00 | 0.01 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.02 |
| t_shape | C_backright | 80 | 5 | 0.00 (part 1 +x + part 1 +y seg 2/2) | 12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| t_shape | D_far_turn | 80 | 5 | 0.00 (part 0 -x seg 1/3 + part 0 corner -x+y) | 12 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| u_channel | A_straight | 80 | 5 | 0.25 (part 0 corner -x-y + part 0 corner -x+y) | 4 | 0.00 | 0.04 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.06 |
| u_channel | B_left | 80 | 9 | 0.25 (part 2 -y seg 2/2 + part 0 -x seg 2/3) | 38 | 0.00 | 0.01 | 0.00 | 0.00 | 0.25 | 0.25 | 0.25 | 0.01 |
| u_channel | C_backright | 80 | 7 | 0.50 (part 2 corner +x+y + part 0 +y) | 10 | 0.00 | 0.05 | 0.50 | 0.00 | 0.50 | 0.49 | 0.50 | 0.25 |
| u_channel | D_far_turn | 80 | 5 | 0.00 (part 0 -x seg 1/3 + part 0 corner -x+y) | 12 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
