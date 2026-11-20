# ANYmal MAPPO pair (nwB_mappo_uniform_s0, iteration 5000): evaluation metrics

12 objects x 4 start positions x 4 masses x 10 trials = 1920 episodes (seed 7100; each trial a different random placement of the same task).

Positions (goal relative to the start, robots behind the object): `A_straight` 3 m straight ahead; `B_left` 3 m at 60 deg left, turn 30 deg; `C_backright` 3 m back-right (-135 deg), turn -60 deg; `D_far_turn` 5 m ahead, turn 90 deg.

Success = within 10 cm and 6 deg of the goal, held 1 s, within 80 s. Time = seconds to success, averaged over the successful trials (n in brackets). Fell = a robot fell. Final error = where the object ended (failed trials included). Per-case rows (mass x object x position, 10 trials each): `metrics_by_case.csv`; every episode: `episodes.csv`.

## By mass

| mass | success | precise | mean time (s) | median time (s) | fell | timeout | final error (m / deg) |
|---|---|---|---|---|---|---|---|
| 20 kg | 90% | 85% | 20.8 (n 433) | 17.5 | 4% | 6% | 0.12 / 5 |
| 40 kg | 78% | 71% | 24.9 (n 375) | 20.0 | 11% | 11% | 0.25 / 9 |
| 60 kg | 53% | 45% | 34.7 (n 255) | 30.6 | 22% | 25% | 0.67 / 18 |
| 80 kg | 24% | 20% | 36.0 (n 115) | 31.6 | 27% | 49% | 1.35 / 29 |

## 20 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 100% | 13.2 (n 40) | 0% | 0.05 / 1 | 10/10, 8 s | 10/10, 14 s | 10/10, 15 s | 10/10, 16 s |
| long | 100% | 16.8 (n 40) | 0% | 0.06 / 1 | 10/10, 16 s | 10/10, 14 s | 10/10, 20 s | 10/10, 18 s |
| sphere | 95% | 22.5 (n 38) | 0% | 0.07 / 0 | 10/10, 24 s | 10/10, 21 s | 8/10, 19 s | 10/10, 25 s |
| cylinder | 65% | 17.9 (n 26) | 8% | 0.16 / 16 | 9/10, 13 s | 8/10, 19 s | 9/10, 21 s | 0/10 |
| arch | 72% | 32.9 (n 29) | 12% | 0.40 / 13 | 6/10, 39 s | 5/10, 34 s | 9/10, 25 s | 9/10, 36 s |
| dumbbell | 100% | 21.0 (n 40) | 0% | 0.06 / 2 | 10/10, 17 s | 10/10, 19 s | 10/10, 18 s | 10/10, 31 s |
| t_shape | 98% | 17.2 (n 39) | 2% | 0.09 / 2 | 10/10, 14 s | 10/10, 25 s | 9/10, 12 s | 10/10, 18 s |
| beam | 78% | 32.9 (n 31) | 8% | 0.12 / 15 | 8/10, 27 s | 8/10, 35 s | 5/10, 34 s | 10/10, 35 s |
| l_shape | 95% | 16.2 (n 38) | 2% | 0.13 / 3 | 10/10, 10 s | 10/10, 15 s | 9/10, 15 s | 9/10, 25 s |
| asym | 92% | 16.3 (n 37) | 5% | 0.05 / 3 | 10/10, 12 s | 10/10, 10 s | 8/10, 26 s | 9/10, 19 s |
| u_channel | 100% | 19.8 (n 40) | 0% | 0.06 / 2 | 10/10, 9 s | 10/10, 20 s | 10/10, 27 s | 10/10, 24 s |
| plus | 88% | 28.1 (n 35) | 12% | 0.23 / 4 | 10/10, 16 s | 8/10, 27 s | 7/10, 47 s | 10/10, 29 s |

