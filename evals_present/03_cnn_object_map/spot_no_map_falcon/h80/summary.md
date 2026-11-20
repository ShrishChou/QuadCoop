# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-spot-falcon/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.61 (n=756, fell 0.18) |
| unseen | 0.42 (n=540, fell 0.34) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7164, 0.7373, 0.7842]; mean |raw output| = [27.95, 6.19, 4.33]; share of outputs beyond the clip = [0.57, 0.583, 0.616].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3654, 0.2172, 0.2731] | 0.382 | 0.747 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.22 (n=108, fell 0.25) |
| asym / in | 0.50 (n=108, fell 0.43) |
| beam / in | 0.25 (n=108, fell 0.22) |
| cube / in | 0.78 (n=108, fell 0.22) |
| cylinder / in | 0.42 (n=108, fell 0.09) |
| dumbbell / in | 0.44 (n=108, fell 0.19) |
| l_shape / in | 0.54 (n=108, fell 0.34) |
| long / in | 0.72 (n=108, fell 0.27) |
| plus / in | 0.26 (n=108, fell 0.42) |
| sphere / in | 0.95 (n=108, fell 0.05) |
| t_shape / in | 0.72 (n=108, fell 0.22) |
| u_channel / in | 0.56 (n=108, fell 0.30) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.25 (n=36, fell 0.31) |
| arch start yaw 45 / in | 0.17 (n=36, fell 0.22) |
| arch start yaw 90 / in | 0.25 (n=36, fell 0.22) |
| u_channel start yaw 0 / in | 0.61 (n=36, fell 0.31) |
| u_channel start yaw 45 / in | 0.56 (n=36, fell 0.25) |
| u_channel start yaw 90 / in | 0.53 (n=36, fell 0.33) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.76 (n=252, fell 0.06) |
| seen / 25 kg | 0.68 (n=252, fell 0.14) |
| seen / 40 kg | 0.38 (n=252, fell 0.36) |
| unseen / 10 kg | 0.59 (n=180, fell 0.15) |
| unseen / 25 kg | 0.53 (n=180, fell 0.27) |
| unseen / 40 kg | 0.14 (n=180, fell 0.61) |
