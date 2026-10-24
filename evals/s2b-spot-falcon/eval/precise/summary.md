# Stage 2b evaluation: /orcd/home/002/shrishc/quadcoop/logs/evals/s2b-spot-falcon/model.pt
success = held within 0.1 m / 3.0 deg for 0.02 s inside 80.0 s; ablation cells show success (change vs normal)

unseen shapes: beam, l_shape, asym, u_channel, plus (asym = long box with split friction: same geometry as a seen shape, different physics)

## success by object group

| | normal |
|---|---|
| seen | 0.71 (n=756, fell 0.10) |
| unseen | 0.67 (n=540, fell 0.17) |

## action sensitivity (does the output change at all?)

Same observation, one input ablated; |change| in the command the walker receives (policy output clipped to [-1, 1], per vx, vy, yaw rate), averaged over live envs every 10 steps of the normal rollouts. Mean |clipped action| = [0.7392, 0.7325, 0.763]; mean |raw output| = [7.82, 3.93, 2.48]; share of outputs beyond the clip = [0.572, 0.539, 0.571].

| ablation | mean abs change (vx, vy, wz) | relative to mean abs action | share of samples changed > 0.05 |
|---|---|---|---|
| heading_zero | [0.261, 0.1952, 0.1902] | 0.289 | 0.769 |
| heading_zero_map | [0.3497, 0.2783, 0.2502] | 0.393 | 0.807 |
| profile_zero | [0.2294, 0.24, 0.2023] | 0.301 | 0.832 |
| profile_roll | [0.2739, 0.3073, 0.2572] | 0.375 | 0.846 |

## success by object and size set

| | normal |
|---|---|
| arch / in | 0.16 (n=108, fell 0.15) |
| asym / in | 0.57 (n=108, fell 0.27) |
| beam / in | 0.51 (n=108, fell 0.16) |
| cube / in | 0.88 (n=108, fell 0.11) |
| cylinder / in | 0.62 (n=108, fell 0.07) |
| dumbbell / in | 0.69 (n=108, fell 0.11) |
| l_shape / in | 0.64 (n=108, fell 0.17) |
| long / in | 0.82 (n=108, fell 0.11) |
| plus / in | 0.84 (n=108, fell 0.12) |
| sphere / in | 1.00 (n=108, fell 0.00) |
| t_shape / in | 0.78 (n=108, fell 0.14) |
| u_channel / in | 0.80 (n=108, fell 0.16) |

## arch / u_channel by object start yaw

(start yaw 0 = doorway facing the robot)

| | normal |
|---|---|
| arch start yaw 0 / in | 0.14 (n=36, fell 0.11) |
| arch start yaw 45 / in | 0.22 (n=36, fell 0.17) |
| arch start yaw 90 / in | 0.11 (n=36, fell 0.17) |
| u_channel start yaw 0 / in | 0.81 (n=36, fell 0.14) |
| u_channel start yaw 45 / in | 0.81 (n=36, fell 0.19) |
| u_channel start yaw 90 / in | 0.78 (n=36, fell 0.14) |

## by group and mass

| | normal |
|---|---|
| seen / 10 kg | 0.83 (n=252, fell 0.04) |
| seen / 25 kg | 0.74 (n=252, fell 0.07) |
| seen / 40 kg | 0.55 (n=252, fell 0.19) |
| unseen / 10 kg | 0.87 (n=180, fell 0.05) |
| unseen / 25 kg | 0.74 (n=180, fell 0.13) |
| unseen / 40 kg | 0.40 (n=180, fell 0.34) |
