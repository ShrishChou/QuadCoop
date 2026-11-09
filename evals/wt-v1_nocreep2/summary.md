# Walker acceptance test: wt-v1_nocreep2

Walkers: v1, v1_nocreep2. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use each walker's own k (v1: 1000, v1_nocreep2: 1000 N per m/s; common reference k = 1000) and object friction 0.45.

Checkpoints: v1 = `logs/evals/walker-anymal-v1/model.pt`; v1_nocreep2 = `/home/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-09_00-10-27_v1_nocreep2/model_7997.pt`

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v1: achieved (err) | v1_nocreep2: achieved (err) | v1: fell | v1_nocreep2: fell |
|---|---|---|---|---|---|
| back | -0.05 m/s | +0.004 (0.054) | +0.000 (0.050) | 0.00 | 0.00 |
| back | -0.1 m/s | +0.004 (0.104) | -0.144 (0.044) | 0.00 | 0.00 |
| back | -0.3 m/s | -0.380 (0.080) | -0.350 (0.050) | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.003 (0.017) | -0.000 (0.020) | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.002 (0.048) | -0.001 (0.051) | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.097 (0.003) | +0.088 (0.012) | 0.00 | 0.00 |
| fwd | +0.15 m/s | +0.240 (0.090) | +0.125 (0.025) | 0.00 | 0.00 |
| fwd | +0.2 m/s | +0.290 (0.090) | +0.296 (0.096) | 0.00 | 0.00 |
| fwd | +0.3 m/s | +0.378 (0.078) | +0.379 (0.079) | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.525 (0.025) | +0.521 (0.021) | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.672 (0.028) | +0.677 (0.023) | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.380 (0.080) | +0.374 (0.074) | 0.00 | 0.00 |
| side | +0.05 m/s | +0.002 (0.048) | +0.001 (0.049) | 0.00 | 0.00 |
| side | +0.1 m/s | -0.013 (0.114) | +0.189 (0.089) | 0.00 | 0.00 |
| side | +0.2 m/s | +0.297 (0.097) | +0.315 (0.115) | 0.00 | 0.00 |
| side | +0.4 m/s | +0.485 (0.085) | +0.500 (0.100) | 0.00 | 0.00 |
| stand | +0 m/s | +0.003 (0.003) | -0.000 (0.000) | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.013 (0.037) | -0.001 (0.051) | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.019 (0.081) | +0.048 (0.052) | 0.00 | 0.00 |
| yaw | +0.2 rad/s | +0.009 (0.191) | +0.001 (0.199) | 0.00 | 0.00 |
| yaw | +0.4 rad/s | +0.023 (0.377) | +0.007 (0.393) | 0.00 | 0.00 |

**v1, free walking: FAIL** - small commands moved as asked 8%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v1_nocreep2, free walking: FAIL** - small commands moved as asked 15%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

### Response: time until the 0.4 s average reaches 63% of the command (s, includes ~0.2 s of averaging lag; - = never) / instantaneous sway along the command (std over the measured half)

| case | command | v1: t63 / sway | v1_nocreep2: t63 / sway |
|---|---|---|---|
| back | -0.05 | - / 0.001 | - / 0.000 |
| back | -0.1 | - / 0.000 | 2.85 / 0.049 |
| back | -0.3 | 0.80 / 0.042 | 0.40 / 0.035 |
| fwd | +0.02 | - / 0.001 | - / 0.000 |
| fwd | +0.05 | - / 0.001 | - / 0.000 |
| fwd | +0.1 | 2.44 (1/2) / 0.018 | 0.40 (1/2) / 0.007 |
| fwd | +0.15 | 0.70 / 0.029 | 0.40 (1/2) / 0.013 |
| fwd | +0.2 | 0.68 / 0.026 | 0.40 / 0.013 |
| fwd | +0.3 | 0.40 / 0.023 | 0.40 / 0.017 |
| fwd | +0.5 | 0.40 / 0.034 | 0.40 / 0.028 |
| fwd | +0.7 | 0.40 / 0.043 | 0.40 / 0.033 |
| kicked | +0.3 | 0.40 / 0.081 | 0.40 / 0.062 |
| side | +0.05 | - / 0.000 | - / 0.000 |
| side | +0.1 | - / 0.017 | 1.12 / 0.044 |
| side | +0.2 | 0.79 / 0.066 | 0.40 / 0.043 |
| side | +0.4 | 0.40 / 0.067 | 0.40 / 0.054 |
| yaw | +0.05 | - / 0.009 | - / 0.000 |
| yaw | +0.1 | - / 0.003 | 7.86 (1/2) / 0.029 |
| yaw | +0.2 | - / 0.003 | - / 0.000 |
| yaw | +0.4 | - / 0.003 | - / 0.000 |

## Pressing an immovable cube (force on it along the heading, N; swing = std over time, raw / after a 0.4 s moving average; target k x speed)

### 0 deg

| speed (m/s) | target k=1000 (N) | v1: force (swing raw / 0.4 s), touching | v1_nocreep2: force (swing raw / 0.4 s), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 50 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.1 | 100 | 67 (32 / 10), 0.50 | 45 (15 / 8), 0.46 |
| 0.15 | 150 | 162 (34 / 18), 0.99 | 62 (25 / 6), 0.50 |
| 0.2 | 200 | 145 (47 / 23), 0.97 | 162 (60 / 22), 0.98 |
| 0.25 | 250 | 156 (60 / 18), 0.97 | 183 (84 / 25), 0.98 |
| 0.3 | 300 | 176 (82 / 15), 0.97 | 200 (78 / 16), 0.98 |
| 0.4 | 400 | 184 (76 / 18), 0.93 | 220 (80 / 25), 0.96 |

