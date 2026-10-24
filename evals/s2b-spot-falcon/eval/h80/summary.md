# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-spot-falcon/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.74 (n=756, fell 0.08) |
| unseen | 0.67 (n=540, fell 0.19) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7416, 0.7399, 0.7669]; mean |raw output| = [7.65, 4.04, 2.54]; share of outputs beyond the clip = [0.574, 0.549, 0.577].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2648, 0.1979, 0.1951] | 0.293 | 0.765 |
| heading_zero_map | [0.3578, 0.2763, 0.2498] | 0.393 | 0.802 |
| profile_zero | [0.2349, 0.2364, 0.2032] | 0.3 | 0.829 |
| profile_roll | [0.2775, 0.3025, 0.2577] | 0.373 | 0.844 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.19 (n=108, fell 0.16) |
| asym / in | 0.63 (n=108, fell 0.23) |
| beam / in | 0.51 (n=108, fell 0.18) |
| cube / in | 0.92 (n=108, fell 0.08) |
| cylinder / in | 0.66 (n=108, fell 0.03) |
| dumbbell / in | 0.71 (n=108, fell 0.09) |
| l_shape / in | 0.59 (n=108, fell 0.24) |
| long / in | 0.86 (n=108, fell 0.07) |
| plus / in | 0.81 (n=108, fell 0.16) |
| sphere / in | 1.00 (n=108, fell 0.00) |
| t_shape / in | 0.81 (n=108, fell 0.13) |
| u_channel / in | 0.78 (n=108, fell 0.14) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.17 (n=36, fell 0.14) |
| arch start yaw 45 / in | 0.22 (n=36, fell 0.17) |
| arch start yaw 90 / in | 0.19 (n=36, fell 0.17) |
| u_channel start yaw 0 / in | 0.78 (n=36, fell 0.14) |
| u_channel start yaw 45 / in | 0.75 (n=36, fell 0.19) |
| u_channel start yaw 90 / in | 0.81 (n=36, fell 0.08) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.84 (n=252, fell 0.06) |
| seen / 25 kg | 0.77 (n=252, fell 0.07) |
| seen / 40 kg | 0.60 (n=252, fell 0.12) |
| unseen / 10 kg | 0.86 (n=180, fell 0.04) |
| unseen / 25 kg | 0.74 (n=180, fell 0.16) |
| unseen / 40 kg | 0.39 (n=180, fell 0.37) |
