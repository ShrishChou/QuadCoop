# Engaged-start beam push: beam-push2-heavy

2 ANYmals at slots [0.7, -0.7] m, frozen walker, scripted: constant forward command, lateral slot and heading held. Beam broadside, robots start 0.05 m behind it. 20 s per case; force and contact from 2 s until the first fall. Beam friction per repeat: [0.4, 0.5, 0.6]. 'transported' = moved >= 1 m (0.05 m/s average) before any fall.

| mass | speed cmd | transported | dx m (by mu 0.4/0.5/0.6) | v last 10 s | yaw drift deg | falls | F_x N (impulse/time) | F_x per robot | F_x 1 s p90 | duty per robot / all | mu m g N |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 100 | 0.6 | 0/3 | 0.74 / 0.16 / 0.07 | 0.015 | 1 | 0.00 | 322 | 167 / 156 | 356 | 0.89 / 0.88 / 0.79 | 490 |
| 100 | 0.8 | 0/3 | 0.92 / 0.13 / 0.04 | 0.017 | 2 | 0.33 | 303 | 155 / 148 | 337 | 0.85 / 0.84 / 0.71 | 490 |
| 120 | 0.6 | 0/3 | 0.22 / 0.05 / 0.03 | 0.004 | 0 | 0.00 | 318 | 162 / 156 | 357 | 0.88 / 0.89 / 0.79 | 589 |
| 120 | 0.8 | 0/3 | 0.18 / 0.05 / 0.03 | 0.003 | 1 | 0.33 | 299 | 157 / 142 | 346 | 0.84 / 0.84 / 0.71 | 589 |
