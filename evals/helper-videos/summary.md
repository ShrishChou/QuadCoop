# Planner + helper: helper-videos

Seed 7100, 48 tasks per arm and mass, start behind, 80 s. pair250: the planner as in planner-bench; pair160: force limit 160 N; helper: pair160 + a scripted third robot (limit x1.3 once it engages). Success %.

| object | helper 80 kg | helper 100 kg |
|---|---|---|
| cube | 50 | 50 |
| long | 25 | 25 |
| sphere | 75 | 75 |
| cylinder | 25 | 0 |
| arch | 25 | 0 |
| dumbbell | 50 | 0 |
| t_shape | 0 | 0 |
| beam | 0 | 0 |
| l_shape | 25 | 0 |
| asym | 0 | 0 |
| u_channel | 50 | 25 |
| plus | 25 | 25 |
| all | 29 | 17 |

Paired differences (percentage points, 95% bootstrap over tasks, 2000 draws):


Helper: engaged in 80 kg 100%, 100 kg 100%; helper falls 3 of 96.

Outcomes: helper 80: {'success': 14, 'fell_anymal1': 7, 'horizon': 19, 'fell_anymal2': 6, 'fell_anymal3': 2}; helper 100: {'success': 8, 'horizon': 31, 'fell_anymal1': 4, 'fell_anymal2': 4, 'fell_anymal3': 1}
