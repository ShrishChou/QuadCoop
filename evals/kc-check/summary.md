# K -> K+1 tree: kc-check

Seed 1001, 12 tasks per mass; robot 2 added at 8 s (k2a) or 20 s (k2b), robot 3 at 20 s after robot 2 at 8 s (k3). Success over all starts (a task that ended before a branch has the same outcome in every twin). Nets in pp with 95% paired bootstrap.

| mass | k1 | k2b | k2a | k3 | k1null-k1 | k2a-k1 | k3-k2a | k2null-k2a | k2b-k1 |
|---|---|---|---|---|---|---|---|---|---|
| 20 | 0% | 33% | 67% | 67% | +0.0 [+0, +0] | +66.7 [+42, +92] | +0.0 [-25, +25] | -25.0 [-50, +0] | +33.3 [+8, +58] |
| 80 | 0% | 17% | 17% | 17% | +0.0 [+0, +0] | +16.7 [+0, +42] | +0.0 [+0, +0] | -8.3 [-25, +0] | +16.7 [+0, +42] |
| all | 0% | 25% | 42% | 42% | +0.0 [+0, +0] | +41.7 [+21, +62] | +0.0 [-12, +12] | -16.7 [-33, -4] | +25.0 [+8, +46] |
