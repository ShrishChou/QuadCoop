# Third robot by branching: hbj-7500-light

Seed 7500, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 20 kg: 110 branched tasks, pair success 80%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 77% | 10.0% | 12.7% | -2.7 [-11.8, +6.4] |
| h1 | 63% | 4.5% | 21.8% | -17.3 [-26.4, -9.1] |
| joint | 89% | 17.3% | 8.2% | +9.1 [+0.0, +18.2] |
| best_rank | 63% | 4.5% | 21.8% | -17.3 [-26.4, -8.2] |

## 40 kg: 113 branched tasks, pair success 81%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 80% | 7.1% | 8.0% | -0.9 [-8.0, +6.2] |
| h1 | 72% | 7.1% | 15.9% | -8.8 [-17.7, +0.9] |
| joint | 88% | 15.0% | 8.0% | +7.1 [-1.8, +15.9] |
| best_rank | 72% | 7.1% | 15.9% | -8.8 [-17.7, +0.0] |

## all: 223 branched tasks, pair success 80%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 78% | 8.5% | 10.3% | -1.8 [-7.6, +4.0] |
| h1 | 67% | 5.8% | 18.8% | -13.0 [-19.3, -6.3] |
| joint | 88% | 16.1% | 8.1% | +8.1 [+1.3, +14.8] |
| best_rank | 67% | 5.8% | 18.8% | -13.0 [-19.3, -7.2] |

Helper twins: helper fell in 10 of 223; mean push time 18.9 s; robots touching 21% of live time (pair twins: 1%).
