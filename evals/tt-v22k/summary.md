# Walker transition test: tt-v22k

Checkpoints: v21 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_03-50-04_v21/model_5998.pt`; v22 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt`; v22k = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_14-39-28_v22_k1000/model_10496.pt`

Times include about 0.2 s of averaging lag; a crossing counts only if it holds 1 s. (n/m) = trials that got there out of all trials; failures are listed, not averaged in.

## Transitions in free space (start from rest, stop, reverse)

| axis | level | v21: start s / achieved / stop s, stop dist / reverse s / drift | v22: start s / achieved / stop s, stop dist / reverse s / drift | v22k: start s / achieved / stop s, stop dist / reverse s / drift |
|---|---|---|---|---|
| fwd | 0.1 m/s | 0.40 (2/2) / +0.106 / 0.85 (2/2), 0.035 m / 0.40 (1/2) / 0.53 deg | 0.40 (2/2) / +0.097 / 1.02 (2/2), 0.005 m / 0.40 (1/2) / 5.10 deg | 0.40 (2/2) / +0.089 / 1.03 (2/2), 0.029 m / 0.40 (2/2) / 6.29 deg |
| fwd | 0.2 m/s | 0.40 (2/2) / +0.208 / 1.04 (2/2), 0.060 m / 0.40 (2/2) / 7.51 deg | 0.40 (2/2) / +0.243 / 1.30 (2/2), 0.130 m / 0.40 (2/2) / 4.88 deg | 0.40 (2/2) / +0.198 / 0.91 (2/2), 0.069 m / 0.40 (2/2) / 12.15 deg |
| side | 0.1 m/s | never (0/2) / +0.046 / n/a, nan m / never (0/2) / 9.41 deg | 0.40 (2/2) / +0.102 / 1.61 (2/2), 0.037 m / 0.40 (2/2) / 12.34 deg | 0.40 (2/2) / +0.049 / 1.29 (2/2), 0.046 m / 0.40 (2/2) / 9.32 deg |
| side | 0.2 m/s | 1.96 (1/2) / +0.105 / 0.40 (1/1), 0.007 m / 1.10 (2/2) / 29.08 deg | 0.40 (2/2) / +0.224 / 0.42 (2/2), 0.008 m / 0.40 (2/2) / 12.68 deg | 0.40 (2/2) / +0.231 / 1.12 (2/2), 0.017 m / 0.40 (2/2) / 12.82 deg |
| yaw | 0.2 rad/s | never (0/2) / +0.040 / n/a, nan deg / never (0/2) / 0.11 m | 0.40 (2/2) / +0.136 / 1.13 (2/2), 5.118 deg / never (0/2) / 0.06 m | 0.40 (2/2) / +0.127 / never (0/2), 8.065 deg / never (0/2) / 0.10 m |
| yaw | 0.4 rad/s | never (0/2) / +0.030 / n/a, nan deg / never (0/2) / 0.09 m | 0.40 (2/2) / +0.381 / 0.61 (2/2), 4.100 deg / 0.40 (2/2) / 0.02 m | 0.40 (2/2) / +0.331 / 0.40 (2/2), 4.999 deg / 0.40 (2/2) / 0.17 m |

**v21:** failed to start 7/12, to stop 0/5 (of those that started), to reverse 7/12; falls 0.
**v22:** failed to start 0/12, to stop 0/12 (of those that started), to reverse 3/12; falls 0.
**v22k:** failed to start 0/12, to stop 2/12 (of those that started), to reverse 2/12; falls 0.

## Position corrections with one fixed controller (0.3 m moves, 30 deg turns; both directions, twice)

| axis | v21: not initiated / not settled / moves | v22: not initiated / not settled / moves | v22k: not initiated / not settled / moves | v21: settle s / final err / overshoot / flips / unintended | v22: settle s / final err / overshoot / flips / unintended | v22k: settle s / final err / overshoot / flips / unintended |
|---|---|---|---|---|---|---|
| fwd | 0 / 7 / 16 | 0 / 2 / 16 | 0 / 3 / 16 | 2.07 / 0.030 m / 0.001 m / 0.0 / 4.939 deg (yaw) | 1.27 / 0.014 m / 0.024 m / 0.1 / 4.458 deg (yaw) | 1.25 / 0.026 m / 0.019 m / 0.0 / 3.380 deg (yaw) |
| side | 0 / 4 / 16 | 0 / 0 / 16 | 0 / 3 / 16 | 3.32 / 0.038 m / 0.001 m / 0.0 / 15.540 deg (yaw) | 1.25 / 0.015 m / 0.005 m / 0.0 / 4.369 deg (yaw) | 1.95 / 0.025 m / 0.010 m / 0.0 / 7.622 deg (yaw) |
| yaw | 0 / 8 / 16 | 0 / 7 / 16 | 0 / 3 / 16 | 0.47 / 11.988 deg / 0.041 deg / 0.0 / 0.062 m (translation) | 2.03 / 3.626 deg / 0.000 deg / 0.0 / 0.053 m (translation) | 2.45 / 3.376 deg / 0.000 deg / 0.0 / 0.085 m (translation) |

Settle time is over settled moves only; final error, overshoot and flips are over all moves.

Failed moves (walker, axis, rep, move, target): v21 side r0 m0 +0.3m; v21 yaw r0 m0 +30d; v21 yaw r1 m0 +30d; v21 fwd r1 m1 +0m; v21 side r1 m1 +0m; v21 yaw r1 m2 -30d; v21 yaw r0 m2 -30d; v21 fwd r0 m2 -0.3m; v21 fwd r1 m2 -0.3m; v21 side r0 m4 +0.3m; v21 yaw r1 m4 +30d; v21 yaw r0 m4 +30d; v21 fwd r0 m5 +0m; v21 fwd r1 m5 +0m; v21 yaw r1 m6 -30d; v21 yaw r0 m6 -30d; v21 side r1 m5 +0m; v21 fwd r0 m6 -0.3m; v21 fwd r1 m6 -0.3m; v22 yaw r0 m0 +30d; v22 yaw r1 m0 +30d; v22 fwd r1 m2 -0.3m; v22 yaw r1 m1 +0d; v22 yaw r0 m4 +30d; v22 fwd r1 m6 -0.3m; v22 yaw r0 m5 +0d; v22 yaw r1 m5 +0d; v22 yaw r1 m6 -30d; v22k side r1 m0 +0.3m; v22k yaw r0 m0 +30d; v22k fwd r1 m2 -0.3m; v22k side r0 m4 +0.3m; v22k fwd r1 m3 +0m; v22k side r1 m3 +0m; v22k yaw r1 m4 +30d; v22k yaw r0 m3 +0d; v22k fwd r1 m5 +0m

## Under load

### 20 kg cube: push +0.2 m/s 4 s -> stop +0 m/s 2 s -> restart +0.2 m/s 4 s -> back_off -0.1 m/s 2 s

| phase | v21: force N / touching / robot v / cube v | v22: force N / touching / robot v / cube v | v22k: force N / touching / robot v / cube v |
|---|---|---|---|
| push | 83 / 0.62 / +0.177 / +0.176 | 53 / 0.59 / +0.013 / +0.011 | 62 / 0.69 / +0.048 / +0.047 |
| stop | 13 / 0.33 / +0.003 / +0.000 | 6 / 0.42 / +0.003 / +0.000 | 10 / 0.36 / -0.001 / +0.000 |
| restart | 75 / 0.71 / +0.174 / +0.174 | 48 / 0.69 / +0.008 / +0.008 | 66 / 0.76 / +0.064 / +0.062 |
| back_off | 0 / 0.07 / -0.071 / +0.000 | 0 / 0.04 / -0.104 / +0.000 | 0 / 0.04 / -0.098 / +0.000 |

**v21:** cube moving again after restart 0.86 (2/2) s; re-contact never (0/2) s; contact kept while stopped 0.33; backing off: contact released 0.21 (2/2) s, backed 0.112 m; stance while stopped: pitch +8.2 deg, torque at limit 0.50; falls 0/2.
**v22:** cube moving again after restart never (0/2) s; re-contact 1.60 (1/2) s; contact kept while stopped 0.42; backing off: contact released 0.09 (2/2) s, backed 0.169 m; stance while stopped: pitch +3.5 deg, torque at limit 0.95; falls 0/2.
**v22k:** cube moving again after restart never (0/2) s; re-contact 2.46 (1/2) s; contact kept while stopped 0.36; backing off: contact released 0.13 (2/2) s, backed 0.165 m; stance while stopped: pitch +6.6 deg, torque at limit 1.00; falls 0/2.

### 40 kg cube: push +0.2 m/s 4 s -> stop +0 m/s 2 s -> restart +0.2 m/s 4 s -> back_off -0.1 m/s 2 s

| phase | v21: force N / touching / robot v / cube v | v22: force N / touching / robot v / cube v | v22k: force N / touching / robot v / cube v |
|---|---|---|---|
| push | 143 / 0.69 / +0.071 / +0.070 | 53 / 0.52 / -0.001 / +0.001 | 75 / 0.67 / +0.019 / +0.018 |
| stop | 20 / 0.68 / +0.001 / +0.000 | 4 / 0.30 / -0.003 / +0.000 | 10 / 0.35 / -0.003 / +0.000 |
| restart | 133 / 0.82 / +0.062 / +0.060 | 41 / 0.64 / +0.001 / +0.001 | 71 / 0.70 / +0.019 / +0.016 |
| back_off | 0 / 0.01 / -0.072 / +0.000 | 0 / 0.03 / -0.109 / +0.000 | 0 / 0.04 / -0.058 / +0.000 |

**v21:** cube moving again after restart never (0/2) s; re-contact 2.78 (1/2) s; contact kept while stopped 0.68; backing off: contact released 0.03 (2/2) s, backed 0.147 m; stance while stopped: pitch +8.2 deg, torque at limit 0.74; falls 0/2.
**v22:** cube moving again after restart never (0/2) s; re-contact 0.36 (1/2) s; contact kept while stopped 0.30; backing off: contact released 0.06 (2/2) s, backed 0.188 m; stance while stopped: pitch +3.8 deg, torque at limit 1.00; falls 0/2.
**v22k:** cube moving again after restart never (0/2) s; re-contact 1.84 (1/2) s; contact kept while stopped 0.35; backing off: contact released 0.08 (2/2) s, backed 0.119 m; stance while stopped: pitch +6.0 deg, torque at limit 1.00; falls 0/2.

### immovable cube: press +0.2 m/s 4 s -> relax +0 m/s 3 s -> press_again +0.2 m/s 3 s -> release -0.1 m/s 3 s

| phase | v21: force N / touching / robot v / cube v | v22: force N / touching / robot v / cube v | v22k: force N / touching / robot v / cube v |
|---|---|---|---|
| press | 160 / 0.69 / +0.001 / +0.000 | 51 / 0.57 / +0.001 / +0.000 | 58 / 0.56 / +0.002 / +0.000 |
| relax | 3 / 0.23 / +0.001 / +0.000 | 5 / 0.43 / +0.000 / +0.000 | 5 / 0.30 / -0.001 / +0.000 |
| press_again | 163 / 0.83 / +0.000 / +0.000 | 53 / 0.75 / -0.001 / +0.000 | 55 / 0.57 / +0.002 / +0.000 |
| release | 0 / 0.04 / -0.045 / +0.000 | 0 / 0.01 / -0.104 / +0.000 | 0 / 0.04 / -0.107 / +0.000 |

**v21:** force while relaxed 3 N; re-contact on pressing again 0.91 (2/2) s; release 0.12 (2/2) s, backed 0.160 m; stance while relaxed: pitch +9.4 deg, torque at limit 0.49; falls 0/2.
**v22:** force while relaxed 5 N; re-contact on pressing again 1.35 (2/2) s; release 0.00 (1/1) s, backed 0.294 m; stance while relaxed: pitch +3.7 deg, torque at limit 1.00; falls 0/2.
**v22k:** force while relaxed 5 N; re-contact on pressing again never (0/2) s; release 0.12 (2/2) s, backed 0.338 m; stance while relaxed: pitch +7.2 deg, torque at limit 1.00; falls 0/2.

