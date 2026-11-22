# Third robot by branching: hbj-7100-light

Seed 7100, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 20 kg: 107 branched tasks, pair success 72%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 74% | 15.0% | 13.1% | +1.9 [-8.4, +12.1] |
| h1 | 64% | 11.2% | 19.6% | -8.4 [-18.7, +1.9] |
| joint | 89% | 24.3% | 7.5% | +16.8 [+6.5, +27.1] |
| best_rank | 64% | 11.2% | 19.6% | -8.4 [-18.7, +1.9] |

## 40 kg: 111 branched tasks, pair success 80%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 77% | 8.1% | 10.8% | -2.7 [-10.8, +5.4] |
| h1 | 72% | 10.8% | 18.9% | -8.1 [-18.0, +1.8] |
| joint | 87% | 16.2% | 9.0% | +7.2 [-1.8, +16.2] |
| best_rank | 72% | 10.8% | 18.9% | -8.1 [-18.0, +1.8] |

## all: 218 branched tasks, pair success 76%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 76% | 11.5% | 11.9% | -0.5 [-6.4, +6.0] |
| h1 | 68% | 11.0% | 19.3% | -8.3 [-15.1, -1.4] |
| joint | 88% | 20.2% | 8.3% | +11.9 [+5.5, +18.8] |
| best_rank | 68% | 11.0% | 19.3% | -8.3 [-15.6, -0.9] |

Helper twins: helper fell in 9 of 218; mean push time 18.5 s; robots touching 26% of live time (pair twins: 1%).
