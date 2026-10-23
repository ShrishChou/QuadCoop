# Stage 2a evaluation: logs/rsl_rl/push2a_spot/2026-10-22_10-39-43_seed0/model_5999.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| seen | 0.48 (n=756, fell 0.12) | 0.34 (-0.15) | 0.47 (-0.01) | 0.48 (-0.01) |
| seen_out_of_range | 0.40 (n=756, fell 0.14) | 0.29 (-0.11) | 0.39 (-0.01) | 0.40 (-0.00) |
| unseen | 0.36 (n=540, fell 0.14) | 0.21 (-0.14) | 0.33 (-0.03) | 0.38 (+0.02) |
| unseen_out_of_range | 0.32 (n=540, fell 0.11) | 0.17 (-0.16) | 0.29 (-0.04) | 0.29 (-0.04) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |action change| per walker command (vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |action| = [35.03, 9.605, 1.5677].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [1.0836, 0.6377, 0.5414] | 0.049 | 0.924 |
| profile_zero | [0.1754, 0.1394, 0.1072] | 0.009 | 0.948 |
| profile_roll | [0.1977, 0.1685, 0.1301] | 0.011 | 0.903 |

## success by object and size set

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| arch / in | 0.13 (n=108, fell 0.14) | 0.00 (-0.13) | 0.16 (+0.03) | 0.13 (+0.00) |
| arch / out | 0.12 (n=108, fell 0.19) | 0.01 (-0.11) | 0.11 (-0.01) | 0.12 (+0.00) |
| asym / in | 0.30 (n=108, fell 0.09) | 0.21 (-0.08) | 0.33 (+0.04) | 0.34 (+0.05) |
| asym / out | 0.26 (n=108, fell 0.07) | 0.15 (-0.11) | 0.25 (-0.01) | 0.27 (+0.01) |
| beam / in | 0.18 (n=108, fell 0.24) | 0.08 (-0.10) | 0.13 (-0.05) | 0.21 (+0.03) |
| beam / out | 0.24 (n=108, fell 0.13) | 0.06 (-0.18) | 0.19 (-0.05) | 0.14 (-0.10) |
| cube / in | 0.63 (n=108, fell 0.13) | 0.60 (-0.03) | 0.63 (+0.00) | 0.64 (+0.01) |
| cube / out | 0.44 (n=108, fell 0.11) | 0.48 (+0.04) | 0.41 (-0.04) | 0.43 (-0.02) |
| cylinder / in | 0.33 (n=108, fell 0.15) | 0.09 (-0.24) | 0.31 (-0.03) | 0.38 (+0.05) |
| cylinder / out | 0.26 (n=108, fell 0.28) | 0.10 (-0.16) | 0.28 (+0.02) | 0.29 (+0.03) |
| dumbbell / in | 0.33 (n=108, fell 0.10) | 0.11 (-0.22) | 0.25 (-0.08) | 0.18 (-0.15) |
| dumbbell / out | 0.16 (n=108, fell 0.10) | 0.06 (-0.10) | 0.15 (-0.01) | 0.18 (+0.03) |
| l_shape / in | 0.42 (n=108, fell 0.15) | 0.20 (-0.21) | 0.36 (-0.06) | 0.47 (+0.05) |
| l_shape / out | 0.34 (n=108, fell 0.13) | 0.19 (-0.15) | 0.27 (-0.07) | 0.35 (+0.01) |
| long / in | 0.56 (n=108, fell 0.12) | 0.39 (-0.18) | 0.65 (+0.08) | 0.62 (+0.06) |
| long / out | 0.54 (n=108, fell 0.09) | 0.28 (-0.26) | 0.52 (-0.02) | 0.49 (-0.05) |
| plus / in | 0.57 (n=108, fell 0.14) | 0.50 (-0.07) | 0.55 (-0.03) | 0.52 (-0.05) |
| plus / out | 0.50 (n=108, fell 0.15) | 0.38 (-0.12) | 0.54 (+0.04) | 0.48 (-0.02) |
| sphere / in | 0.94 (n=108, fell 0.07) | 0.95 (+0.02) | 0.86 (-0.07) | 0.92 (-0.02) |
| sphere / out | 0.92 (n=108, fell 0.05) | 0.93 (+0.01) | 0.88 (-0.04) | 0.86 (-0.06) |
| t_shape / in | 0.47 (n=108, fell 0.14) | 0.20 (-0.27) | 0.46 (-0.01) | 0.46 (-0.01) |
| t_shape / out | 0.36 (n=108, fell 0.14) | 0.20 (-0.16) | 0.39 (+0.03) | 0.40 (+0.04) |
| u_channel / in | 0.32 (n=108, fell 0.07) | 0.07 (-0.25) | 0.30 (-0.03) | 0.35 (+0.03) |
| u_channel / out | 0.28 (n=108, fell 0.08) | 0.06 (-0.22) | 0.19 (-0.08) | 0.20 (-0.07) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| arch start yaw 0 / in | 0.14 (n=36, fell 0.14) | 0.00 (-0.14) | 0.11 (-0.03) | 0.14 (+0.00) |
| arch start yaw 0 / out | 0.08 (n=36, fell 0.11) | 0.03 (-0.06) | 0.06 (-0.03) | 0.11 (+0.03) |
| arch start yaw 45 / in | 0.03 (n=36, fell 0.25) | 0.00 (-0.03) | 0.11 (+0.08) | 0.11 (+0.08) |
| arch start yaw 45 / out | 0.14 (n=36, fell 0.14) | 0.00 (-0.14) | 0.11 (-0.03) | 0.08 (-0.06) |
| arch start yaw 90 / in | 0.22 (n=36, fell 0.03) | 0.00 (-0.22) | 0.25 (+0.03) | 0.14 (-0.08) |
| arch start yaw 90 / out | 0.14 (n=36, fell 0.33) | 0.00 (-0.14) | 0.17 (+0.03) | 0.17 (+0.03) |
| u_channel start yaw 0 / in | 0.22 (n=36, fell 0.06) | 0.08 (-0.14) | 0.22 (+0.00) | 0.22 (+0.00) |
| u_channel start yaw 0 / out | 0.31 (n=36, fell 0.11) | 0.03 (-0.28) | 0.17 (-0.14) | 0.25 (-0.06) |
| u_channel start yaw 45 / in | 0.39 (n=36, fell 0.00) | 0.14 (-0.25) | 0.42 (+0.03) | 0.33 (-0.06) |
| u_channel start yaw 45 / out | 0.25 (n=36, fell 0.06) | 0.11 (-0.14) | 0.22 (-0.03) | 0.22 (-0.03) |
| u_channel start yaw 90 / in | 0.36 (n=36, fell 0.14) | 0.00 (-0.36) | 0.25 (-0.11) | 0.50 (+0.14) |
| u_channel start yaw 90 / out | 0.28 (n=36, fell 0.08) | 0.03 (-0.25) | 0.19 (-0.08) | 0.14 (-0.14) |

## by group and mass

| | normal | heading_zero | profile_zero | profile_roll |
|---|---|---|---|---|
| seen / 10 kg | 0.64 (n=252, fell 0.08) | 0.42 (-0.22) | 0.59 (-0.05) | 0.59 (-0.04) |
| seen / 25 kg | 0.56 (n=252, fell 0.12) | 0.38 (-0.18) | 0.57 (+0.01) | 0.57 (+0.01) |
| seen / 40 kg | 0.26 (n=252, fell 0.16) | 0.21 (-0.05) | 0.27 (+0.00) | 0.27 (+0.00) |
| seen_out_of_range / 10 kg | 0.53 (n=252, fell 0.10) | 0.36 (-0.17) | 0.46 (-0.06) | 0.51 (-0.02) |
| seen_out_of_range / 25 kg | 0.45 (n=252, fell 0.15) | 0.33 (-0.12) | 0.48 (+0.03) | 0.44 (-0.01) |
| seen_out_of_range / 40 kg | 0.22 (n=252, fell 0.16) | 0.19 (-0.03) | 0.23 (+0.01) | 0.24 (+0.02) |
| unseen / 10 kg | 0.60 (n=180, fell 0.10) | 0.34 (-0.26) | 0.53 (-0.07) | 0.62 (+0.02) |
| unseen / 25 kg | 0.39 (n=180, fell 0.14) | 0.27 (-0.13) | 0.33 (-0.06) | 0.43 (+0.03) |
| unseen / 40 kg | 0.08 (n=180, fell 0.17) | 0.04 (-0.04) | 0.13 (+0.05) | 0.09 (+0.01) |
| unseen_out_of_range / 10 kg | 0.52 (n=180, fell 0.08) | 0.26 (-0.26) | 0.44 (-0.08) | 0.42 (-0.10) |
| unseen_out_of_range / 25 kg | 0.37 (n=180, fell 0.14) | 0.19 (-0.18) | 0.36 (-0.01) | 0.38 (+0.01) |
| unseen_out_of_range / 40 kg | 0.08 (n=180, fell 0.11) | 0.06 (-0.03) | 0.07 (-0.02) | 0.06 (-0.02) |
