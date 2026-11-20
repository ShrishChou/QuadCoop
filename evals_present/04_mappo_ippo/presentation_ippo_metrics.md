# ANYmal IPPO pair (ippo_aa_kl_ten_s0, iteration 4000): evaluation metrics

12 objects x 4 start positions x 4 masses x 10 trials = 1920 episodes (seed 7100; each trial a different random placement of the same task).

Positions (goal relative to the start, robots behind the object): `A_straight` 3 m straight ahead; `B_left` 3 m at 60 deg left, turn 30 deg; `C_backright` 3 m back-right (-135 deg), turn -60 deg; `D_far_turn` 5 m ahead, turn 90 deg.

Success = within 10 cm and 6 deg of the goal, held 1 s, within 80 s. Time = seconds to success, averaged over the successful trials (n in brackets). Fell = a robot fell. Final error = where the object ended (failed trials included). Per-case rows (mass x object x position, 10 trials each): `metrics_by_case.csv`; every episode: `episodes.csv`.

## By mass

| mass | success | precise | mean time (s) | median time (s) | fell | timeout | final error (m / deg) |
|---|---|---|---|---|---|---|---|
| 20 kg | 90% | 86% | 18.0 (n 431) | 15.2 | 5% | 5% | 0.13 / 6 |
| 40 kg | 82% | 76% | 23.4 (n 396) | 20.4 | 8% | 9% | 0.21 / 7 |
| 60 kg | 53% | 48% | 36.2 (n 255) | 33.0 | 24% | 23% | 0.67 / 18 |
| 80 kg | 24% | 21% | 36.0 (n 113) | 32.8 | 26% | 50% | 1.40 / 28 |

## 20 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 98% | 11.7 (n 39) | 2% | 0.11 / 1 | 10/10, 8 s | 10/10, 12 s | 9/10, 12 s | 10/10, 14 s |
| long | 98% | 14.9 (n 39) | 0% | 0.05 / 3 | 9/10, 8 s | 10/10, 19 s | 10/10, 17 s | 10/10, 15 s |
| sphere | 92% | 12.4 (n 37) | 8% | 0.16 / 0 | 9/10, 11 s | 10/10, 11 s | 9/10, 10 s | 9/10, 17 s |
| cylinder | 62% | 16.8 (n 25) | 15% | 0.19 / 16 | 7/10, 10 s | 8/10, 20 s | 10/10, 19 s | 0/10 |
| arch | 55% | 30.8 (n 22) | 20% | 0.33 / 32 | 4/10, 30 s | 6/10, 35 s | 8/10, 25 s | 4/10, 37 s |
| dumbbell | 100% | 20.1 (n 40) | 0% | 0.06 / 2 | 10/10, 16 s | 10/10, 20 s | 10/10, 23 s | 10/10, 22 s |
| t_shape | 98% | 13.9 (n 39) | 2% | 0.15 / 4 | 10/10, 9 s | 10/10, 17 s | 10/10, 12 s | 9/10, 18 s |
| beam | 95% | 29.2 (n 38) | 0% | 0.07 / 5 | 10/10, 21 s | 10/10, 31 s | 8/10, 39 s | 10/10, 28 s |
| l_shape | 100% | 14.7 (n 40) | 0% | 0.05 / 1 | 10/10, 15 s | 10/10, 15 s | 10/10, 11 s | 10/10, 18 s |
| asym | 95% | 14.4 (n 38) | 0% | 0.09 / 2 | 9/10, 15 s | 10/10, 10 s | 10/10, 18 s | 9/10, 15 s |
| u_channel | 100% | 17.9 (n 40) | 0% | 0.05 / 2 | 10/10, 10 s | 10/10, 18 s | 10/10, 21 s | 10/10, 24 s |
| plus | 85% | 25.6 (n 34) | 10% | 0.26 / 2 | 10/10, 11 s | 8/10, 20 s | 9/10, 45 s | 7/10, 28 s |