### 20 deg

| speed (m/s) | target k=1000 (N) | v1: force (swing raw / 0.4 s), touching | v1_nocreep2: force (swing raw / 0.4 s), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0 / 0), 0.00 | 1 (2 / 1), 0.13 |
| 0.05 | 50 | 0 (0 / 0), 0.00 | 19 (8 / 4), 0.43 |
| 0.1 | 100 | 1 (3 / 2), 0.04 | 10 (7 / 1), 0.40 |
| 0.15 | 150 | 86 (56 / 42), 0.91 | 30 (9 / 3), 0.94 |
| 0.2 | 200 | 182 (56 / 38), 0.96 | 178 (74 / 48), 0.94 |
| 0.25 | 250 | 160 (57 / 29), 0.95 | 215 (69 / 20), 0.96 |
| 0.3 | 300 | 159 (67 / 31), 0.93 | 192 (73 / 27), 0.97 |
| 0.4 | 400 | 238 (51 / 27), 0.98 | 197 (94 / 38), 0.97 |

### Why the force stops where it does (square on): share of time any joint is at >= 95% of its 80 Nm limit, mean peak joint torque / limit, foot slip (m/s, feet on the ground), body pitch (deg, + = nose down)

| speed (m/s) | v1: torque-sat, peak torque, slip, pitch | v1_nocreep2: torque-sat, peak torque, slip, pitch |
|---|---|---|
| 0.02 | 0.00, 0.41, 0.008, +2.4 | 0.00, 0.36, 0.003, +4.0 |
| 0.05 | 0.00, 0.37, 0.007, +2.9 | 0.00, 0.35, 0.005, +4.4 |
| 0.1 | 0.00, 0.45, 0.008, +1.2 | 0.00, 0.36, 0.006, +0.9 |
| 0.15 | 0.00, 0.52, 0.013, +0.2 | 0.00, 0.41, 0.007, +1.4 |
| 0.2 | 0.00, 0.47, 0.016, +0.4 | 0.00, 0.55, 0.019, -1.0 |
| 0.25 | 0.00, 0.48, 0.017, +0.7 | 0.00, 0.61, 0.032, -0.7 |
| 0.3 | 0.00, 0.52, 0.029, +0.6 | 0.00, 0.59, 0.018, -0.6 |
| 0.4 | 0.21, 0.86, 0.175, +1.1 | 0.01, 0.71, 0.050, -0.8 |

**v1, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 17%, not rising, steady 33%, touching 73%. (Separate question, not part of the verdict: steady after a 0.4 s average 100%.)
**v1_nocreep2, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 17%, rising, steady 17%, touching 65%. (Separate question, not part of the verdict: steady after a 0.4 s average 100%.)

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k), its own k; 'law' = the same with the force actually measured, max(0, v - (F - 5 N) / k))

| mass | speed cmd | v1: expected (k=1000), law | v1_nocreep2: expected (k=1000), law | v1: robot speed, object speed, force (N), fell | v1_nocreep2: robot speed, object speed, force (N), fell |
|---|---|---|---|---|---|
| 20 kg | 0.1 | 0.01, 0.10 | 0.01, 0.10 | 0.00, 0.00, 0, 0.00 | 0.00, 0.00, 0, 0.00 |
| 20 kg | 0.2 | 0.11, 0.14 | 0.11, 0.12 | 0.23, 0.16, 68, 0.00 | 0.13, 0.13, 84, 0.00 |
| 20 kg | 0.3 | 0.21, 0.26 | 0.21, 0.22 | 0.33, 0.16, 44, 0.00 | 0.23, 0.21, 89, 0.00 |
| 20 kg | 0.5 | 0.41, 0.48 | 0.41, 0.46 | 0.52, 0.13, 26, 0.00 | 0.43, 0.19, 50, 0.00 |
| 40 kg | 0.1 | 0.00, 0.10 | 0.00, 0.10 | 0.00, 0.00, 0, 0.00 | 0.00, 0.00, 0, 0.00 |
| 40 kg | 0.2 | 0.02, 0.05 | 0.02, 0.07 | 0.09, 0.08, 156, 0.00 | 0.01, 0.01, 138, 0.00 |
| 40 kg | 0.3 | 0.12, 0.17 | 0.12, 0.14 | 0.27, 0.18, 134, 0.00 | 0.11, 0.10, 167, 0.00 |
| 40 kg | 0.5 | 0.32, 0.39 | 0.32, 0.33 | 0.45, 0.24, 116, 0.00 | 0.24, 0.23, 178, 0.00 |
| 80 kg | 0.1 | 0.00, 0.10 | 0.00, 0.10 | 0.00, 0.00, 0, 0.00 | 0.00, 0.00, 0, 0.00 |
| 80 kg | 0.2 | 0.00, 0.04 | 0.00, 0.03 | -0.00, 0.00, 167, 0.00 | -0.00, 0.00, 174, 0.00 |
| 80 kg | 0.3 | 0.00, 0.12 | 0.00, 0.10 | 0.00, 0.00, 182, 0.00 | -0.00, 0.00, 207, 0.00 |
| 80 kg | 0.5 | 0.15, 0.30 | 0.15, 0.28 | 0.01, 0.00, 210, 0.00 | 0.01, 0.01, 227, 0.00 |

**v1, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 42%, worst fall rate 0.00. (Separate question: consistent with its own measured force 25%.)
**v1_nocreep2, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 83%, worst fall rate 0.00. (Separate question: consistent with its own measured force 42%.)

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v1 | FAIL | FAIL | FAIL |
| v1_nocreep2 | FAIL | FAIL | FAIL |
