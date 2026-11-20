# Contact game: game-hvB

payoff: score; 2000 rounds x 20 seeds per task; sweep game-hvB-allpairs

## summary

| | tasks | optimum | worst pure Nash | share with a trap (worst NE < optimum - 0.1) | pure NE per task | random usable pair | spread rule | adjacent rule | regret matching (found optimum) | rm plus (found optimum) | hedge (found optimum) | exp3 (found optimum) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| all tasks | 60 | 0.36 | 0.30 | 0.22 | 3.13 | 0.20 | 0.22 | 0.19 | 0.36 (0.88) | 0.36 (0.93) | 0.36 (0.89) | 0.21 (0.52) |
| tasks with 4+ contacts per robot | 54 | 0.34 | 0.27 | 0.24 | 3.26 | 0.16 | 0.17 | 0.13 | 0.33 (0.87) | 0.33 (0.92) | 0.33 (0.88) | 0.17 (0.48) |

Learner columns: expected team payoff of the joint play over the last 100 rounds (and the share of runs whose most played pair is the optimum). All values here are read off the sweep itself, so the optimum is optimistic (the best of noisy cells); see the holdout table.

learned chooser (leave-one-object-out ridge regression on pair features), on the sweep: all tasks: 0.22; tasks with 4+ contacts per robot: 0.18

## how much the pair matters vs noise

Within a task, the true payoffs of different pairs spread by about 0.09 (sd), while one episode of the same pair varies by 0.14. With 4 episodes per pair a pair's estimate has reliability 0.63 (share of its variance that is real differences between pairs); 12 episodes: 0.84, 24 episodes: 0.91, 48 episodes: 0.95.

## choices scored on fresh placements (holdout)

| | sweep's optimum pair | learned chooser (unseen object) | spread rule | adjacent rule | random usable pair | regret matching's final pair | rm plus's final pair | hedge's final pair | exp3's final pair | holdout's own best (optimistic) |
|---|---|---|---|---|---|---|---|---|---|---|
| all tasks | 0.31 | 0.19 | 0.20 | 0.18 | 0.19 | 0.32 | 0.32 | 0.32 | 0.31 | 0.37 |
| tasks with 4+ contacts per robot | 0.31 | 0.17 | 0.16 | 0.15 | 0.16 | 0.31 | 0.31 | 0.31 | 0.30 | 0.37 |

## per task