## 40 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 98% | 19.2 (n 39) | 2% | 0.13 / 1 | 10/10, 13 s | 10/10, 23 s | 9/10, 19 s | 10/10, 22 s |
| long | 100% | 18.8 (n 40) | 0% | 0.05 / 1 | 10/10, 11 s | 10/10, 17 s | 10/10, 27 s | 10/10, 21 s |
| sphere | 90% | 11.7 (n 36) | 10% | 0.30 / 0 | 10/10, 9 s | 10/10, 11 s | 9/10, 12 s | 7/10, 16 s |
| cylinder | 68% | 18.7 (n 27) | 10% | 0.17 / 18 | 10/10, 9 s | 7/10, 18 s | 10/10, 29 s | 0/10 |
| arch | 52% | 41.4 (n 21) | 10% | 0.32 / 26 | 3/10, 54 s | 3/10, 43 s | 10/10, 31 s | 5/10, 53 s |
| dumbbell | 82% | 24.8 (n 33) | 12% | 0.24 / 8 | 8/10, 16 s | 10/10, 29 s | 6/10, 32 s | 9/10, 23 s |
| t_shape | 98% | 19.8 (n 39) | 0% | 0.09 / 2 | 9/10, 16 s | 10/10, 19 s | 10/10, 21 s | 10/10, 24 s |
| beam | 68% | 33.2 (n 27) | 15% | 0.35 / 15 | 9/10, 28 s | 9/10, 33 s | 1/10, 70 s | 8/10, 35 s |
| l_shape | 95% | 24.8 (n 38) | 5% | 0.15 / 4 | 9/10, 19 s | 10/10, 21 s | 10/10, 25 s | 9/10, 34 s |
| asym | 68% | 31.6 (n 27) | 10% | 0.25 / 7 | 5/10, 30 s | 9/10, 14 s | 5/10, 47 s | 8/10, 43 s |
| u_channel | 98% | 21.4 (n 39) | 2% | 0.07 / 2 | 10/10, 18 s | 9/10, 19 s | 10/10, 28 s | 10/10, 20 s |
| plus | 75% | 28.8 (n 30) | 20% | 0.36 / 4 | 10/10, 14 s | 6/10, 22 s | 7/10, 53 s | 7/10, 33 s |

## 60 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 55% | 46.7 (n 22) | 12% | 0.60 / 10 | 8/10, 46 s | 2/10, 57 s | 6/10, 45 s | 6/10, 46 s |
| long | 70% | 35.1 (n 28) | 5% | 0.30 / 8 | 8/10, 24 s | 7/10, 40 s | 6/10, 48 s | 7/10, 31 s |
| sphere | 90% | 11.5 (n 36) | 10% | 0.21 / 0 | 8/10, 9 s | 9/10, 10 s | 10/10, 10 s | 9/10, 17 s |
| cylinder | 30% | 32.4 (n 12) | 40% | 0.81 / 30 | 7/10, 10 s | 3/10, 62 s | 2/10, 67 s | 0/10 |
| arch | 28% | 51.7 (n 11) | 42% | 1.39 / 34 | 3/10, 59 s | 0/10 | 8/10, 49 s | 0/10 |
| dumbbell | 45% | 29.2 (n 18) | 30% | 0.80 / 26 | 4/10, 21 s | 5/10, 31 s | 2/10, 56 s | 7/10, 25 s |
| t_shape | 72% | 42.6 (n 29) | 15% | 0.27 / 8 | 9/10, 40 s | 6/10, 42 s | 7/10, 46 s | 7/10, 43 s |
| beam | 15% | 41.9 (n 6) | 62% | 1.64 / 35 | 3/10, 32 s | 0/10 | 0/10 | 3/10, 52 s |
| l_shape | 65% | 41.1 (n 26) | 18% | 0.39 / 14 | 8/10, 29 s | 6/10, 39 s | 6/10, 49 s | 6/10, 51 s |
| asym | 38% | 50.6 (n 15) | 20% | 0.87 / 35 | 5/10, 62 s | 8/10, 40 s | 2/10, 64 s | 0/10 |
| u_channel | 78% | 39.4 (n 31) | 8% | 0.19 / 11 | 8/10, 44 s | 9/10, 34 s | 7/10, 52 s | 7/10, 28 s |
| plus | 52% | 37.9 (n 21) | 22% | 0.50 / 8 | 7/10, 26 s | 3/10, 28 s | 6/10, 52 s | 5/10, 44 s |