## 40 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 92% | 20.3 (n 37) | 0% | 0.14 / 3 | 9/10, 13 s | 10/10, 17 s | 9/10, 22 s | 9/10, 29 s |
| long | 100% | 21.5 (n 40) | 0% | 0.05 / 1 | 10/10, 15 s | 10/10, 15 s | 10/10, 29 s | 10/10, 27 s |
| sphere | 92% | 17.6 (n 37) | 5% | 0.11 / 0 | 9/10, 12 s | 9/10, 16 s | 9/10, 21 s | 10/10, 21 s |
| cylinder | 50% | 16.5 (n 20) | 20% | 0.40 / 24 | 9/10, 9 s | 6/10, 22 s | 5/10, 23 s | 0/10 |
| arch | 57% | 44.2 (n 23) | 22% | 0.65 / 25 | 5/10, 43 s | 4/10, 50 s | 10/10, 35 s | 4/10, 62 s |
| dumbbell | 65% | 23.6 (n 26) | 22% | 0.31 / 13 | 9/10, 16 s | 6/10, 29 s | 5/10, 21 s | 6/10, 33 s |
| t_shape | 95% | 19.8 (n 38) | 2% | 0.06 / 2 | 10/10, 18 s | 9/10, 17 s | 10/10, 21 s | 9/10, 23 s |
| beam | 52% | 42.5 (n 21) | 25% | 0.37 / 14 | 6/10, 31 s | 6/10, 41 s | 3/10, 68 s | 6/10, 43 s |
| l_shape | 95% | 21.1 (n 38) | 5% | 0.13 / 3 | 10/10, 15 s | 9/10, 20 s | 9/10, 17 s | 10/10, 32 s |
| asym | 65% | 27.9 (n 26) | 5% | 0.26 / 15 | 9/10, 30 s | 10/10, 15 s | 5/10, 41 s | 2/10, 49 s |
| u_channel | 92% | 24.6 (n 37) | 5% | 0.15 / 5 | 10/10, 19 s | 10/10, 19 s | 8/10, 28 s | 9/10, 34 s |
| plus | 80% | 32.6 (n 32) | 15% | 0.32 / 4 | 9/10, 14 s | 7/10, 18 s | 8/10, 57 s | 8/10, 43 s |

## 60 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 57% | 41.0 (n 23) | 12% | 0.69 / 12 | 5/10, 33 s | 6/10, 39 s | 8/10, 43 s | 4/10, 49 s |
| long | 75% | 33.1 (n 30) | 5% | 0.30 / 10 | 10/10, 26 s | 7/10, 28 s | 7/10, 48 s | 6/10, 34 s |
| sphere | 92% | 14.8 (n 37) | 5% | 0.08 / 0 | 9/10, 14 s | 10/10, 12 s | 8/10, 18 s | 10/10, 17 s |
| cylinder | 35% | 20.7 (n 14) | 38% | 0.61 / 33 | 9/10, 10 s | 3/10, 30 s | 2/10, 55 s | 0/10 |
| arch | 18% | 52.0 (n 7) | 42% | 1.64 / 37 | 3/10, 64 s | 0/10 | 4/10, 43 s | 0/10 |
| dumbbell | 52% | 29.3 (n 21) | 28% | 0.63 / 19 | 7/10, 24 s | 5/10, 34 s | 3/10, 34 s | 6/10, 29 s |
| t_shape | 78% | 41.5 (n 31) | 12% | 0.23 / 7 | 9/10, 33 s | 7/10, 39 s | 8/10, 52 s | 7/10, 43 s |
| beam | 15% | 33.3 (n 6) | 50% | 1.42 / 31 | 1/10, 42 s | 0/10 | 0/10 | 5/10, 32 s |
| l_shape | 78% | 39.0 (n 31) | 12% | 0.20 / 9 | 8/10, 31 s | 7/10, 42 s | 8/10, 33 s | 8/10, 50 s |
| asym | 32% | 50.6 (n 13) | 18% | 1.22 / 38 | 3/10, 67 s | 8/10, 39 s | 2/10, 73 s | 0/10 |
| u_channel | 57% | 44.8 (n 23) | 12% | 0.15 / 15 | 9/10, 48 s | 7/10, 32 s | 5/10, 52 s | 2/10, 55 s |
| plus | 48% | 37.9 (n 19) | 28% | 0.87 / 11 | 8/10, 29 s | 5/10, 34 s | 2/10, 50 s | 4/10, 55 s |

