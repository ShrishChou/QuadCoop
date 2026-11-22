# Third robot by branching: hbm-s1001

Seed 1001, 120 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 60 kg: 115 branched tasks, pair success 79%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 78% | 7.0% | 7.8% | -0.9 [-7.8, +6.1] |
| h1 | 58% | 6.1% | 27.0% | -20.9 [-30.4, -11.3] |
| keep | 57% | 5.2% | 27.8% | -22.6 [-32.2, -13.0] |
| move1 | 60% | 6.1% | 25.2% | -19.1 [-28.7, -9.6] |
| move2 | 57% | 4.3% | 27.0% | -22.6 [-32.2, -13.0] |
| best_rank | 58% | 6.1% | 27.0% | -20.9 [-30.4, -11.3] |

## 80 kg: 116 branched tasks, pair success 28%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 30% | 7.8% | 5.2% | +2.6 [-4.3, +8.6] |
| h1 | 23% | 6.0% | 10.3% | -4.3 [-12.1, +2.6] |
| keep | 28% | 9.5% | 8.6% | +0.9 [-6.9, +8.6] |
| move1 | 22% | 7.8% | 12.9% | -5.2 [-13.8, +2.6] |
| move2 | 26% | 7.8% | 9.5% | -1.7 [-8.6, +6.0] |
| best_rank | 23% | 6.0% | 10.3% | -4.3 [-11.2, +2.6] |

## all: 231 branched tasks, pair success 53%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 54% | 7.4% | 6.5% | +0.9 [-3.9, +5.6] |
| h1 | 41% | 6.1% | 18.6% | -12.6 [-18.6, -6.5] |
| keep | 42% | 7.4% | 18.2% | -10.8 [-16.9, -4.3] |
| move1 | 41% | 6.9% | 19.0% | -12.1 [-18.6, -6.1] |
| move2 | 41% | 6.1% | 18.2% | -12.1 [-18.2, -6.1] |
| best_rank | 41% | 6.1% | 18.6% | -12.6 [-19.0, -6.5] |

Helper twins: helper fell in 14 of 231; mean push time 27.0 s; robots touching 26% of live time (pair twins: 2%).
