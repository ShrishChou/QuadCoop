# Engaged-start beam push: beam-push-slot096

Two ANYmals, frozen walker, scripted: constant forward command, lateral slot +/-0.96 m and heading held. Beam broadside, robots start 0.05 m behind it. 20 s per case; force and contact from 2 s until the first fall. Beam friction per repeat: [0.4, 0.5, 0.6]. 'transported' = moved >= 1 m (0.05 m/s average) before any fall.

| mass | speed cmd | transported | dx m (by mu 0.4/0.5/0.6) | v last 10 s | yaw drift deg | falls | F_x N (impulse/time) | F_x 1 s p90 | duty r1 / r2 / both | mu m g N |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 | 0.4 | 3/3 | 6.80 / 5.15 / 4.60 | 0.222 | 53 | 0.00 | 144 | 195 | 0.46 / 0.76 / 0.36 | 196 |
| 40 | 0.6 | 3/3 | 11.50 / 9.93 / 6.59 | 0.467 | 17 | 0.00 | 158 | 197 | 0.54 / 0.58 / 0.30 | 196 |
| 40 | 0.8 | 3/3 | 14.31 / 12.43 / 8.98 | 0.591 | 24 | 0.00 | 174 | 208 | 0.55 / 0.55 / 0.26 | 196 |
| 60 | 0.4 | 3/3 | 5.05 / 3.81 / 2.36 | 0.171 | 44 | 0.00 | 247 | 294 | 0.73 / 0.81 / 0.60 | 294 |
| 60 | 0.6 | 3/3 | 9.43 / 2.97 / 1.12 | 0.200 | 26 | 0.00 | 204 | 267 | 0.71 / 0.58 / 0.45 | 294 |
| 60 | 0.8 | 3/3 | 5.78 / 4.81 / 2.82 | 0.136 | 28 | 0.33 | 245 | 290 | 0.72 / 0.65 / 0.47 | 294 |
| 80 | 0.4 | 1/3 | 1.94 / 0.76 / 0.30 | 0.046 | 15 | 0.00 | 275 | 319 | 0.87 / 0.83 / 0.73 | 392 |
| 80 | 0.6 | 2/3 | 4.17 / 1.57 / 0.36 | 0.102 | 2 | 0.00 | 281 | 319 | 0.83 / 0.83 / 0.69 | 392 |
| 80 | 0.8 | 0/3 | 0.88 / 0.47 / 0.26 | 0.005 | 18 | 0.67 | 250 | 293 | 0.82 / 0.75 / 0.63 | 392 |
