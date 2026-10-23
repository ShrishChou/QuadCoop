# Stage 2ctrl evaluation: logs/rsl_rl/push2ctrl_spot/2026-10-22_12-52-47_seed0/model_6000.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero |
|---|---|---|
| seen | 0.49 (n=756, fell 0.11) | 0.31 (-0.19) |
| seen_out_of_range | 0.43 (n=756, fell 0.12) | 0.26 (-0.17) |
| unseen | 0.37 (n=540, fell 0.13) | 0.09 (-0.29) |
| unseen_out_of_range | 0.33 (n=540, fell 0.11) | 0.11 (-0.22) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |action change| per walker command (vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |action| = [21.9672, 7.3648, 2.3063].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [1.2138, 0.782, 0.7406] | 0.086 | 0.939 |

## success by object and size set

| | normal | heading_zero |
|---|---|---|
| arch / in | 0.19 (n=108, fell 0.14) | 0.01 (-0.18) |
| arch / out | 0.15 (n=108, fell 0.16) | 0.01 (-0.14) |
| asym / in | 0.33 (n=108, fell 0.08) | 0.07 (-0.26) |
| asym / out | 0.26 (n=108, fell 0.09) | 0.10 (-0.16) |
| beam / in | 0.25 (n=108, fell 0.18) | 0.08 (-0.17) |
| beam / out | 0.24 (n=108, fell 0.14) | 0.08 (-0.16) |
| cube / in | 0.70 (n=108, fell 0.14) | 0.50 (-0.20) |
| cube / out | 0.48 (n=108, fell 0.17) | 0.35 (-0.13) |
| cylinder / in | 0.33 (n=108, fell 0.07) | 0.18 (-0.16) |
| cylinder / out | 0.22 (n=108, fell 0.18) | 0.14 (-0.08) |
| dumbbell / in | 0.26 (n=108, fell 0.08) | 0.11 (-0.15) |
| dumbbell / out | 0.28 (n=108, fell 0.07) | 0.07 (-0.21) |
| l_shape / in | 0.54 (n=108, fell 0.19) | 0.20 (-0.33) |
| l_shape / out | 0.51 (n=108, fell 0.11) | 0.16 (-0.35) |
| long / in | 0.63 (n=108, fell 0.10) | 0.27 (-0.36) |
| long / out | 0.56 (n=108, fell 0.07) | 0.22 (-0.34) |
| plus / in | 0.33 (n=108, fell 0.08) | 0.00 (-0.33) |
| plus / out | 0.29 (n=108, fell 0.07) | 0.08 (-0.20) |
| sphere / in | 0.90 (n=108, fell 0.10) | 0.89 (-0.01) |
| sphere / out | 0.90 (n=108, fell 0.08) | 0.88 (-0.02) |
| t_shape / in | 0.43 (n=108, fell 0.14) | 0.18 (-0.25) |
| t_shape / out | 0.41 (n=108, fell 0.15) | 0.15 (-0.26) |
| u_channel / in | 0.41 (n=108, fell 0.10) | 0.07 (-0.33) |
| u_channel / out | 0.35 (n=108, fell 0.13) | 0.10 (-0.25) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero |
|---|---|---|
| arch start yaw 0 / in | 0.22 (n=36, fell 0.14) | 0.00 (-0.22) |
| arch start yaw 0 / out | 0.19 (n=36, fell 0.19) | 0.00 (-0.19) |
| arch start yaw 45 / in | 0.14 (n=36, fell 0.08) | 0.03 (-0.11) |
| arch start yaw 45 / out | 0.08 (n=36, fell 0.11) | 0.00 (-0.08) |
| arch start yaw 90 / in | 0.22 (n=36, fell 0.19) | 0.00 (-0.22) |
| arch start yaw 90 / out | 0.17 (n=36, fell 0.17) | 0.03 (-0.14) |
| u_channel start yaw 0 / in | 0.47 (n=36, fell 0.11) | 0.14 (-0.33) |
| u_channel start yaw 0 / out | 0.33 (n=36, fell 0.14) | 0.11 (-0.22) |
| u_channel start yaw 45 / in | 0.33 (n=36, fell 0.03) | 0.00 (-0.33) |
| u_channel start yaw 45 / out | 0.33 (n=36, fell 0.11) | 0.03 (-0.30) |
| u_channel start yaw 90 / in | 0.42 (n=36, fell 0.17) | 0.08 (-0.33) |
| u_channel start yaw 90 / out | 0.39 (n=36, fell 0.14) | 0.17 (-0.22) |

## by group and mass

| | normal | heading_zero |
|---|---|---|
| seen / 10 kg | 0.64 (n=252, fell 0.08) | 0.39 (-0.25) |
| seen / 25 kg | 0.56 (n=252, fell 0.12) | 0.34 (-0.21) |
| seen / 40 kg | 0.29 (n=252, fell 0.14) | 0.19 (-0.10) |
| seen_out_of_range / 10 kg | 0.51 (n=252, fell 0.14) | 0.30 (-0.21) |
| seen_out_of_range / 25 kg | 0.51 (n=252, fell 0.12) | 0.31 (-0.20) |
| seen_out_of_range / 40 kg | 0.27 (n=252, fell 0.11) | 0.17 (-0.10) |
| unseen / 10 kg | 0.61 (n=180, fell 0.13) | 0.14 (-0.47) |
| unseen / 25 kg | 0.41 (n=180, fell 0.13) | 0.08 (-0.32) |
| unseen / 40 kg | 0.10 (n=180, fell 0.13) | 0.04 (-0.06) |
| unseen_out_of_range / 10 kg | 0.52 (n=180, fell 0.09) | 0.17 (-0.35) |
| unseen_out_of_range / 25 kg | 0.37 (n=180, fell 0.12) | 0.13 (-0.24) |
| unseen_out_of_range / 40 kg | 0.10 (n=180, fell 0.11) | 0.02 (-0.08) |