## 80 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 10% | 38.9 (n 4) | 15% | 1.93 / 19 | 1/10, 12 s | 1/10, 36 s | 1/10, 78 s | 1/10, 29 s |
| long | 35% | 52.4 (n 14) | 12% | 0.96 / 26 | 8/10, 45 s | 1/10, 65 s | 2/10, 73 s | 3/10, 54 s |
| sphere | 95% | 11.6 (n 38) | 5% | 0.08 / 0 | 9/10, 10 s | 9/10, 10 s | 10/10, 12 s | 10/10, 15 s |
| cylinder | 30% | 19.6 (n 12) | 38% | 0.90 / 37 | 10/10, 10 s | 2/10, 66 s | 0/10 | 0/10 |
| arch | 8% | 66.8 (n 3) | 32% | 2.13 / 43 | 1/10, 77 s | 0/10 | 2/10, 62 s | 0/10 |
| dumbbell | 15% | 48.6 (n 6) | 57% | 1.65 / 34 | 2/10, 40 s | 2/10, 54 s | 1/10, 45 s | 1/10, 60 s |
| t_shape | 28% | 64.0 (n 11) | 18% | 1.21 / 24 | 6/10, 64 s | 0/10 | 1/10, 58 s | 4/10, 65 s |
| beam | 2% | 61.7 (n 1) | 75% | 2.65 / 40 | 0/10 | 0/10 | 0/10 | 1/10, 62 s |
| l_shape | 12% | 46.1 (n 5) | 28% | 1.14 / 28 | 3/10, 50 s | 2/10, 40 s | 0/10 | 0/10 |
| asym | 5% | 68.6 (n 2) | 2% | 2.01 / 40 | 0/10 | 2/10, 69 s | 0/10 | 0/10 |
| u_channel | 10% | 59.0 (n 4) | 12% | 1.11 / 32 | 1/10, 76 s | 2/10, 43 s | 1/10, 75 s | 0/10 |
| plus | 32% | 49.4 (n 13) | 20% | 1.05 / 12 | 6/10, 39 s | 2/10, 70 s | 3/10, 53 s | 2/10, 56 s |

## Notes: positions with failures

Per mass and object, each start position that failed at least once: failed / trials, how, and the closest any failed trial got.

**20 kg**

- cube: `C_backright` 1/10 failed (1 fell anymal2; closest stop 2.57 m / 16 deg)
- long: `A_straight` 1/10 failed (1 timeout; closest stop 0.21 m / 73 deg)
- sphere: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.24 m / 0 deg); `C_backright` 1/10 failed (1 fell anymal2; closest stop 0.04 m / 0 deg); `D_far_turn` 1/10 failed (1 fell anymal1; closest stop 4.28 m / 0 deg)
- cylinder: `A_straight` 3/10 failed (3 fell anymal2; closest stop 0.25 m / 4 deg); `B_left` 2/10 failed (1 fell anymal1, 1 fell anymal2; closest stop 1.86 m / 2 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal2; closest stop 0.04 m / 79 deg)
- arch: `A_straight` 6/10 failed (4 fell anymal2, 2 timeout; closest stop 0.14 m / 22 deg); `B_left` 4/10 failed (2 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.42 m / 58 deg); `C_backright` 2/10 failed (1 fell anymal2, 1 timeout; closest stop 0.45 m / 76 deg); `D_far_turn` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.07 m / 86 deg)
- t_shape: `D_far_turn` 1/10 failed (1 fell anymal2; closest stop 4.00 m / 120 deg)
- beam: `C_backright` 2/10 failed (2 timeout; closest stop 0.13 m / 66 deg)
- asym: `A_straight` 1/10 failed (1 tipped; closest stop 1.38 m / 11 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.40 m / 41 deg)
- plus: `B_left` 2/10 failed (2 fell anymal2; closest stop 1.24 m / 6 deg); `C_backright` 1/10 failed (1 timeout; closest stop 0.22 m / 6 deg); `D_far_turn` 3/10 failed (1 fell anymal1, 1 timeout, 1 fell anymal2; closest stop 0.14 m / 30 deg)

**40 kg**

