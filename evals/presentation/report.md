# Presentation: two-robot pushing, all systems on the same tasks

480 matched tasks (10 objects x 4 masses x 4 scenarios x 3 placements, seed 7100). Rates are per-task means over the runs available (n runs in brackets).

| system | runs | success | precise | episodes with a fall | time to success, median s |
|---|---|---|---|---|---|
| single ANYmal | 2 | 52.4% | 47.8% | 7.5% | 18.5 |
| frozen pair | 2 | 46.1% | 41.1% | 37.3% | 17.6 |
| planner + executor | 2 | 65.6% | 54.3% | 3.3% | 30.2 |
| IPPO (it 4000) | 2 | 65.1% | 59.4% | 11.7% | 18.4 |
| MAPPO (B, it 5000) | 2 | 65.0% | 59.4% | 13.5% | 19.9 |

## Success by mass

| system | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| single ANYmal | 86% | 78% | 32% | 12% |
| frozen pair | 71% | 57% | 38% | 19% |
| planner + executor | 82% | 77% | 62% | 42% |
| IPPO (it 4000) | 89% | 81% | 62% | 29% |
| MAPPO (B, it 5000) | 89% | 81% | 65% | 25% |

## Success by object

| system | cube | long | sphere | cylinder | arch | dumbbell | t_shape | l_shape | u_channel | plus |
|---|---|---|---|---|---|---|---|---|---|---|
| single ANYmal | 67% | 51% | 100% | 43% | 24% | 42% | 49% | 58% | 52% | 39% |
| frozen pair | 52% | 52% | 94% | 26% | 14% | 41% | 51% | 60% | 42% | 30% |
| planner + executor | 79% | 54% | 94% | 39% | 73% | 68% | 64% | 65% | 69% | 53% |
| IPPO (it 4000) | 69% | 72% | 98% | 40% | 31% | 55% | 72% | 75% | 74% | 66% |
| MAPPO (B, it 5000) | 68% | 77% | 95% | 44% | 31% | 58% | 75% | 75% | 76% | 51% |

## Success by scenario

| system | A_straight | B_left | C_backright | D_far_turn |
|---|---|---|---|---|
| single ANYmal | 59% | 55% | 58% | 38% |
| frozen pair | 56% | 44% | 50% | 34% |
| planner + executor | 75% | 69% | 62% | 56% |
| IPPO (it 4000) | 76% | 67% | 59% | 58% |
| MAPPO (B, it 5000) | 76% | 68% | 62% | 54% |

## Against one ANYmal (paired per task)

Rescued: the single robot fails in every run and the system succeeds in every run; lost: the reverse.

| system | change in success [95% CI] | rescued | lost | rescued at 60-80 kg |
|---|---|---|---|---|
| frozen pair | -6.2 [-9.9, -2.6] pts | 17 | 34 | 11 |
| planner + executor | +13.2 [+9.1, +17.8] pts | 77 | 19 | 57 |
| IPPO (it 4000) | +12.7 [+9.3, +16.0] pts | 51 | 7 | 40 |
| MAPPO (B, it 5000) | +12.6 [+9.0, +16.2] pts | 51 | 11 | 38 |

## Each trained actor alone (partner parked far away)

| actor | success |
|---|---|
| IPPO actor 1 alone | 13.3% |
| IPPO actor 2 alone | 17.5% |
| MAPPO actor 1 alone | 4.2% |
| MAPPO actor 2 alone | 14.6% |

## Filmed tasks (same tasks for every system, every outcome)

- single ANYmal: 24 videos in `logs/evals/pres-solo-anymal/pair/`
- frozen pair: 24 videos in `logs/evals/pres-frozen-pair/pair/`
- planner + executor: 24 videos in `logs/evals/pres-planner-expert/pair/`
- IPPO (it 4000): 24 videos in `logs/evals/pres-ippo-it4000/pair/`
- MAPPO (B, it 5000): 24 videos in `logs/evals/pres-mappo-B-it5000/pair/`
