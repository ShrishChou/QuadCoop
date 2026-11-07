# Planner physics test (test 1): pp-test

No robots, no learning: the planner's pushes applied as forces at the contact points, held 4 s (measured over the last 3.5 s). Motion = (dx, dy, r_g x dyaw); moved = 2 cm or more; 'as asked' = cosine with the wanted motion >= 0.8. Robot push (normal force): 250 N. Objects at nominal size.

Control (no push, every object and mass): largest motion 0.0 cm (cube, 20 kg) - OK (must stay under 1 cm).

## 1. Is the planner's force model right?
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=11) | 1.00 (n=11) | 0.91 (n=11) | 0.91 (n=11) | 0.95 |
| move_x | 0.92 (n=12) | 0.92 (n=12) | 1.00 (n=12) | 1.00 (n=12) | 0.96 |
| move_y | 1.00 (n=12) | 1.00 (n=12) | 1.00 (n=12) | 1.00 (n=12) | 1.00 |
| move_turn | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 (n=11) | 1.00 |

**Verdict:** 0.98 of the workable planner pushes moved as asked (PASS: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: asym 2, cube 2

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| asym | 20 | move_x | 1 | 0.755 | 0.1377 | 9.42 | 0.086 | 0.143 | 2.951 |
| asym | 40 | move_x | 1 | 0.794 | 0.137 | 9.44 | 0.073 | 0.143 | 1.883 |
| cube | 60 | turn | 0 |  | 0.0 | 1.46 | 0.0 | 0.178 | 1.579 |
| cube | 80 | turn | 0 |  | 0.0 | 0.14 | 0.0 | 0.178 | 1.184 |

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 56 N, 0.00 at limit | 112 N, 0.00 at limit | 167 N, 0.09 at limit | 216 N, 0.27 at limit |
| move_x | 50 N, 0.00 at limit | 101 N, 0.00 at limit | 148 N, 0.08 at limit | 182 N, 0.17 at limit |
| move_y | 54 N, 0.00 at limit | 108 N, 0.00 at limit | 165 N, 0.00 at limit | 208 N, 0.25 at limit |
| move_turn | 53 N, 0.00 at limit | 107 N, 0.00 at limit | 159 N, 0.00 at limit | 176 N, 0.09 at limit |

## 2. Does the planner judge weight right (one robot or both)?
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 27 | 13 | 2 | 4 | 0.87 |
| 40 kg | 26 | 13 | 3 | 4 | 0.85 |
| 60 kg | 6 | 27 | 0 | 13 | 0.72 |
| 80 kg | 2 | 29 | 0 | 15 | 0.67 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 10.19 | 19.30 | 18.73 |
| 40 kg | 0.00 | 10.35 | 19.55 | 18.68 |
| 60 kg | 0.00 | 9.62 | 17.60 | 16.35 |
| 80 kg | 0.00 | 8.68 | 16.30 | 14.43 |

## 3. Turning: one robot, two on one side, or two on opposite sides?
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cube | 20 | 0.28 (10) | - | 1.00 (36) | 1.00 (36) | 1.00 (36) | 1.00 (36) |
| cube | 40 | 0.23 (8) | - | 1.00 (38) | 1.00 (38) | 1.00 (38) | 1.00 (38) |
| cube | 60 | 0.22 (7) | - | 0.61 (20) | 0.61 (20) | 0.00 (1) | 0.00 (1) |
| cube | 80 | 0.35 (1) | - | 0.48 (2) | 0.50 (17) | 0.00 (0) | 0.00 (0) |
| long | 20 | 0.53 (14) | 0.53 (14) | 1.00 (27) | 1.00 (27) | 1.00 (27) | 1.00 (27) |
| long | 40 | 0.52 (14) | 0.52 (14) | 1.00 (29) | 1.00 (29) | 1.00 (28) | 1.00 (28) |
| long | 60 | 0.53 (14) | 0.53 (14) | 1.00 (31) | 1.00 (31) | 1.00 (30) | 1.00 (30) |
| long | 80 | 0.51 (14) | 0.51 (14) | 1.00 (24) | 1.00 (24) | 1.00 (20) | 1.00 (24) |
| cylinder | 20 | 0.08 (2) | 0.07 (1) | 1.00 (23) | 1.00 (23) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.09 (2) | 0.07 (2) | 1.00 (24) | 1.00 (24) | 1.00 (21) | 1.00 (21) |
| cylinder | 60 | 0.08 (2) | 0.07 (2) | 1.00 (25) | 1.00 (25) | 1.00 (25) | 1.00 (25) |
| cylinder | 80 | 0.08 (2) | 0.08 (2) | 1.00 (23) | 1.00 (23) | 1.00 (23) | 1.00 (23) |
| arch | 20 | 0.66 (7) | 0.68 (7) | 1.00 (12) | 1.00 (12) | 1.00 (11) | 1.00 (11) |
| arch | 40 | 0.64 (7) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 60 | 0.64 (7) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| arch | 80 | 0.64 (7) | 0.68 (7) | 1.00 (11) | 1.00 (11) | 1.00 (11) | 1.00 (11) |
| dumbbell | 20 | 0.70 (7) | 0.71 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 40 | 0.69 (7) | 0.73 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 60 | 0.70 (7) | 0.71 (7) | 1.00 (10) | 1.00 (10) | 1.00 (10) | 1.00 (10) |
| dumbbell | 80 | 0.70 (7) | 0.71 (6) | 1.00 (9) | 1.00 (9) | 1.00 (8) | 1.00 (8) |
| t_shape | 20 | 0.74 (17) | 0.74 (17) | 0.99 (18) | 0.99 (18) | 0.97 (17) | 0.98 (17) |
| t_shape | 40 | 0.72 (17) | 0.73 (17) | 0.98 (18) | 0.98 (18) | 0.98 (17) | 0.98 (17) |
| t_shape | 60 | 0.74 (16) | 0.74 (16) | 0.99 (17) | 0.99 (17) | 0.96 (17) | 0.98 (16) |
| t_shape | 80 | 0.72 (15) | 0.72 (15) | 0.99 (17) | 0.99 (17) | 0.98 (16) | 0.99 (16) |
| beam | 20 | 0.53 (6) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (13) |
| beam | 40 | 0.53 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (12) | 1.00 (13) |
| beam | 60 | 0.53 (7) | 0.53 (6) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (13) |
| beam | 80 | 0.52 (7) | 0.53 (7) | 1.00 (13) | 1.00 (13) | 1.00 (13) | 1.00 (12) |
| l_shape | 20 | 0.76 (16) | 0.77 (15) | 0.96 (18) | 0.96 (18) | 0.91 (16) | 0.92 (16) |
| l_shape | 40 | 0.74 (16) | 0.75 (15) | 0.96 (19) | 0.96 (19) | 0.92 (16) | 0.92 (16) |
| l_shape | 60 | 0.73 (13) | 0.74 (15) | 0.98 (8) | 0.98 (8) | 0.92 (17) | 0.92 (17) |
| l_shape | 80 | 0.73 (13) | 0.73 (13) | 0.97 (13) | 0.97 (13) | 0.92 (17) | 0.94 (17) |
| asym | 20 | 0.71 (16) | 0.70 (15) | 0.99 (21) | 0.99 (21) | 0.97 (20) | 0.97 (21) |
| asym | 40 | 0.70 (16) | 0.70 (16) | 0.98 (21) | 0.98 (21) | 0.96 (20) | 0.98 (21) |
| asym | 60 | 0.72 (14) | 0.72 (14) | 0.96 (21) | 0.96 (21) | 0.96 (21) | 0.97 (21) |
| asym | 80 | 0.74 (10) | 0.74 (10) | 0.95 (19) | 0.95 (19) | 0.95 (19) | 0.96 (19) |
| u_channel | 20 | 0.70 (8) | 0.83 (13) | 1.00 (13) | 1.00 (13) | 0.97 (13) | 0.99 (13) |
| u_channel | 40 | 0.69 (11) | 0.83 (13) | 1.00 (12) | 1.00 (12) | 0.97 (12) | 0.99 (12) |
| u_channel | 60 | 0.70 (8) | 0.82 (13) | 1.00 (13) | 1.00 (13) | 0.99 (12) | 0.99 (12) |
| u_channel | 80 | 0.71 (11) | 0.80 (13) | 1.00 (12) | 1.00 (12) | 0.99 (11) | 0.98 (11) |
| plus | 20 | 0.47 (9) | 0.47 (9) | 1.00 (21) | 1.00 (21) | 1.00 (21) | 1.00 (21) |
| plus | 40 | 0.48 (10) | 0.49 (10) | 1.00 (20) | 1.00 (20) | 1.00 (20) | 1.00 (20) |
| plus | 60 | 0.51 (10) | 0.51 (10) | 1.00 (23) | 1.00 (23) | 1.00 (23) | 1.00 (23) |
| plus | 80 | 0.49 (9) | 0.49 (9) | 1.00 (22) | 1.00 (22) | 1.00 (22) | 1.00 (22) |

## 4. Does following the force split matter?
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 0.95 | 0.95 | 0.94 | 0.94 | 0 of 44 |
| move_x | 0.96 | 1.00 | 0.98 | 0.96 | 0 of 48 |
| move_y | 1.00 | 0.92 | 0.97 | 0.95 | 4 of 48 |
| move_turn | 1.00 | 0.68 | 0.92 | 0.85 | 14 of 44 |

## 5. Does the planner pick the best pair?
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 0.94 | 0.97 | 0.95 | 0.95 |
| move_x | 0.98 | 0.99 | 0.98 | 1.00 |
| move_y | 0.97 | 0.99 | 0.92 | 1.00 |
| move_turn | 0.92 | 0.97 | 0.82 | 1.00 |

## Planner push by object
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cube | 1.00 / 1.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.81 / 0.85 / 0.86 / 0.87 |
| long | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 0.99 | 1.00 / 1.00 / 1.00 / 1.00 | 0.88 / 0.91 / 0.92 / 0.83 |
| sphere | - / - / - / - | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | - / - / - / - |
| cylinder | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.90 / 0.90 / 0.90 / 0.90 |
| arch | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.97 / 0.97 / 0.98 / 0.97 |
| dumbbell | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.96 / 0.97 / 0.97 / 0.98 |
| t_shape | 0.97 / 0.98 / 0.96 / 0.98 | 1.00 / 1.00 / 1.00 / 1.00 | 0.82 / 0.84 / 0.83 / 0.97 | 0.89 / 0.92 / 0.92 / 0.93 |
| beam | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.94 / 0.94 / 0.95 / 0.95 |
| l_shape | 0.91 / 0.92 / 0.92 / 0.92 | 0.96 / 0.95 / 0.94 / 0.95 | 0.84 / 0.81 / 0.81 / 0.83 | 0.88 / 0.93 / 0.94 / 0.96 |
| asym | 0.97 / 0.96 / 0.96 / 0.95 | 0.76 / 0.79 / 0.95 / 0.93 | 1.00 / 1.00 / 1.00 / 1.00 | 0.83 / 0.85 / 0.94 / 1.00 |
| u_channel | 0.97 / 0.97 / 0.99 / 0.99 | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 0.99 / 0.99 / 0.94 | 0.94 / 0.96 / 0.94 / 0.96 |
| plus | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.83 / 0.87 / 0.89 / 0.90 |

