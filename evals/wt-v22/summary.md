# Walker acceptance test: wt-v22

Walkers: v21, v22. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use each walker's own k (v21: 1000, v22: 500 N per m/s; common reference k = 1000) and object friction 0.45.

Checkpoints: v21 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_03-50-04_v21/model_5998.pt`; v22 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt`

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v21: achieved (err) | v22: achieved (err) | v21: fell | v22: fell |
|---|---|---|---|---|---|
| back | -0.05 m/s | +0.001 (0.051) | -0.001 (0.049) | 0.00 | 0.00 |
| back | -0.1 m/s | -0.024 (0.076) | -0.107 (0.007) | 0.00 | 0.00 |
| back | -0.3 m/s | -0.362 (0.062) | -0.321 (0.021) | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.011 (0.009) | +0.001 (0.019) | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.017 (0.033) | +0.000 (0.050) | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.088 (0.012) | +0.083 (0.017) | 0.00 | 0.00 |
| fwd | +0.15 m/s | +0.153 (0.003) | +0.191 (0.041) | 0.00 | 0.00 |
| fwd | +0.2 m/s | +0.204 (0.004) | +0.240 (0.040) | 0.00 | 0.00 |
| fwd | +0.3 m/s | +0.323 (0.023) | +0.252 (0.048) | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.516 (0.016) | +0.440 (0.060) | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.712 (0.012) | +0.622 (0.078) | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.311 (0.012) | +0.272 (0.028) | 0.00 | 0.00 |
| side | +0.05 m/s | +0.006 (0.044) | +0.043 (0.007) | 0.00 | 0.00 |
| side | +0.1 m/s | +0.031 (0.069) | +0.127 (0.027) | 0.00 | 0.00 |
| side | +0.2 m/s | +0.088 (0.112) | +0.221 (0.021) | 0.00 | 0.00 |
| side | +0.4 m/s | +0.316 (0.084) | +0.382 (0.018) | 0.00 | 0.00 |
| stand | +0 m/s | +0.006 (0.006) | +0.001 (0.001) | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.005 (0.045) | +0.002 (0.048) | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.040 (0.060) | +0.008 (0.092) | 0.00 | 0.00 |
| yaw | +0.2 rad/s | +0.041 (0.159) | +0.158 (0.042) | 0.00 | 0.00 |
| yaw | +0.4 rad/s | +0.031 (0.369) | +0.335 (0.065) | 0.00 | 0.00 |

**v21, free walking: FAIL** - small commands moved as asked 31%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v22, free walking: FAIL** - small commands moved as asked 62%, normal commands within 0.1 m/s 100%, worst fall rate 0.00.

### Response: time until the 0.4 s average reaches 63% of the command (s, includes ~0.2 s of averaging lag; - = never) / instantaneous sway along the command (std over the measured half)

| case | command | v21: t63 / sway | v22: t63 / sway |
|---|---|---|---|
| back | -0.05 | - / 0.000 | - / 0.000 |
| back | -0.1 | - / 0.019 | 3.99 / 0.036 |
| back | -0.3 | 0.40 / 0.049 | 0.40 / 0.044 |
| fwd | +0.02 | - / 0.014 | - / 0.001 |
| fwd | +0.05 | - / 0.023 | - / 0.003 |
| fwd | +0.1 | 7.90 (1/2) / 0.033 | 1.36 / 0.013 |
| fwd | +0.15 | 0.57 / 0.027 | 0.41 / 0.037 |
| fwd | +0.2 | 0.52 / 0.018 | 0.40 / 0.028 |
| fwd | +0.3 | 0.45 / 0.026 | 0.40 / 0.031 |
| fwd | +0.5 | 0.43 / 0.031 | 0.41 / 0.053 |
| fwd | +0.7 | 0.71 / 0.038 | 0.48 / 0.067 |
| kicked | +0.3 | 3.10 / 0.086 | 2.96 / 0.064 |
| side | +0.05 | - / 0.015 | 1.84 / 0.011 |
| side | +0.1 | 7.68 (1/2) / 0.028 | 0.95 / 0.026 |
| side | +0.2 | - / 0.040 | 0.40 / 0.041 |
| side | +0.4 | 7.86 (1/2) / 0.134 | 0.40 / 0.044 |
| yaw | +0.05 | - / 0.011 | - / 0.001 |
| yaw | +0.1 | 6.99 / 0.039 | - / 0.003 |
| yaw | +0.2 | - / 0.031 | 7.22 (1/2) / 0.061 |
| yaw | +0.4 | - / 0.024 | 3.85 / 0.096 |

