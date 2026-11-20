# Contact planner (expert rule + turn_debug executor): evaluation metrics

12 objects x 4 start positions x 4 masses x 10 trials = 1920 episodes (seed 7100; each trial a different random placement of the same task).

Positions (goal relative to the start, robots behind the object): `A_straight` 3 m straight ahead; `B_left` 3 m at 60 deg left, turn 30 deg; `C_backright` 3 m back-right (-135 deg), turn -60 deg; `D_far_turn` 5 m ahead, turn 90 deg.

Success = within 10 cm and 6 deg of the goal, held 1 s, within 80 s. Time = seconds to success, averaged over the successful trials (n in brackets). Fell = a robot fell. Final error = where the object ended (failed trials included). Per-case rows (mass x object x position, 10 trials each): `metrics_by_case.csv`; every episode: `episodes.csv`.

## By mass

| mass | success | precise | mean time (s) | median time (s) | fell | timeout | final error (m / deg) |
|---|---|---|---|---|---|---|---|
| 20 kg | 72% | 71% | 28.7 (n 348) | 25.6 | 2% | 26% | 0.17 / 8 |
| 40 kg | 67% | 55% | 33.2 (n 323) | 30.0 | 4% | 28% | 0.32 / 10 |
| 60 kg | 50% | 40% | 37.8 (n 238) | 36.8 | 8% | 42% | 0.51 / 13 |
| 80 kg | 33% | 23% | 41.3 (n 159) | 42.9 | 17% | 50% | 1.00 / 19 |

## 20 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 90% | 18.0 (n 36) | 0% | 0.08 / 2 | 10/10, 12 s | 9/10, 18 s | 8/10, 26 s | 9/10, 17 s |
| long | 88% | 26.1 (n 35) | 0% | 0.07 / 7 | 7/10, 19 s | 10/10, 25 s | 8/10, 23 s | 10/10, 35 s |
| sphere | 100% | 18.5 (n 40) | 0% | 0.05 / 0 | 10/10, 11 s | 10/10, 16 s | 10/10, 32 s | 10/10, 15 s |
| cylinder | 42% | 29.5 (n 17) | 12% | 0.42 / 28 | 3/10, 17 s | 6/10, 18 s | 2/10, 26 s | 6/10, 49 s |
| arch | 92% | 28.3 (n 37) | 0% | 0.09 / 3 | 9/10, 23 s | 10/10, 25 s | 8/10, 32 s | 10/10, 33 s |
| dumbbell | 68% | 31.0 (n 27) | 0% | 0.16 / 3 | 10/10, 30 s | 8/10, 33 s | 5/10, 25 s | 4/10, 39 s |
| t_shape | 65% | 36.4 (n 26) | 2% | 0.12 / 5 | 7/10, 28 s | 5/10, 27 s | 6/10, 43 s | 8/10, 44 s |
| beam | 52% | 34.2 (n 21) | 0% | 0.41 / 17 | 4/10, 48 s | 7/10, 33 s | 6/10, 33 s | 4/10, 25 s |
| l_shape | 72% | 36.4 (n 29) | 2% | 0.13 / 11 | 6/10, 36 s | 7/10, 40 s | 8/10, 30 s | 8/10, 41 s |
| asym | 50% | 30.7 (n 20) | 2% | 0.30 / 13 | 8/10, 36 s | 6/10, 17 s | 1/10, 36 s | 5/10, 37 s |
| u_channel | 88% | 30.0 (n 35) | 0% | 0.09 / 3 | 9/10, 20 s | 10/10, 27 s | 9/10, 40 s | 7/10, 34 s |
| plus | 62% | 36.6 (n 25) | 0% | 0.13 / 5 | 5/10, 22 s | 5/10, 28 s | 6/10, 46 s | 9/10, 43 s |

