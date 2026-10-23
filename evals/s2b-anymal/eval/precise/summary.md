# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-anymal/model.pt
success = held within 0.1 m / 3.0 deg for 0.02 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.72 (n=756, fell 0.04) |
| unseen | 0.73 (n=540, fell 0.06) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.6492, 0.7165, 0.7064]; mean |raw output| = [11.82, 11.37, 2.34]; share of outputs beyond the clip = [0.522, 0.573, 0.493].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2988, 0.1979, 0.3882] | 0.427 | 0.749 |
| heading_zero_map | [0.3657, 0.2524, 0.4709] | 0.526 | 0.776 |
| profile_zero | [0.2803, 0.2192, 0.2825] | 0.377 | 0.784 |
| profile_roll | [0.3316, 0.2546, 0.3225] | 0.439 | 0.799 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.43 (n=108, fell 0.07) |
| asym / in | 0.70 (n=108, fell 0.05) |
| beam / in | 0.60 (n=108, fell 0.11) |
| cube / in | 0.94 (n=108, fell 0.02) |
| cylinder / in | 0.40 (n=108, fell 0.06) |
| dumbbell / in | 0.51 (n=108, fell 0.12) |
| l_shape / in | 0.84 (n=108, fell 0.04) |
| long / in | 0.87 (n=108, fell 0.01) |
| plus / in | 0.69 (n=108, fell 0.08) |
| sphere / in | 0.99 (n=108, fell 0.01) |
| t_shape / in | 0.93 (n=108, fell 0.01) |
| u_channel / in | 0.79 (n=108, fell 0.04) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.42 (n=36, fell 0.17) |
| arch start yaw 45 / in | 0.39 (n=36, fell 0.06) |
| arch start yaw 90 / in | 0.47 (n=36, fell 0.00) |
| u_channel start yaw 0 / in | 0.78 (n=36, fell 0.06) |
| u_channel start yaw 45 / in | 0.81 (n=36, fell 0.06) |
| u_channel start yaw 90 / in | 0.78 (n=36, fell 0.00) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.77 (n=252, fell 0.01) |
| seen / 25 kg | 0.74 (n=252, fell 0.02) |
| seen / 40 kg | 0.66 (n=252, fell 0.10) |
| unseen / 10 kg | 0.82 (n=180, fell 0.01) |
| unseen / 25 kg | 0.84 (n=180, fell 0.02) |
| unseen / 40 kg | 0.52 (n=180, fell 0.16) |
