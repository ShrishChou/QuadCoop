# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-spot/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.63 (n=756, fell 0.13) |
| unseen | 0.58 (n=540, fell 0.18) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.6817, 0.6693, 0.6851]; mean |raw output| = [19.7, 7.67, 3.32]; share of outputs beyond the clip = [0.54, 0.509, 0.464].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2743, 0.2544, 0.2623] | 0.388 | 0.789 |
| heading_zero_map | [0.3655, 0.2813, 0.2962] | 0.463 | 0.813 |
| profile_zero | [0.1505, 0.2256, 0.1701] | 0.268 | 0.82 |
| profile_roll | [0.1899, 0.2941, 0.2058] | 0.339 | 0.833 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.20 (n=108, fell 0.18) |
| asym / in | 0.54 (n=108, fell 0.21) |
| beam / in | 0.31 (n=108, fell 0.28) |
| cube / in | 0.85 (n=108, fell 0.10) |
| cylinder / in | 0.40 (n=108, fell 0.14) |
| dumbbell / in | 0.48 (n=108, fell 0.12) |
| l_shape / in | 0.75 (n=108, fell 0.12) |
| long / in | 0.80 (n=108, fell 0.17) |
| plus / in | 0.62 (n=108, fell 0.16) |
| sphere / in | 0.92 (n=108, fell 0.08) |
| t_shape / in | 0.74 (n=108, fell 0.15) |
| u_channel / in | 0.69 (n=108, fell 0.12) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.28 (n=36, fell 0.11) |
| arch start yaw 45 / in | 0.17 (n=36, fell 0.11) |
| arch start yaw 90 / in | 0.17 (n=36, fell 0.31) |
| u_channel start yaw 0 / in | 0.67 (n=36, fell 0.14) |
| u_channel start yaw 45 / in | 0.72 (n=36, fell 0.11) |
| u_channel start yaw 90 / in | 0.67 (n=36, fell 0.11) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.69 (n=252, fell 0.10) |
| seen / 25 kg | 0.67 (n=252, fell 0.12) |
| seen / 40 kg | 0.52 (n=252, fell 0.18) |
| unseen / 10 kg | 0.76 (n=180, fell 0.09) |
| unseen / 25 kg | 0.64 (n=180, fell 0.21) |
| unseen / 40 kg | 0.34 (n=180, fell 0.23) |