## 40 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 90% | 24.3 (n 36) | 0% | 0.07 / 2 | 8/10, 9 s | 10/10, 29 s | 10/10, 33 s | 8/10, 23 s |
| long | 75% | 33.8 (n 30) | 0% | 0.16 / 9 | 9/10, 30 s | 6/10, 33 s | 8/10, 34 s | 7/10, 38 s |
| sphere | 95% | 14.1 (n 38) | 0% | 0.14 / 0 | 10/10, 9 s | 9/10, 14 s | 9/10, 22 s | 10/10, 12 s |
| cylinder | 32% | 41.6 (n 13) | 15% | 0.53 / 25 | 5/10, 34 s | 5/10, 45 s | 2/10, 39 s | 1/10, 69 s |
| arch | 92% | 29.6 (n 37) | 2% | 0.10 / 2 | 9/10, 20 s | 9/10, 24 s | 9/10, 33 s | 10/10, 40 s |
| dumbbell | 65% | 37.9 (n 26) | 2% | 0.26 / 7 | 9/10, 29 s | 7/10, 46 s | 6/10, 32 s | 4/10, 52 s |
| t_shape | 70% | 37.8 (n 28) | 2% | 0.12 / 5 | 7/10, 44 s | 5/10, 28 s | 7/10, 36 s | 9/10, 39 s |
| beam | 35% | 34.6 (n 14) | 8% | 1.01 / 22 | 7/10, 23 s | 5/10, 41 s | 1/10, 67 s | 1/10, 51 s |
| l_shape | 82% | 41.5 (n 33) | 2% | 0.09 / 6 | 8/10, 41 s | 8/10, 38 s | 9/10, 33 s | 8/10, 55 s |
| asym | 28% | 58.4 (n 11) | 12% | 0.71 / 21 | 4/10, 51 s | 2/10, 48 s | 0/10 | 5/10, 68 s |
| u_channel | 75% | 31.1 (n 30) | 0% | 0.42 / 14 | 10/10, 17 s | 10/10, 31 s | 3/10, 35 s | 7/10, 50 s |
| plus | 68% | 44.5 (n 27) | 5% | 0.25 / 7 | 4/10, 49 s | 9/10, 28 s | 7/10, 49 s | 7/10, 58 s |

## 60 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 65% | 40.2 (n 26) | 2% | 0.29 / 5 | 7/10, 26 s | 5/10, 48 s | 6/10, 44 s | 8/10, 45 s |
| long | 60% | 46.3 (n 24) | 8% | 0.35 / 10 | 7/10, 48 s | 6/10, 38 s | 5/10, 55 s | 6/10, 45 s |
| sphere | 98% | 15.9 (n 39) | 0% | 0.06 / 0 | 10/10, 8 s | 10/10, 15 s | 9/10, 32 s | 10/10, 11 s |
| cylinder | 32% | 29.7 (n 13) | 2% | 0.34 / 30 | 9/10, 21 s | 3/10, 57 s | 1/10, 30 s | 0/10 |
| arch | 72% | 40.7 (n 29) | 2% | 0.23 / 4 | 8/10, 30 s | 8/10, 31 s | 6/10, 49 s | 7/10, 56 s |
| dumbbell | 65% | 40.7 (n 26) | 2% | 0.48 / 4 | 8/10, 39 s | 10/10, 37 s | 5/10, 51 s | 3/10, 40 s |
| t_shape | 65% | 44.8 (n 26) | 2% | 0.19 / 8 | 9/10, 50 s | 4/10, 48 s | 7/10, 34 s | 6/10, 46 s |
| beam | 2% | 41.6 (n 1) | 32% | 1.81 / 26 | 1/10, 42 s | 0/10 | 0/10 | 0/10 |
| l_shape | 42% | 40.4 (n 17) | 8% | 0.35 / 14 | 5/10, 48 s | 4/10, 34 s | 8/10, 39 s | 0/10 |
| asym | 10% | 58.3 (n 4) | 25% | 1.13 / 29 | 3/10, 54 s | 1/10, 71 s | 0/10 | 0/10 |
| u_channel | 52% | 38.0 (n 21) | 0% | 0.31 / 9 | 10/10, 28 s | 5/10, 41 s | 3/10, 38 s | 3/10, 68 s |
| plus | 30% | 55.1 (n 12) | 12% | 0.63 / 15 | 3/10, 64 s | 5/10, 43 s | 2/10, 71 s | 2/10, 56 s |

## 80 kg: by object

