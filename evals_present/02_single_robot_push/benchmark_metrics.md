# ANYmal single-robot pusher (s2b-anymal-term80): evaluation metrics

12 objects x 4 start positions x 4 masses x 10 trials = 1920 episodes (seed 7100; each trial a different random placement of the same task).

Positions (goal relative to the start, robots behind the object): `A_straight` 3 m straight ahead; `B_left` 3 m at 60 deg left, turn 30 deg; `C_backright` 3 m back-right (-135 deg), turn -60 deg; `D_far_turn` 5 m ahead, turn 90 deg.

Success = within 10 cm and 6 deg of the goal, held 1 s, within 80 s. Time = seconds to success, averaged over the successful trials (n in brackets). Fell = a robot fell. Final error = where the object ended (failed trials included). Per-case rows (mass x object x position, 10 trials each): `metrics_by_case.csv`; every episode: `episodes.csv`.

## By mass

| mass | success | precise | mean time (s) | median time (s) | fell | timeout | final error (m / deg) |
|---|---|---|---|---|---|---|---|
| 20 kg | 89% | 83% | 18.6 (n 427) | 14.9 | 1% | 10% | 0.08 / 6 |
| 40 kg | 64% | 56% | 30.8 (n 309) | 25.6 | 6% | 29% | 0.42 / 14 |
| 60 kg | 25% | 23% | 37.9 (n 121) | 38.8 | 15% | 60% | 1.40 / 27 |
| 80 kg | 11% | 11% | 19.0 (n 52) | 12.8 | 16% | 74% | 2.29 / 33 |

## 20 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 100% | 11.1 (n 40) | 0% | 0.05 / 1 | 10/10, 8 s | 10/10, 11 s | 10/10, 12 s | 10/10, 13 s |
| long | 100% | 16.3 (n 40) | 0% | 0.05 / 1 | 10/10, 9 s | 10/10, 16 s | 10/10, 19 s | 10/10, 22 s |
| sphere | 100% | 9.7 (n 40) | 0% | 0.05 / 0 | 10/10, 8 s | 10/10, 10 s | 10/10, 10 s | 10/10, 10 s |
| cylinder | 60% | 18.9 (n 24) | 2% | 0.07 / 24 | 10/10, 12 s | 10/10, 15 s | 4/10, 46 s | 0/10 |
| arch | 57% | 30.9 (n 23) | 0% | 0.15 / 24 | 1/10, 58 s | 9/10, 37 s | 10/10, 20 s | 3/10, 39 s |
| dumbbell | 95% | 15.8 (n 38) | 5% | 0.07 / 4 | 10/10, 9 s | 9/10, 18 s | 10/10, 18 s | 9/10, 19 s |
| t_shape | 100% | 15.7 (n 40) | 0% | 0.05 / 2 | 10/10, 10 s | 10/10, 16 s | 10/10, 11 s | 10/10, 26 s |
| beam | 80% | 27.1 (n 32) | 0% | 0.11 / 11 | 10/10, 18 s | 9/10, 39 s | 3/10, 56 s | 10/10, 17 s |
| l_shape | 100% | 16.5 (n 40) | 0% | 0.06 / 2 | 10/10, 10 s | 10/10, 16 s | 10/10, 11 s | 10/10, 29 s |
| asym | 98% | 18.0 (n 39) | 0% | 0.09 / 1 | 9/10, 16 s | 10/10, 16 s | 10/10, 19 s | 10/10, 21 s |
| u_channel | 100% | 18.1 (n 40) | 0% | 0.05 / 2 | 10/10, 10 s | 10/10, 23 s | 10/10, 15 s | 10/10, 24 s |
| plus | 78% | 35.7 (n 31) | 2% | 0.19 / 3 | 9/10, 27 s | 9/10, 39 s | 6/10, 39 s | 7/10, 41 s |