## 80 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 12% | 48.0 (n 5) | 25% | 2.00 / 25 | 2/10, 36 s | 2/10, 48 s | 1/10, 72 s | 0/10 |
| long | 42% | 50.0 (n 17) | 12% | 0.72 / 26 | 6/10, 39 s | 5/10, 63 s | 3/10, 61 s | 3/10, 40 s |
| sphere | 95% | 13.9 (n 38) | 5% | 0.17 / 0 | 9/10, 11 s | 10/10, 11 s | 10/10, 19 s | 9/10, 15 s |
| cylinder | 28% | 19.3 (n 11) | 42% | 0.90 / 39 | 9/10, 10 s | 2/10, 59 s | 0/10 | 0/10 |
| arch | 2% | 68.5 (n 1) | 40% | 2.13 / 39 | 0/10 | 0/10 | 1/10, 68 s | 0/10 |
| dumbbell | 15% | 56.6 (n 6) | 42% | 1.46 / 34 | 3/10, 44 s | 2/10, 72 s | 1/10, 62 s | 0/10 |
| t_shape | 20% | 56.2 (n 8) | 10% | 0.99 / 24 | 3/10, 58 s | 1/10, 44 s | 1/10, 59 s | 3/10, 58 s |
| beam | 0% | – (n 0) | 80% | 2.89 / 41 | 0/10 | 0/10 | 0/10 | 0/10 |
| l_shape | 28% | 56.2 (n 11) | 18% | 0.83 / 27 | 5/10, 59 s | 2/10, 63 s | 2/10, 31 s | 2/10, 68 s |
| asym | 2% | 70.9 (n 1) | 10% | 1.96 / 41 | 0/10 | 1/10, 71 s | 0/10 | 0/10 |
| u_channel | 15% | 44.3 (n 6) | 10% | 0.89 / 31 | 1/10, 66 s | 3/10, 38 s | 2/10, 44 s | 0/10 |
| plus | 28% | 45.0 (n 11) | 28% | 1.19 / 17 | 4/10, 35 s | 2/10, 32 s | 1/10, 49 s | 4/10, 61 s |

## Notes: positions with failures

Per mass and object, each start position that failed at least once: failed / trials, how, and the closest any failed trial got.

**20 kg**

- sphere: `C_backright` 2/10 failed (2 timeout; closest stop 0.15 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.59 m / 2 deg); `B_left` 2/10 failed (2 fell anymal2; closest stop 1.45 m / 9 deg); `C_backright` 1/10 failed (1 timeout; closest stop 0.09 m / 67 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.04 m / 77 deg)
- arch: `A_straight` 4/10 failed (2 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.08 m / 0 deg); `B_left` 5/10 failed (3 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.24 m / 38 deg); `C_backright` 1/10 failed (1 fell anymal2; closest stop 2.53 m / 72 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 2.45 m / 23 deg)
- t_shape: `C_backright` 1/10 failed (1 fell anymal2; closest stop 1.27 m / 18 deg)
- beam: `A_straight` 2/10 failed (1 fell anymal2, 1 timeout; closest stop 0.17 m / 52 deg); `B_left` 2/10 failed (2 fell anymal1; closest stop 0.28 m / 68 deg); `C_backright` 5/10 failed (5 timeout; closest stop 0.19 m / 64 deg)
- l_shape: `C_backright` 1/10 failed (1 fell anymal2; closest stop 2.88 m / 44 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.08 m / 1 deg)
- asym: `C_backright` 2/10 failed (2 fell anymal2; closest stop 0.09 m / 12 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.27 m / 70 deg)
- plus: `B_left` 2/10 failed (1 fell anymal1, 1 fell anymal2; closest stop 0.33 m / 2 deg); `C_backright` 3/10 failed (2 fell anymal1, 1 fell anymal2; closest stop 0.47 m / 16 deg)

**40 kg**