## Pressing an immovable cube (force on it along the heading, N; swing = std over time, raw / after a 0.4 s moving average; target k x speed)

### 0 deg

| speed (m/s) | target k=500 (N) | target k=1000 (N) | v21: force (swing raw / 0.4 s), touching | v22: force (swing raw / 0.4 s), touching |
|---|---|---|---|---|
| 0.02 | 10 | 20 | 2 (4 / 3), 0.13 | 0 (0 / 0), 0.00 |
| 0.05 | 25 | 50 | 2 (8 / 2), 0.07 | 0 (0 / 0), 0.00 |
| 0.1 | 50 | 100 | 128 (88 / 48), 0.81 | 15 (16 / 6), 0.58 |
| 0.15 | 75 | 150 | 163 (89 / 38), 0.84 | 38 (31 / 10), 0.72 |
| 0.2 | 100 | 200 | 152 (99 / 29), 0.78 | 50 (37 / 10), 0.77 |
| 0.25 | 125 | 250 | 152 (95 / 26), 0.80 | 60 (76 / 28), 0.61 |
| 0.3 | 150 | 300 | 177 (92 / 24), 0.88 | 95 (123 / 38), 0.47 |
| 0.4 | 200 | 400 | 137 (99 / 31), 0.77 | 71 (103 / 34), 0.55 |

### 20 deg

| speed (m/s) | target k=500 (N) | target k=1000 (N) | v21: force (swing raw / 0.4 s), touching | v22: force (swing raw / 0.4 s), touching |
|---|---|---|---|---|
| 0.02 | 10 | 20 | 3 (12 / 4), 0.04 | 0 (0 / 0), 0.00 |
| 0.05 | 25 | 50 | 35 (32 / 23), 0.35 | 0 (0 / 0), 0.00 |
| 0.1 | 50 | 100 | 93 (86 / 41), 0.67 | 20 (59 / 14), 0.54 |
| 0.15 | 75 | 150 | 148 (91 / 38), 0.82 | 41 (37 / 11), 0.66 |
| 0.2 | 100 | 200 | 161 (97 / 29), 0.81 | 53 (48 / 12), 0.71 |
| 0.25 | 125 | 250 | 158 (96 / 31), 0.81 | 50 (61 / 15), 0.52 |
| 0.3 | 150 | 300 | 183 (80 / 22), 0.90 | 104 (85 / 30), 0.73 |
| 0.4 | 200 | 400 | 161 (99 / 28), 0.82 | 89 (109 / 42), 0.73 |

### Why the force stops where it does (square on): share of time any joint is at >= 95% of its 80 Nm limit, mean peak joint torque / limit, foot slip (m/s, feet on the ground), body pitch (deg, + = nose down)