## 40 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 98% | 22.3 (n 39) | 0% | 0.09 / 2 | 10/10, 20 s | 10/10, 22 s | 10/10, 19 s | 9/10, 29 s |
| long | 90% | 31.7 (n 36) | 0% | 0.12 / 6 | 10/10, 38 s | 9/10, 27 s | 10/10, 32 s | 7/10, 27 s |
| sphere | 100% | 10.3 (n 40) | 0% | 0.04 / 0 | 10/10, 9 s | 10/10, 11 s | 10/10, 9 s | 10/10, 12 s |
| cylinder | 65% | 25.2 (n 26) | 5% | 0.11 / 18 | 8/10, 11 s | 10/10, 24 s | 8/10, 41 s | 0/10 |
| arch | 38% | 41.5 (n 15) | 0% | 0.26 / 26 | 0/10 | 3/10, 64 s | 10/10, 31 s | 2/10, 58 s |
| dumbbell | 48% | 29.3 (n 19) | 10% | 0.51 / 19 | 9/10, 22 s | 1/10, 31 s | 7/10, 39 s | 2/10, 30 s |
| t_shape | 85% | 35.1 (n 34) | 5% | 0.17 / 8 | 10/10, 36 s | 8/10, 37 s | 9/10, 22 s | 7/10, 49 s |
| beam | 28% | 46.8 (n 11) | 22% | 0.94 / 31 | 5/10, 45 s | 4/10, 50 s | 0/10 | 2/10, 45 s |
| l_shape | 82% | 33.8 (n 33) | 0% | 0.18 / 6 | 9/10, 31 s | 10/10, 34 s | 8/10, 22 s | 6/10, 53 s |
| asym | 12% | 72.2 (n 5) | 20% | 1.27 / 29 | 1/10, 80 s | 4/10, 70 s | 0/10 | 0/10 |
| u_channel | 80% | 36.8 (n 32) | 5% | 0.18 / 8 | 10/10, 24 s | 6/10, 54 s | 8/10, 28 s | 8/10, 49 s |
| plus | 48% | 46.8 (n 19) | 10% | 1.20 / 13 | 8/10, 53 s | 5/10, 40 s | 6/10, 44 s | 0/10 |

## 60 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 55% | 53.2 (n 22) | 5% | 0.74 / 12 | 5/10, 46 s | 6/10, 59 s | 8/10, 50 s | 3/10, 62 s |
| long | 25% | 59.2 (n 10) | 2% | 1.22 / 31 | 2/10, 62 s | 4/10, 68 s | 4/10, 49 s | 0/10 |
| sphere | 98% | 11.5 (n 39) | 2% | 0.06 / 0 | 10/10, 10 s | 9/10, 12 s | 10/10, 10 s | 10/10, 14 s |
| cylinder | 38% | 31.4 (n 15) | 8% | 0.30 / 32 | 8/10, 11 s | 6/10, 55 s | 1/10, 53 s | 0/10 |
| arch | 18% | 48.9 (n 7) | 5% | 1.05 / 25 | 1/10, 62 s | 0/10 | 6/10, 47 s | 0/10 |
| dumbbell | 10% | 65.4 (n 4) | 38% | 2.00 / 36 | 2/10, 74 s | 0/10 | 1/10, 52 s | 1/10, 63 s |
| t_shape | 20% | 49.3 (n 8) | 10% | 1.19 / 32 | 2/10, 63 s | 1/10, 54 s | 5/10, 43 s | 0/10 |
| beam | 0% | – (n 0) | 42% | 3.01 / 43 | 0/10 | 0/10 | 0/10 | 0/10 |
| l_shape | 25% | 56.7 (n 10) | 10% | 1.26 / 21 | 3/10, 65 s | 3/10, 63 s | 4/10, 46 s | 0/10 |
| asym | 0% | – (n 0) | 20% | 2.66 / 39 | 0/10 | 0/10 | 0/10 | 0/10 |
| u_channel | 5% | 59.9 (n 2) | 15% | 1.42 / 29 | 0/10 | 0/10 | 2/10, 60 s | 0/10 |
| plus | 10% | 55.7 (n 4) | 18% | 1.96 / 23 | 0/10 | 1/10, 58 s | 3/10, 55 s | 0/10 |

