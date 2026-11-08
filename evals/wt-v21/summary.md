# Walker acceptance test: wt-v21

Walkers: v2, v21. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use k = 1000 N per m/s and object friction 0.45.

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v2: achieved (err) | v21: achieved (err) | v2: fell | v21: fell |
|---|---|---|---|---|---|
| back | -0.05 m/s | -0.001 (0.049) | +0.001 (0.051) | 0.00 | 0.00 |
| back | -0.1 m/s | -0.163 (0.063) | -0.024 (0.076) | 0.00 | 0.00 |
| back | -0.3 m/s | -0.337 (0.037) | -0.362 (0.062) | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.011 (0.009) | +0.011 (0.009) | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.006 (0.044) | +0.017 (0.033) | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.004 (0.096) | +0.088 (0.012) | 0.00 | 0.00 |
| fwd | +0.15 m/s | +0.171 (0.021) | +0.153 (0.003) | 0.00 | 0.00 |
| fwd | +0.2 m/s | +0.213 (0.013) | +0.204 (0.004) | 0.00 | 0.00 |
| fwd | +0.3 m/s | +0.294 (0.006) | +0.323 (0.023) | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.473 (0.027) | +0.516 (0.016) | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.676 (0.024) | +0.712 (0.012) | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.301 (0.001) | +0.311 (0.012) | 0.00 | 0.00 |
| side | +0.05 m/s | +0.003 (0.047) | +0.006 (0.044) | 0.00 | 0.00 |
| side | +0.1 m/s | +0.000 (0.100) | +0.031 (0.069) | 0.00 | 0.00 |
| side | +0.2 m/s | +0.233 (0.033) | +0.088 (0.112) | 0.00 | 0.00 |
| side | +0.4 m/s | +0.434 (0.034) | +0.316 (0.084) | 0.00 | 0.00 |
| stand | +0 m/s | +0.004 (0.004) | +0.006 (0.006) | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.002 (0.048) | +0.005 (0.045) | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.002 (0.098) | +0.040 (0.060) | 0.00 | 0.00 |
| yaw | +0.2 rad/s | +0.004 (0.196) | +0.041 (0.159) | 0.00 | 0.00 |
| yaw | +0.4 rad/s | -0.002 (0.402) | +0.031 (0.369) | 0.00 | 0.00 |

**v2, free walking: FAIL** - small commands moved as asked 31%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v21, free walking: FAIL** - small commands moved as asked 31%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

## Pressing an immovable cube (force on it along the heading, N; swing = std over time; target k x speed)

### 0 deg

| speed (m/s) | target (N) | v2: force (swing), touching | v21: force (swing), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0), 0.00 | 3 (5), 0.14 |
| 0.05 | 50 | 2 (2), 0.21 | 1 (8), 0.06 |
| 0.1 | 100 | 4 (4), 0.45 | 137 (85), 0.83 |
| 0.15 | 150 | 85 (88), 0.67 | 160 (91), 0.83 |
| 0.2 | 200 | 111 (113), 0.68 | 150 (95), 0.80 |
| 0.25 | 250 | 98 (123), 0.64 | 144 (100), 0.78 |
| 0.3 | 300 | 140 (130), 0.71 | 176 (92), 0.87 |
| 0.4 | 400 | 146 (149), 0.68 | 155 (98), 0.83 |

### 20 deg

| speed (m/s) | target (N) | v2: force (swing), touching | v21: force (swing), touching |
|---|---|---|---|
| 0.02 | 20 | 3 (2), 0.22 | 3 (9), 0.07 |
| 0.05 | 50 | 6 (5), 0.65 | 34 (34), 0.33 |
| 0.1 | 100 | 5 (7), 0.35 | 94 (86), 0.70 |
| 0.15 | 150 | 80 (79), 0.72 | 158 (90), 0.82 |
| 0.2 | 200 | 103 (112), 0.64 | 147 (100), 0.76 |
| 0.25 | 250 | 110 (110), 0.66 | 151 (101), 0.79 |
| 0.3 | 300 | 153 (149), 0.72 | 183 (85), 0.90 |
| 0.4 | 400 | 163 (156), 0.76 | 177 (105), 0.87 |

**v2, force control (square on, 0.05-0.3 m/s): FAIL** - within 25% of k x speed 0%, not rising, steady 0%, touching 56%.
**v21, force control (square on, 0.05-0.3 m/s): FAIL** - within 25% of k x speed 17%, not rising, steady 0%, touching 69%.

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k))

| mass | speed cmd | expected (m/s) | v2: robot speed, object speed, force (N), fell | v21: robot speed, object speed, force (N), fell |
|---|---|---|---|---|
| 20 kg | 0.1 | 0.01 | 0.00, 0.00, 3, 0.00 | 0.07, 0.07, 67, 0.00 |
| 20 kg | 0.2 | 0.11 | 0.09, 0.09, 70, 0.00 | 0.17, 0.17, 70, 0.00 |
| 20 kg | 0.3 | 0.21 | 0.24, 0.24, 73, 0.00 | 0.28, 0.28, 74, 0.00 |
| 20 kg | 0.5 | 0.41 | 0.39, 0.39, 72, 0.00 | 0.45, 0.45, 80, 0.00 |
| 40 kg | 0.1 | 0.00 | 0.00, 0.00, 3, 0.00 | 0.02, 0.02, 101, 0.00 |
| 40 kg | 0.2 | 0.02 | 0.03, 0.03, 95, 0.00 | 0.05, 0.05, 130, 0.00 |
| 40 kg | 0.3 | 0.12 | 0.12, 0.12, 130, 0.00 | 0.14, 0.13, 151, 0.00 |
| 40 kg | 0.5 | 0.32 | 0.24, 0.24, 132, 0.00 | 0.18, 0.18, 142, 0.00 |
| 80 kg | 0.1 | 0.00 | 0.00, 0.00, 3, 0.00 | 0.00, 0.00, 140, 0.00 |
| 80 kg | 0.2 | 0.00 | 0.00, 0.00, 101, 0.00 | 0.00, 0.00, 164, 0.00 |
| 80 kg | 0.3 | 0.00 | 0.01, 0.01, 142, 0.00 | 0.01, 0.01, 181, 0.00 |
| 80 kg | 0.5 | 0.15 | 0.03, 0.02, 187, 0.00 | 0.01, 0.01, 171, 0.00 |

**v2, pushing objects: FAIL** - speed within 0.05 m/s of the compliant expectation 83%, worst fall rate 0.00.
**v21, pushing objects: FAIL** - speed within 0.05 m/s of the compliant expectation 58%, worst fall rate 0.00.

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v2 | FAIL | FAIL | FAIL |
| v21 | FAIL | FAIL | FAIL |