| object | success | mean time (s) | fell | final error (m / deg) | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|---|---|---|---|
| cube | 12% | 52.0 (n 5) | 25% | 1.28 / 14 | 2/10, 39 s | 1/10, 69 s | 2/10, 57 s | 0/10 |
| long | 45% | 46.7 (n 18) | 8% | 0.85 / 15 | 4/10, 43 s | 3/10, 64 s | 6/10, 44 s | 5/10, 43 s |
| sphere | 95% | 13.0 (n 38) | 2% | 0.12 / 0 | 10/10, 9 s | 9/10, 13 s | 9/10, 18 s | 10/10, 13 s |
| cylinder | 28% | 39.9 (n 11) | 20% | 0.72 / 33 | 9/10, 32 s | 2/10, 77 s | 0/10 | 0/10 |
| arch | 50% | 54.0 (n 20) | 10% | 0.47 / 8 | 8/10, 49 s | 6/10, 45 s | 4/10, 68 s | 2/10, 74 s |
| dumbbell | 30% | 51.1 (n 12) | 18% | 0.86 / 17 | 5/10, 44 s | 2/10, 59 s | 3/10, 60 s | 2/10, 47 s |
| t_shape | 35% | 53.1 (n 14) | 8% | 0.60 / 20 | 4/10, 56 s | 3/10, 57 s | 7/10, 50 s | 0/10 |
| beam | 0% | – (n 0) | 68% | 2.82 / 35 | 0/10 | 0/10 | 0/10 | 0/10 |
| l_shape | 25% | 39.5 (n 10) | 10% | 0.76 / 23 | 0/10 | 3/10, 49 s | 6/10, 30 s | 1/10, 65 s |
| asym | 0% | – (n 0) | 28% | 2.19 / 32 | 0/10 | 0/10 | 0/10 | 0/10 |
| u_channel | 40% | 50.9 (n 16) | 2% | 0.51 / 16 | 9/10, 45 s | 2/10, 65 s | 5/10, 55 s | 0/10 |
| plus | 38% | 59.3 (n 15) | 8% | 0.80 / 12 | 3/10, 60 s | 6/10, 56 s | 3/10, 56 s | 3/10, 68 s |

## Notes: positions with failures

Per mass and object, each start position that failed at least once: failed / trials, how, and the closest any failed trial got.

**20 kg**

- cube: `B_left` 1/10 failed (1 timeout; closest stop 0.27 m / 1 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.19 m / 2 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.15 m / 2 deg)
- long: `A_straight` 3/10 failed (3 timeout; closest stop 0.07 m / 49 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.06 m / 53 deg)
- cylinder: `A_straight` 7/10 failed (7 timeout; closest stop 0.05 m / 85 deg); `B_left` 4/10 failed (3 timeout, 1 fell anymal2; closest stop 0.12 m / 14 deg); `C_backright` 8/10 failed (6 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.10 m / 70 deg); `D_far_turn` 4/10 failed (2 timeout, 2 fell anymal1; closest stop 0.10 m / 65 deg)
- arch: `A_straight` 1/10 failed (1 timeout; closest stop 0.19 m / 4 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.26 m / 1 deg)
- dumbbell: `B_left` 2/10 failed (2 timeout; closest stop 0.15 m / 2 deg); `C_backright` 5/10 failed (5 timeout; closest stop 0.11 m / 2 deg); `D_far_turn` 6/10 failed (6 timeout; closest stop 0.20 m / 6 deg)
- t_shape: `A_straight` 3/10 failed (3 timeout; closest stop 0.17 m / 15 deg); `B_left` 5/10 failed (5 timeout; closest stop 0.08 m / 8 deg); `C_backright` 4/10 failed (3 timeout, 1 fell anymal2; closest stop 0.05 m / 12 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.17 m / 1 deg)
- beam: `A_straight` 6/10 failed (6 timeout; closest stop 0.12 m / 1 deg); `B_left` 3/10 failed (3 timeout; closest stop 0.15 m / 3 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.08 m / 52 deg); `D_far_turn` 6/10 failed (6 timeout; closest stop 0.01 m / 28 deg)
- l_shape: `A_straight` 4/10 failed (4 timeout; closest stop 0.11 m / 25 deg); `B_left` 3/10 failed (3 timeout; closest stop 0.10 m / 29 deg); `C_backright` 2/10 failed (1 timeout, 1 fell anymal2; closest stop 0.14 m / 67 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.06 m / 16 deg)
- asym: `A_straight` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.13 m / 17 deg); `B_left` 4/10 failed (4 timeout; closest stop 0.08 m / 31 deg); `C_backright` 9/10 failed (9 timeout; closest stop 0.05 m / 38 deg); `D_far_turn` 5/10 failed (4 timeout, 1 tipped; closest stop 0.30 m / 2 deg)
- u_channel: `A_straight` 1/10 failed (1 timeout; closest stop 0.16 m / 8 deg); `C_backright` 1/10 failed (1 timeout; closest stop 0.65 m / 1 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.06 m / 8 deg)
- plus: `A_straight` 5/10 failed (5 timeout; closest stop 0.14 m / 12 deg); `B_left` 5/10 failed (5 timeout; closest stop 0.12 m / 12 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.12 m / 11 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.20 m / 0 deg)

