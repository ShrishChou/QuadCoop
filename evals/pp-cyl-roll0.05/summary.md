# Planner physics test (test 1): pp-cyl-roll0.05

No robots, no learning: the planner's pushes applied as forces at the contact points, held 4 s (measured over the last 3.5 s). Motion = (dx, dy, r_g x dyaw); moved = 2 cm or more; 'as asked' = cosine with the wanted motion >= 0.8. Robot push (normal force): 150, 250 N. Objects at nominal size.

Control (no push, every object and mass): largest motion 0.0 cm (cylinder, 20 kg) - OK (must stay under 1 cm).

## 1. Is the planner's force model right? (150 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=1) | 1.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.50 |
| move_x | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |
| move_y | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | - | 1.00 |
| move_turn | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.00 |

**Verdict:** 0.60 of the workable planner pushes moved as asked (FAIL: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 6

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| cylinder | 20 | move_turn | 1 | 0.692 | 0.0832 | 17.19 | 0.248 | 0.056 | 3.999 |
| cylinder | 40 | move_turn | 1 | 0.724 | 0.09 | 18.13 | 0.179 | 0.056 | 2.698 |
| cylinder | 60 | move_turn | 0 |  | 0.0028 | 0.94 | 0.014 | 0.056 | 1.801 |
| cylinder | 60 | turn | 0 |  | 0.0 | 0.55 | 0.0 | 0.057 | 1.802 |
| cylinder | 80 | move_turn | 0 |  | 0.0008 | 0.38 | 0.002 | 0.056 | 1.352 |
| cylinder | 80 | turn | 0 |  | 0.0 | 0.39 | 0.0 | 0.057 | 1.352 |

Planner pushes the model rates too weak to slide the object (strength < 1): 1; moved as asked anyway: 0; moved at all: 1.

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 48 N, 0.00 at limit | 95 N, 0.00 at limit | 150 N, 1.00 at limit | 150 N, 1.00 at limit |
| move_x | 9 N, 0.00 at limit | 20 N, 0.00 at limit | 29 N, 0.00 at limit | 40 N, 0.00 at limit |
| move_y | 58 N, 0.00 at limit | 115 N, 0.00 at limit | 138 N, 0.00 at limit | 123 N, 0.00 at limit |
| move_turn | 44 N, 0.00 at limit | 89 N, 0.00 at limit | 150 N, 1.00 at limit | 150 N, 1.00 at limit |

## 2. Does the planner judge weight right (one robot or both)? (150 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 2 | 1 | 0 | 1 | 0.75 |
| 40 kg | 1 | 2 | 0 | 1 | 0.75 |
| 60 kg | 1 | 2 | 0 | 1 | 0.75 |
| 80 kg | 1 | 2 | 0 | 1 | 0.75 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 5.28 | 24.27 | 23.45 |
| 40 kg | 0.00 | 4.47 | 23.25 | 23.54 |
| 60 kg | 0.00 | 2.24 | 10.59 | 0.55 |
| 80 kg | 0.00 | 2.05 | 2.05 | 0.39 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (150 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cylinder | 20 | 0.23 (5) | 0.22 (5) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.41 (4) | 0.41 (4) | 1.00 (23) | 1.00 (23) | 1.00 (24) | 1.00 (24) |
| cylinder | 60 | 0.09 (2) | 0.23 (5) | 0.09 (2) | 0.56 (11) | 0.00 (1) | 0.00 (1) |
| cylinder | 80 | 0.09 (2) | 0.05 (1) | 0.09 (2) | 0.09 (2) | 0.00 (0) | 0.00 (0) |

## 4. Does following the force split matter? (150 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 0.50 | 0.50 | 0.50 | 0.50 | 0 of 4 |
| move_x | 1.00 | 1.00 | 1.00 | 1.00 | 0 of 4 |
| move_y | 0.75 | 0.25 | 0.78 | 0.36 | 2 of 4 |
| move_turn | 0.00 | 0.00 | 0.35 | 0.22 | 0 of 4 |

## 5. Does the planner pick the best pair? (150 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 0.50 | 0.66 | 0.75 | 0.50 |
| move_x | 1.00 | 1.00 | 1.00 | 1.00 |
| move_y | 0.78 | 0.79 | 1.00 | 0.75 |
| move_turn | 0.35 | 0.94 | 0.00 | 1.00 |

## Planner push by object (150 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cylinder | 1.00 / 1.00 / 0.00 / 0.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.98 / 0.98 / 1.00 / 0.15 | 0.69 / 0.72 / 0.00 / 0.00 |

## 1. Is the planner's force model right? (250 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |
| move_x | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |
| move_y | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |
| move_turn | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.00 |

**Verdict:** 0.75 of the workable planner pushes moved as asked (FAIL: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 4

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| cylinder | 20 | move_turn | 1 | 0.701 | 0.0949 | 15.57 | 0.27 | 0.056 | 3.999 |
| cylinder | 40 | move_turn | 1 | 0.721 | 0.0897 | 15.11 | 0.239 | 0.056 | 3.999 |
| cylinder | 60 | move_turn | 1 | 0.702 | 0.0819 | 18.69 | 0.208 | 0.056 | 2.997 |
| cylinder | 80 | move_turn | 1 | 0.761 | 0.0962 | 16.51 | 0.139 | 0.056 | 2.25 |

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 48 N, 0.00 at limit | 94 N, 0.00 at limit | 144 N, 0.00 at limit | 188 N, 0.00 at limit |
| move_x | 10 N, 0.00 at limit | 19 N, 0.00 at limit | 27 N, 0.00 at limit | 38 N, 0.00 at limit |
| move_y | 59 N, 0.00 at limit | 118 N, 0.00 at limit | 175 N, 0.00 at limit | 246 N, 0.00 at limit |
| move_turn | 44 N, 0.00 at limit | 87 N, 0.00 at limit | 133 N, 0.00 at limit | 178 N, 0.00 at limit |

## 2. Does the planner judge weight right (one robot or both)? (250 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 2 | 1 | 0 | 1 | 0.75 |
| 40 kg | 2 | 1 | 0 | 1 | 0.75 |
| 60 kg | 1 | 1 | 0 | 2 | 0.50 |
| 80 kg | 1 | 2 | 0 | 1 | 0.75 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 3.67 | 24.03 | 22.95 |
| 40 kg | 0.00 | 4.67 | 24.26 | 22.01 |
| 60 kg | 0.00 | 6.72 | 25.04 | 25.04 |
| 80 kg | 0.00 | 1.74 | 23.80 | 22.58 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (250 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cylinder | 20 | 0.17 (4) | 0.18 (4) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.23 (5) | 0.23 (5) | 1.00 (24) | 1.00 (24) | 1.00 (22) | 1.00 (21) |
| cylinder | 60 | 0.31 (7) | 0.31 (7) | 1.00 (25) | 1.00 (25) | 1.00 (25) | 1.00 (25) |
| cylinder | 80 | 0.08 (2) | 0.13 (3) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |

## 4. Does following the force split matter? (250 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 1.00 | 1.00 | 1.00 | 1.00 | 0 of 4 |
| move_x | 1.00 | 1.00 | 1.00 | 1.00 | 0 of 4 |
| move_y | 1.00 | 0.00 | 0.98 | 0.18 | 4 of 4 |
| move_turn | 0.00 | 0.00 | 0.72 | 0.45 | 0 of 4 |

## 5. Does the planner pick the best pair? (250 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 1.00 | 1.00 | 1.00 | 1.00 |
| move_x | 1.00 | 1.00 | 1.00 | 1.00 |
| move_y | 0.98 | 1.00 | 1.00 | 1.00 |
| move_turn | 0.72 | 0.96 | 0.00 | 1.00 |

## Planner push by object (250 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cylinder | 1.00 / 1.00 / 1.00 / 1.00 | 1.00 / 1.00 / 1.00 / 1.00 | 0.98 / 0.98 / 0.98 / 0.98 | 0.70 / 0.72 / 0.70 / 0.76 |