- cube: `C_backright` 1/10 failed (1 fell anymal1; closest stop 2.85 m / 15 deg)
- sphere: `C_backright` 1/10 failed (1 fell anymal2; closest stop 0.12 m / 0 deg); `D_far_turn` 3/10 failed (2 fell anymal1, 1 fell anymal2; closest stop 2.79 m / 0 deg)
- cylinder: `B_left` 3/10 failed (1 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.65 m / 2 deg); `D_far_turn` 10/10 failed (8 timeout, 2 fell anymal2; closest stop 0.04 m / 69 deg)
- arch: `A_straight` 7/10 failed (7 timeout; closest stop 0.01 m / 26 deg); `B_left` 7/10 failed (4 fell anymal2, 3 timeout; closest stop 0.24 m / 48 deg); `D_far_turn` 5/10 failed (5 timeout; closest stop 0.11 m / 59 deg)
- dumbbell: `A_straight` 2/10 failed (1 fell anymal2, 1 fell anymal1; closest stop 0.24 m / 12 deg); `C_backright` 4/10 failed (2 fell anymal1, 2 timeout; closest stop 0.36 m / 38 deg); `D_far_turn` 1/10 failed (1 fell anymal1; closest stop 1.96 m / 72 deg)
- t_shape: `A_straight` 1/10 failed (1 timeout; closest stop 1.58 m / 5 deg)
- beam: `A_straight` 1/10 failed (1 fell anymal1; closest stop 0.57 m / 12 deg); `B_left` 1/10 failed (1 timeout; closest stop 0.13 m / 2 deg); `C_backright` 9/10 failed (5 timeout, 3 fell anymal1, 1 fell anymal2; closest stop 0.11 m / 28 deg); `D_far_turn` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.60 m / 13 deg)
- l_shape: `A_straight` 1/10 failed (1 fell anymal1; closest stop 0.31 m / 6 deg); `D_far_turn` 1/10 failed (1 fell anymal2; closest stop 3.97 m / 87 deg)
- asym: `A_straight` 5/10 failed (3 fell anymal1, 1 tipped, 1 timeout; closest stop 0.07 m / 2 deg); `B_left` 1/10 failed (1 fell anymal1; closest stop 0.13 m / 4 deg); `C_backright` 5/10 failed (5 timeout; closest stop 0.74 m / 6 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.20 m / 67 deg)
- u_channel: `B_left` 1/10 failed (1 fell anymal2; closest stop 1.05 m / 8 deg)
- plus: `B_left` 4/10 failed (2 fell anymal2, 2 fell anymal1; closest stop 0.23 m / 2 deg); `C_backright` 3/10 failed (1 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.14 m / 1 deg); `D_far_turn` 3/10 failed (2 fell anymal2, 1 timeout; closest stop 0.07 m / 24 deg)

**60 kg**

