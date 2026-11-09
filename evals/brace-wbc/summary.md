# Brace press check with whole-body balance: evals/brace-wbc

CPU MuJoCo, one ANYmal C, feet planted, no stepping, no learning. Every 0.01 s the min-peak-torque LP (scripts/brace_posture_search.py) is solved at the current state for the push plus a base balance wrench (PD on base pose); the training PD actuators deliver the torques; a slow integral closes the loop on the measured wall force. Each level 2.5 s, measured over the second half. Swing = std of the force, raw / after a 0.4 s average (as evals/wt-v22k). Contact models: **train** = the walker env (pyramidal cone, impratio 1: loaded feet creep, evals/contact-creep), **nocreep** = elliptic cone, impratio 10 (same foot solimp).

- **nominal**: height 0.53 m, pitch 0.0 deg (- = nose up), front feet +0.0 m, hind feet -0.0 m, 0.0 m wider; LP peak torque at 250 N: 27 Nm
- **feasible**: height 0.5 m, pitch 0.0 deg (- = nose up), front feet -0.15 m, hind feet -0.15 m, 0.05 m wider; LP peak torque at 250 N: 16 Nm

## Immovable wall, foot friction 0.6 (LP friction-cone ceiling about 245 N)

| desired (N) | nominal / train: force (swing raw / 0.4 s), torque-sat, slip m/s | feasible / train: force (swing raw / 0.4 s), torque-sat, slip m/s | nominal / nocreep: force (swing raw / 0.4 s), torque-sat, slip m/s | feasible / nocreep: force (swing raw / 0.4 s), torque-sat, slip m/s |
|---|---|---|---|---|
| 50 | 27 (19 / 9), 0.00, 0.066 | 1 (3 / 1), 0.00, 0.045 | 51 (0 / 0), 0.00, 0.003 | 51 (1 / 0), 0.00, 0.005 |
| 100 | 0 (1 / 0), 0.00, 0.009 | 2 (7 / 1), 0.00, 0.023 | 100 (0 / 0), 0.00, 0.005 | 100 (0 / 0), 0.00, 0.008 |
| 150 | 53 (13 / 4), 0.00, 0.087 | 10 (15 / 2), 0.00, 0.019 | 150 (0 / 0), 0.00, 0.008 | 150 (0 / 0), 0.00, 0.009 |
| 200 | 0 (0 / 0), nan, nan FELL | 10 (14 / 1), 0.00, 0.027 | 200 (0 / 0), 0.00, 0.011 | 189 (2 / 2), 0.00, 0.012 |
| 250 | not reached (fell earlier) | 0 (0 / 0), nan, nan FELL | 25 (52 / 52), 0.00, 0.053 FELL | 0 (0 / 0), nan, nan FELL |
| 300 | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) |
| 350 | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) |
| 400 | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) |

## Immovable wall, foot friction 0.8 (LP friction-cone ceiling about 326 N)

| desired (N) | nominal / train: force (swing raw / 0.4 s), torque-sat, slip m/s | feasible / train: force (swing raw / 0.4 s), torque-sat, slip m/s | nominal / nocreep: force (swing raw / 0.4 s), torque-sat, slip m/s | feasible / nocreep: force (swing raw / 0.4 s), torque-sat, slip m/s |
|---|---|---|---|---|
| 50 | 39 (12 / 6), 0.00, 0.065 | 2 (5 / 1), 0.00, 0.046 | 51 (0 / 0), 0.00, 0.003 | 51 (1 / 0), 0.00, 0.005 |
| 100 | 1 (2 / 0), 0.00, 0.016 | 0 (0 / 0), 0.00, 0.010 | 100 (0 / 0), 0.00, 0.005 | 100 (0 / 0), 0.00, 0.008 |
| 150 | 0 (0 / 0), 0.00, 0.001 | 0 (0 / 0), 0.00, 0.001 | 150 (0 / 0), 0.00, 0.008 | 150 (0 / 0), 0.00, 0.010 |
| 200 | 0 (0 / 0), 0.00, 0.000 | 20 (23 / 1), 0.00, 0.031 | 200 (0 / 0), 0.00, 0.011 | 188 (1 / 0), 0.00, 0.011 |
| 250 | 82 (52 / 4), 0.00, 0.112 | 39 (37 / 15), 0.51, 0.067 | 251 (0 / 0), 0.00, 0.014 | 232 (3 / 2), 0.00, 0.013 |
| 300 | 0 (0 / 0), nan, nan FELL | 0 (0 / 0), nan, nan FELL | 294 (22 / 7), 0.00, 0.018 | 246 (7 / 5), 0.00, 0.016 |
| 350 | not reached (fell earlier) | not reached (fell earlier) | 138 (303 / 303), 0.03, 1.097 FELL | 0 (0 / 0), nan, nan FELL |
| 400 | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) | not reached (fell earlier) |

