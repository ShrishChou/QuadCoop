# Third robot by branching: hbm-s7900-80kg

Seed 7900, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 80 kg: 109 branched tasks, pair success 25%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 23% | 4.6% | 6.4% | -1.8 [-8.3, +4.6] |
| h1 | 21% | 8.3% | 11.9% | -3.7 [-12.8, +4.6] |
| joint | 50% | 30.3% | 5.5% | +24.8 [+14.7, +34.9] |
| keep | 54% | 32.1% | 2.8% | +29.4 [+19.3, +39.4] |
| move1 | 52% | 32.1% | 4.6% | +27.5 [+17.4, +36.7] |
| move2 | 48% | 30.3% | 7.3% | +22.9 [+11.9, +33.9] |
| jnet | 50% | 28.4% | 3.7% | +24.8 [+14.7, +33.9] |
| best_rank | 21% | 8.3% | 11.9% | -3.7 [-11.9, +4.6] |

## all: 109 branched tasks, pair success 25%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 23% | 4.6% | 6.4% | -1.8 [-8.3, +4.6] |
| h1 | 21% | 8.3% | 11.9% | -3.7 [-12.8, +4.6] |
| joint | 50% | 30.3% | 5.5% | +24.8 [+14.7, +34.9] |
| keep | 54% | 32.1% | 2.8% | +29.4 [+20.2, +39.4] |
| move1 | 52% | 32.1% | 4.6% | +27.5 [+17.4, +37.6] |
| move2 | 48% | 30.3% | 7.3% | +22.9 [+12.8, +33.9] |
| jnet | 50% | 28.4% | 3.7% | +24.8 [+15.6, +34.9] |
| best_rank | 21% | 8.3% | 11.9% | -3.7 [-11.9, +4.6] |

Helper twins: helper fell in 3 of 109; mean push time 37.7 s; robots touching 23% of live time (pair twins: 2%).
