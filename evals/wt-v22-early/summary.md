# Walker acceptance test: wt-v22-early

Walkers: v22. Each case 8 s, measured over the second half, 2 repeats. Compliant-walker expectations use each walker's own k (v22: 500 N per m/s; common reference k = 1000) and object friction 0.45.

## Free walking (achieved velocity; small commands are the dead-zone test)

| case | command | v22: achieved (err) | v22: fell |
|---|---|---|---|
| back | -0.05 m/s | -0.001 (0.049) | 0.00 |
| back | -0.1 m/s | -0.107 (0.007) | 0.00 |
| back | -0.3 m/s | -0.321 (0.021) | 0.00 |
| fwd | +0.02 m/s | +0.001 (0.019) | 0.00 |
| fwd | +0.05 m/s | +0.000 (0.050) | 0.00 |
| fwd | +0.1 m/s | +0.083 (0.017) | 0.00 |
| fwd | +0.15 m/s | +0.191 (0.041) | 0.00 |
| fwd | +0.2 m/s | +0.240 (0.040) | 0.00 |
| fwd | +0.3 m/s | +0.252 (0.048) | 0.00 |
| fwd | +0.5 m/s | +0.440 (0.060) | 0.00 |
| fwd | +0.7 m/s | +0.622 (0.078) | 0.00 |
| kicked | +0.3 m/s | +0.272 (0.028) | 0.00 |
| side | +0.05 m/s | +0.043 (0.007) | 0.00 |
| side | +0.1 m/s | +0.127 (0.027) | 0.00 |
| side | +0.2 m/s | +0.221 (0.021) | 0.00 |
| side | +0.4 m/s | +0.382 (0.018) | 0.00 |
| stand | +0 m/s | +0.001 (0.001) | 0.00 |
| yaw | +0.05 rad/s | +0.002 (0.048) | 0.00 |
| yaw | +0.1 rad/s | +0.008 (0.092) | 0.00 |
| yaw | +0.2 rad/s | +0.158 (0.042) | 0.00 |
| yaw | +0.4 rad/s | +0.335 (0.065) | 0.00 |

**v22, free walking: FAIL** - small commands moved as asked 62%, normal commands within 0.1 m/s 100%, worst fall rate 0.00.

### Response: time until the 0.4 s average reaches 63% of the command (s, includes ~0.2 s of averaging lag; - = never) / instantaneous sway along the command (std over the measured half)

| case | command | v22: t63 / sway |
|---|---|---|
| back | -0.05 | 0.40 / 0.000 |
| back | -0.1 | 0.40 / 0.036 |
| back | -0.3 | 0.40 / 0.044 |
| fwd | +0.02 | 0.50 / 0.001 |
| fwd | +0.05 | 0.42 / 0.003 |
| fwd | +0.1 | 0.40 / 0.013 |
| fwd | +0.15 | 0.41 / 0.037 |
| fwd | +0.2 | 0.40 / 0.028 |
| fwd | +0.3 | 0.40 / 0.031 |
| fwd | +0.5 | 0.41 / 0.053 |
| fwd | +0.7 | 0.48 / 0.067 |
| kicked | +0.3 | 0.40 / 0.064 |
| side | +0.05 | 0.40 / 0.011 |
| side | +0.1 | 0.40 / 0.026 |
| side | +0.2 | 0.40 / 0.041 |
| side | +0.4 | 0.40 / 0.044 |
| yaw | +0.05 | 0.41 / 0.001 |
| yaw | +0.1 | 0.40 / 0.003 |
| yaw | +0.2 | 0.40 / 0.061 |
| yaw | +0.4 | 0.40 / 0.096 |

## Verdicts

| walker | free |
|---|---|
| v22 | FAIL |