- cube: `A_straight` 1/10 failed (1 timeout; closest stop 1.34 m / 0 deg); `C_backright` 1/10 failed (1 timeout; closest stop 1.37 m / 17 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.53 m / 41 deg)
- sphere: `A_straight` 1/10 failed (1 fell anymal1; closest stop 1.76 m / 0 deg); `B_left` 1/10 failed (1 timeout; closest stop 0.13 m / 0 deg); `C_backright` 1/10 failed (1 fell anymal2; closest stop 0.31 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.31 m / 0 deg); `B_left` 4/10 failed (3 fell anymal2, 1 fell anymal1; closest stop 2.30 m / 6 deg); `C_backright` 5/10 failed (3 timeout, 2 fell anymal2; closest stop 0.03 m / 5 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal2; closest stop 0.07 m / 63 deg)
- arch: `A_straight` 5/10 failed (3 timeout, 2 fell anymal2; closest stop 0.06 m / 58 deg); `B_left` 6/10 failed (2 fell anymal2, 2 timeout, 2 fell anymal1; closest stop 0.08 m / 65 deg); `D_far_turn` 6/10 failed (3 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.16 m / 69 deg)
- dumbbell: `A_straight` 1/10 failed (1 fell anymal1; closest stop 0.16 m / 12 deg); `B_left` 4/10 failed (2 fell anymal1, 2 timeout; closest stop 0.39 m / 4 deg); `C_backright` 5/10 failed (2 fell anymal1, 2 timeout, 1 fell anymal2; closest stop 0.12 m / 34 deg); `D_far_turn` 4/10 failed (2 fell anymal2, 1 fell anymal1, 1 timeout; closest stop 0.07 m / 29 deg)
- t_shape: `B_left` 1/10 failed (1 fell anymal1; closest stop 0.24 m / 5 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.13 m / 0 deg)
- beam: `A_straight` 4/10 failed (3 fell anymal2, 1 fell anymal1; closest stop 0.14 m / 2 deg); `B_left` 4/10 failed (2 timeout, 2 fell anymal2; closest stop 0.22 m / 58 deg); `C_backright` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.08 m / 0 deg); `D_far_turn` 4/10 failed (2 fell anymal2, 1 timeout, 1 fell anymal1; closest stop 0.12 m / 1 deg)
- l_shape: `B_left` 1/10 failed (1 fell anymal1; closest stop 0.12 m / 2 deg); `C_backright` 1/10 failed (1 fell anymal2; closest stop 2.95 m / 52 deg)
- asym: `A_straight` 1/10 failed (1 timeout; closest stop 0.44 m / 20 deg); `C_backright` 5/10 failed (5 timeout; closest stop 0.44 m / 12 deg); `D_far_turn` 8/10 failed (6 timeout, 2 fell anymal2; closest stop 0.25 m / 68 deg)
- u_channel: `C_backright` 2/10 failed (1 fell anymal1, 1 fell anymal2; closest stop 0.43 m / 13 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.25 m / 50 deg)
- plus: `A_straight` 1/10 failed (1 fell anymal2; closest stop 1.61 m / 1 deg); `B_left` 3/10 failed (3 fell anymal2; closest stop 0.41 m / 10 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.09 m / 1 deg); `D_far_turn` 2/10 failed (1 fell anymal2, 1 fell anymal1; closest stop 0.74 m / 43 deg)

**60 kg**

