# Planner + helper: helper-smoke

Seed 7100, 8 tasks per arm and mass, start behind, 10 s. pair250: the planner as in planner-bench; pair160: force limit 160 N; helper: pair160 + a scripted third robot (limit x1.3 once it engages). Success %.

| object | pair250 80 kg | pair160 80 kg | helper 80 kg |
|---|---|---|---|
| cube | 0 | 0 | 0 |
| long | 0 | 0 | 0 |
| all | 0 | 0 | 0 |

Paired differences (percentage points, 95% bootstrap over tasks, 2000 draws):

- helper - pair160, 80 kg: +0.0 [+0.0, +0.0]
- helper - pair160, all: +0.0 [+0.0, +0.0]
- helper - pair250, 80 kg: +0.0 [+0.0, +0.0]
- helper - pair250, all: +0.0 [+0.0, +0.0]
- pair160 - pair250, 80 kg: +0.0 [+0.0, +0.0]
- pair160 - pair250, all: +0.0 [+0.0, +0.0]

Helper: engaged in 80 kg 88%; helper falls 0 of 8.

Outcomes: pair250 80: {'horizon': 8}; pair160 80: {'horizon': 8}; helper 80: {'horizon': 8}
