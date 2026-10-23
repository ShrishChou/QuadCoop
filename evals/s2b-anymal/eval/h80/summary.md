# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-anymal/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.77 (n=756, fell 0.04) |
| unseen | 0.76 (n=540, fell 0.05) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.6724, 0.7378, 0.7168]; mean |raw output| = [12.33, 12.11, 2.19]; share of outputs beyond the clip = [0.545, 0.596, 0.507].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.2959, 0.1901, 0.3793] | 0.407 | 0.747 |
| heading_zero_map | [0.3537, 0.246, 0.4648] | 0.5 | 0.771 |
| profile_zero | [0.2678, 0.2084, 0.2716] | 0.352 | 0.778 |
| profile_roll | [0.3087, 0.245, 0.3094] | 0.406 | 0.794 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.53 (n=108, fell 0.04) |
| asym / in | 0.69 (n=108, fell 0.01) |
| beam / in | 0.56 (n=108, fell 0.13) |
| cube / in | 0.99 (n=108, fell 0.00) |
| cylinder / in | 0.47 (n=108, fell 0.06) |
| dumbbell / in | 0.61 (n=108, fell 0.10) |
| l_shape / in | 0.87 (n=108, fell 0.01) |
| long / in | 0.86 (n=108, fell 0.02) |
| plus / in | 0.80 (n=108, fell 0.07) |
| sphere / in | 0.97 (n=108, fell 0.03) |
| t_shape / in | 0.93 (n=108, fell 0.03) |
| u_channel / in | 0.89 (n=108, fell 0.02) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.47 (n=36, fell 0.08) |
| arch start yaw 45 / in | 0.47 (n=36, fell 0.00) |
| arch start yaw 90 / in | 0.64 (n=36, fell 0.03) |
| u_channel start yaw 0 / in | 0.89 (n=36, fell 0.03) |
| u_channel start yaw 45 / in | 0.89 (n=36, fell 0.00) |
| u_channel start yaw 90 / in | 0.89 (n=36, fell 0.03) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.82 (n=252, fell 0.00) |
| seen / 25 kg | 0.77 (n=252, fell 0.02) |
| seen / 40 kg | 0.70 (n=252, fell 0.09) |
| unseen / 10 kg | 0.87 (n=180, fell 0.00) |
| unseen / 25 kg | 0.84 (n=180, fell 0.06) |
| unseen / 40 kg | 0.57 (n=180, fell 0.08) |