- cube: `A_straight` 5/10 failed (4 timeout, 1 fell anymal1; closest stop 0.15 m / 3 deg); `B_left` 4/10 failed (4 fell anymal1; closest stop 1.71 m / 23 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.37 m / 13 deg); `D_far_turn` 6/10 failed (6 timeout; closest stop 0.62 m / 34 deg)
- long: `B_left` 3/10 failed (3 timeout; closest stop 0.73 m / 13 deg); `C_backright` 3/10 failed (2 timeout, 1 fell anymal2; closest stop 0.18 m / 4 deg); `D_far_turn` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.23 m / 52 deg)
- sphere: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.16 m / 0 deg); `C_backright` 2/10 failed (1 fell anymal2, 1 timeout; closest stop 0.53 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.04 m / 1 deg); `B_left` 7/10 failed (3 fell anymal2, 3 fell anymal1, 1 timeout; closest stop 0.43 m / 5 deg); `C_backright` 8/10 failed (4 timeout, 2 fell anymal2, 2 fell anymal1; closest stop 0.17 m / 74 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal2; closest stop 0.10 m / 70 deg)
- arch: `A_straight` 7/10 failed (3 fell anymal2, 3 timeout, 1 fell anymal1; closest stop 0.07 m / 72 deg); `B_left` 10/10 failed (4 fell anymal2, 3 fell anymal1, 3 timeout; closest stop 0.19 m / 53 deg); `C_backright` 6/10 failed (4 timeout, 2 fell anymal1; closest stop 0.09 m / 0 deg); `D_far_turn` 10/10 failed (6 timeout, 3 fell anymal2, 1 fell anymal1; closest stop 0.06 m / 60 deg)
- dumbbell: `A_straight` 3/10 failed (2 fell anymal1, 1 fell anymal2; closest stop 0.13 m / 4 deg); `B_left` 5/10 failed (2 fell anymal2, 2 timeout, 1 fell anymal1; closest stop 0.20 m / 39 deg); `C_backright` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.13 m / 11 deg); `D_far_turn` 4/10 failed (4 fell anymal2; closest stop 0.21 m / 14 deg)
- t_shape: `A_straight` 1/10 failed (1 fell anymal1; closest stop 2.90 m / 4 deg); `B_left` 3/10 failed (2 fell anymal2, 1 timeout; closest stop 0.33 m / 2 deg); `C_backright` 2/10 failed (1 fell anymal1, 1 timeout; closest stop 0.31 m / 1 deg); `D_far_turn` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.13 m / 0 deg)
- beam: `A_straight` 9/10 failed (5 fell anymal2, 2 fell anymal1, 2 timeout; closest stop 0.03 m / 34 deg); `B_left` 10/10 failed (5 timeout, 4 fell anymal2, 1 fell anymal1; closest stop 0.31 m / 12 deg); `C_backright` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.24 m / 70 deg); `D_far_turn` 5/10 failed (4 fell anymal2, 1 timeout; closest stop 0.17 m / 2 deg)
- l_shape: `A_straight` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.83 m / 12 deg); `B_left` 3/10 failed (2 fell anymal1, 1 timeout; closest stop 0.09 m / 69 deg); `C_backright` 2/10 failed (2 fell anymal1; closest stop 1.58 m / 12 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.20 m / 41 deg)
- asym: `A_straight` 7/10 failed (5 timeout, 2 fell anymal1; closest stop 0.22 m / 1 deg); `B_left` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.18 m / 0 deg); `C_backright` 8/10 failed (5 timeout, 2 fell anymal1, 1 fell anymal2; closest stop 1.50 m / 66 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.93 m / 78 deg)
- u_channel: `A_straight` 1/10 failed (1 fell anymal1; closest stop 0.44 m / 7 deg); `B_left` 3/10 failed (2 timeout, 1 fell anymal2; closest stop 0.14 m / 1 deg); `C_backright` 5/10 failed (3 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.10 m / 2 deg); `D_far_turn` 8/10 failed (7 timeout, 1 fell anymal1; closest stop 0.04 m / 39 deg)
- plus: `A_straight` 2/10 failed (1 timeout, 1 fell anymal2; closest stop 0.78 m / 22 deg); `B_left` 5/10 failed (3 fell anymal1, 1 timeout, 1 fell anymal2; closest stop 0.97 m / 7 deg); `C_backright` 8/10 failed (5 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.15 m / 0 deg); `D_far_turn` 6/10 failed (3 timeout, 3 fell anymal2; closest stop 0.22 m / 4 deg)

**80 kg**

