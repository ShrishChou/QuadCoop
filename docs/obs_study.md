# Observation study: contact geometry and interaction history for the MAPPO pair

Status (2026-11-19): launched (`slurm/submit_obs_study.sh`; check 29722214, arms 29722215 / 17 / 20 / 24, evaluations
29722216 / 19 / 22 / 25).

## Hypothesis

Robots coordinate better when they can tell *where each teammate could push* (contact geometry) apart from *how the
interaction has actually gone* (recent history). No intermediate targets, no new rewards, no prediction heads.

## What the ordinary pair already sees

Object pose and velocity, goal, the partner's pose, velocity and last command (9), the object descriptor, and the
geometry maps (top map with a partner channel, front profile). `surface_distance()` exists but only rewards use it.
The contact executor already gets assigned contact points, push direction and lever arm, so this study is about the
ordinary pair only (the new inputs refuse contact mode).

## New inputs (appended last in `actor_<robot>` and `state_<robot>`)

**Contact geometry** (`--geom-obs`, `mdp.contact_geom_obs`, 14 = 7 for self, then 7 for the partner):
- bumper-to-surface signed distance (-0.5..3 m);
- vector bumper -> nearest surface point (this robot's frame, length capped at 3 m);
- outward surface normal at that point (this robot's frame);
- that surface point relative to the object centre (object frame): central push vs end contact.

Computed on the true body-height slice of the compound shape (`pf.point_distance`, the same field as the rewards'
surface distance; arch and concave shapes included, not a bounding box). Normal = central difference of the distance
field (1 cm); nearest point = bumper - distance x normal. This is geometric proximity, not measured contact. Actor
copy has 0.02 uniform noise, as the other geometric inputs.

**Interaction history** (`--hist-obs`, `mdp.interaction_history_obs`, 10 x 19 + 10 = 200): the last 1 s at 10 Hz,
newest first, for the active object only:
- object velocity (2) and yaw rate;
- per robot (self, then partner): velocity relative to the object (2), yaw rate, executed base command (3, the
  applied limited command, as `partner_obs`), surface distance, touching (> 5 N from the robot-object contact sensor:
  declared sensing, i.e. a bumper force sensor);
- validity mask (10): slots from before the episode started are zero and marked invalid.

Stored in the world frame and rotated into the observing robot's current frame at read time, so the robot's own
turning does not look like object motion. Reset per episode; first sample at the episode's first step. The geometry
maps stay current-only.

**Temporal encoder:** the history enters the actor's first layer (256 units) as a flat window, i.e. a learned
linear temporal filter shared with the rest of the input, not a separate GRU/convolution. This keeps the warm start
exact (new columns zero) and the four arms the same network apart from input width. If C/D show the history is used
but under-exploited, a dedicated encoder is the next step.

## Design

| arm | contact geometry | history | run |
|---|---|---|---|
| A, matched baseline | no | no | `obsA_mappo_base_s0` |
| B | yes | no | `obsB_mappo_geom_s0` |
| C | no | yes | `obsC_mappo_hist_s0` |
| D | yes | yes | `obsD_mappo_geom_hist_s0` |

- All MAPPO, all `--init-from logs/marl2/nwB_mappo_uniform_s0/model_5000.pt` (actors, critics, noise and caps,
  learning rates, curriculum state; new inputs at zero weight, so each arm starts as the parent).
- Parent's recipe unchanged (`submit_next_wave.sh` arm B): r7, KL anchor 0.05, actor lr cap 1e-4, level 4, 20-80 kg,
  ten objects, uniform task bank. Action-saturation handling is the parent's in every arm (no mean clip, no bound
  penalty); not changed in any arm.
- Same budget: 5000 -> 7000 iterations (~3.3 h at the parent's 17k steps/s). A and B on `mit_normal_gpu`, C and D on
  `mit_preemptable` (resumed from the last checkpoint if preempted).
- One difference A has that the parent did not: the robot-object contact sensors are built only in C and D (history
  needs them). Sensors do not change the physics.
- Evaluation: the 480-task benchmark per arm (seed 7100, 20/40/60/80 kg, 3 reps), `obs-<arm>-*-dev7100`.

## Still to build: controlled recovery tests

Ordinary success is not enough to say *which* information helps. To add to `eval_coop2.py`, same tasks, each arm:
- partner briefly loses contact (partner's command forced back for ~0.5 s mid-push);
- partner starts late (held still for the first N s);
- robots exchange start positions (`--swap` exists);
- partner's push capability reduced within a declared range (walker command scale).

Questions: does geometry improve contact separation (robots at different contact points, e.g. distance between the
two surface points / object size)? Does history improve recovery and synchronisation? Does the combination improve
final-pose success? Does it survive a second seed (`ARMS="..." SEED=1`)?

If neither helps and both robots still choose the middle, the remaining problem is discovering complementary
strategies, where demonstrations or explicit contact assignments are more promising than more inputs.
