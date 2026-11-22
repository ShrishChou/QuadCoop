# K -> K+1 tree: kc-check2

Seed 1001, 12 tasks per mass; robot 2 added at 8 s (k2a) or 20 s (k2b), robot 3 at 20 s after robot 2 at 8 s (k3). Success over all starts (a task that ended before a branch has the same outcome in every twin). Nets in pp with 95% paired bootstrap.

| mass | k1 | k2b | k2a | k3 | k1null-k1 | k2a-k1 | k3-k2a | k2null-k2a | k2b-k1 |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 25% | 42% | 75% | 75% | +8.3 [+0, +25] | +50.0 [+8, +92] | +0.0 [+0, +0] | +0.0 [+0, +0] | +16.7 [-17, +50] |
| 80 | 0% | 25% | 17% | 17% | +0.0 [+0, +0] | +16.7 [+0, +42] | +0.0 [+0, +0] | +0.0 [+0, +0] | +25.0 [+0, +50] |
| all | 12% | 33% | 46% | 46% | +4.2 [+0, +12] | +33.3 [+8, +58] | +0.0 [+0, +0] | +0.0 [+0, +0] | +20.8 [+0, +42] |