## 80 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 5% | 78.5 (n 2) | 0% | 2.11 / 23 | 1/10, 78 s | 0/10 | 1/10, 79 s | 0/10 |
| long | 0% | – (n 0) | 18% | 2.56 / 44 | 0/10 | 0/10 | 0/10 | 0/10 |
| sphere | 95% | 13.2 (n 38) | 2% | 0.12 / 0 | 10/10, 12 s | 10/10, 13 s | 10/10, 10 s | 8/10, 18 s |
| cylinder | 25% | 18.3 (n 10) | 2% | 0.59 / 37 | 9/10, 12 s | 1/10, 74 s | 0/10 | 0/10 |
| arch | 2% | 75.5 (n 1) | 18% | 2.15 / 41 | 0/10 | 0/10 | 1/10, 75 s | 0/10 |
| dumbbell | 0% | – (n 0) | 28% | 2.97 / 45 | 0/10 | 0/10 | 0/10 | 0/10 |
| t_shape | 2% | 71.0 (n 1) | 20% | 2.57 / 38 | 0/10 | 0/10 | 1/10, 71 s | 0/10 |
| beam | 0% | – (n 0) | 38% | 3.34 / 42 | 0/10 | 0/10 | 0/10 | 0/10 |
| l_shape | 0% | – (n 0) | 10% | 2.47 / 30 | 0/10 | 0/10 | 0/10 | 0/10 |
| asym | 0% | – (n 0) | 15% | 3.12 / 45 | 0/10 | 0/10 | 0/10 | 0/10 |
| u_channel | 0% | – (n 0) | 12% | 2.57 / 26 | 0/10 | 0/10 | 0/10 | 0/10 |
| plus | 0% | – (n 0) | 25% | 2.92 / 27 | 0/10 | 0/10 | 0/10 | 0/10 |

## Notes: positions with failures

Per mass and object, each start position that failed at least once: failed / trials, how, and the closest any failed trial got.

**20 kg**

- cylinder: `C_backright` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.06 m / 69 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.05 m / 50 deg)
- arch: `A_straight` 9/10 failed (9 timeout; closest stop 0.12 m / 32 deg); `B_left` 1/10 failed (1 timeout; closest stop 0.32 m / 59 deg); `D_far_turn` 7/10 failed (7 timeout; closest stop 0.15 m / 81 deg)
- dumbbell: `B_left` 1/10 failed (1 fell anymal1; closest stop 0.27 m / 35 deg); `D_far_turn` 1/10 failed (1 fell anymal1; closest stop 0.36 m / 55 deg)
- beam: `B_left` 1/10 failed (1 timeout; closest stop 0.20 m / 2 deg); `C_backright` 7/10 failed (7 timeout; closest stop 0.10 m / 65 deg)
- asym: `A_straight` 1/10 failed (1 timeout; closest stop 1.96 m / 1 deg)
- plus: `A_straight` 1/10 failed (1 timeout; closest stop 0.09 m / 35 deg); `B_left` 1/10 failed (1 timeout; closest stop 0.41 m / 22 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.12 m / 1 deg); `D_far_turn` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.16 m / 0 deg)

**40 kg**

