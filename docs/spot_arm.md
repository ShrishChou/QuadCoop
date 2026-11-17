# Spot with an arm: reuse RAI's released walker, train only the pusher

Status (2026-11-14): step 1 done on CPU. Nothing trained yet; the mjlab integration (step 2) is the next piece of work.

## What exists online

- **RAI `sumo` and `judo`** (github.com/rai-opensource, both MIT). Cloned to `~/ext/sumo` and `~/ext/judo` (branch
  `dta/fix_for_sumo`, the one `sumo` pins).
  - A MuJoCo Spot model with the arm: 12 leg joints, 7 arm joints, primitive collision shapes, position actuators.
  - A pretrained whole-body walker, `judo/models/policies/spot_locomotion.onnx`: an MLP, 84 inputs, 12 leg outputs.
  - 20 Spot tasks in `sumo` (box, tire, chair, cone, rack, barrier: push, upright, drag, stack).
  - The pushing itself is not a learned policy. A sampling-based planner (CEM / MPPI) searches over the walker's
    command every step. There is no released training code for the walker and no learned pusher.
- **Others found:** NVIDIA's Isaac Lab Spot example is locomotion only, no arm. RAI's later learned box-pushing policy
  (SMPC demonstrations to RL) has a project page but no code. No other released Spot-arm policy was found.

## The walker's interface (`judo/controller/batched_spot_locomotion.py`)

- **Command, 25 numbers:** base velocity (3), arm joint targets (7), leg joint overrides (12, zero means "walk"),
  torso roll, pitch and height (3; height 0.52 m by default).
- **Observation, 84:** body velocity, angular velocity, gravity direction, the command, 19 joint positions and
  velocities, the previous 12 leg actions.
- **Rate:** 50 Hz, timestep 0.01 s with 2 substeps.
- The arm targets pass straight through to the arm's position actuators; the walker balances around them.

That is the same layering QuadCoop already uses: a pusher policy sends commands to a frozen walker
(`WalkerCommandAction`). Only the command is wider: 3 numbers now, up to 13 with the arm and torso.

## Step 1: does the walker run outside RAI's stack? (`scripts/spot_arm/walker_check.py`, CPU, plain MuJoCo)

The script reads RAI's model and weights as data and rebuilds the network in torch. Results in
`evals/spot_arm/walker_check.json`.

| command | arm stowed: achieved | arm out: achieved |
|---|---|---|
| stand | 0.00 m/s, upright | 0.00 m/s, upright |
| forward 0.5 m/s | 0.49 | 0.48 |
| forward 1.0 m/s | 0.95 | 0.93 |
| sideways 0.3 m/s | 0.28 | 0.28 |
| turn 0.5 rad/s | 0.46 | 0.48 |
| forward 0.5 m/s, arm sweeping | | 0.48 |

No falls in any case. (A first attempt fell within 2 s because the torso-height command was left at 0; the walker
needs 0.52 m.)

**Pushing by walking into a 0.6 m cube for 10 s at 0.5 m/s** (box friction 0.5):

| box | arm stowed | arm out |
|---|---|---|
| 20 kg | moved 0.59 m, turned 6° | moved 0.40 m, turned 31° (arm on the box 7.4 s) |
| 40 kg | moved 0.05 m | moved 0.01 m |

**Reading:**
- The walker is usable as released, with the arm moving, and needs no training.
- It is not a pusher by itself. It tracks velocity and gives way against a load: 20 kg moves slowly and 40 kg stalls.
  QuadCoop's ANYmal walker was trained with a push curriculum; this one was not.
- The arm changes what happens to the object: with the arm out, the box turned 31° instead of 6°. That is the lever
  for heading correction, uncontrolled here.
- One run per case, on CPU MuJoCo, not on MuJoCo Warp.

## Path to pushing, then to two robots

1. **Port to mjlab** (not started). A `spot_arm` robot built from RAI's model, and a walker action term with the
   84-number observation and the 25-number command. Acceptance: the tracking table above reproduced on MuJoCo Warp.
   QuadCoop's contact settings differ from RAI's (friction cone, `impratio`), so this must be measured, not assumed.
2. **Capability test before training.** Stall force and pushable mass, as was done for ANYmal. If the frozen walker
   cannot move 40 kg with any arm or torso command, the walker needs fine-tuning with push disturbances first.
3. **Train a single-robot pusher** on the long rectangular object, straight goal and move-plus-turn, 20 and 40 kg.
   Two arms: commands of base velocity only (arm stowed), against base velocity plus arm targets. Same reward and
   budget. The question is whether the arm reduces heading error and settling failures.
