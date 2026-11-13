# Engaged-start beam push: beam-push-slot048

Two ANYmals, frozen walker, scripted: constant forward command, lateral slot +/-0.48 m and heading held. Beam broadside, robots start 0.05 m behind it. 20 s per case; force and contact from 2 s until the first fall. Beam friction per repeat: [0.4, 0.5, 0.6]. 'transported' = moved >= 1 m (0.05 m/s average) before any fall.

| mass | speed cmd | transported | dx m (by mu 0.4/0.5/0.6) | v last 10 s | yaw drift deg | falls | F_x N (impulse/time) | F_x 1 s p90 | duty r1 / r2 / both | mu m g N |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 | 0.4 | 3/3 | 8.63 / 7.97 / 8.12 | 0.421 | 5 | 0.00 | 191 | 211 | 0.73 / 0.66 / 0.48 | 196 |
| 40 | 0.6 | 3/3 | 11.66 / 11.18 / 5.17 | 0.463 | 9 | 0.00 | 186 | 207 | 0.65 / 0.66 / 0.43 | 196 |
| 40 | 0.8 | 3/3 | 8.03 / 9.52 / 7.81 | 0.275 | 48 | 0.00 | 150 | 203 | 0.45 / 0.51 / 0.29 | 196 |
| 60 | 0.4 | 3/3 | 6.84 / 3.20 / 1.27 | 0.196 | 4 | 0.00 | 270 | 299 | 0.84 / 0.83 / 0.71 | 294 |
| 60 | 0.6 | 2/3 | 9.96 / 6.51 / 0.82 | 0.285 | 5 | 0.00 | 256 | 283 | 0.79 / 0.77 / 0.61 | 294 |
| 60 | 0.8 | 2/3 | 5.82 / 2.32 / 1.00 | 0.022 | 22 | 0.33 | 216 | 284 | 0.61 / 0.64 / 0.47 | 294 |
| 80 | 0.4 | 1/3 | 2.29 / 0.43 / 0.20 | 0.046 | 3 | 0.00 | 309 | 336 | 0.90 / 0.89 / 0.80 | 392 |
| 80 | 0.6 | 1/3 | 4.06 / 0.85 / 0.15 | 0.086 | 0 | 0.00 | 307 | 340 | 0.87 / 0.86 / 0.75 | 392 |
| 80 | 0.8 | 1/3 | 5.00 / 0.72 / 0.13 | 0.082 | 4 | 0.00 | 289 | 334 | 0.84 / 0.87 / 0.73 | 392 |
