# Compliant walker in the two-robot env: wiring-v22k

Walker: `/orcd/home/002/shrishc/quadcoop/logs/rsl_rl/walker_anymal_c_compliant/2026-11-08_14-39-28_v22_k1000/model_10496.pt` (kind compliant).

## 1. Inputs

- **anymal1: OK** - terms in the training order: True; size 50 vs checkpoint 50; normalizer finite True, spread > 0 True; force-input normalizer mean [-0.0156, -0.0004], std [0.6401, 0.631]; force term params {'sensor_name': 'push_anymal1', 'felt_load_term': None, 'entity': 'anymal1'}.
- **anymal2: OK** - terms in the training order: True; size 50 vs checkpoint 50; normalizer finite True, spread > 0 True; force-input normalizer mean [-0.0156, -0.0004], std [0.6401, 0.631]; force term params {'sensor_name': 'push_anymal2', 'felt_load_term': None, 'entity': 'anymal2'}.

## 2. Force wiring vs an independent recomputation (CPU MuJoCo contact forces, robot frame)

Agreeing = vector difference <= max(10 N, 15% of the force). Samples with force > 5 N.

Per step:

| where | samples | agree | median diff N | p90 diff N | median force N | median cos | input x / recomputed x (N) |
|---|---|---|---|---|---|---|---|
| walker training env, pressing a cube | 703 | 50% | 36.6 | 230.7 | 149 | 0.998 | -169 / -156 |
| two-robot env, press | 828 | 49% | 27.6 | 199.7 | 103 | 0.992 | -123 / -66 |
| two-robot env, pushed | 263 | 33% | 72.0 | 396.6 | 305 | 0.989 | -199 / -117 |
| two-robot env, partner | 0 | - | - | - | - | - | - |
| two-robot env, alone | 0 | - | - | - | - | - | - |

Averaged over blocks of 10 samples (0.2 s) per env:

| where | blocks | agree | median diff N | p90 diff N | median force N | median cos | input x / recomputed x (N) |
|---|---|---|---|---|---|---|---|
| walker training env, pressing a cube | 96 | 48% | 22.2 | 113.5 | 119 | 0.999 | -121 / -111 |
| two-robot env, press | 158 | 52% | 10.9 | 107.1 | 58 | 0.998 | -64 / -34 |
| two-robot env, pushed | 50 | 50% | 26.2 | 138.4 | 137 | 0.996 | -105 / -61 |
| two-robot env, partner | 0 | - | - | - | - | - | - |
| two-robot env, alone | 0 | - | - | - | - | - | - |

**Same sensing in both envs** (the question this check answers): input / recomputed force along the force (median scale) 0.98 in the walker's training env vs 1.01 in the two-robot env; median angle between them 3.2 vs 8.4 deg -> CONSISTENT. (The CPU recomputation is an independent physics evaluation, not a replica of the GPU solver: a common scale offset in both envs is a solver difference; a difference between the envs would be a wiring problem.)

State fields not copied into the recomputation: none. Observation noise on the force input in the two-robot walker group (as in the walker's training): up to 4.0 N per component.
Physical sign (pressing an object ahead -> force on the robot points backward, x < 0): OK.
Same term order in the walker env: True. Examples (input x, y | recomputed x, y), two-robot cube pushed into the robot: [[-500.0, 15.6, 0.0, 0.0], [-249.2, 158.7, -237.8, 182.2], [-433.8, 103.4, 0.0, 0.0], [-41.5, -2.0, -115.9, -5.7], [-294.0, -15.0, 0.0, 0.0]]

## 3. Exclusions

- partner walking into robot A (away from the object): 1447 env-steps with the robots touching; largest force input on A then 0.0 N (should be ~0).
- robot standing alone: largest force input 0.0 N (should be ~0).

## 4. Smoke run (robot A presses the 80 kg cube: 0.2 m/s 4 s, stop 2 s, 0.2 m/s 3 s)

- falls (robot A, all scenarios): 1 of 16 (pressing: 0 of 4)
- time touching per phase: {'press': 0.399, 'stop': 0.36, 'press_again': 0.56}; force on the cube per phase (N): {'press': 60.3, 'stop': 22.5, 'press_again': 74.1}
- force inputs: non-finite rows 0, at the clip (+-2.5) 1.0% of env-steps, largest |z| under the checkpoint's normalizer 4.0

Inputs OK; see the tables for force agreement, exclusions and the smoke run.
