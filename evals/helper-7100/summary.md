# Planner + helper: helper-7100

Seed 7100, 120 tasks per arm and mass, start behind, 80 s. pair250: the planner as in planner-bench; pair160: force limit 160 N; helper: pair160 + a scripted third robot (limit x1.3 once it engages). Success %.

| object | pair250 60 kg | pair160 60 kg | helper 60 kg | pair250 80 kg | pair160 80 kg | helper 80 kg | pair250 100 kg | pair160 100 kg | helper 100 kg |
|---|---|---|---|---|---|---|---|---|---|
| cube | 58 | 67 | 58 | 25 | 8 | 8 | 0 | 0 | 8 |
| long | 33 | 92 | 50 | 67 | 17 | 33 | 8 | 8 | 8 |
| sphere | 92 | 83 | 92 | 83 | 75 | 92 | 92 | 75 | 75 |
| cylinder | 25 | 33 | 50 | 25 | 25 | 25 | 25 | 8 | 8 |
| arch | 25 | 75 | 75 | 42 | 25 | 33 | 8 | 0 | 17 |
| dumbbell | 50 | 50 | 67 | 8 | 17 | 50 | 17 | 0 | 17 |
| t_shape | 58 | 75 | 58 | 58 | 25 | 33 | 17 | 0 | 17 |
| l_shape | 58 | 92 | 42 | 25 | 58 | 17 | 0 | 0 | 8 |
| u_channel | 58 | 67 | 50 | 33 | 17 | 50 | 33 | 0 | 8 |
| plus | 42 | 42 | 58 | 17 | 50 | 50 | 0 | 8 | 8 |
| all | 50 | 68 | 60 | 38 | 32 | 39 | 20 | 10 | 18 |

Paired differences (percentage points, 95% bootstrap over tasks, 2000 draws):

- helper - pair160, 60 kg: -7.5 [-18.3, +3.3]
- helper - pair160, 80 kg: +7.5 [-2.5, +17.5]
- helper - pair160, 100 kg: +7.5 [+1.7, +13.3]
- helper - pair160, all: +2.5 [-3.1, +7.8]
- helper - pair250, 60 kg: +10.0 [-1.7, +21.7]
- helper - pair250, 80 kg: +0.8 [-10.0, +11.7]
- helper - pair250, 100 kg: -2.5 [-10.0, +5.8]
- helper - pair250, all: +2.8 [-3.3, +9.2]
- pair160 - pair250, 60 kg: +17.5 [+5.8, +28.3]
- pair160 - pair250, 80 kg: -6.7 [-18.3, +5.0]
- pair160 - pair250, 100 kg: -10.0 [-15.8, -4.2]
- pair160 - pair250, all: +0.3 [-5.3, +6.1]

Helper: engaged in 60 kg 94%, 80 kg 100%, 100 kg 100%; helper falls 17 of 360.

Outcomes: pair250 60: {'success': 60, 'horizon': 44, 'fell_anymal1': 9, 'fell_anymal2': 6, 'tipped': 1}; pair160 60: {'success': 81, 'fell_anymal2': 10, 'horizon': 24, 'fell_anymal1': 5}; helper 60: {'success': 72, 'fell_anymal1': 16, 'fell_anymal3': 4, 'horizon': 23, 'fell_anymal2': 5}; pair250 80: {'fell_anymal1': 9, 'horizon': 62, 'success': 46, 'fell_anymal2': 3}; pair160 80: {'horizon': 72, 'success': 38, 'fell_anymal1': 7, 'fell_anymal2': 3}; helper 80: {'horizon': 42, 'fell_anymal1': 16, 'success': 47, 'fell_anymal2': 7, 'fell_anymal3': 8}; pair250 100: {'horizon': 83, 'success': 24, 'fell_anymal1': 10, 'fell_anymal2': 3}; pair160 100: {'horizon': 102, 'success': 12, 'fell_anymal2': 2, 'fell_anymal1': 4}; helper 100: {'horizon': 69, 'fell_anymal1': 17, 'fell_anymal2': 8, 'success': 21, 'fell_anymal3': 5}
