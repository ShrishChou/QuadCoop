# Walker acceptance test: wt-nocreep

Walkers: v1, v22, v22k. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use each walker's own k (v1: 1000, v22: 500, v22k: 1000 N per m/s; common reference k = 1000) and object friction 0.45.

Checkpoints: v1 = `logs/evals/walker-anymal-v1/model.pt`; v22 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt`; v22k = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_14-39-28_v22_k1000/model_10496.pt`

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v1: achieved (err) | v22: achieved (err) | v22k: achieved (err) | v1: fell | v22: fell | v22k: fell |
|---|---|---|---|---|---|---|---|
| back | -0.05 m/s | +0.004 (0.054) | -0.002 (0.048) | -0.000 (0.050) | 0.00 | 0.00 | 0.00 |
| back | -0.1 m/s | +0.004 (0.104) | -0.002 (0.098) | -0.002 (0.098) | 0.00 | 0.00 | 0.00 |
| back | -0.3 m/s | -0.380 (0.080) | -0.354 (0.054) | -0.308 (0.008) | 0.00 | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.003 (0.017) | +0.001 (0.019) | +0.000 (0.020) | 0.00 | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.002 (0.048) | +0.001 (0.049) | +0.001 (0.050) | 0.00 | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.097 (0.003) | +0.005 (0.095) | +0.000 (0.100) | 0.00 | 0.00 | 0.00 |
| fwd | +0.15 m/s | +0.240 (0.090) | +0.091 (0.059) | +0.015 (0.135) | 0.00 | 1.00 | 0.00 |
| fwd | +0.2 m/s | +0.290 (0.090) | +0.254 (0.054) | +0.125 (0.075) | 0.00 | 0.50 | 0.00 |
| fwd | +0.3 m/s | +0.378 (0.078) | +0.292 (0.008) | +0.280 (0.020) | 0.00 | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.525 (0.025) | +0.476 (0.024) | +0.452 (0.048) | 0.00 | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.672 (0.028) | +0.711 (0.011) | +0.635 (0.065) | 0.00 | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.380 (0.080) | +0.289 (0.011) | +0.273 (0.027) | 0.00 | 0.00 | 0.00 |
| side | +0.05 m/s | +0.002 (0.048) | +0.003 (0.047) | +0.001 (0.049) | 0.00 | 0.00 | 0.00 |
| side | +0.1 m/s | -0.013 (0.114) | +0.024 (0.076) | +0.030 (0.070) | 0.00 | 0.00 | 0.00 |
| side | +0.2 m/s | +0.297 (0.097) | +0.176 (0.024) | +0.159 (0.041) | 0.00 | 0.00 | 0.00 |
| side | +0.4 m/s | +0.485 (0.085) | +0.318 (0.082) | +0.365 (0.035) | 0.00 | 0.00 | 0.00 |
| stand | +0 m/s | +0.003 (0.003) | +0.000 (0.000) | -0.000 (0.000) | 0.00 | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.013 (0.037) | +0.001 (0.049) | +0.000 (0.050) | 0.00 | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.019 (0.081) | +0.006 (0.094) | +0.002 (0.098) | 0.00 | 0.00 | 0.00 |
| yaw | +0.2 rad/s | +0.009 (0.191) | +0.051 (0.149) | +0.066 (0.134) | 0.00 | 0.00 | 0.00 |
| yaw | +0.4 rad/s | +0.023 (0.377) | +0.134 (0.266) | +0.030 (0.370) | 0.00 | 0.00 | 0.00 |

**v1, free walking: FAIL** - small commands moved as asked 8%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v22, free walking: FAIL** - small commands moved as asked 15%, normal commands within 0.1 m/s 83%, worst fall rate 1.00.
**v22k, free walking: FAIL** - small commands moved as asked 8%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

### Response: time until the 0.4 s average reaches 63% of the command (s, includes ~0.2 s of averaging lag; - = never) / instantaneous sway along the command (std over the measured half)

| case | command | v1: t63 / sway | v22: t63 / sway | v22k: t63 / sway |
|---|---|---|---|---|
| back | -0.05 | - / 0.001 | - / 0.001 | - / 0.000 |
| back | -0.1 | - / 0.000 | - / 0.001 | - / 0.002 |
| back | -0.3 | 0.80 / 0.042 | 0.40 / 0.062 | 0.40 / 0.082 |
| fwd | +0.02 | - / 0.001 | - / 0.000 | - / 0.000 |
| fwd | +0.05 | - / 0.001 | - / 0.000 | - / 0.004 |
| fwd | +0.1 | 2.44 (1/2) / 0.018 | - / 0.012 | - / 0.028 |
| fwd | +0.15 | 0.70 / 0.029 | 6.68 (1/2) / 0.112 | - / 0.043 |
| fwd | +0.2 | 0.68 / 0.026 | 0.41 / 0.064 | 0.40 (1/2) / 0.057 |
| fwd | +0.3 | 0.40 / 0.023 | 0.40 / 0.041 | 0.40 / 0.036 |
| fwd | +0.5 | 0.40 / 0.034 | 0.42 / 0.079 | 0.40 / 0.061 |
| fwd | +0.7 | 0.40 / 0.043 | 0.44 / 0.105 | 0.41 / 0.085 |
| kicked | +0.3 | 0.40 / 0.081 | 3.01 / 0.068 | 3.14 / 0.071 |
| side | +0.05 | - / 0.000 | - / 0.011 | - / 0.000 |
| side | +0.1 | - / 0.017 | - / 0.026 | - / 0.028 |
| side | +0.2 | 0.79 / 0.066 | 3.96 / 0.065 | 6.77 / 0.067 |
| side | +0.4 | 0.40 / 0.067 | 7.86 (1/2) / 0.170 | 0.40 / 0.111 |
| yaw | +0.05 | - / 0.009 | - / 0.001 | - / 0.000 |
| yaw | +0.1 | - / 0.003 | - / 0.002 | - / 0.001 |
| yaw | +0.2 | - / 0.003 | - / 0.052 | - / 0.040 |
| yaw | +0.4 | - / 0.003 | 7.76 (1/2) / 0.119 | - / 0.099 |