- cube: `A_straight` 8/10 failed (8 timeout; closest stop 0.45 m / 7 deg); `B_left` 8/10 failed (4 timeout, 3 fell anymal1, 1 fell anymal2; closest stop 0.46 m / 11 deg); `C_backright` 9/10 failed (3 timeout, 3 fell anymal1, 3 fell anymal2; closest stop 1.38 m / 21 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 2.37 m / 44 deg)
- long: `A_straight` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.10 m / 2 deg); `B_left` 5/10 failed (3 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.44 m / 8 deg); `C_backright` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.27 m / 33 deg); `D_far_turn` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.10 m / 52 deg)
- sphere: `A_straight` 1/10 failed (1 fell anymal2; closest stop 1.45 m / 0 deg); `D_far_turn` 1/10 failed (1 fell anymal2; closest stop 3.41 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.38 m / 0 deg); `B_left` 8/10 failed (4 fell anymal1, 3 timeout, 1 fell anymal2; closest stop 0.96 m / 10 deg); `C_backright` 10/10 failed (6 fell anymal1, 3 timeout, 1 fell anymal2; closest stop 0.78 m / 79 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal2; closest stop 0.05 m / 74 deg)
- arch: `A_straight` 10/10 failed (5 timeout, 3 fell anymal2, 2 fell anymal1; closest stop 0.15 m / 67 deg); `B_left` 10/10 failed (6 fell anymal2, 4 timeout; closest stop 0.34 m / 80 deg); `C_backright` 9/10 failed (8 timeout, 1 fell anymal2; closest stop 0.28 m / 1 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal2; closest stop 2.82 m / 2 deg)
- dumbbell: `A_straight` 7/10 failed (4 fell anymal2, 2 timeout, 1 fell anymal1; closest stop 0.21 m / 2 deg); `B_left` 8/10 failed (3 timeout, 3 fell anymal2, 2 fell anymal1; closest stop 0.27 m / 4 deg); `C_backright` 9/10 failed (6 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.12 m / 32 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.11 m / 4 deg)
- t_shape: `A_straight` 7/10 failed (7 timeout; closest stop 0.07 m / 1 deg); `B_left` 9/10 failed (8 timeout, 1 fell anymal1; closest stop 0.60 m / 19 deg); `C_backright` 9/10 failed (6 timeout, 3 fell anymal1; closest stop 0.55 m / 10 deg); `D_far_turn` 7/10 failed (7 timeout; closest stop 0.09 m / 56 deg)
- beam: `A_straight` 10/10 failed (8 fell anymal2, 2 timeout; closest stop 2.13 m / 0 deg); `B_left` 10/10 failed (6 fell anymal2, 4 fell anymal1; closest stop 2.02 m / 6 deg); `C_backright` 10/10 failed (6 fell anymal1, 3 timeout, 1 fell anymal2; closest stop 0.61 m / 73 deg); `D_far_turn` 10/10 failed (4 fell anymal2, 3 fell anymal1, 3 timeout; closest stop 0.92 m / 32 deg)
- l_shape: `A_straight` 5/10 failed (5 timeout; closest stop 0.13 m / 6 deg); `B_left` 8/10 failed (5 timeout, 3 fell anymal1; closest stop 0.07 m / 65 deg); `C_backright` 8/10 failed (5 timeout, 3 fell anymal1; closest stop 0.57 m / 9 deg); `D_far_turn` 8/10 failed (7 timeout, 1 fell anymal1; closest stop 0.12 m / 8 deg)
- asym: `A_straight` 10/10 failed (10 timeout; closest stop 1.11 m / 7 deg); `B_left` 9/10 failed (8 timeout, 1 fell anymal1; closest stop 0.12 m / 2 deg); `C_backright` 10/10 failed (7 timeout, 2 fell anymal1, 1 fell anymal2; closest stop 0.67 m / 27 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 3.28 m / 88 deg)
- u_channel: `A_straight` 9/10 failed (9 timeout; closest stop 0.09 m / 8 deg); `B_left` 7/10 failed (5 timeout, 2 fell anymal1; closest stop 0.07 m / 9 deg); `C_backright` 8/10 failed (7 timeout, 1 fell anymal2; closest stop 0.47 m / 13 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.10 m / 87 deg)
- plus: `A_straight` 6/10 failed (4 timeout, 2 fell anymal1; closest stop 0.18 m / 2 deg); `B_left` 8/10 failed (6 timeout, 2 fell anymal2; closest stop 0.16 m / 21 deg); `C_backright` 9/10 failed (6 timeout, 3 fell anymal2; closest stop 0.19 m / 14 deg); `D_far_turn` 6/10 failed (3 fell anymal1, 2 timeout, 1 fell anymal2; closest stop 1.58 m / 30 deg)