| speed (m/s) | v21: torque-sat, peak torque, slip, pitch | v22: torque-sat, peak torque, slip, pitch |
|---|---|---|
| 0.02 | 0.34, 0.84, 0.017, +8.4 | 1.00, 1.00, 0.001, +7.9 |
| 0.05 | 0.00, 0.54, 0.016, +5.8 | 0.37, 0.78, 0.018, +8.2 |
| 0.1 | 0.94, 0.99, 0.194, +9.3 | 0.98, 1.00, 0.052, +7.2 |
| 0.15 | 0.82, 0.96, 0.280, +9.2 | 0.88, 0.99, 0.098, +4.2 |
| 0.2 | 0.84, 0.97, 0.309, +9.5 | 0.36, 0.91, 0.105, +2.5 |
| 0.25 | 0.82, 0.96, 0.424, +8.1 | 0.40, 0.91, 0.183, +1.3 |
| 0.3 | 0.90, 0.98, 0.303, +7.5 | 0.77, 0.97, 0.212, +3.4 |
| 0.4 | 0.86, 0.97, 0.351, +5.0 | 0.96, 1.00, 0.275, +2.7 |

**v21, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 33%, not rising, steady 0%, touching 70%. (Separate question, not part of the verdict: steady after a 0.4 s average 67%.)
**v22, force control (square on, 0.05-0.3 m/s, k = 500): FAIL** - within 25% of k x speed 0%, rising, steady 17%, touching 52%. (Separate question, not part of the verdict: steady after a 0.4 s average 33%.)

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k), its own k; 'law' = the same with the force actually measured, max(0, v - (F - 5 N) / k))

| mass | speed cmd | v21: expected (k=1000), law | v22: expected (k=500), law | v21: robot speed, object speed, force (N), fell | v22: robot speed, object speed, force (N), fell |
|---|---|---|---|---|---|
| 20 kg | 0.1 | 0.01, 0.03 | 0.00, 0.08 | 0.07, 0.07, 70, 0.00 | 0.00, 0.00, 17, 0.00 |
| 20 kg | 0.2 | 0.11, 0.13 | 0.02, 0.11 | 0.19, 0.19, 79, 0.00 | 0.01, 0.01, 52, 0.00 |
| 20 kg | 0.3 | 0.21, 0.23 | 0.12, 0.17 | 0.30, 0.30, 74, 0.00 | 0.16, 0.16, 68, 0.00 |
| 20 kg | 0.5 | 0.41, 0.43 | 0.32, 0.38 | 0.43, 0.43, 76, 0.00 | 0.36, 0.36, 66, 0.00 |
| 40 kg | 0.1 | 0.00, 0.00 | 0.00, 0.08 | 0.03, 0.03, 116, 0.00 | 0.00, 0.00, 15, 0.00 |
| 40 kg | 0.2 | 0.02, 0.06 | 0.00, 0.10 | 0.07, 0.06, 142, 0.00 | 0.00, 0.00, 54, 0.00 |
| 40 kg | 0.3 | 0.12, 0.17 | 0.00, 0.12 | 0.14, 0.13, 140, 0.00 | 0.05, 0.05, 96, 0.00 |
| 40 kg | 0.5 | 0.32, 0.36 | 0.15, 0.26 | 0.22, 0.22, 147, 0.00 | 0.18, 0.18, 124, 0.00 |
| 80 kg | 0.1 | 0.00, 0.00 | 0.00, 0.08 | 0.00, 0.00, 122, 0.00 | -0.00, 0.00, 16, 0.00 |
| 80 kg | 0.2 | 0.00, 0.06 | 0.00, 0.10 | 0.00, 0.00, 140, 0.00 | 0.00, 0.00, 54, 0.00 |
| 80 kg | 0.3 | 0.00, 0.13 | 0.00, 0.10 | 0.01, 0.01, 180, 0.00 | 0.01, 0.01, 103, 0.00 |
| 80 kg | 0.5 | 0.15, 0.33 | 0.00, 0.30 | 0.01, 0.01, 172, 0.00 | 0.16, 0.02, 106, 0.00 |

**v21, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 58%, worst fall rate 0.00. (Separate question: consistent with its own measured force 50%.)
**v22, pushing objects (k = 500): FAIL** - speed within 0.05 m/s of the compliant expectation 83%, worst fall rate 0.00. (Separate question: consistent with its own measured force 17%.)

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v21 | FAIL | FAIL | FAIL |
| v22 | FAIL | FAIL | FAIL |