## Pressing an immovable cube (force on it along the heading, N; swing = std over time, raw / after a 0.4 s moving average; target k x speed)

### 0 deg

| speed (m/s) | target k=500 (N) | target k=1000 (N) | v1: force (swing raw / 0.4 s), touching | v22: force (swing raw / 0.4 s), touching | v22k: force (swing raw / 0.4 s), touching |
|---|---|---|---|---|---|
| 0.02 | 10 | 20 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 25 | 50 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.1 | 50 | 100 | 68 (31 / 8), 0.50 | 0 (0 / 0), 0.00 | 1 (3 / 2), 0.05 |
| 0.15 | 75 | 150 | 160 (32 / 16), 1.00 | 55 (8 / 2), 0.97 | 62 (14 / 7), 0.98 |
| 0.2 | 100 | 200 | 141 (49 / 26), 0.95 | 64 (7 / 2), 0.98 | 54 (50 / 16), 0.81 |
| 0.25 | 125 | 250 | 171 (85 / 17), 0.93 | 114 (58 / 23), 0.84 | 94 (125 / 42), 0.62 |
| 0.3 | 150 | 300 | 195 (95 / 22), 0.98 | 123 (55 / 12), 0.90 | 118 (140 / 32), 0.67 |
| 0.4 | 200 | 400 | 153 (84 / 34), 0.87 | 119 (50 / 14), 0.92 | 116 (118 / 32), 0.71 |

### 20 deg

| speed (m/s) | target k=500 (N) | target k=1000 (N) | v1: force (swing raw / 0.4 s), touching | v22: force (swing raw / 0.4 s), touching | v22k: force (swing raw / 0.4 s), touching |
|---|---|---|---|---|---|
| 0.02 | 10 | 20 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 25 | 50 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.1 | 50 | 100 | 0 (3 / 1), 0.02 | 16 (20 / 5), 0.73 | 41 (10 / 3), 0.96 |
| 0.15 | 75 | 150 | 81 (60 / 42), 0.87 | 54 (0 / 0), 1.00 | 65 (14 / 5), 0.96 |
| 0.2 | 100 | 200 | 181 (56 / 39), 0.96 | 45 (32 / 7), 0.83 | 67 (19 / 5), 0.95 |
| 0.25 | 125 | 250 | 173 (86 / 48), 0.89 | 79 (23 / 13), 0.97 | 92 (94 / 37), 0.77 |
| 0.3 | 150 | 300 | 146 (82 / 39), 0.84 | 124 (26 / 7), 0.99 | 112 (109 / 36), 0.73 |
| 0.4 | 200 | 400 | 221 (74 / 29), 0.96 | 131 (36 / 13), 0.97 | 104 (129 / 32), 0.71 |

### Why the force stops where it does (square on): share of time any joint is at >= 95% of its 80 Nm limit, mean peak joint torque / limit, foot slip (m/s, feet on the ground), body pitch (deg, + = nose down)

| speed (m/s) | v1: torque-sat, peak torque, slip, pitch | v22: torque-sat, peak torque, slip, pitch | v22k: torque-sat, peak torque, slip, pitch |
|---|---|---|---|
| 0.02 | 0.00, 0.41, 0.008, +2.4 | 1.00, 1.00, 0.001, +6.7 | 1.00, 1.00, 0.000, +8.4 |
| 0.05 | 0.00, 0.37, 0.007, +2.9 | 1.00, 1.00, 0.002, +8.3 | 1.00, 1.00, 0.003, +8.2 |
| 0.1 | 0.00, 0.45, 0.008, +1.2 | 1.00, 1.00, 0.007, +7.1 | 1.00, 1.00, 0.007, +7.2 |
| 0.15 | 0.00, 0.52, 0.013, +0.2 | 1.00, 1.00, 0.005, +3.8 | 1.00, 1.00, 0.007, +3.6 |
| 0.2 | 0.00, 0.47, 0.015, +0.5 | 1.00, 1.00, 0.005, +4.6 | 1.00, 1.00, 0.016, +1.6 |
| 0.25 | 0.03, 0.56, 0.066, +0.1 | 0.99, 1.00, 0.045, +4.0 | 1.00, 1.00, 0.110, +3.7 |
| 0.3 | 0.03, 0.53, 0.031, +0.6 | 1.00, 1.00, 0.028, +2.2 | 1.00, 1.00, 0.100, +3.4 |
| 0.4 | 0.27, 0.83, 0.082, +1.4 | 1.00, 1.00, 0.025, +2.6 | 0.98, 1.00, 0.100, +3.6 |

