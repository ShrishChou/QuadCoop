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
