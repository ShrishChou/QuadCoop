# Planner physics test (test 1): pp-ends

No robots, no learning: the planner's pushes applied as forces at the contact points, held 4 s (measured over the last 3.5 s). Motion = (dx, dy, r_g x dyaw); moved = 2 cm or more; 'as asked' = cosine with the wanted motion >= 0.8. Robot push (normal force): 150, 250, 350 N. Objects at nominal size.

Control (no push, every object and mass): largest motion 0.0 cm (cube, 20 kg) - OK (must stay under 1 cm).

## 1. Is the planner's force model right? (150 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=11) | 1.00 (n=11) | 0.36 (n=11) | 0.11 (n=9) | 0.64 |
| move_x | 0.92 (n=12) | 1.00 (n=12) | 1.00 (n=12) | - | 0.97 |
| move_y | 0.92 (n=12) | 0.92 (n=12) | 0.83 (n=12) | - | 0.89 |
| move_turn | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=10) | 1.00 (n=5) | 1.00 |

**Verdict:** 0.87 of the workable planner pushes moved as asked (FAIL: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 5, cube 2, long 2, dumbbell 2, beam 2, plus 2, asym 1, arch 1, t_shape 1, l_shape 1, u_channel 1

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| arch | 60 | turn | 0 |  | 0.0 | 0.29 | 0.0 | 0.088 | 1.07 |
| asym | 20 | move_x | 1 | 0.755 | 0.1426 | 9.67 | 0.086 | 0.104 | 2.531 |
| beam | 60 | turn | 0 |  | 0.0 | 0.11 | 0.0 | 0.038 | 1.771 |
| beam | 80 | turn | 0 |  | 0.0 | 0.06 | 0.0 | 0.038 | 1.328 |
| cube | 60 | turn | 0 |  | 0.0 | 1.83 | 0.0 | 0.082 | 1.474 |
| cube | 80 | turn | 0 |  | 0.0 | 0.12 | 0.0 | 0.082 | 1.105 |
| cylinder | 20 | move_y | 1 | 0.557 | 0.1457 | 0.19 | 0.579 | 0.12 | 3.151 |
| cylinder | 40 | move_y | 1 | 0.573 | 0.1469 | 0.32 | 0.574 | 0.12 | 1.575 |
| cylinder | 60 | move_y | 1 | 0.224 | 0.1535 | -0.03 | 0.417 | 0.12 | 1.05 |
| cylinder | 60 | turn | 0 |  | 0.0 | 0.55 | 0.0 | 0.057 | 1.802 |
| cylinder | 80 | turn | 0 |  | 0.0 | 0.39 | 0.0 | 0.057 | 1.352 |
| dumbbell | 60 | move_y | 0 |  | 0.0048 | -0.0 | 0.003 | 0.13 | 1.081 |
| dumbbell | 60 | turn | 0 |  | 0.0 | 0.23 | 0.0 | 0.086 | 1.146 |
| l_shape | 80 | turn | 0 |  | 0.0002 | 0.07 | 0.0 | 0.071 | 1.209 |
| long | 60 | turn | 0 |  | 0.0 | 0.96 | 0.0 | 0.077 | 1.527 |
| long | 80 | turn | 0 |  | 0.0 | 0.11 | 0.0 | 0.077 | 1.145 |
| plus | 60 | turn | 0 |  | 0.0 | 0.11 | 0.0 | 0.035 | 1.829 |
| plus | 80 | turn | 0 |  | 0.0 | 0.05 | 0.0 | 0.035 | 1.372 |
| t_shape | 80 | turn | 0 |  | 0.0 | 0.06 | 0.0 | 0.055 | 1.202 |
| u_channel | 80 | turn | 0 |  | 0.0004 | 0.31 | 0.007 | 0.088 | 1.017 |

Planner pushes the model rates too weak to slide the object (strength < 1): 32; moved as asked anyway: 11; moved at all: 21.

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 55 N, 0.00 at limit | 110 N, 0.00 at limit | 148 N, 0.82 at limit | 142 N, 0.82 at limit |
| move_x | 49 N, 0.00 at limit | 97 N, 0.08 at limit | 128 N, 0.33 at limit | 118 N, 0.33 at limit |
| move_y | 53 N, 0.00 at limit | 106 N, 0.00 at limit | 136 N, 0.67 at limit | 126 N, 0.50 at limit |
| move_turn | 52 N, 0.00 at limit | 102 N, 0.00 at limit | 113 N, 0.09 at limit | 129 N, 0.27 at limit |

## 2. Does the planner judge weight right (one robot or both)? (150 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 28 | 13 | 1 | 4 | 0.89 |
| 40 kg | 4 | 28 | 0 | 14 | 0.70 |
| 60 kg | 0 | 33 | 0 | 13 | 0.72 |
| 80 kg | 0 | 42 | 0 | 4 | 0.91 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 10.95 | 19.92 | 19.27 |
| 40 kg | 0.00 | 9.26 | 19.08 | 18.55 |
| 60 kg | 0.00 | 4.19 | 9.61 | 4.65 |
| 80 kg | 0.00 | 0.35 | 5.23 | 1.36 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (150 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cube | 20 | 0.52 (17) | 0.51 (17) | 1.00 (37) | 1.00 (37) | 1.00 (37) | 1.00 (37) |
| cube | 40 | 0.51 (17) | 0.51 (18) | 1.00 (35) | 1.00 (35) | 1.00 (35) | 1.00 (35) |
| cube | 60 | 0.46 (1) | 0.36 (2) | 0.58 (3) | 0.66 (23) | 0.00 (2) | 0.00 (2) |
| cube | 80 | 0.00 (0) | 0.31 (10) | 0.00 (0) | 0.56 (1) | 0.00 (0) | 0.00 (0) |
| long | 20 | 0.52 (13) | 0.52 (13) | 1.00 (30) | 1.00 (30) | 1.00 (29) | 1.00 (29) |
| long | 40 | 0.50 (12) | 0.50 (12) | 1.00 (28) | 1.00 (28) | 1.00 (28) | 1.00 (28) |
| long | 60 | 0.00 (1) | 0.00 (1) | 0.00 (1) | 0.52 (15) | 0.00 (1) | 0.00 (1) |
| long | 80 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.49 (1) | 0.00 (0) | 0.00 (0) |
| cylinder | 20 | 0.10 (2) | 0.11 (3) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.10 (2) | 0.09 (2) | 1.00 (23) | 1.00 (23) | 1.00 (23) | 1.00 (24) |
| cylinder | 60 | 0.11 (3) | 0.09 (2) | 0.15 (4) | 0.15 (4) | 0.00 (1) | 0.00 (1) |
| cylinder | 80 | 0.11 (3) | 0.09 (2) | 0.15 (3) | 0.15 (3) | 0.00 (0) | 0.00 (0) |
| arch | 20 | 0.66 (7) | 0.69 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 40 | 0.65 (6) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 60 | 0.62 (3) | 0.67 (7) | 1.00 (1) | 1.00 (1) | 0.00 (0) | 0.00 (0) |
| arch | 80 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.62 (6) | 0.62 (6) | 0.62 (6) |
| dumbbell | 20 | 0.70 (7) | 0.72 (7) | 1.00 (11) | 1.00 (11) | 1.00 (10) | 1.00 (10) |
| dumbbell | 40 | 0.70 (7) | 0.71 (7) | 1.00 (9) | 1.00 (9) | 1.00 (9) | 1.00 (9) |
| dumbbell | 60 | 0.70 (7) | 0.70 (6) | 0.95 (1) | 0.95 (1) | 0.00 (0) | 0.00 (0) |
| dumbbell | 80 | 0.00 (0) | 0.00 (0) | 0.00 (0) | 0.68 (6) | 0.68 (6) | 0.68 (6) |
| t_shape | 20 | 0.74 (16) | 0.74 (16) | 0.98 (18) | 0.98 (18) | 0.97 (17) | 0.98 (18) |
| t_shape | 40 | 0.73 (16) | 0.73 (16) | 0.99 (18) | 0.99 (18) | 0.95 (16) | 0.96 (16) |
| t_shape | 60 | 0.78 (2) | 0.80 (2) | 0.96 (15) | 0.96 (15) | 0.94 (14) | 0.97 (16) |
| t_shape | 80 | 0.00 (0) | 0.72 (14) | 0.85 (3) | 0.85 (3) | 0.00 (0) | 0.00 (0) |
| beam | 20 | 0.53 (6) | 0.53 (6) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (13) |
| beam | 40 | 0.53 (6) | 0.53 (6) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (13) |
| beam | 60 | 0.52 (1) | 0.52 (1) | 0.52 (1) | 0.53 (6) | 0.00 (0) | 0.00 (0) |
| beam | 80 | 0.00 (0) | 0.52 (6) | 0.00 (0) | 0.52 (6) | 0.00 (0) | 0.00 (0) |
| l_shape | 20 | 0.74 (15) | 0.77 (14) | 0.96 (18) | 0.96 (18) | 0.92 (16) | 0.92 (17) |
| l_shape | 40 | 0.73 (14) | 0.77 (14) | 0.96 (18) | 0.96 (18) | 0.93 (17) | 0.92 (17) |
| l_shape | 60 | 0.75 (13) | 0.77 (15) | 0.93 (17) | 0.93 (17) | 0.93 (17) | 0.93 (18) |
| l_shape | 80 | 0.00 (0) | 0.77 (14) | 0.00 (0) | 0.83 (15) | 0.00 (0) | 0.00 (0) |
| asym | 20 | 0.78 (17) | 0.78 (17) | 0.99 (22) | 0.99 (22) | 0.97 (21) | 0.97 (21) |
| asym | 40 | 0.76 (4) | 0.76 (4) | 0.97 (21) | 0.97 (21) | 0.96 (20) | 0.97 (21) |
| asym | 60 | 0.73 (2) | 0.73 (11) | 0.94 (16) | 0.94 (16) | 0.95 (15) | 0.98 (18) |
| asym | 80 | 0.00 (1) | 0.68 (5) | 0.91 (1) | 0.91 (1) | 0.91 (1) | 0.94 (1) |
| u_channel | 20 | 0.69 (10) | 0.81 (13) | 1.00 (12) | 1.00 (12) | 0.99 (13) | 0.99 (13) |
| u_channel | 40 | 0.69 (8) | 0.80 (14) | 1.00 (12) | 1.00 (12) | 0.98 (12) | 1.00 (12) |
| u_channel | 60 | 0.68 (10) | 0.81 (13) | 1.00 (1) | 1.00 (1) | 1.00 (1) | 0.98 (5) |
| u_channel | 80 | 0.00 (0) | 0.75 (13) | 0.88 (3) | 0.88 (3) | 0.00 (0) | 0.00 (0) |
| plus | 20 | 0.52 (10) | 0.54 (11) | 1.00 (22) | 1.00 (22) | 1.00 (22) | 1.00 (22) |
| plus | 40 | 0.52 (10) | 0.54 (11) | 1.00 (21) | 1.00 (21) | 1.00 (20) | 1.00 (20) |
| plus | 60 | 0.54 (4) | 0.54 (4) | 0.54 (4) | 0.72 (8) | 0.00 (0) | 0.00 (0) |
| plus | 80 | 0.00 (0) | 0.51 (10) | 0.00 (0) | 0.51 (10) | 0.00 (0) | 0.00 (0) |

## 4. Does following the force split matter? (150 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 0.61 | 0.61 | 0.63 | 0.63 | 0 of 44 |
| move_x | 0.79 | 0.81 | 0.87 | 0.84 | 0 of 48 |
| move_y | 0.73 | 0.73 | 0.76 | 0.73 | 0 of 48 |
| move_turn | 0.98 | 0.77 | 0.91 | 0.86 | 9 of 44 |

## 5. Does the planner pick the best pair? (150 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 0.63 | 0.85 | 0.66 | 0.73 |
| move_x | 0.87 | 0.89 | 0.94 | 0.85 |
| move_y | 0.76 | 0.89 | 0.77 | 0.88 |
| move_turn | 0.91 | 0.97 | 0.84 | 0.98 |

## Planner push by object (150 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cube | 1.00 / 1.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.00 | 0.86 / 0.91 / 0.84 / 0.93 |
| long | 1.00 / 1.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.00 | 0.90 / 0.94 / 0.84 / 0.97 |
| sphere | - / - / - / - | 1.00 / 1.00 / 1.00 / 0.66 | 1.00 / 1.00 / 1.00 / 0.66 | - / - / - / - |
| cylinder | 1.00 / 1.00 / 0.00 / 0.00 | 0.99 / 0.99 / 1.00 / 0.99 | 0.56 / 0.57 / 0.22 / 0.14 | 0.90 / 0.90 / 0.90 / 0.91 |
| arch | 1.00 / 1.00 / 0.00 / 0.62 | 1.00 / 1.00 / 1.00 / 0.76 | 1.00 / 1.00 / 1.00 / 0.00 | 0.97 / 0.97 / 0.98 / 0.98 |
| dumbbell | 1.00 / 1.00 / 0.00 / 0.68 | 1.00 / 1.00 / 1.00 / 0.70 | 1.00 / 1.00 / 0.00 / 0.00 | 0.97 / 0.98 / 0.97 / 0.98 |
| t_shape | 0.97 / 0.95 / 0.94 / 0.00 | 1.00 / 1.00 / 1.00 / 0.00 | 0.83 / 0.83 / 0.95 / 0.87 | 0.91 / 0.93 / 0.98 / 0.93 |
| beam | 1.00 / 1.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.84 | 1.00 / 1.00 / 1.00 / 0.00 | 0.94 / 0.95 / 0.95 / 0.95 |
| l_shape | 0.92 / 0.93 / 0.93 / 0.00 | 0.93 / 0.95 / 0.99 / 0.79 | 0.81 / 0.81 / 0.96 / 0.80 | 0.91 / 0.96 / 0.96 / 1.00 |
| asym | 0.97 / 0.96 / 0.95 / 0.91 | 0.76 / 0.94 / 0.94 / 0.00 | 0.98 / 1.00 / 1.00 / 0.00 | 0.86 / 0.86 / 0.99 / 0.00 |
| u_channel | 0.99 / 0.98 / 1.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.62 | 0.96 / 0.99 / 1.00 / 0.77 | 0.94 / 0.96 / 0.94 / 0.93 |
| plus | 1.00 / 1.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 0.87 | 1.00 / 1.00 / 1.00 / 0.87 | 0.88 / 0.91 / 0.98 / 0.97 |

## 1. Is the planner's force model right? (250 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 |
| move_x | 0.92 (n=12) | 0.92 (n=12) | 1.00 (n=12) | 1.00 (n=12) | 0.96 |
| move_y | 0.92 (n=12) | 0.92 (n=12) | 0.83 (n=12) | 0.92 (n=12) | 0.90 |
| move_turn | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 |

**Verdict:** 0.96 of the workable planner pushes moved as asked (PASS: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 4, asym 2, l_shape 1

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| asym | 20 | move_x | 1 | 0.757 | 0.1353 | 9.15 | 0.078 | 0.104 | 3.524 |
| asym | 40 | move_x | 1 | 0.783 | 0.1379 | 9.1 | 0.079 | 0.104 | 2.283 |
| cylinder | 20 | move_y | 1 | 0.517 | 0.1461 | 0.07 | 0.575 | 0.12 | 3.998 |
| cylinder | 40 | move_y | 1 | 0.592 | 0.1494 | 0.15 | 0.595 | 0.12 | 2.626 |
| cylinder | 60 | move_y | 1 | 0.577 | 0.1411 | 0.1 | 0.555 | 0.12 | 1.75 |
| cylinder | 80 | move_y | 1 | 0.645 | 0.1523 | 1.14 | 0.567 | 0.12 | 1.313 |
| l_shape | 60 | move_y | 1 | 0.794 | 0.1471 | -0.11 | 0.052 | 0.108 | 1.699 |

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 54 N, 0.00 at limit | 109 N, 0.00 at limit | 164 N, 0.00 at limit | 220 N, 0.27 at limit |
| move_x | 49 N, 0.00 at limit | 97 N, 0.00 at limit | 146 N, 0.08 at limit | 181 N, 0.17 at limit |
| move_y | 53 N, 0.00 at limit | 106 N, 0.00 at limit | 159 N, 0.00 at limit | 210 N, 0.33 at limit |
| move_turn | 53 N, 0.00 at limit | 106 N, 0.00 at limit | 161 N, 0.09 at limit | 169 N, 0.00 at limit |

## 2. Does the planner judge weight right (one robot or both)? (250 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 28 | 13 | 1 | 4 | 0.89 |
| 40 kg | 27 | 13 | 2 | 4 | 0.87 |
| 60 kg | 7 | 27 | 0 | 12 | 0.74 |
| 80 kg | 2 | 29 | 0 | 15 | 0.67 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 11.33 | 19.39 | 18.83 |
| 40 kg | 0.00 | 11.74 | 19.60 | 18.22 |
| 60 kg | 0.00 | 10.87 | 19.23 | 19.67 |
| 80 kg | 0.00 | 10.84 | 14.08 | 14.70 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (250 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cube | 20 | 0.52 (19) | 0.52 (18) | 1.00 (36) | 1.00 (36) | 1.00 (36) | 1.00 (36) |
| cube | 40 | 0.52 (19) | 0.52 (18) | 1.00 (38) | 1.00 (38) | 1.00 (34) | 1.00 (34) |
| cube | 60 | 0.52 (17) | 0.50 (18) | 1.00 (38) | 1.00 (38) | 1.00 (38) | 1.00 (38) |
| cube | 80 | 0.49 (18) | 0.50 (17) | 1.00 (3) | 1.00 (3) | 1.00 (3) | 1.00 (3) |
| long | 20 | 0.53 (14) | 0.53 (14) | 1.00 (27) | 1.00 (27) | 1.00 (27) | 1.00 (27) |
| long | 40 | 0.52 (14) | 0.52 (14) | 1.00 (29) | 1.00 (29) | 1.00 (28) | 1.00 (28) |
| long | 60 | 0.53 (14) | 0.53 (14) | 1.00 (31) | 1.00 (31) | 1.00 (30) | 1.00 (31) |
| long | 80 | 0.51 (14) | 0.51 (14) | 1.00 (24) | 1.00 (24) | 1.00 (20) | 1.00 (20) |
| cylinder | 20 | 0.09 (2) | 0.10 (2) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.10 (2) | 0.12 (3) | 1.00 (24) | 1.00 (24) | 1.00 (21) | 1.00 (22) |
| cylinder | 60 | 0.10 (2) | 0.09 (2) | 1.00 (25) | 1.00 (25) | 1.00 (25) | 1.00 (25) |
| cylinder | 80 | 0.09 (2) | 0.10 (3) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| arch | 20 | 0.65 (7) | 0.68 (7) | 1.00 (12) | 1.00 (12) | 1.00 (11) | 1.00 (11) |
| arch | 40 | 0.64 (7) | 0.68 (8) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 60 | 0.64 (7) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 80 | 0.64 (7) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| dumbbell | 20 | 0.70 (7) | 0.73 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 40 | 0.69 (7) | 0.73 (7) | 1.00 (11) | 1.00 (11) | 1.00 (10) | 1.00 (10) |
| dumbbell | 60 | 0.70 (7) | 0.71 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 80 | 0.70 (7) | 0.71 (6) | 1.00 (9) | 1.00 (9) | 1.00 (8) | 1.00 (8) |
| t_shape | 20 | 0.74 (17) | 0.74 (17) | 0.99 (18) | 0.99 (18) | 0.97 (17) | 0.97 (17) |
| t_shape | 40 | 0.73 (17) | 0.73 (17) | 0.98 (18) | 0.98 (18) | 0.96 (17) | 0.98 (17) |
| t_shape | 60 | 0.74 (16) | 0.74 (16) | 0.99 (17) | 0.99 (17) | 0.96 (17) | 0.97 (17) |
| t_shape | 80 | 0.72 (15) | 0.72 (15) | 0.99 (17) | 0.99 (17) | 0.97 (16) | 0.96 (16) |
| beam | 20 | 0.53 (6) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (12) |
| beam | 40 | 0.53 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (12) | 1.00 (12) |
| beam | 60 | 0.53 (7) | 0.53 (6) | 1.00 (14) | 1.00 (14) | 1.00 (13) | 1.00 (13) |
| beam | 80 | 0.52 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (12) |
| l_shape | 20 | 0.76 (16) | 0.77 (15) | 0.96 (18) | 0.96 (18) | 0.91 (16) | 0.92 (16) |
| l_shape | 40 | 0.74 (16) | 0.75 (14) | 0.96 (19) | 0.96 (19) | 0.92 (16) | 0.93 (16) |
| l_shape | 60 | 0.73 (13) | 0.77 (14) | 0.98 (8) | 0.98 (8) | 0.92 (17) | 0.92 (17) |
| l_shape | 80 | 0.74 (13) | 0.77 (14) | 0.97 (1) | 0.97 (1) | 0.92 (17) | 0.94 (17) |
| asym | 20 | 0.79 (18) | 0.77 (17) | 0.99 (21) | 0.99 (21) | 0.96 (21) | 0.97 (21) |
| asym | 40 | 0.78 (18) | 0.78 (18) | 0.99 (20) | 0.99 (20) | 0.97 (21) | 0.95 (20) |
| asym | 60 | 0.78 (18) | 0.79 (18) | 0.99 (21) | 0.99 (21) | 0.95 (21) | 0.97 (21) |
| asym | 80 | 0.74 (15) | 0.75 (16) | 0.99 (19) | 0.99 (19) | 0.94 (19) | 0.98 (21) |
| u_channel | 20 | 0.70 (8) | 0.83 (13) | 1.00 (13) | 1.00 (13) | 0.97 (13) | 0.99 (13) |
| u_channel | 40 | 0.69 (11) | 0.83 (13) | 1.00 (12) | 1.00 (12) | 0.97 (12) | 0.99 (12) |
| u_channel | 60 | 0.70 (8) | 0.81 (14) | 1.00 (13) | 1.00 (13) | 0.99 (12) | 0.99 (12) |
| u_channel | 80 | 0.71 (11) | 0.80 (13) | 1.00 (12) | 1.00 (12) | 0.99 (11) | 0.98 (11) |
| plus | 20 | 0.51 (11) | 0.55 (11) | 1.00 (21) | 1.00 (21) | 1.00 (21) | 1.00 (21) |
| plus | 40 | 0.51 (11) | 0.55 (11) | 1.00 (20) | 1.00 (20) | 1.00 (19) | 1.00 (19) |
| plus | 60 | 0.51 (10) | 0.54 (12) | 1.00 (23) | 1.00 (23) | 1.00 (23) | 1.00 (23) |
| plus | 80 | 0.52 (11) | 0.54 (11) | 1.00 (22) | 1.00 (22) | 1.00 (21) | 1.00 (21) |

## 4. Does following the force split matter? (250 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 1.00 | 1.00 | 0.98 | 0.99 | 0 of 44 |
| move_x | 0.96 | 0.98 | 0.98 | 0.95 | 1 of 48 |
| move_y | 0.90 | 0.88 | 0.94 | 0.87 | 2 of 48 |
| move_turn | 1.00 | 0.66 | 0.92 | 0.84 | 15 of 44 |

## 5. Does the planner pick the best pair? (250 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 0.98 | 1.00 | 1.00 | 1.00 |
| move_x | 0.98 | 1.00 | 0.96 | 1.00 |
| move_y | 0.94 | 0.99 | 0.81 | 1.00 |
| move_turn | 0.92 | 0.98 | 0.77 | 1.00 |

## Planner push by object (250 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cube | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.97 / 0.99 | 0.99 / 0.99 / 0.97 / 0.99 | 0.86 / 0.89 / 0.90 / 0.82 |
| long | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 0.99 | 1.00 / 1.00 / 1.00 / 1.00 | 0.88 / 0.92 / 0.92 / 0.83 |
| sphere | - / - / - / - | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | - / - / - / - |
| cylinder | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 / 1.00 | 0.52 / 0.59 / 0.58 / 0.65 | 0.90 / 0.90 / 0.90 / 0.90 |
| arch | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.97 / 0.97 / 0.98 / 0.97 |
| dumbbell | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.96 / 0.97 / 0.97 / 0.97 |
| t_shape | 0.97 / 0.96 / 0.96 / 0.97 | 1.00 / 1.00 / 1.00 / 1.00 | 0.83 / 0.84 / 0.83 / 0.97 | 0.89 / 0.92 / 0.92 / 0.93 |
| beam | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.94 / 0.94 / 0.95 / 0.95 |
| l_shape | 0.91 / 0.92 / 0.92 / 0.92 | 0.96 / 0.95 / 0.94 / 0.95 | 0.83 / 0.82 / 0.79 / 0.94 | 0.88 / 0.93 / 0.94 / 0.96 |
| asym | 0.96 / 0.97 / 0.95 / 0.94 | 0.76 / 0.78 / 0.94 / 0.90 | 0.97 / 1.00 / 0.99 / 0.98 | 0.86 / 0.87 / 0.98 / 0.88 |
| u_channel | 0.97 / 0.97 / 0.99 / 0.99 | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.97 / 0.94 | 0.94 / 0.96 / 0.94 / 0.96 |
| plus | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.87 / 0.87 / 0.91 / 0.92 |

## 1. Is the planner's force model right? (350 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 |
| move_x | 0.92 (n=12) | 0.92 (n=12) | 0.92 (n=12) | 1.00 (n=12) | 0.94 |
| move_y | 0.92 (n=12) | 0.92 (n=12) | 0.92 (n=12) | 0.92 (n=12) | 0.92 |
| move_turn | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 |

**Verdict:** 0.96 of the workable planner pushes moved as asked (PASS: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 4, asym 3

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| asym | 20 | move_x | 1 | 0.745 | 0.1371 | 9.65 | 0.08 | 0.104 | 3.999 |
| asym | 40 | move_x | 1 | 0.751 | 0.1456 | 9.98 | 0.08 | 0.104 | 2.779 |
| asym | 60 | move_x | 1 | 0.769 | 0.1451 | 9.54 | 0.073 | 0.104 | 2.2 |
| cylinder | 20 | move_y | 1 | 0.495 | 0.1468 | 0.15 | 0.576 | 0.12 | 3.998 |
| cylinder | 40 | move_y | 1 | 0.535 | 0.1444 | 0.13 | 0.569 | 0.12 | 3.676 |
| cylinder | 60 | move_y | 1 | 0.601 | 0.1494 | 0.18 | 0.597 | 0.12 | 2.451 |
| cylinder | 80 | move_y | 1 | 0.574 | 0.1417 | 0.11 | 0.559 | 0.12 | 1.838 |

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 54 N, 0.00 at limit | 108 N, 0.00 at limit | 162 N, 0.00 at limit | 218 N, 0.00 at limit |
| move_x | 49 N, 0.00 at limit | 98 N, 0.00 at limit | 145 N, 0.00 at limit | 197 N, 0.08 at limit |
| move_y | 53 N, 0.00 at limit | 106 N, 0.00 at limit | 159 N, 0.00 at limit | 211 N, 0.00 at limit |
| move_turn | 53 N, 0.00 at limit | 105 N, 0.00 at limit | 160 N, 0.00 at limit | 216 N, 0.09 at limit |

## 2. Does the planner judge weight right (one robot or both)? (350 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 28 | 13 | 1 | 4 | 0.89 |
| 40 kg | 28 | 13 | 1 | 4 | 0.89 |
| 60 kg | 27 | 13 | 2 | 4 | 0.87 |
| 80 kg | 7 | 24 | 0 | 15 | 0.67 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 11.07 | 19.23 | 18.74 |
| 40 kg | 0.00 | 11.30 | 19.57 | 18.80 |
| 60 kg | 0.00 | 11.20 | 19.54 | 18.44 |
| 80 kg | 0.09 | 11.43 | 19.34 | 19.25 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (350 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cube | 20 | 0.54 (18) | 0.53 (19) | 1.00 (36) | 1.00 (36) | 1.00 (35) | 1.00 (35) |
| cube | 40 | 0.52 (18) | 0.53 (19) | 1.00 (37) | 1.00 (37) | 1.00 (35) | 1.00 (35) |
| cube | 60 | 0.52 (18) | 0.52 (19) | 1.00 (36) | 1.00 (36) | 1.00 (35) | 1.00 (35) |
| cube | 80 | 0.53 (18) | 0.50 (17) | 1.00 (37) | 1.00 (37) | 1.00 (37) | 1.00 (37) |
| long | 20 | 0.53 (14) | 0.53 (14) | 1.00 (27) | 1.00 (27) | 1.00 (27) | 1.00 (27) |
| long | 40 | 0.52 (13) | 0.52 (13) | 1.00 (28) | 1.00 (28) | 1.00 (28) | 1.00 (27) |
| long | 60 | 0.51 (14) | 0.51 (14) | 1.00 (29) | 1.00 (29) | 1.00 (27) | 1.00 (27) |
| long | 80 | 0.51 (14) | 0.52 (14) | 1.00 (28) | 1.00 (28) | 1.00 (28) | 1.00 (28) |
| cylinder | 20 | 0.10 (2) | 0.11 (2) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.10 (2) | 0.11 (2) | 1.00 (23) | 1.00 (23) | 1.00 (22) | 1.00 (22) |
| cylinder | 60 | 0.10 (3) | 0.12 (2) | 1.00 (24) | 1.00 (24) | 1.00 (22) | 1.00 (22) |
| cylinder | 80 | 0.11 (2) | 0.09 (2) | 1.00 (24) | 1.00 (24) | 1.00 (24) | 1.00 (24) |
| arch | 20 | 0.65 (7) | 0.69 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 40 | 0.65 (7) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 60 | 0.64 (7) | 0.68 (7) | 1.00 (12) | 1.00 (12) | 1.00 (12) | 1.00 (11) |
| arch | 80 | 0.65 (8) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| dumbbell | 20 | 0.70 (7) | 0.72 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 40 | 0.69 (7) | 0.71 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 60 | 0.69 (7) | 0.70 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (10) |
| dumbbell | 80 | 0.69 (7) | 0.71 (6) | 1.00 (11) | 1.00 (11) | 1.00 (10) | 1.00 (10) |
| t_shape | 20 | 0.75 (17) | 0.75 (17) | 0.98 (16) | 0.98 (16) | 0.96 (16) | 0.97 (17) |
| t_shape | 40 | 0.76 (17) | 0.75 (16) | 0.99 (18) | 0.99 (18) | 0.97 (17) | 0.98 (17) |
| t_shape | 60 | 0.73 (17) | 0.73 (17) | 0.99 (18) | 0.99 (18) | 0.96 (16) | 0.98 (17) |
| t_shape | 80 | 0.73 (16) | 0.73 (17) | 0.99 (18) | 0.99 (18) | 0.98 (16) | 0.96 (16) |
| beam | 20 | 0.53 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (12) | 1.00 (12) |
| beam | 40 | 0.53 (7) | 0.53 (7) | 1.00 (14) | 1.00 (14) | 1.00 (12) | 1.00 (12) |
| beam | 60 | 0.53 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (13) |
| beam | 80 | 0.53 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (13) |
| l_shape | 20 | 0.75 (15) | 0.77 (14) | 0.97 (19) | 0.97 (19) | 0.91 (16) | 0.92 (16) |
| l_shape | 40 | 0.76 (15) | 0.77 (13) | 0.96 (18) | 0.96 (18) | 0.92 (16) | 0.92 (16) |
| l_shape | 60 | 0.75 (12) | 0.77 (15) | 0.96 (19) | 0.96 (19) | 0.92 (16) | 0.92 (16) |
| l_shape | 80 | 0.73 (16) | 0.75 (14) | 0.96 (18) | 0.96 (18) | 0.92 (16) | 0.93 (17) |
| asym | 20 | 0.77 (18) | 0.77 (18) | 0.99 (22) | 0.99 (22) | 0.97 (21) | 0.98 (21) |
| asym | 40 | 0.79 (18) | 0.79 (18) | 0.99 (21) | 0.99 (21) | 0.97 (22) | 0.97 (22) |
| asym | 60 | 0.79 (18) | 0.79 (18) | 1.00 (20) | 1.00 (20) | 0.93 (19) | 0.97 (20) |
| asym | 80 | 0.80 (18) | 0.80 (18) | 0.99 (18) | 0.99 (18) | 0.96 (21) | 0.97 (21) |
| u_channel | 20 | 0.70 (8) | 0.83 (13) | 1.00 (13) | 1.00 (13) | 0.98 (13) | 0.99 (13) |
| u_channel | 40 | 0.68 (10) | 0.83 (13) | 1.00 (13) | 1.00 (13) | 0.98 (13) | 0.99 (14) |
| u_channel | 60 | 0.69 (10) | 0.82 (13) | 1.00 (13) | 1.00 (13) | 0.99 (12) | 0.98 (12) |
| u_channel | 80 | 0.69 (10) | 0.83 (14) | 1.00 (12) | 1.00 (12) | 0.99 (13) | 0.99 (12) |
| plus | 20 | 0.52 (10) | 0.55 (11) | 1.00 (22) | 1.00 (22) | 1.00 (21) | 1.00 (21) |
| plus | 40 | 0.52 (11) | 0.55 (11) | 1.00 (21) | 1.00 (21) | 1.00 (21) | 1.00 (21) |
| plus | 60 | 0.51 (11) | 0.55 (11) | 1.00 (22) | 1.00 (22) | 1.00 (21) | 1.00 (21) |
| plus | 80 | 0.51 (10) | 0.54 (12) | 1.00 (23) | 1.00 (23) | 1.00 (22) | 1.00 (22) |

## 4. Does following the force split matter? (350 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 1.00 | 1.00 | 0.98 | 0.99 | 0 of 44 |
| move_x | 0.94 | 1.00 | 0.98 | 0.95 | 0 of 48 |
| move_y | 0.92 | 0.92 | 0.93 | 0.87 | 0 of 48 |
| move_turn | 1.00 | 0.59 | 0.92 | 0.82 | 18 of 44 |

## 5. Does the planner pick the best pair? (350 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 0.98 | 0.99 | 1.00 | 1.00 |
| move_x | 0.98 | 1.00 | 0.94 | 1.00 |
| move_y | 0.93 | 0.99 | 0.75 | 1.00 |
| move_turn | 0.92 | 0.97 | 0.77 | 1.00 |

## Planner push by object (350 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cube | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 0.99 / 0.99 | 1.00 / 1.00 / 0.99 / 0.99 | 0.84 / 0.83 / 0.88 / 0.90 |
| long | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.87 / 0.88 / 0.92 / 0.92 |
| sphere | - / - / - / - | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | - / - / - / - |
| cylinder | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 1.00 / 0.99 | 0.49 / 0.54 / 0.60 / 0.57 | 0.90 / 0.90 / 0.90 / 0.90 |
| arch | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.96 / 0.97 / 0.97 / 0.98 |
| dumbbell | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.96 / 0.97 / 0.97 / 0.97 |
| t_shape | 0.96 / 0.97 / 0.96 / 0.98 | 1.00 / 1.00 / 1.00 / 1.00 | 0.84 / 0.84 / 0.85 / 0.83 | 0.89 / 0.90 / 0.92 / 0.91 |
| beam | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.94 / 0.94 / 0.94 / 0.94 |
| l_shape | 0.91 / 0.92 / 0.92 / 0.92 | 0.94 / 0.94 / 0.94 / 0.94 | 0.81 / 0.82 / 0.82 / 0.80 | 0.90 / 0.92 / 0.93 / 0.95 |
| asym | 0.97 / 0.97 / 0.93 / 0.96 | 0.74 / 0.75 / 0.77 / 0.91 | 0.97 / 0.99 / 0.99 / 0.96 | 0.86 / 0.86 / 0.87 / 0.97 |
| u_channel | 0.98 / 0.98 / 0.99 / 0.99 | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.98 / 0.98 | 0.94 / 0.94 / 0.95 / 0.95 |
| plus | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.84 / 0.86 / 0.90 / 0.89 |