## Immovable wall, foot friction 1.0 (LP friction-cone ceiling about 408 N)

| desired (N) | nominal / train: force (swing raw / 0.4 s), torque-sat, slip m/s | feasible / train: force (swing raw / 0.4 s), torque-sat, slip m/s | nominal / nocreep: force (swing raw / 0.4 s), torque-sat, slip m/s | feasible / nocreep: force (swing raw / 0.4 s), torque-sat, slip m/s |
|---|---|---|---|---|
| 50 | 46 (4 / 3), 0.00, 0.059 | 3 (6 / 2), 0.00, 0.046 | 51 (0 / 0), 0.00, 0.003 | 51 (1 / 0), 0.00, 0.005 |
| 100 | 3 (4 / 1), 0.00, 0.021 | 0 (0 / 0), 0.00, 0.014 | 100 (0 / 0), 0.00, 0.005 | 100 (0 / 0), 0.00, 0.008 |
| 150 | 0 (0 / 0), 0.00, 0.003 | 0 (0 / 0), 0.00, 0.002 | 150 (0 / 0), 0.00, 0.008 | 150 (0 / 0), 0.00, 0.010 |
| 200 | 0 (0 / 0), 0.00, 0.000 | 9 (24 / 1), 0.00, 0.034 | 200 (0 / 0), 0.00, 0.011 | 186 (0 / 0), 0.00, 0.011 |
| 250 | 0 (0 / 0), 0.00, 0.000 | 24 (32 / 6), 0.00, 0.032 | 251 (0 / 0), 0.00, 0.014 | 204 (14 / 10), 0.00, 0.013 |
| 300 | 0 (0 / 0), 0.00, 0.000 | 0 (0 / 0), nan, nan FELL | 292 (22 / 8), 0.00, 0.018 | 169 (12 / 8), 0.00, 0.013 |
| 350 | 76 (11 / 8), 0.00, 0.078 | not reached (fell earlier) | 334 (2 / 1), 0.00, 0.018 | 162 (6 / 4), 0.00, 0.014 |
| 400 | 0 (0 / 0), nan, nan FELL | not reached (fell earlier) | 356 (13 / 10), 0.00, 0.021 | 185 (3 / 2), 0.00, 0.015 |

## Holds (within 15% of the target, 0.4 s swing under 15%, touching >= 95%, no fall)

- **nominal / train, foot mu 0.6**: none; fell at the 200 N level
- **feasible / train, foot mu 0.6**: none; fell at the 250 N level
- **nominal / nocreep, foot mu 0.6**: 50, 100, 150, 200 N; fell at the 250 N level
- **feasible / nocreep, foot mu 0.6**: 50, 100, 150, 200 N; fell at the 250 N level
- **nominal / train, foot mu 0.8**: none; fell at the 300 N level
- **feasible / train, foot mu 0.8**: none; fell at the 300 N level
- **nominal / nocreep, foot mu 0.8**: 50, 100, 150, 200, 250, 300 N; fell at the 350 N level
- **feasible / nocreep, foot mu 0.8**: 50, 100, 150, 200, 250 N; fell at the 350 N level
- **nominal / train, foot mu 1.0**: 50 N; fell at the 400 N level
- **feasible / train, foot mu 1.0**: none; fell at the 300 N level
- **nominal / nocreep, foot mu 1.0**: 50, 100, 150, 200, 250, 300, 350, 400 N
- **feasible / nocreep, foot mu 1.0**: 50, 100, 150, 200 N

## The wall gives way while pressing 200 N (foot friction 0.8; the robot cannot step)

| wall speed (m/s) | posture / contact | force before (N) | force during give-way (N) | touching during | fell | base moved (m) |
|---|---|---|---|---|---|---|
| 0.05 | nominal / train | 11 | 0 | 0.0 | False | 0.07 |
| 0.05 | feasible / train | 16 | 0 | 0.0 | False | 0.03 |
| 0.05 | nominal / nocreep | 200 | 220 | 0.5 | False | 0.16 |
| 0.05 | feasible / nocreep | 200 | 92 | 0.28 | False | 0.15 |
| 0.2 | nominal / train | 11 | 0 | 0.0 | False | 0.07 |
| 0.2 | feasible / train | 16 | 0 | 0.0 | False | 0.03 |
| 0.2 | nominal / nocreep | 200 | 13 | 0.01 | True | 0.46 |
| 0.2 | feasible / nocreep | 200 | 0 | 0.0 | True | 0.31 |
