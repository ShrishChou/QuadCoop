# Compliant walker in the two-robot env: wiring-v22

Walker: `/orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_11-35-10_v22/model_8997.pt` (kind compliant).

## 1. Inputs

- **anymal1: OK** - terms in the training order: True; size 50 vs checkpoint 50; normalizer finite True, spread > 0 True; force-input normalizer mean [-0.0151, -0.0002], std [0.6668, 0.6588]; force term params {'sensor_name': 'push_anymal1', 'felt_load_term': None, 'entity': 'anymal1'}.
- **anymal2: OK** - terms in the training order: True; size 50 vs checkpoint 50; normalizer finite True, spread > 0 True; force-input normalizer mean [-0.0151, -0.0002], std [0.6668, 0.6588]; force term params {'sensor_name': 'push_anymal2', 'felt_load_term': None, 'entity': 'anymal2'}.

## 2. Force wiring vs an independent recomputation (CPU MuJoCo contact forces, robot frame)

Agreeing = vector difference <= max(10 N, 15% of the force). Samples with force > 5 N.

Per step:

| where | samples | agree | median diff N | p90 diff N | median force N | median cos | input x / recomputed x (N) |
|---|---|---|---|---|---|---|---|
| walker training env, pressing a cube | 723 | 53% | 19.2 | 151.3 | 75 | 0.998 | -128 / -127 |
| two-robot env, press | 920 | 51% | 11.1 | 121.1 | 79 | 0.997 | -85 / -46 |
| two-robot env, pushed | 258 | 34% | 59.9 | 402.2 | 252 | 0.996 | -187 / -95 |
| two-robot env, partner | 0 | - | - | - | - | - | - |
| two-robot env, alone | 0 | - | - | - | - | - | - |

Averaged over blocks of 10 samples (0.2 s) per env:

| where | blocks | agree | median diff N | p90 diff N | median force N | median cos | input x / recomputed x (N) |
|---|---|---|---|---|---|---|---|
| walker training env, pressing a cube | 96 | 49% | 20.3 | 75.7 | 71 | 0.998 | -94 / -93 |
| two-robot env, press | 157 | 51% | 9.1 | 72.7 | 52 | 0.999 | -50 / -27 |
| two-robot env, pushed | 50 | 46% | 26.5 | 152.1 | 140 | 0.998 | -97 / -49 |
| two-robot env, partner | 0 | - | - | - | - | - | - |
| two-robot env, alone | 0 | - | - | - | - | - | - |

**Same sensing in both envs** (the question this check answers): input / recomputed force along the force (median scale) 0.98 in the walker's training env vs 0.97 in the two-robot env; median angle between them 3.9 vs 5.3 deg -> CONSISTENT. (The CPU recomputation is an independent physics evaluation, not a replica of the GPU solver: a common scale offset in both envs is a solver difference; a difference between the envs would be a wiring problem.)

State fields not copied into the recomputation: none. Observation noise on the force input in the two-robot walker group (as in the walker's training): up to 4.0 N per component.
Physical sign (pressing an object ahead -> force on the robot points backward, x < 0): OK.
Same term order in the walker env: True. Examples (input x, y | recomputed x, y), two-robot cube pushed into the robot: [[-500.0, -13.5, 0.0, 0.0], [-154.5, 164.4, -158.6, 168.7], [-76.7, 186.3, -50.7, 164.9], [-15.9, -1.1, -439.6, -13.7], [-426.9, -22.6, 0.0, 0.0]]

## 3. Exclusions

- partner walking into robot A (away from the object): 1407 env-steps with the robots touching; largest force input on A then 0.0 N (should be ~0).
- robot standing alone: largest force input 0.0 N (should be ~0).

## 4. Smoke run (robot A presses the 80 kg cube: 0.2 m/s 4 s, stop 2 s, 0.2 m/s 3 s)

- falls (robot A, all scenarios): 3 of 16 (pressing: 0 of 4)
- time touching per phase: {'press': 0.525, 'stop': 0.207, 'press_again': 0.648}; force on the cube per phase (N): {'press': 51.9, 'stop': 11.8, 'press_again': 52.6}
- force inputs: non-finite rows 0, at the clip (+-2.5) 0.7% of env-steps, largest |z| under the checkpoint's normalizer 3.8

Inputs OK; see the tables for force agreement, exclusions and the smoke run.
