# Walker acceptance test: wt-v1nc6998

Walkers: v1, v1nc6998. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use each walker's own k (v1: 1000, v1nc6998: 1000 N per m/s; common reference k = 1000) and object friction 0.45.

Checkpoints: v1 = `logs/evals/walker-anymal-v1/model.pt`; v1nc6998 = `/home/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c/2026-11-08_19-58-50_v1_nocreep/model_6998.pt`

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v1: achieved (err) | v1nc6998: achieved (err) | v1: fell | v1nc6998: fell |
|---|---|---|---|---|---|
| back | -0.05 m/s | +0.004 (0.054) | -0.000 (0.050) | 0.00 | 0.00 |
| back | -0.1 m/s | +0.004 (0.104) | -0.001 (0.099) | 0.00 | 0.00 |
| back | -0.3 m/s | -0.380 (0.080) | -0.378 (0.078) | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.003 (0.017) | -0.001 (0.021) | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.002 (0.048) | -0.000 (0.050) | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.097 (0.003) | -0.000 (0.100) | 0.00 | 0.00 |
| fwd | +0.15 m/s | +0.240 (0.090) | -0.000 (0.150) | 0.00 | 0.00 |
| fwd | +0.2 m/s | +0.290 (0.090) | -0.001 (0.201) | 0.00 | 0.00 |
| fwd | +0.3 m/s | +0.378 (0.078) | +0.365 (0.065) | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.525 (0.025) | +0.514 (0.014) | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.672 (0.028) | +0.671 (0.029) | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.380 (0.080) | +0.360 (0.060) | 0.00 | 0.00 |
| side | +0.05 m/s | +0.002 (0.048) | -0.001 (0.051) | 0.00 | 0.00 |
| side | +0.1 m/s | -0.013 (0.114) | +0.001 (0.099) | 0.00 | 0.00 |
| side | +0.2 m/s | +0.297 (0.097) | +0.288 (0.088) | 0.00 | 0.00 |
| side | +0.4 m/s | +0.485 (0.085) | +0.500 (0.100) | 0.00 | 0.00 |
| stand | +0 m/s | +0.003 (0.003) | -0.001 (0.001) | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.013 (0.037) | +0.002 (0.048) | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.019 (0.081) | +0.006 (0.094) | 0.00 | 0.00 |
| yaw | +0.2 rad/s | +0.009 (0.191) | +0.016 (0.184) | 0.00 | 0.00 |
| yaw | +0.4 rad/s | +0.023 (0.377) | +0.006 (0.394) | 0.00 | 0.00 |

**v1, free walking: FAIL** - small commands moved as asked 8%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v1nc6998, free walking: FAIL** - small commands moved as asked 0%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

### Response: time until the 0.4 s average reaches 63% of the command (s, includes ~0.2 s of averaging lag; - = never) / instantaneous sway along the command (std over the measured half)

| case | command | v1: t63 / sway | v1nc6998: t63 / sway |
|---|---|---|---|
| back | -0.05 | - / 0.001 | - / 0.001 |
| back | -0.1 | - / 0.000 | - / 0.000 |
| back | -0.3 | 0.80 / 0.042 | 0.90 / 0.029 |
| fwd | +0.02 | - / 0.001 | - / 0.000 |
| fwd | +0.05 | - / 0.001 | - / 0.000 |
| fwd | +0.1 | 2.44 (1/2) / 0.018 | - / 0.000 |
| fwd | +0.15 | 0.70 / 0.029 | - / 0.000 |
| fwd | +0.2 | 0.68 / 0.026 | - / 0.000 |
| fwd | +0.3 | 0.40 / 0.023 | 0.65 / 0.020 |
| fwd | +0.5 | 0.40 / 0.034 | 0.40 / 0.020 |
| fwd | +0.7 | 0.40 / 0.043 | 0.40 / 0.023 |
| kicked | +0.3 | 0.40 / 0.081 | 1.93 / 0.074 |
| side | +0.05 | - / 0.000 | - / 0.000 |
| side | +0.1 | - / 0.017 | - / 0.000 |
| side | +0.2 | 0.79 / 0.066 | 1.52 / 0.054 |
| side | +0.4 | 0.40 / 0.067 | 0.40 / 0.063 |
| yaw | +0.05 | - / 0.009 | - / 0.002 |
| yaw | +0.1 | - / 0.003 | - / 0.002 |
| yaw | +0.2 | - / 0.003 | - / 0.025 |
| yaw | +0.4 | - / 0.003 | - / 0.008 |

## Pressing an immovable cube (force on it along the heading, N; swing = std over time, raw / after a 0.4 s moving average; target k x speed)

### 0 deg

| speed (m/s) | target k=1000 (N) | v1: force (swing raw / 0.4 s), touching | v1nc6998: force (swing raw / 0.4 s), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 50 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.1 | 100 | 68 (30 / 6), 0.50 | 0 (0 / 0), 0.00 |
| 0.15 | 150 | 164 (33 / 16), 0.99 | 0 (0 / 0), 0.00 |
| 0.2 | 200 | 165 (60 / 23), 0.97 | 0 (0 / 0), 0.00 |
| 0.25 | 250 | 163 (62 / 21), 0.93 | 0 (0 / 0), 0.00 |
| 0.3 | 300 | 196 (100 / 33), 0.99 | 232 (82 / 28), 0.91 |
| 0.4 | 400 | 197 (101 / 30), 0.92 | 213 (58 / 22), 0.99 |

### 20 deg

