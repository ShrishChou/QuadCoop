# Walker acceptance test: wt-v22k

Walkers: v21, v22, v22k. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use each walker's own k (v21: 1000, v22: 500, v22k: 1000 N per m/s; common reference k = 1000) and object friction 0.45.

Checkpoints: v21 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_03-50-04_v21/model_5998.pt`; v22 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt`; v22k = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_14-39-28_v22_k1000/model_10496.pt`

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v21: achieved (err) | v22: achieved (err) | v22k: achieved (err) | v21: fell | v22: fell | v22k: fell |
|---|---|---|---|---|---|---|---|
| back | -0.05 m/s | +0.001 (0.051) | -0.001 (0.049) | -0.006 (0.044) | 0.00 | 0.00 | 0.00 |
| back | -0.1 m/s | -0.024 (0.076) | -0.107 (0.007) | -0.078 (0.022) | 0.00 | 0.00 | 0.00 |
| back | -0.3 m/s | -0.362 (0.062) | -0.321 (0.021) | -0.321 (0.021) | 0.00 | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.011 (0.009) | +0.001 (0.019) | +0.000 (0.020) | 0.00 | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.017 (0.033) | +0.000 (0.050) | +0.001 (0.049) | 0.00 | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.088 (0.012) | +0.083 (0.017) | +0.069 (0.031) | 0.00 | 0.00 | 0.00 |
| fwd | +0.15 m/s | +0.153 (0.003) | +0.191 (0.041) | +0.138 (0.012) | 0.00 | 0.00 | 0.00 |
| fwd | +0.2 m/s | +0.204 (0.004) | +0.240 (0.040) | +0.214 (0.014) | 0.00 | 0.00 | 0.00 |
| fwd | +0.3 m/s | +0.323 (0.023) | +0.252 (0.048) | +0.283 (0.017) | 0.00 | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.516 (0.016) | +0.440 (0.060) | +0.454 (0.046) | 0.00 | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.712 (0.012) | +0.622 (0.078) | +0.656 (0.044) | 0.00 | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.311 (0.012) | +0.272 (0.028) | +0.280 (0.020) | 0.00 | 0.00 | 0.00 |
| side | +0.05 m/s | +0.006 (0.044) | +0.043 (0.007) | +0.009 (0.041) | 0.00 | 0.00 | 0.00 |
| side | +0.1 m/s | +0.031 (0.069) | +0.127 (0.027) | +0.077 (0.023) | 0.00 | 0.00 | 0.00 |
| side | +0.2 m/s | +0.088 (0.112) | +0.221 (0.021) | +0.252 (0.052) | 0.00 | 0.00 | 0.00 |
| side | +0.4 m/s | +0.316 (0.084) | +0.382 (0.018) | +0.425 (0.025) | 0.00 | 0.00 | 0.00 |
| stand | +0 m/s | +0.006 (0.006) | +0.001 (0.001) | -0.000 (0.000) | 0.00 | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.005 (0.045) | +0.002 (0.048) | +0.000 (0.050) | 0.00 | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.040 (0.060) | +0.008 (0.092) | +0.012 (0.088) | 0.00 | 0.00 | 0.00 |
| yaw | +0.2 rad/s | +0.041 (0.159) | +0.158 (0.042) | +0.132 (0.068) | 0.00 | 0.00 | 0.00 |
| yaw | +0.4 rad/s | +0.031 (0.369) | +0.335 (0.065) | +0.283 (0.117) | 0.00 | 0.00 | 0.00 |

**v21, free walking: FAIL** - small commands moved as asked 31%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v22, free walking: FAIL** - small commands moved as asked 62%, normal commands within 0.1 m/s 100%, worst fall rate 0.00.
**v22k, free walking: FAIL** - small commands moved as asked 38%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

### Response: time until the 0.4 s average reaches 63% of the command (s, includes ~0.2 s of averaging lag; - = never) / instantaneous sway along the command (std over the measured half)

| case | command | v21: t63 / sway | v22: t63 / sway | v22k: t63 / sway |
|---|---|---|---|---|
| back | -0.05 | - / 0.000 | - / 0.000 | - / 0.015 |
| back | -0.1 | - / 0.019 | 3.99 / 0.036 | 6.58 (1/2) / 0.058 |
| back | -0.3 | 0.40 / 0.049 | 0.40 / 0.044 | 0.40 / 0.045 |
| fwd | +0.02 | - / 0.014 | - / 0.001 | - / 0.000 |
| fwd | +0.05 | - / 0.023 | - / 0.003 | - / 0.002 |
| fwd | +0.1 | 7.90 (1/2) / 0.033 | 1.36 / 0.013 | 7.98 (1/2) / 0.069 |
| fwd | +0.15 | 0.57 / 0.027 | 0.41 / 0.037 | 4.15 / 0.045 |
| fwd | +0.2 | 0.52 / 0.018 | 0.40 / 0.028 | 0.40 / 0.042 |
| fwd | +0.3 | 0.45 / 0.026 | 0.40 / 0.031 | 0.40 / 0.031 |
| fwd | +0.5 | 0.43 / 0.031 | 0.41 / 0.053 | 0.40 / 0.053 |
| fwd | +0.7 | 0.71 / 0.038 | 0.48 / 0.067 | 0.47 / 0.074 |
| kicked | +0.3 | 3.10 / 0.086 | 2.96 / 0.064 | 2.98 / 0.069 |
| side | +0.05 | - / 0.015 | 1.84 / 0.011 | 7.72 (1/2) / 0.013 |
| side | +0.1 | 7.68 (1/2) / 0.028 | 0.95 / 0.026 | 7.30 (1/2) / 0.025 |
| side | +0.2 | - / 0.040 | 0.40 / 0.041 | 0.40 / 0.042 |
| side | +0.4 | 7.86 (1/2) / 0.134 | 0.40 / 0.044 | 0.40 / 0.062 |
| yaw | +0.05 | - / 0.011 | - / 0.001 | - / 0.000 |
| yaw | +0.1 | 6.99 / 0.039 | - / 0.003 | - / 0.004 |
| yaw | +0.2 | - / 0.031 | 7.22 (1/2) / 0.061 | 7.74 / 0.042 |
| yaw | +0.4 | - / 0.024 | 3.85 / 0.096 | 7.78 / 0.095 |

## Pressing an immovable cube (force on it along the heading, N; swing = std over time, raw / after a 0.4 s moving average; target k x speed)

### 0 deg

| speed (m/s) | target k=500 (N) | target k=1000 (N) | v21: force (swing raw / 0.4 s), touching | v22: force (swing raw / 0.4 s), touching | v22k: force (swing raw / 0.4 s), touching |
|---|---|---|---|---|---|
| 0.02 | 10 | 20 | 2 (4 / 3), 0.15 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 25 | 50 | 2 (8 / 2), 0.06 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.1 | 50 | 100 | 151 (80 / 39), 0.86 | 16 (14 / 4), 0.64 | 37 (30 / 7), 0.72 |
| 0.15 | 75 | 150 | 147 (89 / 31), 0.81 | 40 (35 / 9), 0.72 | 56 (40 / 11), 0.81 |
| 0.2 | 100 | 200 | 166 (80 / 27), 0.87 | 50 (41 / 12), 0.76 | 66 (85 / 20), 0.67 |
| 0.25 | 125 | 250 | 155 (96 / 22), 0.80 | 64 (75 / 30), 0.60 | 66 (116 / 41), 0.44 |
| 0.3 | 150 | 300 | 169 (90 / 25), 0.86 | 87 (123 / 43), 0.42 | 78 (108 / 33), 0.64 |
| 0.4 | 200 | 400 | 137 (106 / 39), 0.76 | 79 (115 / 40), 0.58 | 70 (80 / 25), 0.71 |

### 20 deg

| speed (m/s) | target k=500 (N) | target k=1000 (N) | v21: force (swing raw / 0.4 s), touching | v22: force (swing raw / 0.4 s), touching | v22k: force (swing raw / 0.4 s), touching |
|---|---|---|---|---|---|
| 0.02 | 10 | 20 | 3 (9 / 3), 0.07 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 25 | 50 | 34 (34 / 21), 0.33 | 0 (0 / 0), 0.00 | 3 (7 / 3), 0.19 |
| 0.1 | 50 | 100 | 102 (85 / 46), 0.73 | 14 (16 / 5), 0.53 | 43 (36 / 8), 0.69 |
| 0.15 | 75 | 150 | 131 (91 / 31), 0.77 | 45 (42 / 9), 0.68 | 60 (44 / 12), 0.78 |
| 0.2 | 100 | 200 | 161 (88 / 27), 0.83 | 49 (46 / 14), 0.68 | 71 (95 / 28), 0.64 |
| 0.25 | 125 | 250 | 159 (101 / 26), 0.80 | 50 (54 / 16), 0.56 | 63 (90 / 32), 0.66 |
| 0.3 | 150 | 300 | 168 (92 / 30), 0.85 | 100 (93 / 19), 0.67 | 78 (80 / 24), 0.77 |
| 0.4 | 200 | 400 | 175 (98 / 26), 0.85 | 89 (121 / 35), 0.57 | 41 (44 / 14), 0.40 |

### Why the force stops where it does (square on): share of time any joint is at >= 95% of its 80 Nm limit, mean peak joint torque / limit, foot slip (m/s, feet on the ground), body pitch (deg, + = nose down)

| speed (m/s) | v21: torque-sat, peak torque, slip, pitch | v22: torque-sat, peak torque, slip, pitch | v22k: torque-sat, peak torque, slip, pitch |
|---|---|---|---|
| 0.02 | 0.34, 0.85, 0.016, +8.4 | 1.00, 1.00, 0.001, +7.9 | 1.00, 1.00, 0.000, +8.4 |
| 0.05 | 0.00, 0.54, 0.017, +5.7 | 0.37, 0.78, 0.018, +8.2 | 1.00, 1.00, 0.004, +8.0 |
| 0.1 | 0.78, 0.96, 0.220, +8.4 | 0.99, 1.00, 0.053, +7.2 | 1.00, 1.00, 0.065, +5.7 |
| 0.15 | 0.78, 0.95, 0.270, +9.2 | 0.86, 0.98, 0.091, +4.0 | 1.00, 1.00, 0.100, +2.9 |
| 0.2 | 0.83, 0.96, 0.313, +8.6 | 0.46, 0.93, 0.100, +1.9 | 1.00, 1.00, 0.135, +2.2 |
| 0.25 | 0.80, 0.95, 0.425, +8.2 | 0.35, 0.90, 0.182, +1.6 | 1.00, 1.00, 0.238, +2.5 |
| 0.3 | 0.89, 0.97, 0.292, +7.5 | 0.78, 0.96, 0.201, +3.1 | 1.00, 1.00, 0.234, +2.5 |
| 0.4 | 0.91, 0.99, 0.372, +5.2 | 0.96, 0.99, 0.275, +3.2 | 1.00, 1.00, 0.285, +2.6 |

**v21, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 33%, not rising, steady 0%, touching 71%. (Separate question, not part of the verdict: steady after a 0.4 s average 67%.)
**v22, force control (square on, 0.05-0.3 m/s, k = 500): FAIL** - within 25% of k x speed 0%, rising, steady 17%, touching 52%. (Separate question, not part of the verdict: steady after a 0.4 s average 50%.)
**v22k, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 0%, rising, steady 17%, touching 55%. (Separate question, not part of the verdict: steady after a 0.4 s average 50%.)

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k), its own k; 'law' = the same with the force actually measured, max(0, v - (F - 5 N) / k))

| mass | speed cmd | v21: expected (k=1000), law | v22: expected (k=500), law | v22k: expected (k=1000), law | v21: robot speed, object speed, force (N), fell | v22: robot speed, object speed, force (N), fell | v22k: robot speed, object speed, force (N), fell |
|---|---|---|---|---|---|---|---|
| 20 kg | 0.1 | 0.01, 0.04 | 0.00, 0.08 | 0.01, 0.07 | 0.07, 0.07, 68, 0.00 | 0.00, 0.00, 16, 0.00 | 0.00, 0.00, 35, 0.00 |
| 20 kg | 0.2 | 0.11, 0.13 | 0.02, 0.11 | 0.11, 0.14 | 0.18, 0.18, 75, 0.00 | 0.01, 0.01, 48, 0.00 | 0.04, 0.04, 64, 0.00 |
| 20 kg | 0.3 | 0.21, 0.23 | 0.12, 0.17 | 0.21, 0.23 | 0.29, 0.29, 72, 0.00 | 0.16, 0.16, 71, 0.00 | 0.29, 0.29, 76, 0.00 |
| 20 kg | 0.5 | 0.41, 0.43 | 0.32, 0.36 | 0.41, 0.43 | 0.45, 0.46, 76, 0.00 | 0.35, 0.35, 74, 0.00 | 0.46, 0.46, 72, 0.00 |
| 40 kg | 0.1 | 0.00, 0.00 | 0.00, 0.08 | 0.00, 0.07 | 0.03, 0.03, 115, 0.00 | 0.00, 0.00, 16, 0.00 | 0.00, 0.00, 38, 0.00 |
| 40 kg | 0.2 | 0.02, 0.06 | 0.00, 0.10 | 0.02, 0.13 | 0.06, 0.06, 141, 0.00 | 0.00, 0.00, 56, 0.00 | 0.02, 0.02, 77, 0.00 |
| 40 kg | 0.3 | 0.12, 0.17 | 0.00, 0.12 | 0.12, 0.19 | 0.13, 0.12, 139, 0.00 | 0.05, 0.05, 95, 0.00 | 0.14, 0.13, 120, 0.00 |
| 40 kg | 0.5 | 0.32, 0.36 | 0.15, 0.25 | 0.32, 0.37 | 0.20, 0.19, 148, 0.00 | 0.17, 0.17, 130, 0.00 | 0.24, 0.18, 131, 0.00 |
| 80 kg | 0.1 | 0.00, 0.00 | 0.00, 0.08 | 0.00, 0.07 | 0.00, 0.00, 107, 0.00 | -0.00, 0.00, 17, 0.00 | -0.00, 0.00, 38, 0.00 |
| 80 kg | 0.2 | 0.00, 0.05 | 0.00, 0.10 | 0.00, 0.14 | 0.00, 0.00, 154, 0.00 | 0.00, 0.00, 55, 0.00 | 0.00, 0.00, 62, 0.00 |
| 80 kg | 0.3 | 0.00, 0.12 | 0.00, 0.09 | 0.00, 0.21 | 0.01, 0.01, 184, 0.00 | 0.01, 0.01, 110, 0.00 | 0.09, 0.01, 98, 0.00 |
| 80 kg | 0.5 | 0.15, 0.33 | 0.00, 0.30 | 0.15, 0.44 | 0.01, 0.01, 170, 0.00 | 0.09, 0.02, 103, 0.00 | 0.27, 0.01, 62, 0.00 |

**v21, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 58%, worst fall rate 0.00. (Separate question: consistent with its own measured force 67%.)
**v22, pushing objects (k = 500): FAIL** - speed within 0.05 m/s of the compliant expectation 83%, worst fall rate 0.00. (Separate question: consistent with its own measured force 17%.)
**v22k, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 58%, worst fall rate 0.00. (Separate question: consistent with its own measured force 17%.)

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v21 | FAIL | FAIL | FAIL |
| v22 | FAIL | FAIL | FAIL |
| v22k | FAIL | FAIL | FAIL |
