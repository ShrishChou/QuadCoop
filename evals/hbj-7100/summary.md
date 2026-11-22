# Third robot by branching: hbj-7100

Seed 7100, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 115 branched tasks, pair success 73%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 76% | 11.3% | 8.7% | +2.6 [-5.2, +10.4] |
| h1 | 63% | 9.6% | 19.1% | -9.6 [-19.1, +0.0] |
| joint | 70% | 11.3% | 13.9% | -2.6 [-12.2, +6.1] |
| best_rank | 63% | 9.6% | 19.1% | -9.6 [-19.1, +0.0] |

## 80 kg: 114 branched tasks, pair success 33%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 34% | 9.6% | 8.8% | +0.9 [-7.0, +8.8] |
| h1 | 31% | 7.9% | 10.5% | -2.6 [-10.5, +5.3] |
| joint | 52% | 24.6% | 6.1% | +18.4 [+8.8, +27.2] |
| best_rank | 31% | 7.9% | 10.5% | -2.6 [-10.5, +5.3] |

## all: 229 branched tasks, pair success 53%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 55% | 10.5% | 8.7% | +1.7 [-3.5, +7.4] |
| h1 | 47% | 8.7% | 14.8% | -6.1 [-12.7, +0.0] |
| joint | 61% | 17.9% | 10.0% | +7.9 [+0.9, +14.8] |
| best_rank | 47% | 8.7% | 14.8% | -6.1 [-12.2, +0.0] |

Helper twins: helper fell in 14 of 229; mean push time 26.1 s; robots touching 24% of live time (pair twins: 2%).
