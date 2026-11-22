# Third robot by branching: hb-7100

Seed 7100, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 112 branched tasks, pair success 76%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 75% | 8.0% | 8.9% | -0.9 [-8.1, +7.1] |
| h1 | 59% | 6.2% | 23.2% | -17.0 [-27.7, -8.0] |
| h2 | 59% | 5.4% | 22.3% | -17.0 [-25.9, -8.0] |
| h3 | 68% | 5.4% | 13.4% | -8.0 [-16.1, +0.0] |
| best_rank | 79% | 9.8% | 6.2% | +3.6 [-3.6, +10.7] |

## 80 kg: 111 branched tasks, pair success 36%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 35% | 7.2% | 8.1% | -0.9 [-8.1, +6.3] |
| h1 | 29% | 8.1% | 15.3% | -7.2 [-16.2, +1.8] |
| h2 | 35% | 8.1% | 9.0% | -0.9 [-9.0, +7.2] |
| h3 | 33% | 9.0% | 11.7% | -2.7 [-10.8, +5.4] |
| best_rank | 47% | 15.3% | 4.5% | +10.8 [+3.6, +18.9] |

## 100 kg: 117 branched tasks, pair success 10%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 8% | 0.0% | 2.6% | -2.6 [-6.0, +0.0] |
| h1 | 13% | 4.3% | 1.7% | +2.6 [-1.7, +6.8] |
| h2 | 12% | 2.6% | 0.9% | +1.7 [-1.7, +5.1] |
| h3 | 8% | 0.0% | 2.6% | -2.6 [-6.0, +0.0] |
| best_rank | 15% | 5.1% | 0.9% | +4.3 [+0.0, +8.5] |

## all: 340 branched tasks, pair success 40%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 39% | 5.0% | 6.5% | -1.5 [-5.0, +2.1] |
| h1 | 33% | 6.2% | 13.2% | -7.1 [-11.5, -2.4] |
| h2 | 35% | 5.3% | 10.6% | -5.3 [-9.7, -1.2] |
| h3 | 36% | 4.7% | 9.1% | -4.4 [-8.5, -0.6] |
| best_rank | 46% | 10.0% | 3.8% | +6.2 [+2.4, +10.3] |

Helper twins: helper fell in 25 of 1020; mean push time 30.1 s; robots touching 15% of live time (pair twins: 2%).
