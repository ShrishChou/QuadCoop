# K -> K+1 tree: kc-check3

Seed 1001, 12 tasks per mass; robot 2 added at 8 s (k2a) or 20 s (k2b), robot 3 at 20 s after robot 2 at 8 s (k3). Success over all starts (a task that ended before a branch has the same outcome in every twin). Nets in pp with 95% paired bootstrap.

| mass | k1 | k2b | k2a | k3 | k1null-k1 | k2a-k1 | k3-k2a | k2null-k2a | k2b-k1 |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 17% | 58% | 67% | 58% | +8.3 [-17, +42] | +50.0 [+25, +75] | -8.3 [-33, +17] | +16.7 [+0, +42] | +41.7 [+17, +67] |
| 80 | 0% | 25% | 17% | 25% | +8.3 [+0, +25] | +16.7 [+0, +42] | +8.3 [+0, +25] | +8.3 [+0, +25] | +25.0 [+0, +50] |
| all | 8% | 42% | 42% | 42% | +8.3 [-8, +25] | +33.3 [+17, +50] | +0.0 [-17, +17] | +12.5 [+0, +25] | +33.3 [+17, +54] |
