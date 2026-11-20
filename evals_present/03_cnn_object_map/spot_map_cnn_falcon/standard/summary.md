# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-spot-falcon/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| seen | 0.62 (n=756, fell 0.09) | 0.45 (-0.17) | 0.34 (-0.29) | 0.56 (-0.06) | 0.48 (-0.14) |
| seen_out_of_range | 0.53 (n=756, fell 0.11) | 0.41 (-0.12) | 0.29 (-0.24) | 0.46 (-0.07) | 0.42 (-0.11) |
| unseen | 0.50 (n=540, fell 0.14) | 0.31 (-0.19) | 0.22 (-0.29) | 0.41 (-0.09) | 0.44 (-0.06) |
| unseen_out_of_range | 0.47 (n=540, fell 0.13) | 0.29 (-0.18) | 0.18 (-0.28) | 0.39 (-0.08) | 0.35 (-0.12) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7817, 0.7824, 0.7814]; mean |raw output| = [7.82, 4.4, 2.61]; share of outputs beyond the clip = [0.628, 0.614, 0.597].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2342, 0.1815, 0.187] | 0.257 | 0.736 |
| heading_zero_map | [0.3151, 0.249, 0.2335] | 0.34 | 0.771 |
| profile_zero | [0.2189, 0.2049, 0.184] | 0.259 | 0.804 |
| profile_roll | [0.2539, 0.2609, 0.2344] | 0.319 | 0.818 |

## success by object and size set

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| arch / in | 0.09 (n=108, fell 0.17) | 0.04 (-0.06) | 0.02 (-0.07) | 0.02 (-0.07) | 0.02 (-0.07) |
| arch / out | 0.09 (n=108, fell 0.32) | 0.04 (-0.06) | 0.00 (-0.09) | 0.02 (-0.07) | 0.01 (-0.08) |
| asym / in | 0.48 (n=108, fell 0.18) | 0.35 (-0.13) | 0.13 (-0.35) | 0.50 (+0.02) | 0.44 (-0.04) |
| asym / out | 0.43 (n=108, fell 0.16) | 0.26 (-0.18) | 0.13 (-0.30) | 0.40 (-0.04) | 0.32 (-0.12) |
| beam / in | 0.37 (n=108, fell 0.07) | 0.10 (-0.27) | 0.05 (-0.32) | 0.31 (-0.06) | 0.29 (-0.08) |
| beam / out | 0.37 (n=108, fell 0.07) | 0.12 (-0.25) | 0.02 (-0.35) | 0.27 (-0.10) | 0.18 (-0.18) |
| cube / in | 0.84 (n=108, fell 0.04) | 0.69 (-0.15) | 0.72 (-0.12) | 0.81 (-0.03) | 0.79 (-0.06) |
| cube / out | 0.71 (n=108, fell 0.05) | 0.58 (-0.13) | 0.57 (-0.14) | 0.67 (-0.05) | 0.64 (-0.07) |
| cylinder / in | 0.43 (n=108, fell 0.07) | 0.34 (-0.09) | 0.23 (-0.20) | 0.43 (-0.01) | 0.38 (-0.05) |
| cylinder / out | 0.35 (n=108, fell 0.11) | 0.31 (-0.05) | 0.11 (-0.24) | 0.33 (-0.02) | 0.29 (-0.07) |
| dumbbell / in | 0.53 (n=108, fell 0.17) | 0.21 (-0.32) | 0.08 (-0.45) | 0.44 (-0.08) | 0.14 (-0.39) |
| dumbbell / out | 0.29 (n=108, fell 0.09) | 0.11 (-0.18) | 0.05 (-0.24) | 0.16 (-0.13) | 0.10 (-0.18) |
| l_shape / in | 0.55 (n=108, fell 0.19) | 0.51 (-0.04) | 0.34 (-0.20) | 0.40 (-0.15) | 0.50 (-0.05) |
| l_shape / out | 0.48 (n=108, fell 0.18) | 0.40 (-0.08) | 0.28 (-0.20) | 0.38 (-0.10) | 0.42 (-0.06) |
| long / in | 0.79 (n=108, fell 0.07) | 0.56 (-0.23) | 0.23 (-0.56) | 0.66 (-0.13) | 0.51 (-0.28) |
| long / out | 0.69 (n=108, fell 0.07) | 0.49 (-0.19) | 0.24 (-0.44) | 0.56 (-0.13) | 0.48 (-0.20) |
| plus / in | 0.59 (n=108, fell 0.12) | 0.50 (-0.09) | 0.52 (-0.07) | 0.40 (-0.19) | 0.53 (-0.06) |
| plus / out | 0.53 (n=108, fell 0.08) | 0.53 (+0.00) | 0.45 (-0.07) | 0.49 (-0.04) | 0.51 (-0.02) |
| sphere / in | 1.00 (n=108, fell 0.00) | 0.98 (-0.02) | 0.98 (-0.02) | 0.98 (-0.02) | 0.94 (-0.06) |
| sphere / out | 0.93 (n=108, fell 0.05) | 0.92 (-0.01) | 0.94 (+0.01) | 0.91 (-0.02) | 0.88 (-0.05) |
| t_shape / in | 0.69 (n=108, fell 0.12) | 0.34 (-0.34) | 0.07 (-0.61) | 0.60 (-0.08) | 0.61 (-0.07) |
| t_shape / out | 0.66 (n=108, fell 0.11) | 0.40 (-0.26) | 0.12 (-0.54) | 0.56 (-0.09) | 0.52 (-0.14) |
| u_channel / in | 0.52 (n=108, fell 0.15) | 0.08 (-0.44) | 0.05 (-0.47) | 0.47 (-0.05) | 0.44 (-0.08) |
| u_channel / out | 0.54 (n=108, fell 0.18) | 0.17 (-0.37) | 0.05 (-0.49) | 0.43 (-0.11) | 0.34 (-0.19) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| arch start yaw 0 / in | 0.03 (n=36, fell 0.25) | 0.00 (-0.03) | 0.00 (-0.03) | 0.00 (-0.03) | 0.03 (+0.00) |
| arch start yaw 0 / out | 0.06 (n=36, fell 0.22) | 0.03 (-0.03) | 0.00 (-0.06) | 0.00 (-0.06) | 0.00 (-0.06) |
| arch start yaw 45 / in | 0.14 (n=36, fell 0.14) | 0.03 (-0.11) | 0.03 (-0.11) | 0.00 (-0.14) | 0.00 (-0.14) |
| arch start yaw 45 / out | 0.08 (n=36, fell 0.39) | 0.06 (-0.03) | 0.00 (-0.08) | 0.00 (-0.08) | 0.00 (-0.08) |
| arch start yaw 90 / in | 0.11 (n=36, fell 0.11) | 0.08 (-0.03) | 0.03 (-0.08) | 0.06 (-0.06) | 0.03 (-0.08) |
| arch start yaw 90 / out | 0.14 (n=36, fell 0.33) | 0.03 (-0.11) | 0.00 (-0.14) | 0.06 (-0.08) | 0.03 (-0.11) |
| u_channel start yaw 0 / in | 0.50 (n=36, fell 0.14) | 0.14 (-0.36) | 0.08 (-0.42) | 0.47 (-0.03) | 0.42 (-0.08) |
| u_channel start yaw 0 / out | 0.58 (n=36, fell 0.14) | 0.14 (-0.44) | 0.06 (-0.53) | 0.50 (-0.08) | 0.28 (-0.30) |
| u_channel start yaw 45 / in | 0.47 (n=36, fell 0.14) | 0.00 (-0.47) | 0.00 (-0.47) | 0.39 (-0.08) | 0.42 (-0.05) |
| u_channel start yaw 45 / out | 0.42 (n=36, fell 0.17) | 0.17 (-0.25) | 0.06 (-0.36) | 0.28 (-0.14) | 0.31 (-0.11) |
| u_channel start yaw 90 / in | 0.58 (n=36, fell 0.17) | 0.11 (-0.47) | 0.06 (-0.53) | 0.56 (-0.03) | 0.50 (-0.08) |
| u_channel start yaw 90 / out | 0.61 (n=36, fell 0.22) | 0.19 (-0.42) | 0.03 (-0.58) | 0.50 (-0.11) | 0.44 (-0.17) |