**40 kg**

- cube: `A_straight` 2/10 failed (2 timeout; closest stop 0.09 m / 17 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.15 m / 3 deg)
- long: `A_straight` 1/10 failed (1 timeout; closest stop 0.13 m / 5 deg); `B_left` 4/10 failed (4 timeout; closest stop 0.11 m / 35 deg); `C_backright` 2/10 failed (2 timeout; closest stop 0.14 m / 51 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.13 m / 41 deg)
- sphere: `B_left` 1/10 failed (1 timeout; closest stop 0.25 m / 0 deg); `C_backright` 1/10 failed (1 timeout; closest stop 3.00 m / 0 deg)
- cylinder: `A_straight` 5/10 failed (4 timeout, 1 fell anymal1; closest stop 0.06 m / 52 deg); `B_left` 5/10 failed (4 timeout, 1 fell anymal2; closest stop 0.06 m / 29 deg); `C_backright` 8/10 failed (6 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.04 m / 31 deg); `D_far_turn` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.07 m / 10 deg)
- arch: `A_straight` 1/10 failed (1 timeout; closest stop 0.25 m / 5 deg); `B_left` 1/10 failed (1 fell anymal1; closest stop 0.78 m / 7 deg); `C_backright` 1/10 failed (1 timeout; closest stop 0.41 m / 1 deg)
- dumbbell: `A_straight` 1/10 failed (1 timeout; closest stop 0.18 m / 6 deg); `B_left` 3/10 failed (3 timeout; closest stop 0.16 m / 6 deg); `C_backright` 4/10 failed (3 timeout, 1 fell anymal2; closest stop 0.19 m / 1 deg); `D_far_turn` 6/10 failed (6 timeout; closest stop 0.12 m / 0 deg)
- t_shape: `A_straight` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.07 m / 18 deg); `B_left` 5/10 failed (5 timeout; closest stop 0.13 m / 19 deg); `C_backright` 3/10 failed (3 timeout; closest stop 0.13 m / 10 deg); `D_far_turn` 1/10 failed (1 timeout; closest stop 0.28 m / 12 deg)
- beam: `A_straight` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.23 m / 8 deg); `B_left` 5/10 failed (5 timeout; closest stop 1.12 m / 5 deg); `C_backright` 9/10 failed (9 timeout; closest stop 0.15 m / 4 deg); `D_far_turn` 9/10 failed (7 timeout, 2 fell anymal1; closest stop 0.13 m / 51 deg)
- l_shape: `A_straight` 2/10 failed (2 timeout; closest stop 0.10 m / 30 deg); `B_left` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.12 m / 17 deg); `C_backright` 1/10 failed (1 timeout; closest stop 0.17 m / 7 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 0.15 m / 12 deg)
- asym: `A_straight` 6/10 failed (6 timeout; closest stop 0.04 m / 5 deg); `B_left` 8/10 failed (6 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.03 m / 32 deg); `C_backright` 10/10 failed (7 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.08 m / 71 deg); `D_far_turn` 5/10 failed (4 timeout, 1 tipped; closest stop 0.10 m / 64 deg)
- u_channel: `C_backright` 7/10 failed (7 timeout; closest stop 0.76 m / 26 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.12 m / 0 deg)
- plus: `A_straight` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.11 m / 23 deg); `B_left` 1/10 failed (1 timeout; closest stop 0.20 m / 1 deg); `C_backright` 3/10 failed (2 timeout, 1 fell anymal2; closest stop 0.18 m / 3 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.12 m / 3 deg)

**60 kg**

