# Walker transition test: tt-walkers

Checkpoints: v1 = `logs/evals/walker-anymal-v1/model.pt`; v21 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_03-50-04_v21/model_5998.pt`; v22 = `logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt`

Times include about 0.2 s of averaging lag; a crossing counts only if it holds 1 s. (n/m) = trials that got there out of all trials; failures are listed, not averaged in.

## Transitions in free space (start from rest, stop, reverse)

| axis | level | v1: start s / achieved / stop s, stop dist / reverse s / drift | v21: start s / achieved / stop s, stop dist / reverse s / drift | v22: start s / achieved / stop s, stop dist / reverse s / drift |
|---|---|---|---|---|
| fwd | 0.1 m/s | never (0/2) / -0.001 / n/a, nan m / never (0/2) / 4.28 deg | 0.40 (2/2) / +0.106 / 0.85 (2/2), 0.035 m / 0.40 (1/2) / 0.53 deg | 0.40 (2/2) / +0.097 / 1.02 (2/2), 0.005 m / 0.40 (1/2) / 5.10 deg |
| fwd | 0.2 m/s | never (0/2) / -0.004 / n/a, nan m / never (0/2) / 8.22 deg | 0.40 (2/2) / +0.208 / 1.04 (2/2), 0.060 m / 0.40 (2/2) / 7.51 deg | 0.40 (2/2) / +0.243 / 1.30 (2/2), 0.130 m / 0.40 (2/2) / 4.88 deg |
| side | 0.1 m/s | never (0/2) / -0.022 / n/a, nan m / never (0/2) / 11.78 deg | never (0/2) / +0.046 / n/a, nan m / never (0/2) / 9.41 deg | 0.40 (2/2) / +0.102 / 1.61 (2/2), 0.037 m / 0.40 (2/2) / 12.34 deg |
| side | 0.2 m/s | never (0/2) / +0.001 / n/a, nan m / 2.70 (1/2) / 5.36 deg | 1.96 (1/2) / +0.105 / 0.40 (1/1), 0.007 m / 1.10 (2/2) / 29.08 deg | 0.40 (2/2) / +0.224 / 0.42 (2/2), 0.008 m / 0.40 (2/2) / 12.68 deg |
| yaw | 0.2 rad/s | never (0/2) / +0.024 / n/a, nan deg / never (0/2) / 0.08 m | never (0/2) / +0.040 / n/a, nan deg / never (0/2) / 0.11 m | 0.40 (2/2) / +0.136 / 1.13 (2/2), 5.118 deg / never (0/2) / 0.06 m |
| yaw | 0.4 rad/s | never (0/2) / +0.010 / n/a, nan deg / never (0/2) / 0.06 m | never (0/2) / +0.030 / n/a, nan deg / never (0/2) / 0.09 m | 0.40 (2/2) / +0.381 / 0.61 (2/2), 4.101 deg / 0.40 (2/2) / 0.02 m |

**v1:** failed to start 12/12, to stop 0/0 (of those that started), to reverse 11/12; falls 0.
**v21:** failed to start 7/12, to stop 0/5 (of those that started), to reverse 7/12; falls 0.
**v22:** failed to start 0/12, to stop 0/12 (of those that started), to reverse 3/12; falls 0.

## Position corrections with one fixed controller (0.3 m moves, 30 deg turns; both directions, twice)

| axis | v1: not initiated / not settled / moves | v21: not initiated / not settled / moves | v22: not initiated / not settled / moves | v1: settle s / final err / overshoot / flips / unintended | v21: settle s / final err / overshoot / flips / unintended | v22: settle s / final err / overshoot / flips / unintended |
|---|---|---|---|---|---|---|
| fwd | 4 / 11 / 16 | 0 / 7 / 16 | 0 / 2 / 16 | 0.46 / 0.207 m / 0.011 m / 0.1 / 6.291 deg (yaw) | 2.07 / 0.030 m / 0.001 m / 0.0 / 4.939 deg (yaw) | 1.27 / 0.014 m / 0.024 m / 0.1 / 4.458 deg (yaw) |
| side | 2 / 12 / 16 | 0 / 4 / 16 | 0 / 0 / 16 | 1.31 / 0.141 m / 0.018 m / 0.1 / 8.489 deg (yaw) | 3.32 / 0.038 m / 0.001 m / 0.0 / 15.541 deg (yaw) | 1.25 / 0.015 m / 0.005 m / 0.0 / 4.369 deg (yaw) |
| yaw | 1 / 15 / 16 | 0 / 8 / 16 | 0 / 7 / 16 | 0.02 / 13.613 deg / 1.329 deg / 0.0 / 0.073 m (translation) | 0.47 / 11.988 deg / 0.041 deg / 0.0 / 0.062 m (translation) | 2.03 / 3.626 deg / 0.000 deg / 0.0 / 0.053 m (translation) |

Settle time is over settled moves only; final error, overshoot and flips are over all moves.

Failed moves (walker, axis, rep, move, target): v1 fwd r0 m0 +0.3m; v1 side r0 m0 +0.3m; v1 side r1 m0 +0.3m; v1 yaw r0 m0 +30d; v1 yaw r1 m0 +30d; v1 fwd r0 m1 +0m (never started); v1 fwd r1 m1 +0m; v1 yaw r0 m1 +0d; v1 yaw r1 m1 +0d; v1 fwd r0 m2 -0.3m; v1 side r1 m2 -0.3m; v1 side r0 m2 -0.3m; v1 fwd r1 m2 -0.3m; v1 yaw r0 m2 -30d; v1 yaw r1 m2 -30d; v1 side r1 m3 +0m; v1 side r0 m3 +0m; v1 fwd r0 m4 +0.3m; v1 fwd r1 m3 +0m (never started); v1 fwd r0 m5 +0m (never started); v1 yaw r0 m3 +0d; v1 yaw r1 m4 +30d; v1 side r1 m4 +0.3m; v1 side r0 m4 +0.3m; v1 fwd r1 m4 +0.3m; v1 fwd r0 m6 -0.3m; v1 yaw r0 m4 +30d; v1 yaw r1 m5 +0d; v1 side r1 m5 +0m (never started); v1 side r0 m5 +0m (never started); v1 fwd r1 m5 +0m; v1 yaw r0 m5 +0d; v1 yaw r1 m6 -30d; v1 fwd r1 m6 -0.3m; v1 side r1 m7 +0m; v1 side r0 m7 +0m; v1 yaw r0 m6 -30d; v1 yaw r1 m7 +0d; v1 fwd r1 m7 +0m (never started); v1 yaw r0 m7 +0d (never started); v21 side r0 m0 +0.3m; v21 yaw r0 m0 +30d; v21 yaw r1 m0 +30d; v21 fwd r1 m1 +0m; v21 side r1 m1 +0m; v21 yaw r1 m2 -30d; v21 yaw r0 m2 -30d; v21 fwd r0 m2 -0.3m; v21 fwd r1 m2 -0.3m; v21 side r0 m4 +0.3m; v21 yaw r1 m4 +30d; v21 yaw r0 m4 +30d; v21 fwd r0 m5 +0m; v21 fwd r1 m5 +0m; v21 yaw r1 m6 -30d; v21 yaw r0 m6 -30d; v21 side r1 m5 +0m; v21 fwd r0 m6 -0.3m; v21 fwd r1 m6 -0.3m; v22 yaw r0 m0 +30d; v22 yaw r1 m0 +30d; v22 fwd r1 m2 -0.3m; v22 yaw r1 m1 +0d; v22 yaw r0 m4 +30d; v22 fwd r1 m6 -0.3m; v22 yaw r0 m5 +0d; v22 yaw r1 m5 +0d; v22 yaw r1 m6 -30d

## Under load

### 20 kg cube: push +0.2 m/s 4 s -> stop +0 m/s 2 s -> restart +0.2 m/s 4 s -> back_off -0.1 m/s 2 s

| phase | v1: force N / touching / robot v / cube v | v21: force N / touching / robot v / cube v | v22: force N / touching / robot v / cube v |
|---|---|---|---|
| push | 0 / 0.00 / -0.001 / +0.000 | 77 / 0.59 / +0.149 / +0.150 | 50 / 0.58 / +0.012 / +0.011 |
| stop | 0 / 0.00 / +0.005 / +0.000 | 16 / 0.49 / -0.000 / +0.000 | 5 / 0.38 / +0.002 / +0.000 |
| restart | 0 / 0.00 / -0.004 / +0.000 | 86 / 0.73 / +0.195 / +0.193 | 47 / 0.72 / +0.006 / +0.007 |
| back_off | 0 / 0.00 / +0.008 / +0.000 | 0 / 0.06 / -0.080 / +0.000 | 0 / 0.04 / -0.105 / +0.000 |

**v1:** cube moving again after restart never (0/2) s; re-contact never (0/2) s; contact kept while stopped 0.00; backing off: contact released n/a s, backed 0.048 m; stance while stopped: pitch +3.7 deg, torque at limit 0.00; falls 0/2.
**v21:** cube moving again after restart 1.25 (2/2) s; re-contact never (0/2) s; contact kept while stopped 0.49; backing off: contact released 0.26 (2/2) s, backed 0.122 m; stance while stopped: pitch +8.5 deg, torque at limit 0.65; falls 0/2.
**v22:** cube moving again after restart never (0/2) s; re-contact 0.20 (1/2) s; contact kept while stopped 0.38; backing off: contact released 0.10 (2/2) s, backed 0.167 m; stance while stopped: pitch +3.5 deg, torque at limit 0.96; falls 0/2.

### 40 kg cube: push +0.2 m/s 4 s -> stop +0 m/s 2 s -> restart +0.2 m/s 4 s -> back_off -0.1 m/s 2 s

| phase | v1: force N / touching / robot v / cube v | v21: force N / touching / robot v / cube v | v22: force N / touching / robot v / cube v |
|---|---|---|---|
| push | 0 / 0.00 / -0.001 / +0.000 | 136 / 0.69 / +0.059 / +0.058 | 58 / 0.52 / +0.006 / +0.006 |
| stop | 0 / 0.00 / +0.005 / +0.000 | 12 / 0.61 / -0.000 / +0.000 | 6 / 0.38 / +0.001 / +0.000 |
| restart | 0 / 0.00 / -0.004 / +0.000 | 131 / 0.83 / +0.057 / +0.055 | 65 / 0.70 / +0.005 / +0.004 |
| back_off | 0 / 0.00 / +0.008 / +0.000 | 0 / 0.09 / -0.067 / +0.000 | 0 / 0.03 / -0.101 / +0.000 |

**v1:** cube moving again after restart never (0/2) s; re-contact never (0/2) s; contact kept while stopped 0.00; backing off: contact released n/a s, backed 0.048 m; stance while stopped: pitch +3.7 deg, torque at limit 0.00; falls 0/2.
**v21:** cube moving again after restart never (0/2) s; re-contact never (0/2) s; contact kept while stopped 0.61; backing off: contact released 0.18 (2/2) s, backed 0.121 m; stance while stopped: pitch +8.2 deg, torque at limit 0.75; falls 0/2.
**v22:** cube moving again after restart never (0/2) s; re-contact 1.68 (2/2) s; contact kept while stopped 0.38; backing off: contact released 0.05 (2/2) s, backed 0.179 m; stance while stopped: pitch +3.7 deg, torque at limit 1.00; falls 0/2.

### immovable cube: press +0.2 m/s 4 s -> relax +0 m/s 3 s -> press_again +0.2 m/s 3 s -> release -0.1 m/s 3 s

| phase | v1: force N / touching / robot v / cube v | v21: force N / touching / robot v / cube v | v22: force N / touching / robot v / cube v |
|---|---|---|---|
| press | 0 / 0.00 / -0.001 / +0.000 | 158 / 0.70 / +0.000 / +0.000 | 45 / 0.51 / +0.000 / +0.000 |
| relax | 0 / 0.00 / +0.005 / +0.000 | 4 / 0.30 / -0.002 / +0.000 | 6 / 0.64 / -0.000 / +0.000 |
| press_again | 0 / 0.00 / -0.002 / +0.000 | 160 / 0.78 / +0.001 / +0.000 | 46 / 0.67 / -0.000 / +0.000 |
| release | 0 / 0.00 / +0.013 / +0.000 | 0 / 0.06 / -0.050 / +0.000 | 0 / 0.00 / -0.099 / +0.000 |

**v1:** force while relaxed 0 N; re-contact on pressing again never (0/2) s; release n/a s, backed 0.034 m; stance while relaxed: pitch +3.3 deg, torque at limit 0.00; falls 0/2.
**v21:** force while relaxed 4 N; re-contact on pressing again 0.76 (1/2) s; release 0.20 (2/2) s, backed 0.163 m; stance while relaxed: pitch +9.2 deg, torque at limit 0.42; falls 0/2.
**v22:** force while relaxed 6 N; re-contact on pressing again 1.48 (1/2) s; release 0.03 (2/2) s, backed 0.253 m; stance while relaxed: pitch +3.2 deg, torque at limit 1.00; falls 0/2.

