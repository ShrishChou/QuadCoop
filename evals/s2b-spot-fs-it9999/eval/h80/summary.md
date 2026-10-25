# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-spot-fs-it9999/model.pt
success = held within 0.1 m / 6.0 deg for 1.0 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.66 (n=756, fell 0.22) |
| unseen | 0.64 (n=540, fell 0.27) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7349, 0.7, 0.8297]; mean |raw output| = [8.69, 5.17, 5.95]; share of outputs beyond the clip = [0.596, 0.514, 0.678].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.0976, 0.1166, 0.1129] | 0.144 | 0.668 |
| heading_zero_map | [0.3307, 0.2915, 0.3128] | 0.413 | 0.794 |
| profile_zero | [0.2995, 0.4306, 0.3608] | 0.482 | 0.871 |
| profile_roll | [0.3348, 0.3692, 0.3438] | 0.463 | 0.869 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.25 (n=108, fell 0.40) |
| asym / in | 0.54 (n=108, fell 0.40) |
| beam / in | 0.49 (n=108, fell 0.26) |
| cube / in | 0.86 (n=108, fell 0.14) |
| cylinder / in | 0.53 (n=108, fell 0.14) |
| dumbbell / in | 0.63 (n=108, fell 0.27) |
| l_shape / in | 0.69 (n=108, fell 0.28) |
| long / in | 0.69 (n=108, fell 0.29) |
| plus / in | 0.77 (n=108, fell 0.18) |
| sphere / in | 0.99 (n=108, fell 0.01) |
| t_shape / in | 0.70 (n=108, fell 0.28) |
| u_channel / in | 0.73 (n=108, fell 0.21) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.25 (n=36, fell 0.31) |
| arch start yaw 45 / in | 0.31 (n=36, fell 0.39) |
| arch start yaw 90 / in | 0.19 (n=36, fell 0.50) |
| u_channel start yaw 0 / in | 0.78 (n=36, fell 0.17) |
| u_channel start yaw 45 / in | 0.78 (n=36, fell 0.14) |
| u_channel start yaw 90 / in | 0.64 (n=36, fell 0.33) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.82 (n=252, fell 0.10) |
| seen / 25 kg | 0.71 (n=252, fell 0.16) |
| seen / 40 kg | 0.46 (n=252, fell 0.39) |
| unseen / 10 kg | 0.90 (n=180, fell 0.04) |
| unseen / 25 kg | 0.73 (n=180, fell 0.23) |
| unseen / 40 kg | 0.31 (n=180, fell 0.52) |