4. **Two robots, only if step 3 shows an arm advantage.** ANYmal plus Spot-arm with IPPO, against the same pair with
   the arm stowed and against Spot-arm alone. The `mixed` pair slot and the per-robot actor already exist.

**Risks:** the walker stalls at loads the ANYmal handles; RAI's model uses soft friction settings that differ from
ours; MIT licence, so the files can be vendored with attribution, but they are not copied into the repo yet.

## Step 2 result (2026-11-14): the frozen walker cannot push 40 kg or more

`scripts/spot_arm/push_capability.py` (CPU job 29136861; `evals/spot_arm/push_capability.json`). Per mass: 150 random
constant commands (speed 0.3–1.2 m/s, torso pitch and height, arm pose) held for 10 s against a 0.6 m cube with
friction 0.5, plus the two fixed baselines.

| box | baseline, arm stowed | best of 150 commands | commands moving it more than 1 m | commands that fell |
|---|---|---|---|---|
| 20 kg | 0.59 m | 3.23 m | 21 | 44 |
| 40 kg | 0.05 m | 0.19 m | 0 | 47 |
| 60 kg | 0.01 m | 0.06 m | 0 | 47 |

**Reading:**
- **At 20 kg the command matters a lot:** 0.6 m by walking into the box, 3.2 m with a low torso and the arm braced
  on it. A pusher policy over these commands has something to learn. The best commands also turn the box about 60°,
  so they need steering.
- **At 40 kg and above nothing works.** No constant command moves the box 0.2 m in 10 s. The walker was trained to
  track velocity, not to push, and gives way.
- **Traction estimate (an estimate, not a measured limit).** With foot friction 0.7 and a robot of about 39 kg,
  friction alone allows roughly 270 N of horizontal force; a 60 kg box at friction 0.5 needs about 295 N to slide.
  So the heavy cases are near what friction allows for a robot pushing alone. The measured stall describes this
  walker, posture and contact; posture, contact location (the arm lowers or raises the line of force) and joint
  torque limits change it, and none of those was varied systematically here.
- About 30% of random commands made it fall, so the pusher's command range has to be limited.
- Constant commands only, one seed, plain MuJoCo with RAI's contact settings.

**Consequence for the plan.** Step 3 changes: a pusher on the frozen walker is limited to about 20 kg. To push
30–40 kg, the walker itself must be trained with push loads. RAI released no training code, so that means training
our own Spot-arm walker in mjlab, started from RAI's weights (same network shape, 84 → 512 → 256 → 128 → 12).
The mjlab port (step 1) is needed for either route and is still not started.

## Port acceptance (2026-11-15): passed

`src/quadcoop/robots/spot_arm.py` (robot from RAI's model, `RaiWalker`) and `scripts/spot_arm/warp_check.py`, job
29147569, `evals/spot_arm/warp_check.json`. 11 cases × 16 envs on MuJoCo Warp, under RAI's timing (0.01 s × 2) and
QuadCoop's (0.005 s × 4).

- **Both timings pass:** no falls, every achieved velocity within 0.08 of the command, and within 0.01 of the CPU
  numbers (forward 0.5 → 0.48–0.50, forward 1.0 → 0.93–0.95, sideways 0.3 → 0.28, turn 0.5 → 0.46–0.47).
- **QuadCoop's timestep works,** so Spot-arm can share a scene with ANYmal without changing the physics rate.
- **The arm must be moved gradually.** The first run (job 29146215) snapped the arm from stowed to out at the instant
  of the drop, and every arm-out env fell. Ramping it over 1.5 s removes that. The pusher's arm command needs a
  rate limit.

Next: the 20 kg steering pusher (step 3), arm active against arm stowed.

## Pushing walker (2026-11-17): RAI's walker fine-tuned with ANYmal v1's push curriculum

Why: the frozen walker gives way under load (step 2 above): with the default posture and these contacts, no constant
command moved 40 kg. That is a property of this walker, posture and contact, not a measured limit of the robot.

Code: `src/quadcoop/spot_arm_walker.py` (task `QuadCoop-Walker-SpotArm`), `ROBOT=spot_arm sbatch
slurm/train_walker.sbatch`; resolved configuration of the run in `configs/walker_spot_arm/push_ft_s1/`. Check script
`scripts/spot_arm/walker_ft_check.py` (any policy in this env: falls by reason, height, tracking; `--compare` checks
the env's actor input against `RaiWalker`'s term by term). Use a trained walker in the pair env with
`QUADCOOP_SPOT_ARM_WALKER=<model_N.pt>`.

- **Start:** RAI's network (84 -> 512 -> 256 -> 128 -> 12), weights loaded from `spot_locomotion.onnx`; raw inputs
  (no normalizer). Checked: the iteration-0 checkpoint equals RAI's weights exactly; the actor stays frozen for the
  first 100 iterations while the new critic learns; all values finite.
- **Inputs and outputs:** RAI's 84 inputs in RAI's order, its 12 leg outputs x 0.2 + RAI's offsets (Isaac -> MuJoCo
  order). `--compare`: identical to `RaiWalker` (max difference 0.0000 for every part).
