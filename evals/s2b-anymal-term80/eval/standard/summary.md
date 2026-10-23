# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-anymal-term80/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 40.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| seen | 0.73 (n=756, fell 0.02) | 0.59 (-0.14) | 0.44 (-0.29) | 0.67 (-0.05) | 0.59 (-0.14) |
| seen_out_of_range | 0.57 (n=756, fell 0.03) | 0.47 (-0.10) | 0.38 (-0.19) | 0.56 (-0.01) | 0.52 (-0.05) |
| unseen | 0.58 (n=540, fell 0.04) | 0.29 (-0.29) | 0.21 (-0.37) | 0.48 (-0.10) | 0.52 (-0.06) |
| unseen_out_of_range | 0.49 (n=540, fell 0.03) | 0.30 (-0.18) | 0.20 (-0.29) | 0.46 (-0.03) | 0.44 (-0.04) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.8047, 0.8264, 0.7178]; mean |raw output| = [16.16, 16.44, 2.23]; share of outputs beyond the clip = [0.678, 0.699, 0.498].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.271, 0.2054, 0.3497] | 0.352 | 0.718 |
| heading_zero_map | [0.3091, 0.2613, 0.4069] | 0.416 | 0.746 |
| profile_zero | [0.239, 0.2078, 0.2808] | 0.31 | 0.777 |
| profile_roll | [0.264, 0.2499, 0.3554] | 0.37 | 0.792 |

## success by object and size set

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| arch / in | 0.42 (n=108, fell 0.04) | 0.24 (-0.18) | 0.03 (-0.39) | 0.23 (-0.19) | 0.15 (-0.27) |
| arch / out | 0.26 (n=108, fell 0.05) | 0.23 (-0.03) | 0.07 (-0.19) | 0.19 (-0.07) | 0.20 (-0.06) |
| asym / in | 0.54 (n=108, fell 0.01) | 0.38 (-0.16) | 0.21 (-0.32) | 0.53 (-0.01) | 0.53 (-0.01) |
| asym / out | 0.32 (n=108, fell 0.04) | 0.20 (-0.11) | 0.09 (-0.22) | 0.32 (+0.00) | 0.33 (+0.02) |
| beam / in | 0.42 (n=108, fell 0.07) | 0.18 (-0.23) | 0.05 (-0.37) | 0.37 (-0.05) | 0.46 (+0.05) |
| beam / out | 0.40 (n=108, fell 0.07) | 0.26 (-0.14) | 0.11 (-0.29) | 0.44 (+0.05) | 0.43 (+0.03) |
| cube / in | 0.91 (n=108, fell 0.02) | 0.88 (-0.03) | 0.92 (+0.01) | 0.95 (+0.05) | 0.92 (+0.01) |
| cube / out | 0.56 (n=108, fell 0.00) | 0.55 (-0.01) | 0.52 (-0.04) | 0.57 (+0.02) | 0.52 (-0.04) |
| cylinder / in | 0.39 (n=108, fell 0.05) | 0.30 (-0.09) | 0.04 (-0.35) | 0.37 (-0.02) | 0.36 (-0.03) |
| cylinder / out | 0.35 (n=108, fell 0.05) | 0.26 (-0.09) | 0.23 (-0.12) | 0.35 (+0.00) | 0.37 (+0.02) |
| dumbbell / in | 0.73 (n=108, fell 0.04) | 0.36 (-0.37) | 0.29 (-0.44) | 0.64 (-0.09) | 0.26 (-0.47) |
| dumbbell / out | 0.55 (n=108, fell 0.04) | 0.32 (-0.23) | 0.28 (-0.27) | 0.45 (-0.09) | 0.38 (-0.17) |
| l_shape / in | 0.79 (n=108, fell 0.02) | 0.36 (-0.43) | 0.19 (-0.59) | 0.68 (-0.11) | 0.64 (-0.15) |
| l_shape / out | 0.68 (n=108, fell 0.01) | 0.37 (-0.31) | 0.19 (-0.48) | 0.64 (-0.04) | 0.59 (-0.08) |
| long / in | 0.84 (n=108, fell 0.00) | 0.79 (-0.06) | 0.46 (-0.38) | 0.80 (-0.05) | 0.82 (-0.02) |
| long / out | 0.58 (n=108, fell 0.01) | 0.43 (-0.15) | 0.19 (-0.39) | 0.58 (+0.00) | 0.58 (+0.00) |
| plus / in | 0.45 (n=108, fell 0.05) | 0.29 (-0.17) | 0.44 (-0.01) | 0.21 (-0.24) | 0.31 (-0.15) |
| plus / out | 0.53 (n=108, fell 0.01) | 0.38 (-0.15) | 0.43 (-0.09) | 0.40 (-0.13) | 0.43 (-0.10) |
| sphere / in | 1.00 (n=108, fell 0.00) | 0.99 (-0.01) | 1.00 (+0.00) | 1.00 (+0.00) | 0.97 (-0.03) |
| sphere / out | 0.94 (n=108, fell 0.04) | 0.97 (+0.04) | 0.98 (+0.05) | 0.99 (+0.06) | 0.87 (-0.07) |
| t_shape / in | 0.80 (n=108, fell 0.02) | 0.58 (-0.21) | 0.35 (-0.44) | 0.70 (-0.09) | 0.65 (-0.15) |
| t_shape / out | 0.77 (n=108, fell 0.01) | 0.50 (-0.27) | 0.36 (-0.41) | 0.76 (-0.01) | 0.72 (-0.05) |
| u_channel / in | 0.70 (n=108, fell 0.04) | 0.23 (-0.47) | 0.17 (-0.54) | 0.60 (-0.10) | 0.64 (-0.06) |
| u_channel / out | 0.52 (n=108, fell 0.03) | 0.30 (-0.22) | 0.15 (-0.37) | 0.48 (-0.04) | 0.43 (-0.08) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| arch start yaw 0 / in | 0.39 (n=36, fell 0.11) | 0.25 (-0.14) | 0.03 (-0.36) | 0.25 (-0.14) | 0.11 (-0.28) |
| arch start yaw 0 / out | 0.33 (n=36, fell 0.08) | 0.19 (-0.14) | 0.06 (-0.28) | 0.28 (-0.05) | 0.22 (-0.11) |
| arch start yaw 45 / in | 0.39 (n=36, fell 0.00) | 0.17 (-0.22) | 0.03 (-0.36) | 0.14 (-0.25) | 0.11 (-0.28) |
| arch start yaw 45 / out | 0.14 (n=36, fell 0.03) | 0.19 (+0.05) | 0.06 (-0.08) | 0.06 (-0.08) | 0.08 (-0.06) |
| arch start yaw 90 / in | 0.47 (n=36, fell 0.00) | 0.31 (-0.17) | 0.03 (-0.44) | 0.31 (-0.17) | 0.22 (-0.25) |
| arch start yaw 90 / out | 0.31 (n=36, fell 0.03) | 0.31 (+0.00) | 0.08 (-0.22) | 0.25 (-0.06) | 0.31 (+0.00) |
| u_channel start yaw 0 / in | 0.72 (n=36, fell 0.03) | 0.19 (-0.53) | 0.17 (-0.55) | 0.58 (-0.14) | 0.69 (-0.03) |
| u_channel start yaw 0 / out | 0.53 (n=36, fell 0.03) | 0.39 (-0.14) | 0.19 (-0.33) | 0.47 (-0.06) | 0.50 (-0.03) |
| u_channel start yaw 45 / in | 0.72 (n=36, fell 0.03) | 0.33 (-0.39) | 0.17 (-0.55) | 0.64 (-0.08) | 0.61 (-0.11) |
| u_channel start yaw 45 / out | 0.47 (n=36, fell 0.03) | 0.19 (-0.28) | 0.11 (-0.36) | 0.39 (-0.08) | 0.31 (-0.17) |
| u_channel start yaw 90 / in | 0.67 (n=36, fell 0.06) | 0.17 (-0.50) | 0.17 (-0.50) | 0.58 (-0.08) | 0.61 (-0.06) |
| u_channel start yaw 90 / out | 0.56 (n=36, fell 0.03) | 0.31 (-0.25) | 0.14 (-0.42) | 0.58 (+0.03) | 0.50 (-0.06) |

