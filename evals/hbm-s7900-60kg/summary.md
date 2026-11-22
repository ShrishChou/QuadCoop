# Third robot by branching: hbm-s7900-60kg

Seed 7900, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 112 branched tasks, pair success 74%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 75% | 8.9% | 8.0% | +0.9 [-6.3, +8.0] |
| h1 | 64% | 7.1% | 17.0% | -9.8 [-18.8, -0.9] |
| joint | 75% | 14.3% | 13.4% | +0.9 [-8.9, +10.7] |
| keep | 81% | 17.0% | 9.8% | +7.1 [-1.8, +16.1] |
| move1 | 69% | 12.5% | 17.9% | -5.4 [-15.2, +4.5] |
| move2 | 72% | 15.2% | 17.0% | -1.8 [-12.5, +9.8] |
| jnet | 76% | 16.1% | 14.3% | +1.8 [-8.9, +11.6] |
| best_rank | 64% | 7.1% | 17.0% | -9.8 [-18.8, -0.9] |

## all: 112 branched tasks, pair success 74%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 75% | 8.9% | 8.0% | +0.9 [-6.2, +8.9] |
| h1 | 64% | 7.1% | 17.0% | -9.8 [-19.6, -0.9] |
| joint | 75% | 14.3% | 13.4% | +0.9 [-8.1, +9.8] |
| keep | 81% | 17.0% | 9.8% | +7.1 [-2.7, +17.0] |
| move1 | 69% | 12.5% | 17.9% | -5.4 [-15.2, +5.4] |
| move2 | 72% | 15.2% | 17.0% | -1.8 [-12.5, +8.9] |
| jnet | 76% | 16.1% | 14.3% | +1.8 [-8.0, +11.6] |
| best_rank | 64% | 7.1% | 17.0% | -9.8 [-18.8, -0.9] |

Helper twins: helper fell in 4 of 112; mean push time 16.6 s; robots touching 24% of live time (pair twins: 3%).