- **Recipe:** walker v1's (push episodes with objects on the line of travel, 25% free walk, push-progress reward,
  mass curriculum gated on falls and tracking), objects 5 -> 40 kg, foot friction 0.6-0.9 (pair env: 0.7),
  3000 iterations, lr 1e-4 (adaptive, KL 0.005), std 0.25 -> learned.
- **Run `push_ft_s0` is invalid.** The joint-reset event covered only the legs, so the arm started every episode at
  the model's zero pose and was then driven to stowed, throwing the robot over (frozen RAI walker: every episode
  ended by body-ground contact at 0.34 s). The fine-tune learned to survive this and stood unusually tall (0.58-0.62 m).
  Fixed (reset on all joints): the frozen RAI walker then runs 10 s without a fall, at 0.49-0.52 m, within
  0.08-0.11 m/s of the command, with the arm moving and with the training noise. `push_ft_s1` is the run.

### What it trains on (coverage audit)

| load or motion | in `push_ft_s1` | note |
|---|---|---|
| arm configurations changing while walking | yes | new goal every 2-6 s: stowed 40%, RAI's "out" 20%, random 40% (shoulder yaw +-0.4, pitch -2.6..-0.3, elbow 0.5..2.9, wrist -1.5..0.8), at most 1.5 rad/s |
| sustained body load from objects | yes | objects on the line of travel, 5 -> 40 kg, contact anywhere on the robot (mostly the front) |
| sustained force at the hand | no | the arm touches objects only by chance; hand contact gives different moments from trunk contact |
| short disturbances | yes | velocity kicks every 4-8 s (horizontal) |
| walk -> push -> release | partly | objects appear on the line and are replaced once passed or lost; direction changes every 5-10 s; no explicit stop-while-pushing or back-off-and-release |
| torso posture commands | no | always roll 0, pitch 0, height 0.52 (RAI trained height 0.25-0.65 m, roll and pitch +-0.35): the fine-tune may lose the posture interface |

Smallest additions, to run as a separate continuation from `push_ft_s1` (labelled `push_ft_s1_handload`) so the two
are compared:
1. torso commands sampled per segment inside a bounded range (height 0.40-0.55 m, pitch +-0.2 rad, roll 0), so the
   posture interface survives and can be used by the pusher;
2. a sustained external force at the gripper body when the arm is out: ramp-hold-ramp, 0-100 N, mostly against the
   hand's forward direction, with the walker commanded forward or holding;
3. release segments: while pushing, command 0 or a slow back-off for 1-2 s, then resume.

### ReLIC (github.com/rai-opensource/relic) against what we import

- **Same network.** ReLIC's pretrained `policy.pt` is identical, weight for weight, to Judo's `spot_locomotion.onnx`
  (largest difference 0.0): our imported walker is ReLIC's.
- **How it was trained** (Isaac Lab, rsl_rl, four phases with changing reward weights): velocity commands +-1 m/s,
  +-1 rad/s; arm targets sampled over the full joint range along 1-3 s trajectories with 0.5-2 s holds; torso roll and
  pitch +-0.35 rad, height 0.25-0.65 m; one leg can be commanded instead of walking; friction 0.3-1.0; base mass
  +-2.5 kg, arm mass +-0.5 kg; reset roll and pitch +-0.5 rad, joints +-0.2 rad; external force on the body +-5 N and
  torque +-2 N m every 7-10 s; velocity kicks. Observation noise: linear velocity 0.1, angular 0.2, joints 0.05,
  joint velocity 0.5 (ours: 0.1, 0.1, 0.01, 0.5).
- **What it lacks for pushing:** no objects, no sustained loads (the 5 N external force is a disturbance), no hand
  contact. That is consistent with the walker giving way under load.
- **To reuse:** its torso ranges (for the posture test and the continuation above), its arm trajectory sampling
  (wider than ours), its friction and mass randomization, and its staged reward weights (base height and orientation
  tracking weights grow over the phases; worth adopting if the fine-tune drifts in posture).