- cube: `A_straight` 2/10 failed (2 timeout; closest stop 0.07 m / 0 deg); `B_left` 8/10 failed (5 timeout, 3 fell anymal1; closest stop 0.18 m / 8 deg); `C_backright` 4/10 failed (2 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.18 m / 6 deg); `D_far_turn` 4/10 failed (4 timeout; closest stop 1.23 m / 42 deg)
- long: `A_straight` 2/10 failed (1 timeout, 1 fell anymal2; closest stop 0.32 m / 1 deg); `B_left` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.20 m / 3 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.19 m / 8 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.03 m / 7 deg)
- sphere: `A_straight` 2/10 failed (2 fell anymal1; closest stop 0.71 m / 0 deg); `B_left` 1/10 failed (1 fell anymal2; closest stop 0.34 m / 0 deg); `D_far_turn` 1/10 failed (1 fell anymal1; closest stop 4.72 m / 0 deg)
- cylinder: `A_straight` 3/10 failed (2 fell anymal2, 1 fell anymal1; closest stop 0.03 m / 1 deg); `B_left` 7/10 failed (4 timeout, 3 fell anymal1; closest stop 0.71 m / 33 deg); `C_backright` 8/10 failed (3 fell anymal1, 3 fell anymal2, 2 timeout; closest stop 0.29 m / 16 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal2; closest stop 0.05 m / 68 deg)
- arch: `A_straight` 7/10 failed (5 fell anymal2, 1 fell anymal1, 1 timeout; closest stop 0.27 m / 80 deg); `B_left` 10/10 failed (6 fell anymal2, 2 timeout, 2 fell anymal1; closest stop 0.48 m / 69 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.20 m / 2 deg); `D_far_turn` 10/10 failed (7 timeout, 3 fell anymal2; closest stop 0.65 m / 44 deg)
- dumbbell: `A_straight` 6/10 failed (2 fell anymal2, 2 fell anymal1, 2 timeout; closest stop 0.06 m / 26 deg); `B_left` 5/10 failed (3 timeout, 2 fell anymal2; closest stop 0.10 m / 76 deg); `C_backright` 8/10 failed (5 timeout, 2 fell anymal1, 1 fell anymal2; closest stop 0.23 m / 53 deg); `D_far_turn` 3/10 failed (2 fell anymal2, 1 fell anymal1; closest stop 1.22 m / 34 deg)
- t_shape: `A_straight` 1/10 failed (1 fell anymal1; closest stop 0.56 m / 0 deg); `B_left` 4/10 failed (2 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.34 m / 4 deg); `C_backright` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.13 m / 4 deg); `D_far_turn` 3/10 failed (2 fell anymal1, 1 timeout; closest stop 0.21 m / 73 deg)
- beam: `A_straight` 7/10 failed (6 fell anymal2, 1 fell anymal1; closest stop 0.79 m / 13 deg); `B_left` 10/10 failed (7 fell anymal2, 2 timeout, 1 fell anymal1; closest stop 0.16 m / 0 deg); `C_backright` 10/10 failed (5 timeout, 4 fell anymal1, 1 fell anymal2; closest stop 0.22 m / 66 deg); `D_far_turn` 7/10 failed (3 fell anymal2, 2 timeout, 2 fell anymal1; closest stop 0.15 m / 2 deg)
- l_shape: `A_straight` 2/10 failed (2 timeout; closest stop 0.12 m / 5 deg); `B_left` 4/10 failed (3 fell anymal2, 1 fell anymal1; closest stop 0.13 m / 5 deg); `C_backright` 4/10 failed (2 fell anymal2, 1 timeout, 1 fell anymal1; closest stop 1.46 m / 15 deg); `D_far_turn` 4/10 failed (4 timeout; closest stop 0.12 m / 74 deg)
- asym: `A_straight` 5/10 failed (3 timeout, 2 fell anymal1; closest stop 0.09 m / 2 deg); `B_left` 2/10 failed (1 fell anymal2, 1 fell anymal1; closest stop 0.16 m / 0 deg); `C_backright` 8/10 failed (4 timeout, 2 fell anymal1, 2 fell anymal2; closest stop 0.12 m / 3 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.79 m / 87 deg)
- u_channel: `A_straight` 2/10 failed (2 fell anymal2; closest stop 0.21 m / 0 deg); `B_left` 1/10 failed (1 timeout; closest stop 0.87 m / 2 deg); `C_backright` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.27 m / 17 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.08 m / 88 deg)
- plus: `A_straight` 3/10 failed (2 fell anymal1, 1 timeout; closest stop 0.13 m / 4 deg); `B_left` 7/10 failed (3 fell anymal2, 2 timeout, 2 fell anymal1; closest stop 0.06 m / 22 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.10 m / 3 deg); `D_far_turn` 5/10 failed (3 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.08 m / 19 deg)

**80 kg**

