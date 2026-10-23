# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-anymal-term80/model.pt
success = held within 0.1 m / 3.0 deg for 0.02 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.81 (n=756, fell 0.02) |
| unseen | 0.78 (n=540, fell 0.04) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7597, 0.7868, 0.7065]; mean |raw output| = [15.93, 29.31, 2.54]; share of outputs beyond the clip = [0.626, 0.65, 0.482].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.3223, 0.2247, 0.3731] | 0.408 | 0.736 |
| heading_zero_map | [0.3688, 0.2907, 0.426] | 0.482 | 0.761 |
| profile_zero | [0.2606, 0.2152, 0.3028] | 0.346 | 0.781 |
| profile_roll | [0.2911, 0.2626, 0.3999] | 0.423 | 0.795 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.56 (n=108, fell 0.03) |
| asym / in | 0.71 (n=108, fell 0.02) |
| beam / in | 0.67 (n=108, fell 0.09) |
| cube / in | 0.95 (n=108, fell 0.02) |
| cylinder / in | 0.49 (n=108, fell 0.04) |
| dumbbell / in | 0.86 (n=108, fell 0.04) |
| l_shape / in | 0.85 (n=108, fell 0.01) |
| long / in | 0.89 (n=108, fell 0.02) |
| plus / in | 0.80 (n=108, fell 0.06) |
| sphere / in | 1.00 (n=108, fell 0.00) |
| t_shape / in | 0.94 (n=108, fell 0.02) |
| u_channel / in | 0.87 (n=108, fell 0.05) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.53 (n=36, fell 0.03) |
| arch start yaw 45 / in | 0.56 (n=36, fell 0.03) |
| arch start yaw 90 / in | 0.61 (n=36, fell 0.03) |
| u_channel start yaw 0 / in | 0.89 (n=36, fell 0.06) |
| u_channel start yaw 45 / in | 0.81 (n=36, fell 0.06) |
| u_channel start yaw 90 / in | 0.92 (n=36, fell 0.03) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.85 (n=252, fell 0.00) |
| seen / 25 kg | 0.83 (n=252, fell 0.02) |
| seen / 40 kg | 0.75 (n=252, fell 0.04) |
| unseen / 10 kg | 0.92 (n=180, fell 0.01) |
| unseen / 25 kg | 0.83 (n=180, fell 0.03) |
| unseen / 40 kg | 0.58 (n=180, fell 0.10) |
