# Walker force test (test A): wf-test

One ANYmal walking into a cube face at a fixed commanded speed; force on the object along the face normal, measured from 3 s to 6 s. Each cell: mean force (N) over 3 repeats; in brackets its typical swing over time (std, N). 'sustained' = touching > 90% of the time and std < 30% of the mean.

## 5000 kg (immovable: what the robot holds against a wall)

| speed cmd (m/s) | 0 deg: force (swing) | 15 deg: force (swing) | 30 deg: force (swing) | touching | force along heading (cos) | fell | turned (deg) |
|---|---|---|---|---|---|---|---|
| 0.05 | 0 (0) | 0 (0) | 4 (18) | 0.02 | 0.27 | 0.00 | 8 / 7 / 7 |
| 0.1 | 0 (0) | 0 (0) | 0 (0) | 0.00 | 0.00 | 0.00 | 1 / 1 / 1 |
| 0.2 | 32 (33) | 0 (0) | 0 (0) | 0.08 | 0.11 | 0.00 | 1 / -0 / -0 |
| 0.3 | 139 (107) | 138 (119) | 114 (109) | 0.78 | 0.97 | 0.00 | -1 / -1 / -1 |
| 0.4 | 168 (128) | 128 (107) | 46 (65) | 0.64 | 0.91 | 0.00 | -1 / -2 / -1 |
| 0.5 | 181 (123) | 168 (129) | 96 (116) | 0.68 | 0.96 | 0.00 | 1 / -0 / -3 |
| 0.6 | 200 (137) | 164 (162) | 60 (61) | 0.62 | 0.85 | 0.00 | 0 / 1 / 1 |
| 0.8 | 174 (160) | 166 (173) | 109 (108) | 0.60 | 0.93 | 0.00 | 4 / -1 / -0 |

**5000 kg, square on:** NOT DISTINCT: 0 to 200 N across speeds (not monotonic), sustained in 0% of square-on cases.

## 80 kg

| speed cmd (m/s) | 0 deg: force (swing) | 15 deg: force (swing) | 30 deg: force (swing) | touching | force along heading (cos) | fell | object speed (m/s) |
|---|---|---|---|---|---|---|---|
| 0.05 | 0 (0) | 0 (0) | 4 (20) | 0.02 | 0.27 | 0.00 | 0.00 |
| 0.1 | 0 (0) | 0 (0) | 0 (0) | 0.00 | 0.00 | 0.00 | 0.00 |
| 0.2 | 30 (29) | 0 (0) | 0 (0) | 0.07 | 0.11 | 0.00 | 0.00 |
| 0.3 | 143 (108) | 143 (103) | 77 (96) | 0.72 | 0.97 | 0.00 | 0.00 |
| 0.4 | 177 (123) | 127 (106) | 58 (92) | 0.66 | 0.96 | 0.00 | 0.00 |
| 0.5 | 180 (119) | 182 (126) | 78 (80) | 0.69 | 0.95 | 0.00 | 0.01 |
| 0.6 | 186 (129) | 163 (134) | 80 (90) | 0.64 | 0.85 | 0.00 | 0.01 |
| 0.8 | 193 (144) | 193 (139) | 166 (146) | 0.77 | 0.96 | 0.00 | 0.01 |

**80 kg, square on:** DISTINCT LEVELS: 0 to 193 N across speeds (rising), sustained in 0% of square-on cases.

## 40 kg

| speed cmd (m/s) | 0 deg: force (swing) | 15 deg: force (swing) | 30 deg: force (swing) | touching | force along heading (cos) | fell | object speed (m/s) |
|---|---|---|---|---|---|---|---|
| 0.05 | 0 (0) | 0 (0) | 3 (16) | 0.02 | 0.27 | 0.00 | 0.00 |
| 0.1 | 0 (0) | 0 (0) | 0 (0) | 0.00 | 0.00 | 0.00 | 0.00 |
| 0.2 | 29 (24) | 0 (0) | 0 (0) | 0.08 | 0.11 | 0.00 | 0.00 |
| 0.3 | 131 (93) | 137 (95) | 58 (77) | 0.69 | 0.96 | 0.00 | 0.03 |
| 0.4 | 161 (109) | 124 (95) | 84 (88) | 0.72 | 0.96 | 0.00 | 0.05 |
| 0.5 | 164 (116) | 168 (120) | 113 (86) | 0.76 | 0.96 | 0.00 | 0.11 |
| 0.6 | 161 (147) | 157 (121) | 60 (64) | 0.64 | 0.85 | 0.00 | 0.15 |
| 0.8 | 152 (149) | 154 (136) | 106 (103) | 0.70 | 0.97 | 0.00 | 0.29 |

**40 kg, square on:** DISTINCT LEVELS: 0 to 164 N across speeds (rising), sustained in 0% of square-on cases.

## 20 kg

| speed cmd (m/s) | 0 deg: force (swing) | 15 deg: force (swing) | 30 deg: force (swing) | touching | force along heading (cos) | fell | object speed (m/s) |
|---|---|---|---|---|---|---|---|
| 0.05 | 0 (0) | 0 (0) | 3 (14) | 0.02 | 0.28 | 0.00 | 0.00 |
| 0.1 | 0 (0) | 0 (0) | 0 (0) | 0.00 | 0.00 | 0.00 | 0.00 |
| 0.2 | 27 (23) | 0 (0) | 25 (22) | 0.17 | 0.21 | 0.00 | 0.02 |
| 0.3 | 89 (80) | 95 (77) | 52 (65) | 0.74 | 0.94 | 0.00 | 0.17 |
| 0.4 | 86 (82) | 74 (77) | 45 (64) | 0.65 | 0.93 | 0.00 | 0.25 |
| 0.5 | 53 (69) | 76 (89) | 49 (79) | 0.57 | 0.96 | 0.00 | 0.35 |
| 0.6 | 61 (83) | 69 (77) | 40 (61) | 0.55 | 0.85 | 0.00 | 0.37 |
| 0.8 | 34 (52) | 22 (56) | 65 (112) | 0.37 | 0.80 | 0.00 | 0.36 |

**20 kg, square on:** NOT DISTINCT: 0 to 89 N across speeds (not monotonic), sustained in 0% of square-on cases.

