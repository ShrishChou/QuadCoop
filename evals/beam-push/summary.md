# Engaged-start beam push: beam-push

Two ANYmals, frozen walker, scripted: constant forward command, lateral slot +/-0.7 m and heading held. Beam broadside, robots start 0.05 m behind it. 20 s per case; force and contact from 2 s until the first fall. Beam friction per repeat: [0.4, 0.5, 0.6]. 'transported' = moved >= 1 m (0.05 m/s average) before any fall.

| mass | speed cmd | transported | dx m (by mu 0.4/0.5/0.6) | v last 10 s | yaw drift deg | falls | F_x N (impulse/time) | F_x 1 s p90 | duty r1 / r2 / both | mu m g N |
|---|---|---|---|---|---|---|---|---|---|---|
| 40 | 0.4 | 3/3 | 8.74 / 7.87 / 8.12 | 0.424 | 6 | 0.00 | 188 | 209 | 0.72 / 0.67 / 0.49 | 196 |
| 40 | 0.6 | 3/3 | 11.70 / 11.34 / 4.77 | 0.457 | 8 | 0.00 | 183 | 203 | 0.65 / 0.66 / 0.44 | 196 |
| 40 | 0.8 | 3/3 | 14.38 / 7.46 / 8.35 | 0.420 | 27 | 0.00 | 161 | 207 | 0.49 / 0.53 / 0.27 | 196 |
| 60 | 0.4 | 3/3 | 6.83 / 2.96 / 1.77 | 0.200 | 6 | 0.00 | 266 | 290 | 0.83 / 0.82 / 0.68 | 294 |
| 60 | 0.6 | 2/3 | 10.32 / 6.88 / 0.89 | 0.294 | 7 | 0.00 | 253 | 285 | 0.78 / 0.76 / 0.60 | 294 |
| 60 | 0.8 | 3/3 | 9.41 / 4.42 / 1.32 | 0.211 | 24 | 0.00 | 238 | 285 | 0.65 / 0.72 / 0.51 | 294 |
| 80 | 0.4 | 1/3 | 2.65 / 0.40 / 0.19 | 0.052 | 3 | 0.00 | 307 | 330 | 0.91 / 0.88 / 0.80 | 392 |
| 80 | 0.6 | 2/3 | 4.21 / 1.02 / 0.16 | 0.080 | 2 | 0.00 | 304 | 333 | 0.86 / 0.85 / 0.74 | 392 |
| 80 | 0.8 | 1/3 | 5.94 / 0.56 / 0.20 | 0.132 | 4 | 0.00 | 292 | 333 | 0.85 / 0.83 / 0.71 | 392 |