## by group and mass

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| seen / 10 kg | 0.75 (n=252, fell 0.07) | 0.57 (-0.19) | 0.38 (-0.38) | 0.69 (-0.06) | 0.59 (-0.16) |
| seen / 25 kg | 0.68 (n=252, fell 0.06) | 0.49 (-0.19) | 0.37 (-0.31) | 0.63 (-0.05) | 0.54 (-0.14) |
| seen / 40 kg | 0.44 (n=252, fell 0.14) | 0.30 (-0.14) | 0.26 (-0.19) | 0.37 (-0.07) | 0.33 (-0.12) |
| seen_out_of_range / 10 kg | 0.64 (n=252, fell 0.08) | 0.49 (-0.15) | 0.32 (-0.32) | 0.54 (-0.10) | 0.48 (-0.16) |
| seen_out_of_range / 25 kg | 0.54 (n=252, fell 0.11) | 0.45 (-0.08) | 0.31 (-0.22) | 0.51 (-0.03) | 0.48 (-0.06) |
| seen_out_of_range / 40 kg | 0.42 (n=252, fell 0.15) | 0.27 (-0.14) | 0.23 (-0.18) | 0.33 (-0.09) | 0.29 (-0.13) |
| unseen / 10 kg | 0.72 (n=180, fell 0.06) | 0.44 (-0.28) | 0.30 (-0.42) | 0.63 (-0.08) | 0.68 (-0.04) |
| unseen / 25 kg | 0.61 (n=180, fell 0.16) | 0.37 (-0.24) | 0.25 (-0.36) | 0.49 (-0.12) | 0.51 (-0.10) |
| unseen / 40 kg | 0.18 (n=180, fell 0.22) | 0.12 (-0.06) | 0.10 (-0.08) | 0.12 (-0.06) | 0.13 (-0.04) |
| unseen_out_of_range / 10 kg | 0.69 (n=180, fell 0.05) | 0.38 (-0.31) | 0.27 (-0.42) | 0.59 (-0.09) | 0.51 (-0.18) |
| unseen_out_of_range / 25 kg | 0.57 (n=180, fell 0.13) | 0.41 (-0.16) | 0.20 (-0.37) | 0.44 (-0.13) | 0.39 (-0.18) |
| unseen_out_of_range / 40 kg | 0.15 (n=180, fell 0.22) | 0.09 (-0.06) | 0.09 (-0.06) | 0.14 (-0.01) | 0.16 (+0.01) |