## by group and mass

| | normal | heading_zero | heading_zero_map | profile_zero | profile_roll |
|---|---|---|---|---|---|
| seen / 10 kg | 0.83 (n=252, fell 0.00) | 0.74 (-0.09) | 0.53 (-0.30) | 0.76 (-0.07) | 0.69 (-0.14) |
| seen / 25 kg | 0.79 (n=252, fell 0.03) | 0.61 (-0.18) | 0.45 (-0.34) | 0.74 (-0.05) | 0.62 (-0.17) |
| seen / 40 kg | 0.55 (n=252, fell 0.04) | 0.42 (-0.13) | 0.34 (-0.22) | 0.51 (-0.04) | 0.45 (-0.10) |
| seen_out_of_range / 10 kg | 0.67 (n=252, fell 0.01) | 0.59 (-0.08) | 0.48 (-0.19) | 0.64 (-0.02) | 0.60 (-0.07) |
| seen_out_of_range / 25 kg | 0.63 (n=252, fell 0.02) | 0.49 (-0.14) | 0.41 (-0.21) | 0.60 (-0.02) | 0.56 (-0.07) |
| seen_out_of_range / 40 kg | 0.42 (n=252, fell 0.05) | 0.31 (-0.11) | 0.24 (-0.18) | 0.43 (+0.01) | 0.41 (-0.01) |
| unseen / 10 kg | 0.77 (n=180, fell 0.00) | 0.47 (-0.30) | 0.33 (-0.43) | 0.67 (-0.10) | 0.73 (-0.04) |
| unseen / 25 kg | 0.67 (n=180, fell 0.02) | 0.30 (-0.37) | 0.23 (-0.44) | 0.56 (-0.11) | 0.60 (-0.07) |
| unseen / 40 kg | 0.31 (n=180, fell 0.09) | 0.10 (-0.21) | 0.08 (-0.23) | 0.21 (-0.10) | 0.22 (-0.09) |
| unseen_out_of_range / 10 kg | 0.64 (n=180, fell 0.00) | 0.42 (-0.22) | 0.28 (-0.36) | 0.68 (+0.04) | 0.59 (-0.05) |
| unseen_out_of_range / 25 kg | 0.57 (n=180, fell 0.03) | 0.36 (-0.21) | 0.23 (-0.33) | 0.49 (-0.08) | 0.54 (-0.03) |
| unseen_out_of_range / 40 kg | 0.26 (n=180, fell 0.06) | 0.13 (-0.13) | 0.08 (-0.18) | 0.20 (-0.06) | 0.19 (-0.06) |