**v1, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 17%, not rising, steady 33%, touching 73%. (Separate question, not part of the verdict: steady after a 0.4 s average 100%.)
**v22, force control (square on, 0.05-0.3 m/s, k = 500): FAIL** - within 25% of k x speed 33%, rising, steady 67%, touching 61%. (Separate question, not part of the verdict: steady after a 0.4 s average 100%.)
**v22k, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 0%, rising, steady 33%, touching 52%. (Separate question, not part of the verdict: steady after a 0.4 s average 33%.)

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k), its own k; 'law' = the same with the force actually measured, max(0, v - (F - 5 N) / k))

| mass | speed cmd | v1: expected (k=1000), law | v22: expected (k=500), law | v22k: expected (k=1000), law | v1: robot speed, object speed, force (N), fell | v22: robot speed, object speed, force (N), fell | v22k: robot speed, object speed, force (N), fell |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.1 | 0.01, 0.10 | 0.00, 0.10 | 0.01, 0.08 | 0.00, 0.00, 0, 0.00 | 0.01, 0.00, 0, 0.00 | 0.00, 0.00, 26, 0.00 |
| 20 kg | 0.2 | 0.11, 0.13 | 0.02, 0.12 | 0.11, 0.14 | 0.22, 0.17, 71, 0.00 | 0.00, 0.00, 46, 0.00 | 0.00, 0.00, 69, 0.00 |
| 20 kg | 0.3 | 0.21, 0.26 | 0.12, 0.15 | 0.21, 0.22 | 0.32, 0.16, 46, 0.00 | 0.21, 0.21, 82, 0.00 | 0.29, 0.29, 86, 0.00 |
| 20 kg | 0.5 | 0.41, 0.49 | 0.32, 0.34 | 0.41, 0.42 | 0.53, 0.11, 19, 0.00 | 0.38, 0.38, 84, 0.00 | 0.49, 0.49, 87, 0.00 |
| 40 kg | 0.1 | 0.00, 0.10 | 0.00, 0.10 | 0.00, 0.08 | 0.00, 0.00, 0, 0.00 | 0.01, 0.00, 0, 0.00 | 0.00, 0.00, 28, 0.00 |
| 40 kg | 0.2 | 0.02, 0.10 | 0.00, 0.12 | 0.02, 0.13 | 0.05, 0.04, 107, 0.00 | 0.00, 0.00, 43, 0.00 | 0.01, 0.01, 79, 0.00 |
| 40 kg | 0.3 | 0.12, 0.17 | 0.00, 0.10 | 0.12, 0.16 | 0.27, 0.17, 132, 0.00 | 0.01, 0.01, 106, 0.00 | 0.12, 0.11, 141, 0.00 |
| 40 kg | 0.5 | 0.32, 0.41 | 0.15, 0.32 | 0.32, 0.35 | 0.47, 0.19, 99, 0.00 | 0.01, 0.01, 93, 0.00 | 0.20, 0.19, 158, 0.00 |
| 80 kg | 0.1 | 0.00, 0.10 | 0.00, 0.10 | 0.00, 0.08 | 0.00, 0.00, 0, 0.00 | 0.01, 0.00, 0, 0.00 | 0.00, 0.00, 28, 0.00 |
| 80 kg | 0.2 | 0.00, 0.03 | 0.00, 0.12 | 0.00, 0.13 | -0.00, 0.00, 170, 0.00 | 0.00, 0.00, 43, 0.00 | 0.00, 0.00, 71, 0.00 |
| 80 kg | 0.3 | 0.00, 0.13 | 0.00, 0.05 | 0.00, 0.19 | -0.00, 0.00, 176, 0.00 | 0.00, 0.00, 128, 0.00 | 0.08, 0.01, 120, 0.00 |
| 80 kg | 0.5 | 0.15, 0.29 | 0.00, 0.22 | 0.15, 0.37 | 0.00, 0.00, 214, 0.00 | 0.00, 0.00, 146, 0.00 | 0.07, 0.01, 131, 0.00 |

**v1, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 50%, worst fall rate 0.00. (Separate question: consistent with its own measured force 25%.)
**v22, pushing objects (k = 500): FAIL** - speed within 0.05 m/s of the compliant expectation 75%, worst fall rate 0.00. (Separate question: consistent with its own measured force 8%.)
**v22k, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 50%, worst fall rate 0.00. (Separate question: consistent with its own measured force 8%.)

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v1 | FAIL | FAIL | FAIL |
| v22 | FAIL | FAIL | FAIL |
| v22k | FAIL | FAIL | FAIL |
