# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-anymal-term80/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero |
|---|---|---|
| seen | 0.62 (n=756, fell 0.04) | 0.45 (-0.18) |
| seen_out_of_range | 0.53 (n=756, fell 0.06) | 0.34 (-0.19) |
| unseen | 0.49 (n=540, fell 0.05) | 0.23 (-0.25) |
| unseen_out_of_range | 0.36 (n=540, fell 0.07) | 0.21 (-0.16) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.8789, 0.9015, 0.7913]; mean |raw output| = [36.52, 13.53, 3.09]; share of outputs beyond the clip = [0.788, 0.821, 0.611].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2721, 0.1666, 0.419] | 0.334 | 0.648 |

## success by object and size set

| | normal | heading_zero |
|---|---|---|
| arch / in | 0.17 (n=108, fell 0.07) | 0.07 (-0.09) |
| arch / out | 0.20 (n=108, fell 0.17) | 0.07 (-0.13) |
| asym / in | 0.43 (n=108, fell 0.07) | 0.24 (-0.19) |
| asym / out | 0.26 (n=108, fell 0.07) | 0.15 (-0.11) |
| beam / in | 0.39 (n=108, fell 0.07) | 0.12 (-0.27) |
| beam / out | 0.32 (n=108, fell 0.11) | 0.13 (-0.18) |
| cube / in | 0.93 (n=108, fell 0.01) | 0.86 (-0.07) |
| cube / out | 0.56 (n=108, fell 0.01) | 0.46 (-0.09) |
| cylinder / in | 0.39 (n=108, fell 0.05) | 0.12 (-0.27) |
| cylinder / out | 0.28 (n=108, fell 0.07) | 0.18 (-0.10) |
| dumbbell / in | 0.58 (n=108, fell 0.07) | 0.20 (-0.38) |
| dumbbell / out | 0.52 (n=108, fell 0.03) | 0.15 (-0.37) |
| l_shape / in | 0.56 (n=108, fell 0.04) | 0.40 (-0.16) |
| l_shape / out | 0.43 (n=108, fell 0.04) | 0.26 (-0.17) |
| long / in | 0.76 (n=108, fell 0.01) | 0.56 (-0.19) |
| long / out | 0.59 (n=108, fell 0.03) | 0.33 (-0.26) |
| plus / in | 0.50 (n=108, fell 0.07) | 0.20 (-0.30) |
| plus / out | 0.42 (n=108, fell 0.07) | 0.35 (-0.07) |
| sphere / in | 0.99 (n=108, fell 0.01) | 0.98 (-0.01) |
| sphere / out | 0.96 (n=108, fell 0.04) | 0.93 (-0.04) |
| t_shape / in | 0.56 (n=108, fell 0.05) | 0.33 (-0.22) |
| t_shape / out | 0.59 (n=108, fell 0.06) | 0.27 (-0.32) |
| u_channel / in | 0.56 (n=108, fell 0.03) | 0.20 (-0.35) |
| u_channel / out | 0.40 (n=108, fell 0.07) | 0.15 (-0.25) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero |
|---|---|---|
| arch start yaw 0 / in | 0.19 (n=36, fell 0.08) | 0.06 (-0.14) |
| arch start yaw 0 / out | 0.31 (n=36, fell 0.22) | 0.06 (-0.25) |
| arch start yaw 45 / in | 0.06 (n=36, fell 0.06) | 0.00 (-0.06) |
| arch start yaw 45 / out | 0.08 (n=36, fell 0.17) | 0.03 (-0.06) |
| arch start yaw 90 / in | 0.25 (n=36, fell 0.06) | 0.17 (-0.08) |
| arch start yaw 90 / out | 0.22 (n=36, fell 0.11) | 0.14 (-0.08) |
| u_channel start yaw 0 / in | 0.64 (n=36, fell 0.08) | 0.28 (-0.36) |
| u_channel start yaw 0 / out | 0.44 (n=36, fell 0.08) | 0.17 (-0.28) |
| u_channel start yaw 45 / in | 0.53 (n=36, fell 0.00) | 0.14 (-0.39) |
| u_channel start yaw 45 / out | 0.31 (n=36, fell 0.08) | 0.08 (-0.22) |
| u_channel start yaw 90 / in | 0.50 (n=36, fell 0.00) | 0.19 (-0.31) |
| u_channel start yaw 90 / out | 0.44 (n=36, fell 0.03) | 0.19 (-0.25) |

## by group and mass

| | normal | heading_zero |
|---|---|---|
| seen / 10 kg | 0.73 (n=252, fell 0.01) | 0.56 (-0.17) |
| seen / 25 kg | 0.67 (n=252, fell 0.03) | 0.48 (-0.20) |
| seen / 40 kg | 0.47 (n=252, fell 0.07) | 0.31 (-0.17) |
| seen_out_of_range / 10 kg | 0.64 (n=252, fell 0.01) | 0.45 (-0.19) |
| seen_out_of_range / 25 kg | 0.54 (n=252, fell 0.05) | 0.35 (-0.18) |
| seen_out_of_range / 40 kg | 0.41 (n=252, fell 0.10) | 0.22 (-0.19) |
| unseen / 10 kg | 0.67 (n=180, fell 0.00) | 0.38 (-0.29) |
| unseen / 25 kg | 0.59 (n=180, fell 0.04) | 0.23 (-0.36) |
| unseen / 40 kg | 0.20 (n=180, fell 0.11) | 0.09 (-0.11) |
| unseen_out_of_range / 10 kg | 0.49 (n=180, fell 0.01) | 0.33 (-0.17) |
| unseen_out_of_range / 25 kg | 0.44 (n=180, fell 0.04) | 0.22 (-0.22) |
| unseen_out_of_range / 40 kg | 0.16 (n=180, fell 0.16) | 0.08 (-0.08) |
