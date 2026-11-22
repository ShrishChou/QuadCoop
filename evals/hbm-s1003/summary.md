# Third robot by branching: hbm-s1003

Seed 1003, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 114 branched tasks, pair success 82%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 77% | 4.4% | 8.8% | -4.4 [-11.4, +1.8] |
| h1 | 65% | 2.6% | 19.3% | -16.7 [-24.6, -8.8] |
| keep | 54% | 1.8% | 28.9% | -27.2 [-36.0, -18.4] |
| move1 | 60% | 6.1% | 28.1% | -21.9 [-32.5, -12.3] |
| move2 | 58% | 3.5% | 27.2% | -23.7 [-33.3, -14.9] |
| best_rank | 65% | 2.6% | 19.3% | -16.7 [-25.4, -8.8] |

## 80 kg: 115 branched tasks, pair success 37%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 35% | 4.3% | 6.1% | -1.7 [-7.0, +4.3] |
| h1 | 34% | 7.0% | 9.6% | -2.6 [-9.6, +4.3] |
| keep | 31% | 5.2% | 10.4% | -5.2 [-12.2, +1.7] |
| move1 | 29% | 6.1% | 13.9% | -7.8 [-15.7, +0.0] |
| move2 | 29% | 5.2% | 13.0% | -7.8 [-15.7, +0.0] |
| best_rank | 34% | 7.0% | 9.6% | -2.6 [-10.4, +4.3] |

## all: 229 branched tasks, pair success 59%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 56% | 4.4% | 7.4% | -3.1 [-7.4, +1.3] |
| h1 | 49% | 4.8% | 14.4% | -9.6 [-15.3, -3.9] |
| keep | 43% | 3.5% | 19.7% | -16.2 [-22.3, -10.5] |
| move1 | 44% | 6.1% | 21.0% | -14.8 [-21.4, -8.3] |
| move2 | 43% | 4.4% | 20.1% | -15.7 [-21.4, -10.0] |
| best_rank | 49% | 4.8% | 14.4% | -9.6 [-15.3, -4.4] |

Helper twins: helper fell in 10 of 229; mean push time 25.5 s; robots touching 22% of live time (pair twins: 2%).