- cube: `A_straight` 3/10 failed (2 timeout, 1 fell anymal1; closest stop 0.22 m / 3 deg); `B_left` 5/10 failed (5 timeout; closest stop 0.13 m / 3 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.12 m / 18 deg); `D_far_turn` 2/10 failed (2 timeout; closest stop 2.27 m / 33 deg)
- long: `A_straight` 3/10 failed (3 timeout; closest stop 0.14 m / 40 deg); `B_left` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.04 m / 17 deg); `C_backright` 5/10 failed (3 timeout, 2 fell anymal2; closest stop 0.13 m / 10 deg); `D_far_turn` 4/10 failed (4 timeout; closest stop 0.03 m / 30 deg)
- sphere: `C_backright` 1/10 failed (1 timeout; closest stop 0.13 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 timeout; closest stop 0.04 m / 27 deg); `B_left` 7/10 failed (7 timeout; closest stop 0.06 m / 8 deg); `C_backright` 9/10 failed (9 timeout; closest stop 0.04 m / 74 deg); `D_far_turn` 10/10 failed (9 timeout, 1 fell anymal1; closest stop 0.02 m / 36 deg)
- arch: `A_straight` 2/10 failed (2 timeout; closest stop 0.20 m / 4 deg); `B_left` 2/10 failed (2 timeout; closest stop 0.11 m / 0 deg); `C_backright` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.42 m / 3 deg); `D_far_turn` 3/10 failed (3 timeout; closest stop 0.14 m / 5 deg)
- dumbbell: `A_straight` 2/10 failed (2 timeout; closest stop 0.03 m / 8 deg); `C_backright` 5/10 failed (5 timeout; closest stop 0.14 m / 7 deg); `D_far_turn` 7/10 failed (6 timeout, 1 fell anymal1; closest stop 0.46 m / 6 deg)
- t_shape: `A_straight` 1/10 failed (1 timeout; closest stop 0.09 m / 3 deg); `B_left` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.14 m / 1 deg); `C_backright` 3/10 failed (3 timeout; closest stop 0.08 m / 8 deg); `D_far_turn` 4/10 failed (4 timeout; closest stop 0.15 m / 1 deg)
- beam: `A_straight` 9/10 failed (5 timeout, 2 fell anymal2, 2 fell anymal1; closest stop 0.12 m / 6 deg); `B_left` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 0.91 m / 29 deg); `C_backright` 10/10 failed (8 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 1.60 m / 12 deg); `D_far_turn` 10/10 failed (6 timeout, 3 fell anymal1, 1 fell anymal2; closest stop 0.07 m / 1 deg)
- l_shape: `A_straight` 5/10 failed (4 timeout, 1 fell anymal1; closest stop 0.02 m / 26 deg); `B_left` 6/10 failed (5 timeout, 1 fell anymal1; closest stop 0.04 m / 6 deg); `C_backright` 2/10 failed (1 timeout, 1 fell anymal1; closest stop 0.92 m / 8 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.10 m / 11 deg)
- asym: `A_straight` 7/10 failed (5 timeout, 2 fell anymal1; closest stop 0.06 m / 23 deg); `B_left` 9/10 failed (7 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.28 m / 5 deg); `C_backright` 10/10 failed (8 timeout, 2 fell anymal2; closest stop 0.17 m / 33 deg); `D_far_turn` 10/10 failed (6 timeout, 3 fell anymal1, 1 fell anymal2; closest stop 0.27 m / 18 deg)
- u_channel: `B_left` 5/10 failed (5 timeout; closest stop 0.21 m / 28 deg); `C_backright` 7/10 failed (7 timeout; closest stop 0.15 m / 8 deg); `D_far_turn` 7/10 failed (7 timeout; closest stop 0.16 m / 17 deg)
- plus: `A_straight` 7/10 failed (7 timeout; closest stop 0.11 m / 14 deg); `B_left` 5/10 failed (4 timeout, 1 fell anymal2; closest stop 0.13 m / 10 deg); `C_backright` 8/10 failed (6 timeout, 2 fell anymal2; closest stop 0.13 m / 2 deg); `D_far_turn` 8/10 failed (6 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.13 m / 20 deg)

**80 kg**