| speed (m/s) | target k=1000 (N) | v1: force (swing raw / 0.4 s), touching | v1nc6998: force (swing raw / 0.4 s), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.05 | 50 | 0 (0 / 0), 0.00 | 0 (0 / 0), 0.00 |
| 0.1 | 100 | 1 (3 / 1), 0.03 | 0 (0 / 0), 0.00 |
| 0.15 | 150 | 85 (61 / 43), 0.90 | 0 (0 / 0), 0.00 |
| 0.2 | 200 | 174 (64 / 40), 0.94 | 0 (0 / 0), 0.00 |
| 0.25 | 250 | 152 (43 / 17), 0.96 | 6 (3 / 1), 0.42 |
| 0.3 | 300 | 146 (70 / 34), 0.85 | 228 (20 / 17), 1.00 |
| 0.4 | 400 | 221 (70 / 20), 0.96 | 242 (73 / 36), 0.96 |

### Why the force stops where it does (square on): share of time any joint is at >= 95% of its 80 Nm limit, mean peak joint torque / limit, foot slip (m/s, feet on the ground), body pitch (deg, + = nose down)

| speed (m/s) | v1: torque-sat, peak torque, slip, pitch | v1nc6998: torque-sat, peak torque, slip, pitch |
|---|---|---|
| 0.02 | 0.00, 0.41, 0.008, +2.4 | 0.00, 0.43, 0.007, +0.7 |
| 0.05 | 0.00, 0.37, 0.007, +2.9 | 0.00, 0.44, 0.007, +0.8 |
| 0.1 | 0.00, 0.45, 0.008, +1.2 | 0.00, 0.41, 0.006, +0.3 |
| 0.15 | 0.00, 0.52, 0.014, +0.2 | 0.00, 0.41, 0.004, +0.6 |
| 0.2 | 0.00, 0.55, 0.017, -0.1 | 0.00, 0.37, 0.004, +0.3 |
| 0.25 | 0.01, 0.49, 0.033, +0.6 | 0.00, 0.35, 0.002, +0.8 |
| 0.3 | 0.05, 0.55, 0.033, +0.5 | 0.00, 0.67, 0.033, -0.1 |
| 0.4 | 0.15, 0.80, 0.179, +1.2 | 0.00, 0.62, 0.036, -0.5 |

**v1, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 33%, rising, steady 33%, touching 73%. (Separate question, not part of the verdict: steady after a 0.4 s average 100%.)
**v1nc6998, force control (square on, 0.05-0.3 m/s, k = 1000): FAIL** - within 25% of k x speed 17%, rising, steady 83%, touching 15%. (Separate question, not part of the verdict: steady after a 0.4 s average 100%.)

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k), its own k; 'law' = the same with the force actually measured, max(0, v - (F - 5 N) / k))

| mass | speed cmd | v1: expected (k=1000), law | v1nc6998: expected (k=1000), law | v1: robot speed, object speed, force (N), fell | v1nc6998: robot speed, object speed, force (N), fell |
|---|---|---|---|---|---|
| 20 kg | 0.1 | 0.01, 0.10 | 0.01, 0.10 | 0.00, 0.00, 0, 0.00 | -0.00, 0.00, 0, 0.00 |
| 20 kg | 0.2 | 0.11, 0.13 | 0.11, 0.20 | 0.23, 0.18, 72, 0.00 | -0.00, 0.00, 0, 0.00 |
| 20 kg | 0.3 | 0.21, 0.26 | 0.21, 0.21 | 0.31, 0.16, 44, 0.00 | 0.20, 0.18, 91, 0.00 |
| 20 kg | 0.5 | 0.41, 0.49 | 0.41, 0.43 | 0.53, 0.09, 17, 0.00 | 0.39, 0.30, 72, 0.00 |
| 40 kg | 0.1 | 0.00, 0.10 | 0.00, 0.10 | 0.00, 0.00, 0, 0.00 | -0.00, 0.00, 0, 0.00 |
| 40 kg | 0.2 | 0.02, 0.10 | 0.02, 0.20 | 0.03, 0.03, 108, 0.00 | -0.00, 0.00, 0, 0.00 |
| 40 kg | 0.3 | 0.12, 0.17 | 0.12, 0.15 | 0.28, 0.17, 139, 0.00 | 0.08, 0.07, 160, 0.00 |
| 40 kg | 0.5 | 0.32, 0.39 | 0.32, 0.34 | 0.46, 0.23, 120, 0.00 | 0.28, 0.27, 162, 0.00 |
| 80 kg | 0.1 | 0.00, 0.10 | 0.00, 0.10 | 0.00, 0.00, 0, 0.00 | -0.00, 0.00, 0, 0.00 |
| 80 kg | 0.2 | 0.00, 0.04 | 0.00, 0.20 | 0.00, 0.00, 170, 0.00 | -0.00, 0.00, 0, 0.00 |
| 80 kg | 0.3 | 0.00, 0.13 | 0.00, 0.08 | 0.00, 0.00, 176, 0.00 | 0.00, 0.00, 222, 0.00 |
| 80 kg | 0.5 | 0.15, 0.32 | 0.15, 0.30 | 0.00, 0.00, 187, 0.00 | 0.00, 0.00, 201, 0.00 |

**v1, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 50%, worst fall rate 0.00. (Separate question: consistent with its own measured force 17%.)
**v1nc6998, pushing objects (k = 1000): FAIL** - speed within 0.05 m/s of the compliant expectation 83%, worst fall rate 0.00. (Separate question: consistent with its own measured force 17%.)

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v1 | FAIL | FAIL | FAIL |
| v1nc6998 | FAIL | FAIL | FAIL |
