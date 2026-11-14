# Contact loss and recovery

Logging pass vs ten-ippo-source-dev7100: same outcome on 398/480 tasks; successes 309 vs 303

## ten-ippo-source-dev7100-recovery

480 episodes, 802 disengagements (315 episodes with at least one; 1.67 per episode)

| window after confirmation | recovered | not recovered | censored (success / own fall / partner fall / other) |
|---|---|---|---|
| 1 s | 266 (34% of decided) | 511 | 14 / 5 / 2 / 4 |
| 3 s | 420 (56% of decided) | 333 | 28 / 5 / 7 / 9 |
| 5 s | 508 (69% of decided) | 232 | 35 / 6 / 8 / 13 |

Re-engagement time after confirmation (s): median 1.6, p90 10.4 (contact-free time is that + 1 s); place: same 276, different 375

| during separation | n | partner pushing (mean share) | object pos change m (median) | heading change deg (median) | episode success |
|---|---|---|---|---|---|
| stall | 165 | 0.29 | -0.01 | +0.0 | 29% |
| productive | 287 | 0.56 | -0.36 | -1.2 | 54% |
| modest | 67 | 0.39 | -0.06 | -1.5 | 31% |
| release_near_goal | 283 | 0.19 | -0.00 | -0.5 | 63% |

Prolonged (>= 3 s) separations: 412; by kind productive 215, release_near_goal 122, stall 46, modest 29
Episodes with a prolonged stalled separation: 37/480, success 19%; the other episodes: success 68%

| object | disengagements | prolonged stalls | episodes failed with a prolonged stall |
|---|---|---|---|
| arch | 206 | 9 | 7 |
| cube | 21 | 1 | 1 |
| cylinder | 92 | 5 | 4 |
| dumbbell | 86 | 6 | 2 |
| l_shape | 52 | 4 | 3 |
| long | 88 | 3 | 2 |
| plus | 72 | 5 | 3 |
| sphere | 22 | 0 | 0 |
| t_shape | 80 | 7 | 3 |
| u_channel | 83 | 6 | 5 |

Logging pass vs ten-ippo-it4000-dev7100: same outcome on 412/480 tasks; successes 311 vs 315

## ten-ippo-it4000-dev7100-recovery

480 episodes, 774 disengagements (322 episodes with at least one; 1.61 per episode)

| window after confirmation | recovered | not recovered | censored (success / own fall / partner fall / other) |
|---|---|---|---|
| 1 s | 249 (33% of decided) | 495 | 24 / 4 / 1 / 1 |
| 3 s | 407 (57% of decided) | 311 | 41 / 5 / 2 / 8 |
| 5 s | 495 (71% of decided) | 207 | 50 / 7 / 3 / 12 |

Re-engagement time after confirmation (s): median 1.7, p90 9.2 (contact-free time is that + 1 s); place: same 246, different 376

| during separation | n | partner pushing (mean share) | object pos change m (median) | heading change deg (median) | episode success |
|---|---|---|---|---|---|
| stall | 165 | 0.29 | -0.01 | +0.0 | 23% |
| productive | 282 | 0.57 | -0.42 | -1.2 | 63% |
| modest | 42 | 0.37 | -0.06 | -0.7 | 38% |
| release_near_goal | 285 | 0.25 | -0.01 | -0.3 | 68% |

Prolonged (>= 3 s) separations: 389; by kind productive 214, release_near_goal 123, stall 38, modest 14
Episodes with a prolonged stalled separation: 27/480, success 11%; the other episodes: success 68%

| object | disengagements | prolonged stalls | episodes failed with a prolonged stall |
|---|---|---|---|
| arch | 161 | 12 | 8 |
| cube | 28 | 1 | 1 |
| cylinder | 88 | 4 | 3 |
| dumbbell | 89 | 11 | 6 |
| l_shape | 63 | 1 | 0 |
| long | 45 | 2 | 1 |
| plus | 68 | 0 | 0 |
| sphere | 32 | 0 | 0 |
| t_shape | 105 | 5 | 3 |
| u_channel | 95 | 2 | 2 |
