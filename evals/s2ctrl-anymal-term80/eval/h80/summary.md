# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-anymal-term80/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.73 (n=756, fell 0.06) |
| unseen | 0.72 (n=540, fell 0.08) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.8371, 0.8552, 0.7821]; mean |raw output| = [30.61, 12.61, 3.01]; share of outputs beyond the clip = [0.724, 0.756, 0.597].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3533, 0.2331, 0.4482] | 0.418 | 0.688 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.29 (n=108, fell 0.13) |
| asym / in | 0.61 (n=108, fell 0.07) |
| beam / in | 0.56 (n=108, fell 0.10) |
| cube / in | 0.98 (n=108, fell 0.01) |
| cylinder / in | 0.36 (n=108, fell 0.06) |
| dumbbell / in | 0.76 (n=108, fell 0.07) |
| l_shape / in | 0.81 (n=108, fell 0.08) |
| long / in | 0.88 (n=108, fell 0.05) |
| plus / in | 0.79 (n=108, fell 0.12) |
| sphere / in | 0.99 (n=108, fell 0.01) |
| t_shape / in | 0.84 (n=108, fell 0.09) |
| u_channel / in | 0.85 (n=108, fell 0.05) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.33 (n=36, fell 0.19) |
| arch start yaw 45 / in | 0.14 (n=36, fell 0.14) |
| arch start yaw 90 / in | 0.39 (n=36, fell 0.06) |
| u_channel start yaw 0 / in | 0.86 (n=36, fell 0.00) |
| u_channel start yaw 45 / in | 0.83 (n=36, fell 0.06) |
| u_channel start yaw 90 / in | 0.86 (n=36, fell 0.08) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.79 (n=252, fell 0.01) |
| seen / 25 kg | 0.77 (n=252, fell 0.04) |
| seen / 40 kg | 0.63 (n=252, fell 0.13) |
| unseen / 10 kg | 0.86 (n=180, fell 0.01) |
| unseen / 25 kg | 0.83 (n=180, fell 0.03) |
| unseen / 40 kg | 0.48 (n=180, fell 0.21) |
