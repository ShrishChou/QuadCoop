# Two Spots with arms: IPPO / MAPPO, arms stowed vs learned

Status (2026-11-15): pair wired into the trainer and evaluator; wiring test passed (job 29207519); the four pilot runs are queued (training jobs 29207944, 29207946, 29207948, 29207950; evaluations 29207945, 29207947, 29207949, 29207951). No pilot result yet.

**Questions.**
- Does learning to use the arms improve transport? Compare arms learned against arms stowed, on the same bodies.
- Does a centralized critic help the robots coordinate arm use? Compare MAPPO against IPPO, in each arm mode.

The armless Spot pair (Menagerie Spot on our own walker) is only a loose reference: 58.5% (IPPO) and 56.0% (MAPPO)
on the ten-object suite. Attaching the arm changes mass, balance, collisions and the walker, so the baseline that
matters is the same two arm-equipped Spots with their arms stowed.

## What was built

| piece | where | what |
|---|---|---|
| pair | `quadcoop/coop2/pairs.py` | `spot_arm`: slots `spotarm1`, `spotarm2`, robot type `spot_arm` |
| robot | `quadcoop/robots/spot_arm.py` | RAI's model and frozen walker (`docs/spot_arm.md`); contact priority set to QuadCoop's robot value |
| action | `quadcoop/coop2/spot_arm_term.py` | per robot 3 actions (arm stowed) or 9 (arm learned); each robot has its own walker state |
| observations | `quadcoop/coop2/env_cfg.py` | the existing object, goal and partner inputs + the arm (23 numbers) |
| trainer | `quadcoop/coop2/marl.py` | action widths read from the env's action terms; arm logs |
| evaluator | `scripts/eval_coop2.py`, `scripts/spot_arm/pair_eval.py` | widths from the env; `--arm-lock`; pilot evaluation |

**Actions** (`train_coop2.py --pair spot_arm --arm stowed|learned`).
- Base: forward, lateral and yaw velocity, the same ranges and smoothing as the other robots.
- Arm (learned): six joint targets. Action 0 is the stowed pose; action a moves a joint a × span from stowed
  (shoulder and elbow: + unfolds), clamped to the joint limits.
- Targets are rate-limited to 1.5 rad/s. The port check passed with a gradual arm motion and fell when the arm
  was snapped outward.
- The gripper is held closed.
- A zero action is "stand still, arm stowed": that is what a parked or finished robot gets.

**Observations.** Each actor gets the same inputs under IPPO and MAPPO:
- the existing ones: own motion, object, goal, own walker command, own last action (now including the arm
  outputs), object description, hold progress, partner (pose, velocity, base command);
- new, last: arm joint positions and velocities (12), the arm targets the actuators got (6), the gripper's position
  relative to the object (3), and two flags: arm touching the object, trunk touching the object.

**Trainer and checkpoints.**
- Actor heads, rollout storage, log-probabilities and the update use each robot's action width from the env.
- Every checkpoint records the robot types, the action widths and the arm mode (`robots`, `act_dims`, `arm`).
  The evaluation loader builds the actors from them; older checkpoints default to 3.
- No Stage 2 policy exists for this body, so runs start from random weights (`--scratch`), and there is no
  imitation penalty on any output.
- wandb `Arm/*` per robot: share of time the arm and the trunk touch the object, arm contact force, how far the
  arm is unfolded, and how fast the heading error shrinks while the arm touches vs while it does not.

**Contact friction.** RAI's model gave every robot shape priority 4 and friction 0.15, which would override the
objects' own friction (priority 2, 0.4–0.6). The shapes now have priority 1, as ANYmal and the armless Spot, so the
object sets the robot–object friction. The feet keep 0.7 on the ground, as in the port check.

**Not yet covered.** A mixed ANYmal + Spot-arm pair (the env code is per slot, the pair is not registered), the
contact planner for this body, and the torque each arm applies about the object's centre (only contact and force
are logged; the arm ablation below is the causal test).

## Wiring test (`slurm/spot_arm_wiring.sbatch`, `scripts/spot_arm/pair_wiring.py`)

1. `train_coop2.py --check` for IPPO and MAPPO, arms learned and stowed: build, two iterations, checkpoint.
2. Spot 1 runs a scripted arm action (unfold and sweep) while Spot 2 gets zeros, then the reverse.
   - Pass: the moving arm leaves stowed by more than 0.8 rad and ends within 0.15 rad of its targets; the other
     arm stays within 0.1 rad of stowed; both return; nobody falls.