- cube: `A_straight` 9/10 failed (8 timeout, 1 fell anymal2; closest stop 0.25 m / 0 deg); `B_left` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.12 m / 3 deg); `C_backright` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 1.33 m / 28 deg); `D_far_turn` 9/10 failed (8 timeout, 1 fell anymal1; closest stop 1.77 m / 40 deg)
- long: `A_straight` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 1.25 m / 1 deg); `B_left` 9/10 failed (6 timeout, 2 fell anymal1, 1 fell anymal2; closest stop 0.20 m / 7 deg); `C_backright` 8/10 failed (8 timeout; closest stop 0.11 m / 21 deg); `D_far_turn` 7/10 failed (6 timeout, 1 fell anymal2; closest stop 0.17 m / 52 deg)
- sphere: `A_straight` 1/10 failed (1 fell anymal2; closest stop 0.86 m / 0 deg); `B_left` 1/10 failed (1 fell anymal2; closest stop 0.52 m / 0 deg)
- cylinder: `B_left` 8/10 failed (3 timeout, 3 fell anymal1, 2 fell anymal2; closest stop 0.26 m / 8 deg); `C_backright` 10/10 failed (5 fell anymal1, 3 timeout, 2 fell anymal2; closest stop 0.07 m / 77 deg); `D_far_turn` 10/10 failed (7 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.08 m / 72 deg)
- arch: `A_straight` 9/10 failed (7 timeout, 2 fell anymal2; closest stop 0.52 m / 80 deg); `B_left` 10/10 failed (5 timeout, 4 fell anymal2, 1 fell anymal1; closest stop 0.09 m / 67 deg); `C_backright` 8/10 failed (7 timeout, 1 fell anymal1; closest stop 0.38 m / 1 deg); `D_far_turn` 10/10 failed (5 timeout, 4 fell anymal2, 1 fell anymal1; closest stop 2.69 m / 6 deg)
- dumbbell: `A_straight` 8/10 failed (3 fell anymal2, 3 fell anymal1, 2 timeout; closest stop 0.17 m / 12 deg); `B_left` 8/10 failed (6 fell anymal2, 1 timeout, 1 fell anymal1; closest stop 0.30 m / 12 deg); `C_backright` 9/10 failed (5 timeout, 2 fell anymal2, 2 fell anymal1; closest stop 0.16 m / 54 deg); `D_far_turn` 9/10 failed (4 fell anymal1, 3 timeout, 2 fell anymal2; closest stop 0.10 m / 55 deg)
- t_shape: `A_straight` 4/10 failed (4 timeout; closest stop 1.16 m / 24 deg); `B_left` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.19 m / 6 deg); `C_backright` 9/10 failed (5 fell anymal1, 4 timeout; closest stop 0.98 m / 28 deg); `D_far_turn` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.09 m / 42 deg)
- beam: `A_straight` 10/10 failed (8 fell anymal2, 1 fell anymal1, 1 timeout; closest stop 0.15 m / 3 deg); `B_left` 10/10 failed (6 fell anymal2, 2 timeout, 2 fell anymal1; closest stop 1.89 m / 16 deg); `C_backright` 10/10 failed (5 timeout, 4 fell anymal1, 1 fell anymal2; closest stop 0.22 m / 67 deg); `D_far_turn` 9/10 failed (4 fell anymal2, 4 fell anymal1, 1 timeout; closest stop 1.56 m / 71 deg)
- l_shape: `A_straight` 7/10 failed (4 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.11 m / 2 deg); `B_left` 8/10 failed (3 fell anymal1, 3 timeout, 2 fell anymal2; closest stop 0.10 m / 0 deg); `C_backright` 10/10 failed (7 timeout, 2 fell anymal1, 1 fell anymal2; closest stop 0.82 m / 13 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.04 m / 7 deg)
- asym: `A_straight` 10/10 failed (10 timeout; closest stop 1.08 m / 3 deg); `B_left` 8/10 failed (8 timeout; closest stop 0.17 m / 2 deg); `C_backright` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.84 m / 29 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 3.24 m / 83 deg)
- u_channel: `A_straight` 9/10 failed (9 timeout; closest stop 0.57 m / 5 deg); `B_left` 8/10 failed (6 timeout, 2 fell anymal1; closest stop 0.39 m / 18 deg); `C_backright` 9/10 failed (8 timeout, 1 fell anymal2; closest stop 0.43 m / 20 deg); `D_far_turn` 10/10 failed (8 timeout, 2 fell anymal2; closest stop 0.11 m / 15 deg)
- plus: `A_straight` 4/10 failed (2 fell anymal1, 2 timeout; closest stop 1.04 m / 9 deg); `B_left` 8/10 failed (7 timeout, 1 fell anymal2; closest stop 0.29 m / 15 deg); `C_backright` 7/10 failed (5 timeout, 2 fell anymal1; closest stop 0.11 m / 6 deg); `D_far_turn` 8/10 failed (5 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.08 m / 2 deg)

