# Planner physics test (test 1): pp-cyl-roll0

No robots, no learning: the planner's pushes applied as forces at the contact points, held 4 s (measured over the last 3.5 s). Motion = (dx, dy, r_g x dyaw); moved = 2 cm or more; 'as asked' = cosine with the wanted motion >= 0.8. Robot push (normal force): 150, 250 N. Objects at nominal size.

Control (no push, every object and mass): largest motion 0.0 cm (cylinder, 20 kg) - OK (must stay under 1 cm).

## 1. Is the planner's force model right? (150 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=1) | 1.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.50 |
| move_x | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | - | 1.00 |
| move_y | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | - | 0.00 |
| move_turn | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | - | 1.00 |

**Verdict:** 0.62 of the workable planner pushes moved as asked (FAIL: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 5

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| cylinder | 20 | move_y | 1 | 0.558 | 0.1454 | 0.19 | 0.577 | 0.12 | 3.151 |
| cylinder | 40 | move_y | 1 | 0.573 | 0.1469 | 0.32 | 0.574 | 0.12 | 1.575 |
| cylinder | 60 | move_y | 1 | 0.224 | 0.1535 | -0.03 | 0.417 | 0.12 | 1.05 |
| cylinder | 60 | turn | 0 |  | 0.0 | 0.55 | 0.0 | 0.057 | 1.802 |
| cylinder | 80 | turn | 0 |  | 0.0 | 0.39 | 0.0 | 0.057 | 1.352 |

Planner pushes the model rates too weak to slide the object (strength < 1): 3; moved as asked anyway: 2; moved at all: 3.

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 48 N, 0.00 at limit | 95 N, 0.00 at limit | 150 N, 1.00 at limit | 150 N, 1.00 at limit |
| move_x | 11 N, 0.00 at limit | 22 N, 0.00 at limit | 25 N, 0.00 at limit | 50 N, 0.00 at limit |
| move_y | 51 N, 0.00 at limit | 100 N, 0.00 at limit | 109 N, 0.00 at limit | 59 N, 0.00 at limit |
| move_turn | 12 N, 0.00 at limit | 25 N, 0.00 at limit | 24 N, 0.00 at limit | 40 N, 0.00 at limit |

## 2. Does the planner judge weight right (one robot or both)? (150 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 1 | 1 | 0 | 2 | 0.50 |
| 40 kg | 0 | 2 | 0 | 2 | 0.50 |
| 60 kg | 0 | 2 | 0 | 2 | 0.50 |
| 80 kg | 0 | 2 | 0 | 2 | 0.50 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 2.26 | 24.27 | 23.45 |
| 40 kg | 0.00 | 1.80 | 23.25 | 23.54 |
| 60 kg | 0.00 | 2.63 | 3.51 | 0.55 |
| 80 kg | 0.00 | 2.68 | 3.37 | 0.39 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (150 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cylinder | 20 | 0.10 (2) | 0.11 (3) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.10 (2) | 0.09 (2) | 1.00 (23) | 1.00 (23) | 1.00 (24) | 1.00 (24) |
| cylinder | 60 | 0.11 (3) | 0.09 (2) | 0.15 (4) | 0.15 (4) | 0.00 (1) | 0.00 (1) |
| cylinder | 80 | 0.11 (3) | 0.09 (2) | 0.15 (3) | 0.15 (3) | 0.00 (0) | 0.00 (0) |

## 4. Does following the force split matter? (150 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 0.50 | 0.50 | 0.50 | 0.50 | 0 of 4 |
| move_x | 1.00 | 1.00 | 0.99 | 1.00 | 0 of 4 |
| move_y | 0.00 | 0.00 | 0.37 | 0.18 | 0 of 4 |
| move_turn | 1.00 | 1.00 | 0.90 | 0.90 | 0 of 4 |

## 5. Does the planner pick the best pair? (150 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 0.50 | 0.57 | 0.50 | 0.50 |
| move_x | 0.99 | 1.00 | 1.00 | 1.00 |
| move_y | 0.37 | 0.81 | 0.25 | 0.75 |
| move_turn | 0.90 | 0.91 | 1.00 | 1.00 |

## Planner push by object (150 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cylinder | 1.00 / 1.00 / 0.00 / 0.00 | 0.99 / 0.99 / 1.00 / 0.99 | 0.56 / 0.57 / 0.22 / 0.14 | 0.90 / 0.90 / 0.90 / 0.91 |

## 1. Is the planner's force model right? (250 N)
Planner pushes the model rates workable (strength >= 1: strong enough to slide it; residual <= 0.3: the pushes make the wanted motion). Share that moved as asked, by motion and mass; then the cases the model gets wrong.

| motion | 20 kg | 40 kg | 60 kg | 80 kg | all |
|---|---|---|---|---|---|
| turn | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |
| move_x | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |
| move_y | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.00 (n=1) | 0.00 |
| move_turn | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 (n=1) | 1.00 |

**Verdict:** 0.75 of the workable planner pushes moved as asked (FAIL: 0.90 needed).

Model wrong (predicted workable, did not move as asked), by object: cylinder 4

| object | mass | motion | moved | cos | speed (m/s) | yaw rate (deg/s) | tilt (rad/s) | residual | strength |
|---|---|---|---|---|---|---|---|---|---|
| cylinder | 20 | move_y | 1 | 0.517 | 0.1461 | 0.07 | 0.575 | 0.12 | 3.998 |
| cylinder | 40 | move_y | 1 | 0.592 | 0.1494 | 0.15 | 0.595 | 0.12 | 2.626 |
| cylinder | 60 | move_y | 1 | 0.577 | 0.1411 | 0.1 | 0.555 | 0.12 | 1.75 |
| cylinder | 80 | move_y | 1 | 0.645 | 0.1523 | 1.14 | 0.567 | 0.12 | 1.313 |

How hard the planner's pushes pressed (hardest robot's normal force, N, mean over objects) and the share of objects where they ended at the limit without reaching the target speed.

| motion | 20 kg | 40 kg | 60 kg | 80 kg |
|---|---|---|---|---|
| turn | 48 N, 0.00 at limit | 94 N, 0.00 at limit | 144 N, 0.00 at limit | 188 N, 0.00 at limit |
| move_x | 10 N, 0.00 at limit | 20 N, 0.00 at limit | 33 N, 0.00 at limit | 42 N, 0.00 at limit |
| move_y | 52 N, 0.00 at limit | 104 N, 0.00 at limit | 153 N, 0.00 at limit | 209 N, 0.00 at limit |
| move_turn | 13 N, 0.00 at limit | 23 N, 0.00 at limit | 38 N, 0.00 at limit | 34 N, 0.00 at limit |

## 2. Does the planner judge weight right (one robot or both)? (250 N)
Per object x mass x motion: the model says one robot can (some single contact has strength >= 1 and residual <= 0.3) or cannot; the sim says one can (some single contact moved it as asked) or cannot. Counts: agree (one can / one cannot) and disagree (model says one can, it cannot / model says it cannot, it can).

| mass | agree: one can | agree: one cannot | model too optimistic | model too cautious | agreement |
|---|---|---|---|---|---|
| 20 kg | 1 | 1 | 0 | 2 | 0.50 |
| 40 kg | 1 | 1 | 0 | 2 | 0.50 |
| 60 kg | 0 | 2 | 0 | 2 | 0.50 |
| 80 kg | 0 | 2 | 0 | 2 | 0.50 |

Turning with one robot, by mass (best single contact, motion turn): share of objects it turns as asked, and the mean yaw rate (deg/s) of the best single, against the best pair.

| mass | one robot turns it | best single yaw rate | best pair yaw rate | planner yaw rate |
|---|---|---|---|---|
| 20 kg | 0.00 | 2.02 | 24.12 | 22.95 |
| 40 kg | 0.00 | 2.42 | 24.46 | 21.76 |
| 60 kg | 0.00 | 1.99 | 25.04 | 25.04 |
| 80 kg | 0.00 | 1.96 | 23.80 | 22.58 |

## 3. Turning: one robot, two on one side, or two on opposite sides? (250 N)
Motion turn. Each cell: cosine with a pure turn of the best push of that kind (- = none of that kind exists; 0 = did not move), yaw rate (deg/s) in brackets.

| object | mass | best single | best same side | best opposite | best mixed / any pair | planner | equal split |
|---|---|---|---|---|---|---|---|
| cylinder | 20 | 0.09 (2) | 0.10 (2) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |
| cylinder | 40 | 0.10 (2) | 0.12 (3) | 1.00 (24) | 1.00 (24) | 1.00 (22) | 1.00 (21) |
| cylinder | 60 | 0.10 (2) | 0.09 (2) | 1.00 (25) | 1.00 (25) | 1.00 (25) | 1.00 (25) |
| cylinder | 80 | 0.09 (2) | 0.10 (3) | 1.00 (24) | 1.00 (24) | 1.00 (23) | 1.00 (23) |

## 4. Does following the force split matter? (250 N)
Same pair and directions: the planner's shares against both robots pushing equally hard (robots that ignore their share). Share moved as asked, and mean cosine (no motion = 0).

| motion | planner as asked | equal as asked | planner mean cos | equal mean cos | equal fails where planner works |
|---|---|---|---|---|---|
| turn | 1.00 | 1.00 | 1.00 | 1.00 | 0 of 4 |
| move_x | 1.00 | 1.00 | 1.00 | 1.00 | 0 of 4 |
| move_y | 0.00 | 0.00 | 0.58 | 0.20 | 0 of 4 |
| move_turn | 1.00 | 1.00 | 0.90 | 0.89 | 0 of 4 |

## 5. Does the planner pick the best pair? (250 N)
The planner's pair against the best of every usable pair (each with its own split), by motion: mean cosine, and the share of cases where the planner is within 0.1 of the best.

| motion | planner mean cos | best pair mean cos | planner within 0.1 | best pair moved as asked |
|---|---|---|---|---|
| turn | 1.00 | 1.00 | 1.00 | 1.00 |
| move_x | 1.00 | 1.00 | 1.00 | 1.00 |
| move_y | 0.58 | 1.00 | 0.00 | 1.00 |
| move_turn | 0.90 | 0.91 | 1.00 | 1.00 |

## Planner push by object (250 N)
Cosine with the wanted motion (0 = did not move), masses 20 / 40 / 60 / 80 kg.

| object | turn | move_x | move_y | move_turn |
|---|---|---|---|---|
| cylinder | 1.00 / 1.00 / 1.00 / 1.00 | 0.99 / 1.00 / 1.00 / 1.00 | 0.52 / 0.59 / 0.58 / 0.65 | 0.90 / 0.90 / 0.90 / 0.90 |

