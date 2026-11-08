# Walker acceptance test: wt-v2

Walkers: v1, v2. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use k = 1000 N per m/s and object friction 0.45.

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v1: achieved (err) | v2: achieved (err) | v1: fell | v2: fell |
|---|---|---|---|---|---|
| back | -0.05 m/s | -0.001 (0.049) | -0.001 (0.049) | 0.00 | 0.00 |
| back | -0.1 m/s | -0.003 (0.097) | -0.163 (0.063) | 0.00 | 0.00 |
| back | -0.3 m/s | -0.380 (0.080) | -0.337 (0.037) | 0.00 | 0.00 |
| fwd | +0.02 m/s | +0.002 (0.018) | +0.011 (0.009) | 0.00 | 0.00 |
| fwd | +0.05 m/s | +0.002 (0.048) | +0.006 (0.044) | 0.00 | 0.00 |
| fwd | +0.1 m/s | +0.001 (0.099) | +0.004 (0.096) | 0.00 | 0.00 |
| fwd | +0.15 m/s | -0.000 (0.150) | +0.171 (0.021) | 0.00 | 0.00 |
| fwd | +0.2 m/s | -0.000 (0.200) | +0.213 (0.013) | 0.00 | 0.00 |
| fwd | +0.3 m/s | +0.378 (0.078) | +0.294 (0.006) | 0.00 | 0.00 |
| fwd | +0.5 m/s | +0.536 (0.036) | +0.473 (0.027) | 0.00 | 0.00 |
| fwd | +0.7 m/s | +0.686 (0.014) | +0.676 (0.024) | 0.00 | 0.00 |
| kicked | +0.3 m/s | +0.384 (0.084) | +0.301 (0.001) | 0.00 | 0.00 |
| side | +0.05 m/s | -0.002 (0.052) | +0.003 (0.047) | 0.00 | 0.00 |
| side | +0.1 m/s | -0.006 (0.106) | +0.000 (0.100) | 0.00 | 0.00 |
| side | +0.2 m/s | -0.000 (0.200) | +0.233 (0.033) | 0.00 | 0.00 |
| side | +0.4 m/s | +0.468 (0.068) | +0.434 (0.034) | 0.00 | 0.00 |
| stand | +0 m/s | -0.001 (0.001) | +0.004 (0.004) | 0.00 | 0.00 |
| yaw | +0.05 rad/s | +0.005 (0.045) | +0.002 (0.048) | 0.00 | 0.00 |
| yaw | +0.1 rad/s | +0.005 (0.095) | +0.002 (0.098) | 0.00 | 0.00 |
| yaw | +0.2 rad/s | -0.001 (0.201) | +0.004 (0.196) | 0.00 | 0.00 |
| yaw | +0.4 rad/s | +0.008 (0.392) | -0.002 (0.402) | 0.00 | 0.00 |

**v1, free walking: FAIL** - small commands moved as asked 0%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.
**v2, free walking: FAIL** - small commands moved as asked 31%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

## Pressing an immovable cube (force on it along the heading, N; swing = std over time; target k x speed)

### 0 deg

| speed (m/s) | target (N) | v1: force (swing), touching | v2: force (swing), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0), 0.00 | 0 (0), 0.00 |
| 0.05 | 50 | 0 (0), 0.00 | 2 (2), 0.18 |
| 0.1 | 100 | 0 (0), 0.00 | 4 (4), 0.49 |
| 0.15 | 150 | 0 (0), 0.00 | 79 (88), 0.65 |
| 0.2 | 200 | 0 (0), 0.00 | 110 (110), 0.68 |
| 0.25 | 250 | 0 (0), 0.00 | 105 (115), 0.68 |
| 0.3 | 300 | 147 (133), 0.76 | 141 (122), 0.74 |
| 0.4 | 400 | 151 (119), 0.81 | 147 (142), 0.71 |

### 20 deg

| speed (m/s) | target (N) | v1: force (swing), touching | v2: force (swing), touching |
|---|---|---|---|
| 0.02 | 20 | 0 (0), 0.00 | 3 (3), 0.20 |
| 0.05 | 50 | 0 (0), 0.00 | 7 (5), 0.68 |
| 0.1 | 100 | 0 (0), 0.00 | 5 (7), 0.34 |
| 0.15 | 150 | 0 (0), 0.00 | 81 (87), 0.72 |
| 0.2 | 200 | 0 (0), 0.00 | 103 (99), 0.65 |
| 0.25 | 250 | 0 (0), 0.00 | 110 (121), 0.66 |
| 0.3 | 300 | 150 (133), 0.74 | 144 (130), 0.70 |
| 0.4 | 400 | 156 (120), 0.81 | 153 (154), 0.72 |

**v1, force control (square on, 0.05-0.3 m/s): FAIL** - within 25% of k x speed 0%, rising, steady 83%, touching 13%.
**v2, force control (square on, 0.05-0.3 m/s): FAIL** - within 25% of k x speed 0%, rising, steady 0%, touching 57%.

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k))

| mass | speed cmd | expected (m/s) | v1: robot speed, object speed, force (N), fell | v2: robot speed, object speed, force (N), fell |
|---|---|---|---|---|
| 20 kg | 0.1 | 0.01 | 0.00, 0.00, 0, 0.00 | 0.00, 0.00, 3, 0.00 |
| 20 kg | 0.2 | 0.11 | -0.00, 0.00, 0, 0.00 | 0.08, 0.09, 69, 0.00 |
| 20 kg | 0.3 | 0.21 | 0.28, 0.12, 41, 0.00 | 0.22, 0.22, 71, 0.00 |
| 20 kg | 0.5 | 0.41 | 0.53, 0.09, 12, 0.00 | 0.40, 0.42, 74, 0.00 |
| 40 kg | 0.1 | 0.00 | 0.00, 0.00, 0, 0.00 | 0.00, 0.00, 3, 0.00 |
| 40 kg | 0.2 | 0.02 | -0.00, 0.00, 0, 0.00 | 0.03, 0.03, 97, 0.00 |
| 40 kg | 0.3 | 0.12 | 0.12, 0.11, 146, 0.00 | 0.16, 0.17, 132, 0.00 |
| 40 kg | 0.5 | 0.32 | 0.28, 0.19, 152, 0.00 | 0.27, 0.27, 139, 0.00 |
| 80 kg | 0.1 | 0.00 | 0.00, 0.00, 0, 0.00 | 0.00, 0.00, 3, 0.00 |
| 80 kg | 0.2 | 0.00 | -0.00, 0.00, 0, 0.00 | 0.00, 0.00, 109, 0.00 |
| 80 kg | 0.3 | 0.00 | 0.01, 0.01, 146, 0.00 | 0.01, 0.01, 156, 0.00 |
| 80 kg | 0.5 | 0.15 | 0.01, 0.01, 180, 0.00 | 0.06, 0.03, 177, 0.00 |

**v1, pushing objects: FAIL** - speed within 0.05 m/s of the compliant expectation 67%, worst fall rate 0.00.
**v2, pushing objects: FAIL** - speed within 0.05 m/s of the compliant expectation 83%, worst fall rate 0.00.

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v1 | FAIL | FAIL | FAIL |
| v2 | FAIL | FAIL | FAIL |
