# Stage 2ctrl evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2ctrl-anymal-term80/model.pt
success = held within 0.1 m / 3.0 deg for 0.02 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.75 (n=756, fell 0.06) |
| unseen | 0.74 (n=540, fell 0.08) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.8464, 0.8713, 0.787]; mean |raw output| = [31.72, 13.23, 3.03]; share of outputs beyond the clip = [0.737, 0.78, 0.603].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3413, 0.2146, 0.4542] | 0.403 | 0.687 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.43 (n=108, fell 0.07) |
| asym / in | 0.62 (n=108, fell 0.10) |
| beam / in | 0.61 (n=108, fell 0.08) |
| cube / in | 0.96 (n=108, fell 0.03) |
| cylinder / in | 0.44 (n=108, fell 0.08) |
| dumbbell / in | 0.78 (n=108, fell 0.07) |
| l_shape / in | 0.85 (n=108, fell 0.06) |
| long / in | 0.87 (n=108, fell 0.03) |
| plus / in | 0.77 (n=108, fell 0.09) |
| sphere / in | 0.98 (n=108, fell 0.02) |
| t_shape / in | 0.77 (n=108, fell 0.12) |
| u_channel / in | 0.84 (n=108, fell 0.07) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.47 (n=36, fell 0.11) |
| arch start yaw 45 / in | 0.28 (n=36, fell 0.08) |
| arch start yaw 90 / in | 0.53 (n=36, fell 0.03) |
| u_channel start yaw 0 / in | 0.83 (n=36, fell 0.08) |
| u_channel start yaw 45 / in | 0.81 (n=36, fell 0.06) |
| u_channel start yaw 90 / in | 0.89 (n=36, fell 0.08) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.83 (n=252, fell 0.02) |
| seen / 25 kg | 0.79 (n=252, fell 0.04) |
| seen / 40 kg | 0.63 (n=252, fell 0.13) |
| unseen / 10 kg | 0.89 (n=180, fell 0.00) |
| unseen / 25 kg | 0.85 (n=180, fell 0.04) |
| unseen / 40 kg | 0.48 (n=180, fell 0.21) |
