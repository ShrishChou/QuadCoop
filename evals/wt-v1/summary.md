# Walker acceptance test: wt-v1

Walkers: v1. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use k = 1000 N per m/s and object friction 0.45.

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v1: achieved (err) | v1: fell |
|---|---|---|---|
| back | -0.05 m/s | -0.001 (0.049) | 0.00 |
| back | -0.1 m/s | -0.003 (0.097) | 0.00 |
| back | -0.3 m/s | -0.380 (0.080) | 0.00 |
| fwd | +0.02 m/s | +0.002 (0.018) | 0.00 |
| fwd | +0.05 m/s | +0.002 (0.048) | 0.00 |
| fwd | +0.1 m/s | +0.001 (0.099) | 0.00 |
| fwd | +0.15 m/s | -0.000 (0.150) | 0.00 |
| fwd | +0.2 m/s | -0.000 (0.200) | 0.00 |
| fwd | +0.3 m/s | +0.378 (0.078) | 0.00 |
| fwd | +0.5 m/s | +0.536 (0.036) | 0.00 |
| fwd | +0.7 m/s | +0.686 (0.014) | 0.00 |
| kicked | +0.3 m/s | +0.384 (0.084) | 0.00 |
| side | +0.05 m/s | -0.002 (0.052) | 0.00 |
| side | +0.1 m/s | -0.006 (0.106) | 0.00 |
| side | +0.2 m/s | -0.000 (0.200) | 0.00 |
| side | +0.4 m/s | +0.468 (0.068) | 0.00 |
| stand | +0 m/s | -0.001 (0.001) | 0.00 |
| yaw | +0.05 rad/s | +0.005 (0.045) | 0.00 |
| yaw | +0.1 rad/s | +0.005 (0.095) | 0.00 |
| yaw | +0.2 rad/s | -0.001 (0.201) | 0.00 |
| yaw | +0.4 rad/s | +0.008 (0.392) | 0.00 |

**v1, free walking: FAIL** - small commands moved as asked 0%, normal commands within 0.1 m/s 83%, worst fall rate 0.00.

## Pressing an immovable cube (force on it along the heading, N; swing = std over time; target k x speed)

### 0 deg

| speed (m/s) | target (N) | v1: force (swing), touching |
|---|---|---|
| 0.02 | 20 | 0 (0), 0.00 |
| 0.05 | 50 | 0 (0), 0.00 |
| 0.1 | 100 | 0 (0), 0.00 |
| 0.15 | 150 | 0 (0), 0.00 |
| 0.2 | 200 | 0 (0), 0.00 |
| 0.25 | 250 | 0 (0), 0.00 |
| 0.3 | 300 | 145 (124), 0.75 |
| 0.4 | 400 | 153 (117), 0.82 |

### 20 deg

| speed (m/s) | target (N) | v1: force (swing), touching |
|---|---|---|
| 0.02 | 20 | 0 (0), 0.00 |
| 0.05 | 50 | 0 (0), 0.00 |
| 0.1 | 100 | 0 (0), 0.00 |
| 0.15 | 150 | 0 (0), 0.00 |
| 0.2 | 200 | 0 (0), 0.00 |
| 0.25 | 250 | 0 (0), 0.00 |
| 0.3 | 300 | 154 (136), 0.74 |
| 0.4 | 400 | 173 (111), 0.87 |

**v1, force control (square on, 0.05-0.3 m/s): FAIL** - within 25% of k x speed 0%, rising, steady 83%, touching 13%.

## Pushing movable cubes (robot speed; a compliant walker should go at max(0, v - mu m g / k))

| mass | speed cmd | expected (m/s) | v1: robot speed, object speed, force (N), fell |
|---|---|---|---|
| 20 kg | 0.1 | 0.01 | 0.00, 0.00, 0, 0.00 |
| 20 kg | 0.2 | 0.11 | -0.00, 0.00, 0, 0.00 |
| 20 kg | 0.3 | 0.21 | 0.28, 0.12, 48, 0.00 |
| 20 kg | 0.5 | 0.41 | 0.52, 0.07, 10, 0.00 |
| 40 kg | 0.1 | 0.00 | 0.00, 0.00, 0, 0.00 |
| 40 kg | 0.2 | 0.02 | -0.00, 0.00, 0, 0.00 |
| 40 kg | 0.3 | 0.12 | 0.13, 0.10, 151, 0.00 |
| 40 kg | 0.5 | 0.32 | 0.26, 0.17, 144, 0.00 |
| 80 kg | 0.1 | 0.00 | 0.00, 0.00, 0, 0.00 |
| 80 kg | 0.2 | 0.00 | -0.00, 0.00, 0, 0.00 |
| 80 kg | 0.3 | 0.00 | 0.01, 0.01, 152, 0.00 |
| 80 kg | 0.5 | 0.15 | 0.01, 0.01, 173, 0.00 |

**v1, pushing objects: FAIL** - speed within 0.05 m/s of the compliant expectation 58%, worst fall rate 0.00.

## Verdicts

| walker | free | objects | wall |
|---|---|---|---|
| v1 | FAIL | FAIL | FAIL |
