# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-spot/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.59 (n=756, fell 0.12) |
| unseen | 0.50 (n=540, fell 0.16) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.6431, 0.631, 0.6448]; mean |raw output| = [18.15, 5.92, 2.12]; share of outputs beyond the clip = [0.52, 0.462, 0.404].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3464, 0.3281, 0.3886] | 0.554 | 0.831 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.32 (n=108, fell 0.12) |
| asym / in | 0.51 (n=108, fell 0.13) |
| beam / in | 0.35 (n=108, fell 0.19) |
| cube / in | 0.82 (n=108, fell 0.13) |
| cylinder / in | 0.37 (n=108, fell 0.09) |
| dumbbell / in | 0.43 (n=108, fell 0.11) |
| l_shape / in | 0.69 (n=108, fell 0.17) |
| long / in | 0.71 (n=108, fell 0.13) |
| plus / in | 0.34 (n=108, fell 0.14) |
| sphere / in | 0.89 (n=108, fell 0.07) |
| t_shape / in | 0.62 (n=108, fell 0.15) |
| u_channel / in | 0.60 (n=108, fell 0.15) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.33 (n=36, fell 0.06) |
| arch start yaw 45 / in | 0.31 (n=36, fell 0.14) |
| arch start yaw 90 / in | 0.31 (n=36, fell 0.17) |
| u_channel start yaw 0 / in | 0.61 (n=36, fell 0.17) |
| u_channel start yaw 45 / in | 0.64 (n=36, fell 0.08) |
| u_channel start yaw 90 / in | 0.56 (n=36, fell 0.19) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.66 (n=252, fell 0.09) |
| seen / 25 kg | 0.65 (n=252, fell 0.10) |
| seen / 40 kg | 0.48 (n=252, fell 0.15) |
| unseen / 10 kg | 0.65 (n=180, fell 0.14) |
| unseen / 25 kg | 0.59 (n=180, fell 0.13) |
| unseen / 40 kg | 0.26 (n=180, fell 0.20) |
