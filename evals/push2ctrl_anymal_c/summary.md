# Stage 2ctrl evaluation: logs/rsl_rl/push2ctrl_anymal_c/2026-10-22_10-29-41_seed0/model_5999.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero |
|---|---|---|
| seen | 0.64 (n=756, fell 0.02) | 0.38 (-0.26) |
| seen_out_of_range | 0.50 (n=756, fell 0.04) | 0.34 (-0.17) |
| unseen | 0.49 (n=540, fell 0.06) | 0.14 (-0.35) |
| unseen_out_of_range | 0.39 (n=540, fell 0.07) | 0.17 (-0.22) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |action change| per walker command (vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |action| = [24.4202, 10.5348, 4.8995].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [3.2402, 1.1788, 1.4035] | 0.146 | 0.931 |

## success by object and size set

| | normal | heading_zero |
|---|---|---|
| arch / in | 0.18 (n=108, fell 0.02) | 0.07 (-0.10) |
| arch / out | 0.20 (n=108, fell 0.07) | 0.06 (-0.15) |
| asym / in | 0.51 (n=108, fell 0.08) | 0.19 (-0.32) |
| asym / out | 0.34 (n=108, fell 0.04) | 0.07 (-0.27) |
| beam / in | 0.37 (n=108, fell 0.07) | 0.03 (-0.34) |
| beam / out | 0.37 (n=108, fell 0.18) | 0.09 (-0.28) |
| cube / in | 0.94 (n=108, fell 0.00) | 0.83 (-0.11) |
| cube / out | 0.56 (n=108, fell 0.00) | 0.42 (-0.14) |
| cylinder / in | 0.35 (n=108, fell 0.05) | 0.02 (-0.33) |
| cylinder / out | 0.32 (n=108, fell 0.07) | 0.24 (-0.07) |
| dumbbell / in | 0.54 (n=108, fell 0.03) | 0.18 (-0.35) |
| dumbbell / out | 0.36 (n=108, fell 0.01) | 0.18 (-0.18) |
| l_shape / in | 0.64 (n=108, fell 0.03) | 0.32 (-0.32) |
| l_shape / out | 0.53 (n=108, fell 0.03) | 0.26 (-0.27) |
| long / in | 0.81 (n=108, fell 0.01) | 0.43 (-0.37) |
| long / out | 0.57 (n=108, fell 0.02) | 0.27 (-0.30) |
| plus / in | 0.40 (n=108, fell 0.09) | 0.09 (-0.31) |
| plus / out | 0.35 (n=108, fell 0.04) | 0.34 (-0.01) |
| sphere / in | 0.99 (n=108, fell 0.01) | 0.98 (-0.01) |
| sphere / out | 0.96 (n=108, fell 0.03) | 1.00 (+0.04) |
| t_shape / in | 0.67 (n=108, fell 0.05) | 0.16 (-0.51) |
| t_shape / out | 0.56 (n=108, fell 0.05) | 0.18 (-0.37) |
| u_channel / in | 0.54 (n=108, fell 0.04) | 0.08 (-0.45) |
| u_channel / out | 0.37 (n=108, fell 0.06) | 0.08 (-0.29) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero |
|---|---|---|
| arch start yaw 0 / in | 0.17 (n=36, fell 0.03) | 0.06 (-0.11) |
| arch start yaw 0 / out | 0.19 (n=36, fell 0.14) | 0.06 (-0.14) |
| arch start yaw 45 / in | 0.08 (n=36, fell 0.00) | 0.03 (-0.06) |
| arch start yaw 45 / out | 0.19 (n=36, fell 0.03) | 0.03 (-0.17) |
| arch start yaw 90 / in | 0.28 (n=36, fell 0.03) | 0.14 (-0.14) |
| arch start yaw 90 / out | 0.22 (n=36, fell 0.06) | 0.08 (-0.14) |
| u_channel start yaw 0 / in | 0.53 (n=36, fell 0.06) | 0.11 (-0.42) |
| u_channel start yaw 0 / out | 0.36 (n=36, fell 0.06) | 0.06 (-0.30) |
| u_channel start yaw 45 / in | 0.56 (n=36, fell 0.03) | 0.03 (-0.53) |
| u_channel start yaw 45 / out | 0.28 (n=36, fell 0.06) | 0.03 (-0.25) |
| u_channel start yaw 90 / in | 0.53 (n=36, fell 0.03) | 0.11 (-0.42) |
| u_channel start yaw 90 / out | 0.47 (n=36, fell 0.06) | 0.17 (-0.30) |

## by group and mass

| | normal | heading_zero |
|---|---|---|
| seen / 10 kg | 0.75 (n=252, fell 0.01) | 0.50 (-0.25) |
| seen / 25 kg | 0.71 (n=252, fell 0.02) | 0.40 (-0.30) |
| seen / 40 kg | 0.46 (n=252, fell 0.04) | 0.25 (-0.21) |
| seen_out_of_range / 10 kg | 0.59 (n=252, fell 0.00) | 0.41 (-0.18) |
| seen_out_of_range / 25 kg | 0.54 (n=252, fell 0.03) | 0.33 (-0.21) |
| seen_out_of_range / 40 kg | 0.38 (n=252, fell 0.07) | 0.27 (-0.11) |
| unseen / 10 kg | 0.71 (n=180, fell 0.00) | 0.24 (-0.47) |
| unseen / 25 kg | 0.58 (n=180, fell 0.03) | 0.13 (-0.45) |
| unseen / 40 kg | 0.19 (n=180, fell 0.16) | 0.06 (-0.13) |
| unseen_out_of_range / 10 kg | 0.54 (n=180, fell 0.00) | 0.27 (-0.28) |
| unseen_out_of_range / 25 kg | 0.46 (n=180, fell 0.06) | 0.19 (-0.27) |
| unseen_out_of_range / 40 kg | 0.17 (n=180, fell 0.14) | 0.06 (-0.12) |