- cube: `A_straight` 8/10 failed (5 timeout, 3 fell anymal1; closest stop 0.21 m / 0 deg); `B_left` 9/10 failed (7 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.04 m / 6 deg); `C_backright` 8/10 failed (7 timeout, 1 fell anymal2; closest stop 0.16 m / 5 deg); `D_far_turn` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.12 m / 32 deg)
- long: `A_straight` 6/10 failed (6 timeout; closest stop 0.21 m / 0 deg); `B_left` 7/10 failed (5 timeout, 2 fell anymal1; closest stop 0.36 m / 8 deg); `C_backright` 4/10 failed (4 timeout; closest stop 1.71 m / 10 deg); `D_far_turn` 5/10 failed (4 timeout, 1 fell anymal1; closest stop 0.41 m / 47 deg)
- sphere: `B_left` 1/10 failed (1 fell anymal2; closest stop 0.23 m / 0 deg); `C_backright` 1/10 failed (1 timeout; closest stop 3.00 m / 0 deg)
- cylinder: `A_straight` 1/10 failed (1 fell anymal1; closest stop 0.97 m / 9 deg); `B_left` 8/10 failed (8 timeout; closest stop 0.10 m / 8 deg); `C_backright` 10/10 failed (6 timeout, 4 fell anymal1; closest stop 0.05 m / 86 deg); `D_far_turn` 10/10 failed (7 timeout, 2 fell anymal2, 1 fell anymal1; closest stop 0.07 m / 52 deg)
- arch: `A_straight` 2/10 failed (2 timeout; closest stop 0.78 m / 6 deg); `B_left` 4/10 failed (3 timeout, 1 fell anymal1; closest stop 0.17 m / 0 deg); `C_backright` 6/10 failed (4 timeout, 1 fell anymal1, 1 fell anymal2; closest stop 0.15 m / 1 deg); `D_far_turn` 8/10 failed (7 timeout, 1 fell anymal1; closest stop 0.16 m / 0 deg)
- dumbbell: `A_straight` 5/10 failed (4 timeout, 1 fell anymal1; closest stop 0.21 m / 4 deg); `B_left` 8/10 failed (5 timeout, 3 fell anymal1; closest stop 0.16 m / 10 deg); `C_backright` 7/10 failed (6 timeout, 1 fell anymal2; closest stop 0.75 m / 1 deg); `D_far_turn` 8/10 failed (6 timeout, 2 fell anymal1; closest stop 0.15 m / 8 deg)
- t_shape: `A_straight` 6/10 failed (6 timeout; closest stop 0.05 m / 6 deg); `B_left` 7/10 failed (4 timeout, 3 fell anymal1; closest stop 0.12 m / 5 deg); `C_backright` 3/10 failed (3 timeout; closest stop 0.15 m / 24 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.13 m / 11 deg)
- beam: `A_straight` 10/10 failed (6 fell anymal1, 3 timeout, 1 fell anymal2; closest stop 0.98 m / 15 deg); `B_left` 10/10 failed (7 fell anymal1, 3 timeout; closest stop 2.26 m / 12 deg); `C_backright` 10/10 failed (6 fell anymal2, 3 timeout, 1 fell anymal1; closest stop 2.87 m / 57 deg); `D_far_turn` 10/10 failed (5 fell anymal1, 4 timeout, 1 fell anymal2; closest stop 1.76 m / 11 deg)
- l_shape: `A_straight` 10/10 failed (7 timeout, 3 fell anymal1; closest stop 0.03 m / 14 deg); `B_left` 7/10 failed (7 timeout; closest stop 0.12 m / 32 deg); `C_backright` 4/10 failed (4 timeout; closest stop 0.48 m / 0 deg); `D_far_turn` 9/10 failed (8 timeout, 1 fell anymal2; closest stop 0.27 m / 25 deg)
- asym: `A_straight` 10/10 failed (10 timeout; closest stop 0.83 m / 60 deg); `B_left` 10/10 failed (6 fell anymal1, 4 timeout; closest stop 0.39 m / 10 deg); `C_backright` 10/10 failed (7 timeout, 3 fell anymal2; closest stop 2.33 m / 69 deg); `D_far_turn` 10/10 failed (8 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 1.59 m / 45 deg)
- u_channel: `A_straight` 1/10 failed (1 timeout; closest stop 0.18 m / 11 deg); `B_left` 8/10 failed (7 timeout, 1 fell anymal2; closest stop 0.29 m / 22 deg); `C_backright` 5/10 failed (5 timeout; closest stop 0.30 m / 32 deg); `D_far_turn` 10/10 failed (10 timeout; closest stop 0.15 m / 5 deg)
- plus: `A_straight` 7/10 failed (7 timeout; closest stop 0.06 m / 40 deg); `B_left` 4/10 failed (4 timeout; closest stop 0.14 m / 32 deg); `C_backright` 7/10 failed (5 timeout, 1 fell anymal2, 1 fell anymal1; closest stop 0.27 m / 1 deg); `D_far_turn` 7/10 failed (6 timeout, 1 fell anymal2; closest stop 0.12 m / 3 deg)

## Videos

One per mass x object x position: the fastest successful trial, or when none succeeded, the trial that ended closest to the goal (closeness = final distance / task distance + heading error / 180 deg). File name: `<object>_<mass>kg_<position>_rep<trial>__<outcome>.mp4`.

