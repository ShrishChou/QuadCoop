# Stage 2a evaluation: logs/rsl_rl/push2a_anymal_c/2026-10-22_10-31-59_seed0/model_5999.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| seen | 0.70 (n=756, fell 0.04) | 0.47 (-0.23) | 0.69 (-0.02) | 0.64 (-0.06) |
| seen_out_of_range | 0.56 (n=756, fell 0.05) | 0.40 (-0.16) | 0.55 (-0.01) | 0.52 (-0.03) |
| unseen | 0.49 (n=540, fell 0.09) | 0.22 (-0.28) | 0.50 (+0.01) | 0.51 (+0.02) |
| unseen_out_of_range | 0.46 (n=540, fell 0.07) | 0.22 (-0.24) | 0.43 (-0.03) | 0.44 (-0.02) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |action change| per walker command (vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |action| = [20.7173, 8.2531, 3.4993].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [2.4104, 0.9911, 1.1496] | 0.14 | 0.924 |
| profile_zero | [0.6472, 0.3942, 0.4084] | 0.045 | 0.995 |
| profile_roll | [0.6332, 0.4374, 0.4287] | 0.046 | 0.988 |

## success by object and size set

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| arch / in | 0.29 (n=108, fell 0.07) | 0.17 (-0.12) | 0.33 (+0.05) | 0.28 (-0.01) |
| arch / out | 0.25 (n=108, fell 0.08) | 0.06 (-0.19) | 0.21 (-0.04) | 0.24 (-0.01) |
| asym / in | 0.45 (n=108, fell 0.13) | 0.25 (-0.20) | 0.50 (+0.05) | 0.53 (+0.07) |
| asym / out | 0.29 (n=108, fell 0.07) | 0.21 (-0.07) | 0.33 (+0.05) | 0.34 (+0.06) |
| beam / in | 0.41 (n=108, fell 0.15) | 0.06 (-0.35) | 0.37 (-0.04) | 0.45 (+0.05) |
| beam / out | 0.42 (n=108, fell 0.11) | 0.09 (-0.32) | 0.40 (-0.02) | 0.40 (-0.02) |
| cube / in | 0.93 (n=108, fell 0.02) | 0.82 (-0.10) | 0.94 (+0.01) | 0.91 (-0.02) |
| cube / out | 0.56 (n=108, fell 0.04) | 0.52 (-0.04) | 0.57 (+0.02) | 0.57 (+0.02) |
| cylinder / in | 0.36 (n=108, fell 0.05) | 0.13 (-0.23) | 0.37 (+0.01) | 0.35 (-0.01) |
| cylinder / out | 0.35 (n=108, fell 0.06) | 0.26 (-0.09) | 0.33 (-0.02) | 0.34 (-0.01) |
| dumbbell / in | 0.76 (n=108, fell 0.08) | 0.30 (-0.46) | 0.62 (-0.14) | 0.45 (-0.30) |
| dumbbell / out | 0.52 (n=108, fell 0.05) | 0.27 (-0.25) | 0.43 (-0.09) | 0.36 (-0.16) |
| l_shape / in | 0.70 (n=108, fell 0.05) | 0.35 (-0.35) | 0.72 (+0.02) | 0.68 (-0.03) |
| l_shape / out | 0.60 (n=108, fell 0.05) | 0.32 (-0.29) | 0.54 (-0.06) | 0.57 (-0.03) |
| long / in | 0.82 (n=108, fell 0.01) | 0.57 (-0.25) | 0.81 (-0.01) | 0.80 (-0.03) |
| long / out | 0.57 (n=108, fell 0.02) | 0.34 (-0.23) | 0.60 (+0.03) | 0.58 (+0.01) |
| plus / in | 0.23 (n=108, fell 0.10) | 0.07 (-0.16) | 0.24 (+0.01) | 0.29 (+0.06) |
| plus / out | 0.45 (n=108, fell 0.08) | 0.26 (-0.20) | 0.41 (-0.05) | 0.39 (-0.07) |
| sphere / in | 0.98 (n=108, fell 0.02) | 0.98 (+0.00) | 0.99 (+0.01) | 1.00 (+0.02) |
| sphere / out | 0.94 (n=108, fell 0.06) | 0.95 (+0.01) | 0.94 (+0.00) | 0.84 (-0.10) |
| t_shape / in | 0.80 (n=108, fell 0.05) | 0.35 (-0.44) | 0.74 (-0.06) | 0.72 (-0.07) |
| t_shape / out | 0.71 (n=108, fell 0.06) | 0.38 (-0.33) | 0.73 (+0.02) | 0.72 (+0.01) |
| u_channel / in | 0.67 (n=108, fell 0.02) | 0.35 (-0.32) | 0.66 (-0.01) | 0.61 (-0.06) |
| u_channel / out | 0.54 (n=108, fell 0.06) | 0.24 (-0.30) | 0.48 (-0.06) | 0.50 (-0.04) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| arch start yaw 0 / in | 0.33 (n=36, fell 0.06) | 0.14 (-0.19) | 0.33 (+0.00) | 0.22 (-0.11) |
| arch start yaw 0 / out | 0.33 (n=36, fell 0.06) | 0.06 (-0.28) | 0.22 (-0.11) | 0.25 (-0.08) |
| arch start yaw 45 / in | 0.17 (n=36, fell 0.08) | 0.19 (+0.03) | 0.28 (+0.11) | 0.17 (+0.00) |
| arch start yaw 45 / out | 0.14 (n=36, fell 0.14) | 0.06 (-0.08) | 0.17 (+0.03) | 0.22 (+0.08) |
| arch start yaw 90 / in | 0.36 (n=36, fell 0.06) | 0.17 (-0.19) | 0.39 (+0.03) | 0.44 (+0.08) |
| arch start yaw 90 / out | 0.28 (n=36, fell 0.06) | 0.06 (-0.22) | 0.25 (-0.03) | 0.25 (-0.03) |
| u_channel start yaw 0 / in | 0.69 (n=36, fell 0.00) | 0.28 (-0.42) | 0.72 (+0.03) | 0.64 (-0.05) |
| u_channel start yaw 0 / out | 0.47 (n=36, fell 0.08) | 0.25 (-0.22) | 0.50 (+0.03) | 0.47 (+0.00) |
| u_channel start yaw 45 / in | 0.64 (n=36, fell 0.06) | 0.31 (-0.33) | 0.64 (+0.00) | 0.56 (-0.08) |
| u_channel start yaw 45 / out | 0.47 (n=36, fell 0.06) | 0.22 (-0.25) | 0.47 (+0.00) | 0.50 (+0.03) |
| u_channel start yaw 90 / in | 0.67 (n=36, fell 0.00) | 0.47 (-0.20) | 0.61 (-0.06) | 0.64 (-0.03) |
| u_channel start yaw 90 / out | 0.67 (n=36, fell 0.03) | 0.25 (-0.42) | 0.47 (-0.20) | 0.53 (-0.14) |

## by group and mass

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| seen / 10 kg | 0.82 (n=252, fell 0.01) | 0.62 (-0.20) | 0.80 (-0.02) | 0.77 (-0.05) |
| seen / 25 kg | 0.76 (n=252, fell 0.02) | 0.48 (-0.28) | 0.76 (+0.00) | 0.68 (-0.08) |
| seen / 40 kg | 0.54 (n=252, fell 0.09) | 0.33 (-0.22) | 0.50 (-0.04) | 0.49 (-0.05) |
| seen_out_of_range / 10 kg | 0.66 (n=252, fell 0.01) | 0.46 (-0.20) | 0.66 (-0.00) | 0.66 (-0.00) |
| seen_out_of_range / 25 kg | 0.61 (n=252, fell 0.03) | 0.44 (-0.16) | 0.57 (-0.04) | 0.55 (-0.05) |
| seen_out_of_range / 40 kg | 0.41 (n=252, fell 0.11) | 0.28 (-0.12) | 0.41 (+0.00) | 0.36 (-0.04) |
| unseen / 10 kg | 0.76 (n=180, fell 0.01) | 0.32 (-0.44) | 0.69 (-0.07) | 0.73 (-0.03) |
| unseen / 25 kg | 0.51 (n=180, fell 0.08) | 0.25 (-0.26) | 0.57 (+0.07) | 0.59 (+0.09) |
| unseen / 40 kg | 0.21 (n=180, fell 0.18) | 0.08 (-0.13) | 0.23 (+0.02) | 0.21 (-0.01) |
| unseen_out_of_range / 10 kg | 0.65 (n=180, fell 0.00) | 0.34 (-0.31) | 0.61 (-0.04) | 0.61 (-0.04) |
| unseen_out_of_range / 25 kg | 0.55 (n=180, fell 0.06) | 0.28 (-0.27) | 0.48 (-0.07) | 0.54 (-0.01) |
| unseen_out_of_range / 40 kg | 0.18 (n=180, fell 0.16) | 0.05 (-0.13) | 0.20 (+0.02) | 0.18 (+0.00) |