3. Arm lock: the same action with the arm locked leaves it stowed.
4. The MAPPO learned-arm checkpoint is reloaded: it outputs 18 actions and its arm outputs move both arms.

Video: `evals/spot_arm/pair_wiring/arms.mp4`, captions show commanded, rate-limited and measured shoulder and
elbow angles for both robots.

**Result (job 29207519): every check passed.**

| check | result |
|---|---|
| actions | 9 per robot, 18 in all; each actor reads 80 numbers plus its top map and the front profile |
| trainer | IPPO and MAPPO, arms learned and stowed: built, two iterations each, checkpoints written |
| Spot 1 moves, Spot 2 holds | Spot 1's arm left stowed by 1.48 rad and ended 0.09 rad from its targets; Spot 2's stayed within 0.03 rad |
| Spot 2 moves, Spot 1 holds | 1.47 rad and 0.10 rad; Spot 1's stayed within 0.02 rad |
| arm lock | the locked arm stayed within 0.02 rad of stowed under the same action |
| falls | none |
| reloaded MAPPO checkpoint | records robot type `spot_arm`, widths 9 + 9, arm `learned`; outputs 18 actions; its arm outputs moved both arms (up to 0.60 and 0.28 rad) |

Rerun with the full visual model (job 29210929): the same checks passed with the same numbers. The first run drew
the robots from RAI's primitive collision shapes, because Judo's git has no mesh files and the model was loaded
without them. The visual meshes are MuJoCo Menagerie's Spot meshes, already in `src/quadcoop/assets/spot/assets`,
and are now attached. They are visual only (no contacts, and every body has an explicit inertia), so checkpoints
trained before the change evaluate under the same physics.

## Turn pilot (`slurm/submit_spot_arm_pilot.sh`, settings in `slurm/spot_arm_pilot.env`)

**Task.** One elongated object (`long`), 18–22 kg, goal 1 m ahead, heading goal straight, +30° or −30° equally
often. The robots start behind the object, mirrored (each within ±25° of behind, at least 60° apart, 0.3–0.9 m
clear). Success: within 0.10 m and 6° for 1 s, in a 20 s episode. Both robots are free to reach, reposition, push
or yield.

**Why this task.** With one Spot, the same walking command turned a 20 kg cube 6° with the arm stowed and 31° with
it extended, so the arm can change yaw here. At 40 kg Spot held arm contact for 9.38 s while moving the cube
0.009 m, so nothing pays for arm contact itself.

**Reward.** r7, unchanged from the two-ANYmal runs: object position and heading progress, the success bonus, the
goal-error cost, fall and robot-contact costs. The two shaping terms that are per robot (approach the surface,
push credit) are measured at the body's front, so they neither pay for nor penalize arm contact.

| run | algorithm | arms | question |
|---|---|---|---|
| A `sa_ippo_stowed_s0` | IPPO | both stowed | what independent learners do with these bodies using base motion |
| B `sa_ippo_learned_s0` | IPPO | both learned | what arm control adds under IPPO |
| C `sa_mappo_stowed_s0` | MAPPO | both stowed | what the centralized critic adds for base pushing |
| D `sa_mappo_learned_s0` | MAPPO | both learned | whether the centralized critic helps coordinate arm use |

Matched: actor architecture, random initial weights (seed 0), tasks, reward, 4096 envs × 24 steps × 2000
iterations. One seed shows that the system learns and renders; an algorithm claim needs at least three.

**Evaluation** (`scripts/spot_arm/pair_eval.py`, runs after each training job).
- Held-out starts: 20 placements per turn direction, each also with the start places exchanged (120 tasks).
- Learned-arm checkpoints run every task four ways: both arms active, only Spot 1's, only Spot 2's, both held
  stowed. Disabling an arm tests whether the policy relies on it; the separately trained stowed runs (A, C) test
  whether arm access improves what the team achieves.
- Reported: success, falls, time, final position error, heading error by turn direction; paired change when an
  arm is disabled (tasks lost and gained); success with start places exchanged; each robot's arm contact by start
  side and turn direction.
- Videos: the first placement of each turn, in every arm mode, with wanted and actual object heading in the caption.
- `pair_eval.py --report <names>` puts the four systems side by side on the same tasks.

**Next, if the pilot learns:** the ordinary approach distance and 40 kg; then the four policies on the ten-object,
20–80 kg benchmark (`eval_coop2.py` already takes these checkpoints); three seeds for B and D. If PPO mostly
body-pushes and barely explores the arms, the next run is MAPPO initialized from planner demonstrations.