- cube: `D_far_turn` 1/10 failed (1 timeout; closest stop 0.82 m / 42 deg)
- long: `B_left` 1/10 failed (1 timeout; closest stop 1.03 m / 55 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.22 m / 23 deg)
- cylinder: `A_straight` 2/10 failed (2 fell anymal1; closest stop 0.12 m / 0 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.06 m / 9 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.07 m / 51 deg)
- arch: `A_straight` 10/10 failed (10 timeout; closest stop 0.07 m / 27 deg); `B_left` 7/10 failed (7 timeout; closest stop 0.18 m / 33 deg); `D_far_turn` 8/10 failed (8 timeout; closest stop 0.12 m / 68 deg)
- dumbbell: `A_straight` 1/10 failed (1 fell anymal1; closest stop 1.37 m / 1 deg); `B_left` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.19 m / 10 deg); `C_backright` 3/10 failed (3 timeout; closest stop 0.11 m / 78 deg); `D_far_turn` 8/10 failed (7 timeout, 1 fell anymal1; closest stop 0.20 m / 14 deg)
- t_shape: `B_left` 2/10 failed (1 fell anymal1, 1 tipped; closest stop 0.05 m / 6 deg); `C_backright` 1/10 failed (1 fell anymal1; closest stop 2.97 m / 60 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.24 m / 30 deg)
- beam: `A_straight` 5/10 failed (3 timeout, 2 fell anymal1; closest stop 0.10 m / 0 deg); `B_left` 6/10 failed (4 timeout, 2 fell anymal1; closest stop 0.04 m / 7 deg); `C_backright` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 0.30 m / 32 deg); `D_far_turn` 8/10 failed (5 timeout, 3 fell anymal1; closest stop 0.29 m / 31 deg)
- l_shape: `A_straight` 1/10 failed (1 timeout; closest stop 0.10 m / 5 deg); `C_backright` 2/10 failed (2 timeout; closest stop 1.37 m / 9 deg); `D_far_turn` 4/10 failed (4 timeout; closest stop 0.13 m / 6 deg)
- asym: `A_straight` 9/10 failed (5 timeout, 4 fell anymal1; closest stop 0.33 m / 6 deg); `B_left` 6/10 failed (4 timeout, 2 fell anymal1; closest stop 0.10 m / 5 deg); `C_backright` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 0.51 m / 27 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 1.17 m / 79 deg)
- u_channel: `B_left` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.08 m / 6 deg); `C_backright` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.13 m / 8 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.68 m / 87 deg)
- plus: `A_straight` 2/10 failed (2 timeout; closest stop 0.25 m / 15 deg); `B_left` 5/10 failed (5 timeout; closest stop 0.05 m / 15 deg); `C_backright` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.42 m / 11 deg); `D_far_turn` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 0.83 m / 19 deg)

**60 kg**

- cube: `A_straight` 5/10 failed (3 timeout, 2 fell anymal1; closest stop 0.52 m / 5 deg); `B_left` 4/10 failed (4 timeout; closest stop 0.48 m / 19 deg); `C_backright` 2/10 failed (2 timeout; closest stop 1.27 m / 19 deg); `D_far_turn` 7/10 failed (7 timeout; closest stop 0.09 m / 3 deg)
- long: `A_straight` 8/10 failed (8 timeout; closest stop 0.51 m / 3 deg); `B_left` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.83 m / 50 deg); `C_backright` 6/10 failed (6 timeout; closest stop 0.22 m / 10 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.35 m / 41 deg)
- sphere: `B_left` 1/10 failed (1 fell anymal1; closest stop 0.44 m / 0 deg)
- cylinder: `A_straight` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.23 m / 2 deg); `B_left` 4/10 failed (4 timeout; closest stop 0.33 m / 14 deg); `C_backright` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.06 m / 80 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.07 m / 69 deg)
- arch: `A_straight` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.04 m / 19 deg); `B_left` 10/10 failed (10 timeout; closest stop 0.26 m / 28 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.34 m / 5 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 1.49 m / 24 deg)
- dumbbell: `A_straight` 8/10 failed (5 fell anymal1, 3 timeout; closest stop 0.77 m / 8 deg); `B_left` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.78 m / 59 deg); `C_backright` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.16 m / 19 deg); `D_far_turn` 9/10 failed (5 timeout, 4 fell anymal1; closest stop 1.11 m / 54 deg)
- t_shape: `A_straight` 8/10 failed (6 timeout, 2 fell anymal1; closest stop 0.11 m / 2 deg); `B_left` 9/10 failed (8 timeout, 1 fell anymal1; closest stop 0.08 m / 0 deg); `C_backright` 5/10 failed (4 timeout, 1 fell anymal1; closest stop 0.89 m / 16 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.48 m / 64 deg)
- beam: `A_straight` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 2.12 m / 7 deg); `B_left` 10/10 failed (6 fell anymal1, 4 timeout; closest stop 1.75 m / 12 deg); `C_backright` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.83 m / 80 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 3.70 m / 87 deg)
- l_shape: `A_straight` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.14 m / 7 deg); `B_left` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.13 m / 2 deg); `C_backright` 6/10 failed (4 timeout, 2 fell anymal1; closest stop 0.42 m / 3 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.68 m / 28 deg)
- asym: `A_straight` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 2.09 m / 1 deg); `B_left` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 1.59 m / 48 deg); `C_backright` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 1.39 m / 37 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 3.91 m / 83 deg)
- u_channel: `A_straight` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.15 m / 1 deg); `B_left` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 0.36 m / 10 deg); `C_backright` 8/10 failed (7 timeout, 1 fell anymal1; closest stop 0.18 m / 12 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.70 m / 72 deg)
- plus: `A_straight` 10/10 failed (10 timeout; closest stop 0.25 m / 13 deg); `B_left` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.47 m / 10 deg); `C_backright` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.26 m / 10 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.56 m / 37 deg)

