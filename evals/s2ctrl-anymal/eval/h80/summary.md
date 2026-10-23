# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-anymal/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.75 (n=756, fell 0.06) |
| unseen | 0.69 (n=540, fell 0.09) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7747, 0.8695, 0.8173]; mean |raw output| = [20.87, 9.83, 4.41]; share of outputs beyond the clip = [0.637, 0.775, 0.661].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3832, 0.1838, 0.4257] | 0.403 | 0.697 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.49 (n=108, fell 0.07) |
| asym / in | 0.68 (n=108, fell 0.07) |
| beam / in | 0.55 (n=108, fell 0.18) |
| cube / in | 0.98 (n=108, fell 0.02) |
| cylinder / in | 0.39 (n=108, fell 0.08) |
| dumbbell / in | 0.69 (n=108, fell 0.12) |
| l_shape / in | 0.86 (n=108, fell 0.02) |
| long / in | 0.91 (n=108, fell 0.04) |
| plus / in | 0.59 (n=108, fell 0.15) |
| sphere / in | 0.99 (n=108, fell 0.01) |
| t_shape / in | 0.81 (n=108, fell 0.08) |
| u_channel / in | 0.79 (n=108, fell 0.06) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.53 (n=36, fell 0.06) |
| arch start yaw 45 / in | 0.53 (n=36, fell 0.06) |
| arch start yaw 90 / in | 0.42 (n=36, fell 0.08) |
| u_channel start yaw 0 / in | 0.81 (n=36, fell 0.06) |
| u_channel start yaw 45 / in | 0.72 (n=36, fell 0.08) |
| u_channel start yaw 90 / in | 0.83 (n=36, fell 0.03) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.85 (n=252, fell 0.01) |
| seen / 25 kg | 0.77 (n=252, fell 0.04) |
| seen / 40 kg | 0.63 (n=252, fell 0.13) |
| unseen / 10 kg | 0.84 (n=180, fell 0.01) |
| unseen / 25 kg | 0.77 (n=180, fell 0.07) |
| unseen / 40 kg | 0.47 (n=180, fell 0.21) |
