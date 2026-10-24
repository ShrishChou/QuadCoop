# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-spot-falcon/model.pt
success = held within 0.1 m / 3.0 deg for 0.02 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.63 (n=756, fell 0.16) |
| unseen | 0.45 (n=540, fell 0.31) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.72, 0.7335, 0.7809]; mean |raw output| = [28.21, 6.01, 4.31]; share of outputs beyond the clip = [0.576, 0.574, 0.61].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3505, 0.2173, 0.2765] | 0.378 | 0.749 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.20 (n=108, fell 0.32) |
| asym / in | 0.56 (n=108, fell 0.34) |
| beam / in | 0.30 (n=108, fell 0.23) |
| cube / in | 0.78 (n=108, fell 0.20) |
| cylinder / in | 0.42 (n=108, fell 0.08) |
| dumbbell / in | 0.45 (n=108, fell 0.15) |
| l_shape / in | 0.55 (n=108, fell 0.32) |
| long / in | 0.80 (n=108, fell 0.18) |
| plus / in | 0.19 (n=108, fell 0.43) |
| sphere / in | 1.00 (n=108, fell 0.00) |
| t_shape / in | 0.75 (n=108, fell 0.21) |
| u_channel / in | 0.67 (n=108, fell 0.21) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.22 (n=36, fell 0.31) |
| arch start yaw 45 / in | 0.22 (n=36, fell 0.42) |
| arch start yaw 90 / in | 0.17 (n=36, fell 0.25) |
| u_channel start yaw 0 / in | 0.64 (n=36, fell 0.19) |
| u_channel start yaw 45 / in | 0.67 (n=36, fell 0.25) |
| u_channel start yaw 90 / in | 0.69 (n=36, fell 0.19) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.75 (n=252, fell 0.06) |
| seen / 25 kg | 0.68 (n=252, fell 0.15) |
| seen / 40 kg | 0.45 (n=252, fell 0.28) |
| unseen / 10 kg | 0.68 (n=180, fell 0.10) |
| unseen / 25 kg | 0.49 (n=180, fell 0.31) |
| unseen / 40 kg | 0.18 (n=180, fell 0.52) |
