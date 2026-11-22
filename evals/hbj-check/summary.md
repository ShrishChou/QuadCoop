# Third robot by branching: hbj-check

Seed 7100, 8 tasks per mass, branch at 10 s, helper staged 3 m behind; pair = the planner pair continues (abstain); null = the same, a noise floor; h<r> = helper to the r-th best third contact. Tasks that ended before the branch are excluded. Rescue = pair fails and the twin succeeds; disruption = the reverse; net = rescue - disruption (pp, 95% paired bootstrap over tasks).

## 80 kg: 7 branched tasks, pair success 0%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 0% | 0.0% | 0.0% | +0.0 [+0.0, +0.0] |
| h1 | 0% | 0.0% | 0.0% | +0.0 [+0.0, +0.0] |
| joint | 14% | 14.3% | 0.0% | +14.3 [+0.0, +42.9] |
| best_rank | 0% | 0.0% | 0.0% | +0.0 [+0.0, +0.0] |

## all: 7 branched tasks, pair success 0%

| twin | success | rescue | disruption | net [95% CI] |
|---|---|---|---|---|
| null | 0% | 0.0% | 0.0% | +0.0 [+0.0, +0.0] |
| h1 | 0% | 0.0% | 0.0% | +0.0 [+0.0, +0.0] |
| joint | 14% | 14.3% | 0.0% | +14.3 [+0.0, +42.9] |
| best_rank | 0% | 0.0% | 0.0% | +0.0 [+0.0, +0.0] |

Helper twins: helper fell in 0 of 7; mean push time 8.4 s; robots touching 13% of live time (pair twins: 0%).
