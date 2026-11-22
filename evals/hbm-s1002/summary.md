# Third robot by branching: hbm-s1002

Seed 1002, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 112 branched tasks, pair success 76%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 78% | 9.8% | 8.0% | +1.8 [-6.2, +9.8] |
| h1 | 62% | 7.1% | 20.5% | -13.4 [-23.2, -3.6] |
| keep | 72% | 10.7% | 14.3% | -3.6 [-12.5, +5.4] |
| move1 | 51% | 4.5% | 29.5% | -25.0 [-34.8, -15.2] |
| move2 | 51% | 6.2% | 31.2% | -25.0 [-35.7, -15.2] |
| best_rank | 62% | 7.1% | 20.5% | -13.4 [-23.2, -4.5] |

## 80 kg: 113 branched tasks, pair success 28%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 30% | 5.3% | 3.5% | +1.8 [-3.5, +8.0] |
| h1 | 32% | 10.6% | 7.1% | +3.5 [-3.5, +11.5] |
| keep | 24% | 6.2% | 10.6% | -4.4 [-12.4, +2.7] |
| move1 | 29% | 9.7% | 8.8% | +0.9 [-7.1, +8.8] |
| move2 | 21% | 6.2% | 13.3% | -7.1 [-15.0, +0.9] |
| best_rank | 32% | 10.6% | 7.1% | +3.5 [-4.4, +11.5] |

## all: 225 branched tasks, pair success 52%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 54% | 7.6% | 5.8% | +1.8 [-3.1, +6.7] |
| h1 | 47% | 8.9% | 13.8% | -4.9 [-11.1, +0.9] |
| keep | 48% | 8.4% | 12.4% | -4.0 [-10.2, +2.2] |
| move1 | 40% | 7.1% | 19.1% | -12.0 [-18.7, -5.3] |
| move2 | 36% | 6.2% | 22.2% | -16.0 [-22.7, -9.8] |
| best_rank | 47% | 8.9% | 13.8% | -4.9 [-11.1, +1.3] |

Helper twins: helper fell in 9 of 225; mean push time 25.2 s; robots touching 24% of live time (pair twins: 2%).
