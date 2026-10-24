# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-spot-falcon/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero |
|---|---|---|
| seen | 0.53 (n=756, fell 0.15) | 0.33 (-0.20) |
| seen_out_of_range | 0.45 (n=756, fell 0.16) | 0.28 (-0.17) |
| unseen | 0.30 (n=540, fell 0.27) | 0.10 (-0.19) |
| unseen_out_of_range | 0.31 (n=540, fell 0.22) | 0.13 (-0.18) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.774, 0.7972, 0.8052]; mean |raw output| = [28.59, 7.2, 4.52]; share of outputs beyond the clip = [0.641, 0.653, 0.646].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2836, 0.1818, 0.2473] | 0.3 | 0.702 |

## success by object and size set

| | normal | heading_zero |
|---|---|---|
| arch / in | 0.07 (n=108, fell 0.22) | 0.02 (-0.05) |
| arch / out | 0.02 (n=108, fell 0.22) | 0.01 (-0.01) |
| asym / in | 0.40 (n=108, fell 0.31) | 0.21 (-0.19) |
| asym / out | 0.31 (n=108, fell 0.25) | 0.14 (-0.17) |
| beam / in | 0.21 (n=108, fell 0.18) | 0.01 (-0.20) |
| beam / out | 0.25 (n=108, fell 0.14) | 0.07 (-0.18) |
| cube / in | 0.69 (n=108, fell 0.27) | 0.61 (-0.07) |
| cube / out | 0.64 (n=108, fell 0.19) | 0.57 (-0.07) |
| cylinder / in | 0.37 (n=108, fell 0.04) | 0.16 (-0.21) |
| cylinder / out | 0.30 (n=108, fell 0.14) | 0.12 (-0.18) |
| dumbbell / in | 0.33 (n=108, fell 0.17) | 0.10 (-0.23) |
| dumbbell / out | 0.23 (n=108, fell 0.18) | 0.08 (-0.15) |
| l_shape / in | 0.41 (n=108, fell 0.31) | 0.23 (-0.18) |
| l_shape / out | 0.39 (n=108, fell 0.22) | 0.17 (-0.22) |
| long / in | 0.67 (n=108, fell 0.17) | 0.32 (-0.35) |
| long / out | 0.62 (n=108, fell 0.18) | 0.33 (-0.29) |
| plus / in | 0.10 (n=108, fell 0.32) | 0.03 (-0.07) |
| plus / out | 0.28 (n=108, fell 0.29) | 0.25 (-0.03) |
| sphere / in | 0.97 (n=108, fell 0.01) | 0.98 (+0.01) |
| sphere / out | 0.83 (n=108, fell 0.08) | 0.80 (-0.04) |
| t_shape / in | 0.59 (n=108, fell 0.18) | 0.12 (-0.47) |
| t_shape / out | 0.53 (n=108, fell 0.12) | 0.06 (-0.47) |
| u_channel / in | 0.36 (n=108, fell 0.25) | 0.04 (-0.32) |
| u_channel / out | 0.31 (n=108, fell 0.19) | 0.02 (-0.29) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero |
|---|---|---|
| arch start yaw 0 / in | 0.03 (n=36, fell 0.28) | 0.00 (-0.03) |
| arch start yaw 0 / out | 0.03 (n=36, fell 0.31) | 0.00 (-0.03) |
| arch start yaw 45 / in | 0.08 (n=36, fell 0.28) | 0.03 (-0.06) |
| arch start yaw 45 / out | 0.00 (n=36, fell 0.22) | 0.00 (+0.00) |
| arch start yaw 90 / in | 0.11 (n=36, fell 0.11) | 0.03 (-0.08) |
| arch start yaw 90 / out | 0.03 (n=36, fell 0.14) | 0.03 (+0.00) |
| u_channel start yaw 0 / in | 0.36 (n=36, fell 0.19) | 0.06 (-0.30) |
| u_channel start yaw 0 / out | 0.25 (n=36, fell 0.17) | 0.03 (-0.22) |
| u_channel start yaw 45 / in | 0.25 (n=36, fell 0.28) | 0.00 (-0.25) |
| u_channel start yaw 45 / out | 0.19 (n=36, fell 0.22) | 0.00 (-0.19) |
| u_channel start yaw 90 / in | 0.47 (n=36, fell 0.28) | 0.06 (-0.42) |
| u_channel start yaw 90 / out | 0.47 (n=36, fell 0.19) | 0.03 (-0.44) |

## by group and mass

| | normal | heading_zero |
|---|---|---|
| seen / 10 kg | 0.69 (n=252, fell 0.05) | 0.41 (-0.28) |
| seen / 25 kg | 0.57 (n=252, fell 0.14) | 0.35 (-0.21) |
| seen / 40 kg | 0.33 (n=252, fell 0.26) | 0.23 (-0.10) |
| seen_out_of_range / 10 kg | 0.59 (n=252, fell 0.05) | 0.31 (-0.28) |
| seen_out_of_range / 25 kg | 0.49 (n=252, fell 0.14) | 0.31 (-0.18) |
| seen_out_of_range / 40 kg | 0.28 (n=252, fell 0.30) | 0.22 (-0.06) |
| unseen / 10 kg | 0.48 (n=180, fell 0.12) | 0.18 (-0.30) |
| unseen / 25 kg | 0.32 (n=180, fell 0.31) | 0.09 (-0.22) |
| unseen / 40 kg | 0.09 (n=180, fell 0.38) | 0.03 (-0.06) |
| unseen_out_of_range / 10 kg | 0.45 (n=180, fell 0.09) | 0.22 (-0.23) |
| unseen_out_of_range / 25 kg | 0.37 (n=180, fell 0.24) | 0.12 (-0.24) |
| unseen_out_of_range / 40 kg | 0.10 (n=180, fell 0.32) | 0.04 (-0.06) |
