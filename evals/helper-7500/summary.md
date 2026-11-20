# Planner + helper: helper-7500

Seed 7500, 120 tasks per arm and mass, start behind, 80 s. pair250: the planner as in planner-bench; pair160: force limit 160 N; helper: pair160 + a scripted third robot (limit x1.3 once it engages). Success %.

| object | pair250 60 kg | pair160 60 kg | helper 60 kg | pair250 80 kg | pair160 80 kg | helper 80 kg | pair250 100 kg | pair160 100 kg | helper 100 kg |
|---|---|---|---|---|---|---|---|---|---|
| cube | 75 | 83 | 67 | 42 | 25 | 33 | 0 | 0 | 17 |
| long | 83 | 100 | 50 | 17 | 17 | 17 | 8 | 0 | 0 |
| sphere | 100 | 100 | 100 | 92 | 75 | 92 | 100 | 67 | 100 |
| cylinder | 33 | 33 | 25 | 17 | 25 | 25 | 17 | 25 | 17 |
| arch | 75 | 75 | 67 | 42 | 25 | 33 | 17 | 0 | 0 |
| dumbbell | 58 | 75 | 67 | 33 | 33 | 50 | 8 | 0 | 17 |
| t_shape | 50 | 83 | 75 | 50 | 25 | 50 | 17 | 0 | 42 |
| l_shape | 83 | 75 | 67 | 25 | 25 | 17 | 8 | 0 | 8 |
| u_channel | 42 | 83 | 58 | 8 | 17 | 58 | 0 | 0 | 8 |
| plus | 42 | 67 | 67 | 25 | 17 | 8 | 8 | 8 | 25 |
| all | 64 | 78 | 64 | 35 | 28 | 38 | 18 | 10 | 23 |

Paired differences (percentage points, 95% bootstrap over tasks, 2000 draws):

- helper - pair160, 60 kg: -13.3 [-23.3, -2.5]
- helper - pair160, 80 kg: +10.0 [+0.0, +20.0]
- helper - pair160, 100 kg: +13.3 [+6.7, +20.0]
- helper - pair160, all: +3.3 [-2.5, +8.9]
- helper - pair250, 60 kg: +0.0 [-10.9, +11.7]
- helper - pair250, 80 kg: +3.3 [-6.7, +13.3]
- helper - pair250, 100 kg: +5.0 [-1.7, +11.7]
- helper - pair250, all: +2.8 [-2.8, +8.1]
- pair160 - pair250, 60 kg: +13.3 [+3.3, +24.2]
- pair160 - pair250, 80 kg: -6.7 [-16.7, +3.3]
- pair160 - pair250, 100 kg: -8.3 [-14.2, -2.5]
- pair160 - pair250, all: -0.6 [-6.1, +5.0]

Helper: engaged in 60 kg 95%, 80 kg 100%, 100 kg 100%; helper falls 21 of 360.

Outcomes: pair250 60: {'success': 77, 'horizon': 36, 'fell_anymal1': 3, 'fell_anymal2': 4}; pair160 60: {'success': 93, 'horizon': 20, 'fell_anymal1': 5, 'fell_anymal2': 2}; helper 60: {'success': 77, 'fell_anymal3': 7, 'fell_anymal2': 4, 'horizon': 25, 'fell_anymal1': 7}; pair250 80: {'horizon': 67, 'success': 42, 'fell_anymal2': 3, 'fell_anymal1': 8}; pair160 80: {'success': 34, 'horizon': 81, 'fell_anymal2': 1, 'fell_anymal1': 4}; helper 80: {'success': 46, 'fell_anymal3': 11, 'horizon': 40, 'fell_anymal1': 15, 'fell_anymal2': 8}; pair250 100: {'horizon': 84, 'fell_anymal1': 11, 'success': 22, 'fell_anymal2': 3}; pair160 100: {'horizon': 98, 'fell_anymal1': 8, 'success': 12, 'fell_anymal2': 2}; helper 100: {'horizon': 72, 'fell_anymal1': 12, 'success': 28, 'fell_anymal3': 3, 'fell_anymal2': 5}
