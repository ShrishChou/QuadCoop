# Third robot by branching: hbj-7500

Seed 7500, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 113 branched tasks, pair success 72%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 71% | 12.4% | 13.3% | -0.9 [-10.6, +8.8] |
| h1 | 59% | 8.8% | 21.2% | -12.4 [-22.1, -2.7] |
| joint | 73% | 13.3% | 12.4% | +0.9 [-8.0, +9.7] |
| best_rank | 59% | 8.8% | 21.2% | -12.4 [-22.1, -2.7] |

## 80 kg: 110 branched tasks, pair success 32%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 35% | 8.2% | 4.5% | +3.6 [-3.6, +10.0] |
| h1 | 27% | 5.5% | 10.0% | -4.5 [-11.8, +2.7] |
| joint | 42% | 14.5% | 4.5% | +10.0 [+1.8, +18.2] |
| best_rank | 27% | 5.5% | 10.0% | -4.5 [-11.8, +2.7] |

## all: 223 branched tasks, pair success 52%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 53% | 10.3% | 9.0% | +1.3 [-4.5, +6.7] |
| h1 | 43% | 7.2% | 15.7% | -8.5 [-15.2, -2.2] |
| joint | 57% | 13.9% | 8.5% | +5.4 [-0.9, +11.2] |
| best_rank | 43% | 7.2% | 15.7% | -8.5 [-14.8, -2.7] |

Helper twins: helper fell in 15 of 223; mean push time 26.5 s; robots touching 23% of live time (pair twins: 2%).