**80 kg**

- cube: `A_straight` 9/10 failed (9 timeout; closest stop 0.39 m / 2 deg); `B_left` 10/10 failed (10 timeout; closest stop 0.73 m / 37 deg); `C_backright` 9/10 failed (9 timeout; closest stop 1.05 m / 21 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 2.57 m / 44 deg)
- long: `A_straight` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 1.60 m / 2 deg); `B_left` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 1.25 m / 54 deg); `C_backright` 10/10 failed (10 timeout; closest stop 0.70 m / 55 deg); `D_far_turn` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 3.76 m / 90 deg)
- sphere: `D_far_turn` 2/10 failed (1 fell anymal1, 1 timeout; closest stop 1.37 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 timeout; closest stop 1.00 m / 1 deg); `B_left` 9/10 failed (9 timeout; closest stop 0.71 m / 36 deg); `C_backright` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.03 m / 12 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.06 m / 69 deg)
- arch: `A_straight` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.97 m / 82 deg); `B_left` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 0.35 m / 54 deg); `C_backright` 9/10 failed (9 timeout; closest stop 0.29 m / 4 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 3.25 m / 9 deg)
- dumbbell: `A_straight` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 2.29 m / 2 deg); `B_left` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 2.32 m / 42 deg); `C_backright` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.20 m / 3 deg); `D_far_turn` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 3.49 m / 90 deg)
- t_shape: `A_straight` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 1.47 m / 2 deg); `B_left` 10/10 failed (5 fell anymal1, 5 timeout; closest stop 1.03 m / 42 deg); `C_backright` 9/10 failed (8 timeout, 1 fell anymal1; closest stop 1.59 m / 25 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 3.37 m / 96 deg)
- beam: `A_straight` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 2.63 m / 6 deg); `B_left` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 2.44 m / 0 deg); `C_backright` 10/10 failed (7 fell anymal1, 3 timeout; closest stop 2.82 m / 64 deg); `D_far_turn` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 4.48 m / 84 deg)
- l_shape: `A_straight` 10/10 failed (10 timeout; closest stop 1.20 m / 8 deg); `B_left` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 0.97 m / 52 deg); `C_backright` 10/10 failed (8 timeout, 2 fell anymal1; closest stop 0.93 m / 5 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 3.36 m / 48 deg)
- asym: `A_straight` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 2.65 m / 10 deg); `B_left` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 2.28 m / 29 deg); `C_backright` 10/10 failed (10 timeout; closest stop 2.40 m / 53 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 4.43 m / 74 deg)
- u_channel: `A_straight` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 1.97 m / 3 deg); `B_left` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 1.57 m / 38 deg); `C_backright` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 1.01 m / 8 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 2.94 m / 52 deg)
- plus: `A_straight` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 2.18 m / 13 deg); `B_left` 10/10 failed (10 timeout; closest stop 1.04 m / 40 deg); `C_backright` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 1.09 m / 39 deg); `D_far_turn` 10/10 failed (6 fell anymal1, 4 timeout; closest stop 4.03 m / 30 deg)

## Videos

One per mass x object x position: the fastest successful trial, or when none succeeded, the trial that ended closest to the goal (closeness = final distance / task distance + heading error / 180 deg). File name: `<object>_<mass>kg_<position>_rep<trial>__<outcome>.mp4`.

