# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-anymal-term80/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.81 (n=756, fell 0.02) |
| unseen | 0.76 (n=540, fell 0.05) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7564, 0.7838, 0.7058]; mean |raw output| = [15.26, 27.41, 2.43]; share of outputs beyond the clip = [0.618, 0.644, 0.483].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.326, 0.23, 0.3782] | 0.416 | 0.739 |
| heading_zero_map | [0.3762, 0.2905, 0.4311] | 0.489 | 0.765 |
| profile_zero | [0.2694, 0.2248, 0.3047] | 0.356 | 0.786 |
| profile_roll | [0.295, 0.2731, 0.4014] | 0.432 | 0.8 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.52 (n=108, fell 0.04) |
| asym / in | 0.68 (n=108, fell 0.07) |
| beam / in | 0.62 (n=108, fell 0.08) |
| cube / in | 0.98 (n=108, fell 0.00) |
| cylinder / in | 0.47 (n=108, fell 0.02) |
| dumbbell / in | 0.84 (n=108, fell 0.04) |
| l_shape / in | 0.85 (n=108, fell 0.04) |
| long / in | 0.93 (n=108, fell 0.01) |
| plus / in | 0.75 (n=108, fell 0.04) |
| sphere / in | 0.99 (n=108, fell 0.01) |
| t_shape / in | 0.94 (n=108, fell 0.03) |
| u_channel / in | 0.89 (n=108, fell 0.02) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.50 (n=36, fell 0.08) |
| arch start yaw 45 / in | 0.56 (n=36, fell 0.00) |
| arch start yaw 90 / in | 0.50 (n=36, fell 0.03) |
| u_channel start yaw 0 / in | 0.92 (n=36, fell 0.03) |
| u_channel start yaw 45 / in | 0.86 (n=36, fell 0.00) |
| u_channel start yaw 90 / in | 0.89 (n=36, fell 0.03) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.85 (n=252, fell 0.01) |
| seen / 25 kg | 0.84 (n=252, fell 0.01) |
| seen / 40 kg | 0.73 (n=252, fell 0.04) |
| unseen / 10 kg | 0.91 (n=180, fell 0.00) |
| unseen / 25 kg | 0.81 (n=180, fell 0.02) |
| unseen / 40 kg | 0.55 (n=180, fell 0.12) |