| object | scenario | mass | contacts | optimum (pair) | pure NE | worst NE | random | spread | adjacent | regret matching | rm plus | hedge | exp3 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| arch | A_straight | 40 | 6 | 0.63 (part 3 corner -x+y + part 2 -x) | 4 | 0.56 | 0.33 | 0.34 | 0.34 | 0.58 | 0.62 | 0.60 | 0.41 |
| arch | A_straight | 80 | 6 | 0.40 (part 3 corner -x-y + part 2 corner -x+y) | 4 | 0.38 | 0.22 | 0.34 | 0.34 | 0.40 | 0.39 | 0.40 | 0.19 |
| arch | B_left | 40 | 8 | 0.57 (part 3 corner -x-y + part 2 corner -x-y) | 6 | 0.16 | 0.13 | 0.02 | 0.03 | 0.53 | 0.56 | 0.57 | 0.25 |
| arch | B_left | 80 | 8 | 0.70 (part 3 corner -x-y + part 2 corner -x-y) | 6 | 0.14 | 0.10 | 0.00 | 0.07 | 0.70 | 0.70 | 0.70 | 0.41 |
| arch | C_backright | 40 | 6 | 0.40 (part 2 +y + part 3 corner +x+y) | 2 | 0.40 | 0.17 | 0.00 | 0.00 | 0.40 | 0.40 | 0.40 | 0.19 |
| arch | C_backright | 80 | 6 | 0.39 (part 2 +y + part 3 corner +x+y) | 4 | 0.21 | 0.14 | 0.00 | 0.00 | 0.39 | 0.39 | 0.39 | 0.16 |
| arch | D_far_turn | 40 | 6 | 0.57 (part 3 -x + part 2 corner -x+y) | 4 | 0.39 | 0.26 | 0.23 | 0.23 | 0.57 | 0.57 | 0.57 | 0.37 |
| arch | D_far_turn | 80 | 6 | 0.31 (part 3 -x + part 2 corner -x+y) | 2 | 0.31 | 0.13 | 0.18 | 0.18 | 0.31 | 0.30 | 0.31 | 0.10 |
| asym | A_straight | 80 | 4 | 0.16 (part 1 corner -x-y + part 0 -x) | 4 | 0.12 | 0.12 |  |  | 0.15 | 0.16 | 0.16 | 0.05 |
| asym | B_left | 80 | 5 | 0.05 (part 1 corner -x-y + part 1 corner +x-y) | 4 | 0.01 | 0.01 |  |  | 0.05 | 0.05 | 0.03 | 0.01 |
| asym | C_backright | 80 | 4 | 0.04 (part 1 +x + part 0 +y) | 2 | 0.04 | 0.03 |  |  | 0.04 | 0.04 | 0.02 | 0.01 |
| asym | D_far_turn | 80 | 4 | 0.06 (part 0 corner -x+y + part 1 -x) | 2 | 0.06 | 0.03 |  |  | 0.06 | 0.06 | 0.04 | 0.01 |
| beam | A_straight | 80 | 7 | 0.17 (part 0 -x seg 2/5 + part 0 -x seg 4/5) | 4 | 0.12 | 0.07 | 0.11 | 0.05 | 0.14 | 0.15 | 0.17 | 0.04 |
| beam | B_left | 80 | 8 | 0.07 (part 0 -x seg 1/5 + part 0 -x seg 4/5) | 4 | 0.06 | 0.02 | 0.03 | 0.02 | 0.06 | 0.06 | 0.03 | 0.01 |
| beam | C_backright | 80 | 7 | 0.02 (part 0 +x seg 1/5 + part 0 +x seg 5/5) | 4 | 0.00 | 0.00 | 0.01 | 0.00 | 0.02 | 0.02 | 0.00 | 0.00 |
| beam | D_far_turn | 80 | 7 | 0.10 (part 0 -x seg 1/5 + part 0 -x seg 4/5) | 2 | 0.10 | 0.03 | 0.08 | 0.02 | 0.10 | 0.10 | 0.09 | 0.02 |
| cube | A_straight | 40 | 2 | 0.23 (part 0 corner -x+y + part 0 corner -x-y) | 2 | 0.23 | 0.23 |  |  | 0.23 | 0.23 | 0.23 | 0.12 |
| cube | B_left | 40 | 4 | 0.56 (part 0 -x + part 0 -y) | 2 | 0.56 | 0.36 |  |  | 0.56 | 0.56 | 0.56 | 0.46 |
| cube | C_backright | 40 | 2 | 0.83 (part 0 +x + part 0 +y) | 2 | 0.83 | 0.83 |  |  | 0.83 | 0.83 | 0.83 | 0.81 |
| cube | D_far_turn | 40 | 2 | 0.10 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.10 | 0.10 |  |  | 0.10 | 0.10 | 0.09 | 0.05 |
| cylinder | A_straight | 40 | 4 | 0.52 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.52 | 0.41 |  |  | 0.52 | 0.52 | 0.52 | 0.39 |
| cylinder | A_straight | 80 | 4 | 0.82 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.82 | 0.68 |  |  | 0.82 | 0.82 | 0.82 | 0.76 |
| cylinder | B_left | 40 | 5 | 0.30 (part 0 corner -x-y + part 0 corner +x-y) | 4 | 0.25 | 0.17 |  |  | 0.28 | 0.29 | 0.29 | 0.10 |
| cylinder | B_left | 80 | 5 | 0.25 (part 0 -x seg 1/2 + part 0 corner +x-y) | 4 | 0.25 | 0.16 |  |  | 0.25 | 0.25 | 0.25 | 0.09 |
| cylinder | C_backright | 40 | 4 | 0.12 (part 0 +x seg 1/2 + part 0 +y) | 2 | 0.12 | 0.04 |  |  | 0.12 | 0.12 | 0.12 | 0.03 |
| cylinder | C_backright | 80 | 4 | 0.08 (part 0 +x seg 2/2 + part 0 +y) | 4 | 0.02 | 0.03 |  |  | 0.07 | 0.08 | 0.06 | 0.01 |
| cylinder | D_far_turn | 40 | 4 | 0.01 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.01 | 0.01 |  |  | 0.01 | 0.01 | 0.00 | 0.00 |
| cylinder | D_far_turn | 80 | 4 | 0.00 (part 0 -x seg 1/2 + part 0 corner -x+y) | 6 | 0.00 | 0.00 |  |  | 0.00 | 0.00 | 0.00 | 0.00 |
| dumbbell | A_straight | 40 | 7 | 0.70 (part 1 corner -x-y + part 0 corner -x+y) | 2 | 0.70 | 0.21 | 0.36 | 0.11 | 0.70 | 0.70 | 0.70 | 0.52 |
| dumbbell | A_straight | 80 | 7 | 0.55 (part 1 -x + part 0 corner -x+y) | 2 | 0.55 | 0.17 | 0.51 | 0.02 | 0.55 | 0.55 | 0.55 | 0.32 |
| dumbbell | B_left | 40 | 8 | 0.65 (part 2 -x seg 2/3 + part 1 corner +x-y) | 4 | 0.30 | 0.15 | 0.01 | 0.21 | 0.58 | 0.64 | 0.65 | 0.31 |
| dumbbell | B_left | 80 | 8 | 0.37 (part 2 -x seg 2/3 + part 1 -y) | 4 | 0.31 | 0.09 | 0.00 | 0.27 | 0.33 | 0.33 | 0.31 | 0.08 |
| dumbbell | C_backright | 40 | 6 | 0.42 (part 0 +y + part 1 +x) | 4 | 0.37 | 0.19 | 0.00 | 0.00 | 0.40 | 0.41 | 0.42 | 0.16 |
| dumbbell | C_backright | 80 | 6 | 0.34 (part 1 corner +x+y + part 0 +y) | 6 | 0.21 | 0.15 | 0.03 | 0.03 | 0.33 | 0.33 | 0.33 | 0.11 |
| dumbbell | D_far_turn | 40 | 7 | 0.42 (part 1 corner -x-y + part 0 -x) | 4 | 0.33 | 0.18 | 0.19 | 0.15 | 0.38 | 0.40 | 0.42 | 0.14 |
| dumbbell | D_far_turn | 80 | 7 | 0.31 (part 1 -x + part 0 corner -x+y) | 4 | 0.22 | 0.11 | 0.07 | 0.07 | 0.29 | 0.29 | 0.31 | 0.08 |
| l_shape | A_straight | 80 | 6 | 0.25 (part 0 corner -x-y + part 1 -x) | 4 | 0.04 | 0.09 | 0.05 | 0.16 | 0.25 | 0.25 | 0.25 | 0.06 |
| l_shape | B_left | 80 | 7 | 0.12 (part 1 corner +x-y + part 1 -x) | 2 | 0.12 | 0.04 |  |  | 0.12 | 0.12 | 0.12 | 0.03 |
| l_shape | C_backright | 80 | 6 | 0.31 (part 1 corner +x+y + part 1 +y seg 1/2) | 2 | 0.31 | 0.14 |  |  | 0.31 | 0.30 | 0.30 | 0.11 |
| l_shape | D_far_turn | 80 | 6 | 0.15 (part 0 corner -x-y + part 1 corner -x+y) | 2 | 0.15 | 0.10 | 0.15 | 0.09 | 0.15 | 0.15 | 0.15 | 0.04 |
| long | A_straight | 40 | 4 | 0.45 (part 0 -x seg 1/2 + part 0 corner -x+y) | 2 | 0.45 | 0.36 | 0.37 | 0.45 | 0.45 | 0.45 | 0.45 | 0.31 |
| long | B_left | 40 | 5 | 0.51 (part 0 corner +x-y + part 0 -x seg 2/2) | 2 | 0.51 | 0.17 | 0.38 | 0.05 | 0.51 | 0.50 | 0.51 | 0.32 |
| long | C_backright | 40 | 4 | 0.36 (part 0 +x seg 1/2 + part 0 +y) | 2 | 0.36 | 0.26 | 0.36 | 0.08 | 0.36 | 0.36 | 0.36 | 0.20 |
| long | D_far_turn | 40 | 4 | 0.33 (part 0 corner -x-y + part 0 -x seg 2/2) | 4 | 0.25 | 0.24 | 0.14 | 0.25 | 0.31 | 0.31 | 0.33 | 0.12 |
| plus | A_straight | 80 | 5 | 0.34 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.34 | 0.16 |  |  | 0.34 | 0.33 | 0.34 | 0.13 |
| plus | B_left | 80 | 6 | 0.42 (part 1 corner -x-y + part 0 corner +x-y) | 4 | 0.24 | 0.18 |  |  | 0.38 | 0.41 | 0.42 | 0.15 |
| plus | C_backright | 80 | 4 | 0.38 (part 1 corner +x+y + part 0 +y) | 4 | 0.24 | 0.28 |  |  | 0.35 | 0.38 | 0.38 | 0.17 |
| plus | D_far_turn | 80 | 5 | 0.17 (part 1 corner -x-y + part 0 corner -x+y) | 2 | 0.17 | 0.10 |  |  | 0.17 | 0.17 | 0.17 | 0.06 |
| sphere | A_straight | 40 | 2 | 0.99 (sector 225 + sector 135) | 2 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.99 | 0.97 |
| sphere | B_left | 40 | 4 | 0.59 (sector 315 + sector 180) | 2 | 0.59 | 0.48 | 0.41 | 0.41 | 0.59 | 0.59 | 0.59 | 0.50 |
| sphere | C_backright | 40 | 2 | 0.72 (sector 90 + sector 0) | 2 | 0.72 | 0.72 | 0.72 | 0.72 | 0.72 | 0.72 | 0.72 | 0.69 |
| sphere | D_far_turn | 40 | 2 | 0.73 (sector 225 + sector 135) | 2 | 0.73 | 0.73 | 0.73 | 0.73 | 0.73 | 0.73 | 0.73 | 0.72 |
| t_shape | A_straight | 80 | 5 | 0.41 (part 0 -x seg 1/3 + part 0 corner -x+y) | 2 | 0.41 | 0.22 |  |  | 0.41 | 0.41 | 0.41 | 0.20 |
| t_shape | B_left | 80 | 8 | 0.25 (part 1 -y seg 2/2 + part 0 -x seg 3/3) | 6 | 0.11 | 0.07 | 0.00 | 0.00 | 0.24 | 0.25 | 0.25 | 0.06 |
| t_shape | C_backright | 80 | 5 | 0.30 (part 1 corner +x+y + part 0 +y) | 2 | 0.30 | 0.11 | 0.21 | 0.21 | 0.30 | 0.30 | 0.30 | 0.12 |
| t_shape | D_far_turn | 80 | 5 | 0.21 (part 0 -x seg 1/3 + part 0 corner -x+y) | 4 | 0.09 | 0.06 |  |  | 0.18 | 0.21 | 0.21 | 0.04 |
| u_channel | A_straight | 80 | 5 | 0.48 (part 0 corner -x-y + part 0 corner -x+y) | 4 | 0.36 | 0.24 | 0.36 | 0.36 | 0.46 | 0.47 | 0.48 | 0.26 |
| u_channel | B_left | 80 | 9 | 0.28 (part 2 -y seg 2/2 + part 0 -x seg 2/3) | 4 | 0.14 | 0.08 | 0.01 | 0.04 | 0.28 | 0.27 | 0.28 | 0.07 |
| u_channel | C_backright | 80 | 7 | 0.65 (part 2 corner +x+y + part 0 +y) | 2 | 0.65 | 0.12 | 0.65 | 0.00 | 0.65 | 0.65 | 0.65 | 0.44 |
| u_channel | D_far_turn | 80 | 5 | 0.23 (part 0 corner -x-y + part 0 corner -x+y) | 2 | 0.23 | 0.09 | 0.02 | 0.02 | 0.23 | 0.23 | 0.23 | 0.08 |
