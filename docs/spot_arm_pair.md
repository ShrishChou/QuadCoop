# Two Spots with arms: IPPO / MAPPO, arms stowed vs learned

Status (2026-11-15): turn pilot (A-D) done: the arms go unused. Hand wave: H2, H3 running; H1 and H4 paused (checkpoints at iterations 1200 and 600). Turn in place: scripted maneuver and demonstrations done, three MAPPO runs (T1-T3) submitted.

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

**Mid-run reading (iteration ~950, training statistics).** Both learned-arm runs train well (IPPO 0.86, MAPPO 0.93
success) but mostly with the body: arm on the object 0.0-1.5% of the time vs the trunk 17-20%. The arm outputs'
exploration noise has stayed at its initial 0.60 while the base noise fell to 0.44-0.54. This says the robots
usually solve the ±30° task by body pushing; it does not show that the arm outputs learned nothing (their mean can
still depend on the object or goal) or cost nothing. The matched evaluation and the arm ablation answer that.

**Pilot result (2000 iterations, 120 held-out tasks each; `evals/spot_arm/pilot_report.md`).**

| run | success | with both arms held stowed | arm on the object | median time to success |
|---|---|---|---|---|
| A IPPO, stowed | 93.3% | - | 0% | |
| B IPPO, joint targets | 100% | 99.2% (1 task lost) | ≤ 1.3% | 4.0 s |
| C MAPPO, stowed | 93.3% | - | 0% | 4.1 s |
| D MAPPO, joint targets | 96.7% | 99.2% (+2.5 pts, CI −0.8 to +6.7) | ≤ 0.4% | 3.8 s |

- B beats A by +6.7 points (95% CI +2.5 to +11.7; 8 tasks gained, 0 lost), but B with its arms locked stowed
  still scores 99.2%. The gain is a better body-pushing policy, not arm use; with one seed this is within the
  variation expected between training runs.
- MAPPO vs IPPO with stowed arms: +0.0 points (CI −6.7 to +6.7).
- The ±30° task is solved by body pushing in about 4 s of the 20 s episode; neither algorithm uses the arms.

## Hand-position control and the ±60° turn (wave 2)

Two separate questions: does hand-position control make useful arm actions easier to learn, and does using the arms
improve transport when a larger turn is required?

**Interface** (`--arm hand`, `quadcoop/coop2/spot_arm_term.py`; IK in `quadcoop/robots/spot_arm.py`). 7 actions per
robot:
- base: forward, lateral and yaw velocity, as before;
- hand point (3), in the robot's body frame: (0.80, 0, -0.05) m + a × (0.25, 0.45, 0.25), i.e. 0.55-1.05 m ahead
  (the trunk front is at 0.42), ±0.45 m to the side, 0.30 m below to 0.20 m above the shoulder line;
- extension (1), one job only: w = clamp(a, 0, 1) blends the joint targets from stowed (w = 0) to the IK solution of
  the hand point (w = 1). A zero action is still "stand still, arm stowed", and small positive exploration starts
  the reach from the initial pose.

The IK is closed form: the model's yaw, pitch and pitch joints, gripper kept level, rolls 0. It matches MuJoCo's
forward kinematics to under 1 mm wherever the point is reachable, which is 81% of the box. In the near corners
(beside the shoulder) and the far low corners, the joint limits bring the hand to the nearest point the arm can
reach. Targets are rate-limited at 1.5 rad/s as before, and the gripper stays closed. Where and when to reach
stays with the policy.

**Observations** (`--hand-obs`, every arm mode in this wave): as before plus the measured hand point and the
commanded one (body frame) and the extension (7 numbers). Joint-target and stowed runs get zeros for the command
and the extension.

**Preflight** (`slurm/spot_arm_hand_wiring.sbatch`, `scripts/spot_arm/hand_reach.py`). The trainer builds and
updates for MAPPO with hand, joint-target and stowed arms at ±60°. Then each Spot runs alone (partner parked) from
6 matched starts straight behind the 20 kg long object. It reaches left (y = +0.35 m), reaches right (−0.35 m) or
keeps the arm stowed, then walks forward at 0.25 m/s with the same base command in every case. Recorded:
requested vs measured hand point, hand and trunk contact and which comes first, signed object rotation, travel,
falls. Videos for each robot and condition.

Pass criteria:
- the hand gets within 5 cm of the requested point;
- no falls;
- the hand touches before the trunk;
- the left reach turns the object clockwise and the right reach counter-clockwise, each by at least 3° more than
  with the arm stowed.

**Preflight result (jobs 29222369, 29222956, 29223636): passed at 0.5 m/s.** Trainer checks built and updated in all
three arm modes; each actor reads 85 numbers in this wave. Each Spot alone, 6 matched starts per condition, the same
walking command:

| walking command | condition | rotation, Spot 1 / Spot 2 (mean, deg) | travel (m) | hand / trunk contact | falls |
|---|---|---|---|---|---|
| 0.25 m/s | hand left / right / stowed | −0.6 / −0.4, +1.3 / +2.0, +0.6 / −0.1 | 0.01-0.06 | hand first in all reaches | 0 |
| 0.5 m/s | hand left | −15.5 / −25.9 | 0.41-0.52 | hand first 6/6 each, trunk ≤ 2% | 0 |
| 0.5 m/s | hand right | +34.6 / +31.0 | 0.43-0.44 | hand first 6/6 each, trunk ≤ 1% | 0 |
| 0.5 m/s | stowed (trunk) | +4.5 / +7.1 | 0.28-0.41 | trunk 46-47% | 0 |
| 0.8 m/s | hand left / right / stowed | −40.6 / −38.5, +38.0 / +37.9, +37.7 / +18.6 | 0.59-0.77 | | 0 |

- A placed hand steers the object. At 0.5 m/s, left and right reaches with the same base command end 50-57° apart,
  each 20-33° from the stowed push, in the expected direction, upright.
- At 0.25 m/s nothing moves 20 kg, with the trunk either: the walker's push grows with its velocity error.
- At 0.8 m/s the stowed push alone already swings the object 19-38°.
- The test speed is therefore 0.5 m/s.

The hand sits 8.5-9 cm from the requested point before any contact. That is gravity sag of the arm's position
actuators (120 Nm/rad), not the IK. Pushing moves it further: mid-push it was measured at (0.67, 0.31, −0.23) m
against (0.80, 0.35, −0.05) m. The tolerance was set at 5 cm before measuring and is now 10 cm. The policy reads the
measured hand point.

Videos: `evals/spot_arm/hand_reach/spotarm{1,2}_{left,right,stowed}.mp4` (0.5 m/s; the 0.5 and 0.8 m/s sweeps are in
`hand_reach_vx0.5/`, `hand_reach_vx0.8/`, the 0.5 m/s ones with a camera that frames the parked partner too).

**Turns.** The goal heading change is 0 or ±60° (equally often); everything else is the turn pilot's. The long box
allows up to 81° (0.9 × its 90° symmetry), so 60° is not capped. A cube would cap at 40.5°. The evaluation records
the goal heading change as placed (`turn_realized_deg`), and training logs `Task/goal_turn_*`.

**Runs** (`slurm/submit_spot_arm_hand.sh`), all MAPPO, from scratch (seed 0), r7, 4096 envs × 24 steps × 2000
iterations, evaluated on the same held-out starts with the four-way arm ablation:

| run | arm | turns | compared with | tells |
|---|---|---|---|---|
| H1 `sa_mappo_hand30_s0` | hand position | 0 / ±30° | pilot D (joint targets, ±30°) | the interface change alone (H1 also reads the hand inputs) |
| H2 `sa_mappo_stowed60_s0` | stowed | 0 / ±60° | | how far body pushing gets on the larger turn |
| H3 `sa_mappo_learned60_s0` | joint targets | 0 / ±60° | H2 | whether the larger turn alone brings arm use |
| H4 `sa_mappo_hand60_s0` | hand position | 0 / ±60° | H2, H3 | arm advantage (vs H2), interface advantage (vs H3) |

Submitted 2026-11-15: training H1 29224198, H2 29224200, H3 29224202, H4 29224204; evaluations (`--turn 30` for
H1, `--turn 60` for the others) 29224199, 29224201, 29224203, 29224206. Report:
`pair_eval.py --report sa-hand-sa_mappo_stowed60_s0,sa-hand-sa_mappo_learned60_s0,sa-hand-sa_mappo_hand60_s0
--report-out evals/spot_arm/hand_report.md`; H1 against pilot D with `--report sa-pilot-sa_mappo_learned_s0,sa-hand-sa_mappo_hand30_s0`.

**What decides the next run.**
- If hand control turns better than both stowed and joint control: IPPO vs MAPPO with hand control, matched
  budgets, several seeds.
- If a scripted hand placement steers the object (the preflight) but PPO still trunk-pushes: initialize the arm
  from successful scripted reaches and compare demonstration-assisted PPO with PPO alone.
- If stowed control already solves ±60° reliably: stop enlarging the turn or shortening the clock, and switch to a
  task that needs a reach, e.g. correcting a long object's heading with its centre already at the goal.

Arm contact stays out of the reward.

## Turn in place (wave 3)

**Why this task.** The ±30° and probably ±60° turns are solved by body pushing, so they cannot show what an arm
adds.

Here the 20 kg long object starts at its goal centre and must turn 40° clockwise or counter-clockwise and settle:
centre within 0.10 m and heading within 6°, held 1 s, in 20 s. The largest centre drift during the maneuver is also
recorded.

With the gripper closed the robots can only push, and two pushes on the same face always add a net force, so the
centre moves. A turn in place therefore needs a couple: the robot behind pushes forward at one end, the robot in
front pushes back at the other. So one Spot starts behind the 1 m face and one in front (±15°), exchanged in half
the placements. Which end each robot takes depends on the turn direction; no roles are assigned.

H1 and H4 were stopped (checkpoints kept). With per-step noise on an absolute extension, the rate limiter tracks
roughly the median of the command, i.e. stowed, so the hand never left. H2 and H3 run to completion as the ±60°
controls.

**Interface `--arm hand_rate`** (7 actions per robot), a persistent, bounded hand target:
- base: as before;
- hand point: moves at a × 0.6 m/s inside the hand box; zero holds it;
- extension: moves at a × 1.5 /s inside [0, 1]; negative retracts; zero holds;
- joint targets: as `hand`, rate-limited at 1.5 rad/s;
- the action-rate cost skips these four arm outputs;
- `--arm-hold-steps k` latches the arm action for k steps, but a retract still acts at once. It is implemented and
  off in these runs: with a persistent target, zero already holds, and a latch would make PPO credit actions the
  arm never executed.

Captions and logs show the requested hand point and extension, the executed target (the rate limiter's lag in joint
space) and the measured hand point.

**Scripted maneuver** (`quadcoop/coop2/spot_arm_script.py`, `scripts/spot_arm/turn_inplace.py`). Each robot faces its
face and stays centred on it, reaches to the end that makes the requested turn (counter-clockwise: each robot's
right-hand end), walks in until the hand touches and pushes, slowing near the goal. The two robots trade push speed
to cancel centre drift. Within 2.5° they retract and step back. In the stowed version the robot side-steps so its
trunk pushes that end.

Mirrored opposite starts, 8 placements × 2 directions × exchanged = 32 episodes per row:

| scripted, ±40° | success | largest centre drift (median) | end heading error (median) |
|---|---|---|---|
| both hands | 78% (counter-clockwise 69%, clockwise 88%) | 0.02 m | 2.3° |
| one hand + the partner's trunk | 47-59% | 0.06 m | 3.0-5.9° |
| both stowed (trunks) | 25% (counter-clockwise 50%, clockwise 0%) | 0.03 m | 8.8° |
| one robot alone (partner parked) | 0% | 0.13 m | 29° |

There were no falls. At ±60° the hands reach 34% and the trunks 0%, both too slow for 20 s: mid-push the hand sits
22 cm back and 15 cm below its target, because the push goes through a compliant arm. The task is set at ±40°.

Videos: `evals/spot_arm/turn_inplace_40/{both_hands,stowed}_{ccw,cw}.mp4`, captions with wanted and actual heading,
centre drift, and each robot's requested, executed and measured hand. The stowed result is this script's; a trained
stowed pair may do better (run T1).

**Demonstrations** (`scripts/spot_arm/collect_demos.py`, `logs/demos/turn40.pt`). The script in the training env
(observation noise and resets as in training) succeeded on 781 of 1065 episodes (73%), giving 215,567 samples
(every second step of successful episodes, up to success).

**Trainer** (`--bc-data`, `--bc-pretrain-steps`, `--bc-coef`, `--bc-iters`):
- the actor normalizers are fitted to the demonstrations and then frozen;
- 2000 behaviour-cloning steps (action mean squared error 0.74 → 0.0012-0.0016);
- PPO on fresh rollouts, plus a separate imitation loss on demonstration minibatches, weight 1 fading linearly to 0
  by iteration 1000;
- 50 critic-only iterations first.

The cloned policy before any PPO update, on the held-out tasks (4 placements): 69% success (counter-clockwise 100%,
clockwise 38%), centre drift 0.10 m. With any arm locked it fails, and alone it falls in half the episodes (Spot 2):
it imitates and has not learned to adapt.

**Runs** (`slurm/submit_spot_arm_turn.sh`, settings `slurm/spot_arm_turn.env`). All MAPPO, seed 0, 4096 envs × 24
steps × 2000 iterations, r7 unchanged, no arm-contact reward:

| run | arms | started from | evaluation |
|---|---|---|---|
| T1 `sa_turn_stowed_s0` | stowed | random | stowed, each robot alone |
| T2 `sa_turn_hand_s0` | hand targets | random (PPO alone) | both hands, either arm stowed, both stowed, each robot alone |
| T3 `sa_turn_bc_s0` | hand targets | cloned maneuver, then PPO + fading imitation | as T2 |

Jobs: T1 29238126 (evaluation 29238127), T2 29238128 (29238129), T3 29238130 (29238131). The evaluation is
`turn_inplace.py --checkpoint`: the same 192 held-out episodes, start places exchanged, videos of the same
clockwise and counter-clockwise placement.

What each comparison tells:
- T3 vs T2: what demonstrations add to learning arm use.
- T3 and T2 vs T1: what arm access adds.
- Arm-stowed and partner-parked conditions: whether the trained pair relies on its arms and on its partner.

If T3 improves settling, the next step is IPPO vs MAPPO with the same demonstrations, over several seeds.

**Next, if the pilot learns:** the ordinary approach distance and 40 kg; then the four policies on the ten-object,
20–80 kg benchmark (`eval_coop2.py` already takes these checkpoints); three seeds for B and D. If PPO mostly
body-pushes and barely explores the arms, the next run is MAPPO initialized from planner demonstrations.

## Heavy transport (wave 4, `slurm/submit_spot_arm_heavy.sh`)

Why: on the 1 m / 20 kg pilot task one Spot can move the object, and the pairs learned a role split rather than a
joint push. `sa_mappo_learned60_s0`: in 21 of 120 episodes one robot barely touches the object and the episode still
succeeds (robot 1 idles on right turns, robot 2 on left). On the standard evaluator (long object, 192 episodes,
swapped starts) the Spot-arm pairs spend 6-7% of the time with both robots pushing (armless Spot pair: 40-41%) and
score 4-23% at 40 kg (armless Spot pair 81-86%, ANYmal + Spot 92-94%). The push-share numbers are fractions of
episode time each robot is classified as pushing; they overlap, so the two can sum above one.

"Partner parked" (solo_k) measures reliance on a present partner, not physical need: the ANYmal of the ANYmal + Spot
policy scores 1-3% alone, while the single-robot ANYmal policy succeeds about 80% of the time on the same tasks. The
solo control below is the fair comparison.

Runs (MAPPO, seed 0, from scratch, r7, 4096 envs, 4000 iterations, identical task draws and schedule):

| run | robots | arms |
|---|---|---|
| `sa_heavy_learned_s0` | two Spot-arms | joint-target arms |
| `sa_heavy_stowed_s0` | two Spot-arms | stowed |
| `sa_heavy_solo_s0` | spotarm1 alone (`--solo-agent 0`: partner parked 40 m away, zero actions, its falls do not end episodes) | joint-target arm |

Levels (`--pilot-level` + `--extra-levels`): L0 1 m 18-22 kg; L1 1.5-2.5 m 38-42 kg; L2 2-3 m 40-60 kg. Randomized
rear-side starts (each robot within +-25 deg of behind, at least 60 deg apart, 0.3-0.9 m gap, +-20 deg yaw); goal
heading change 0 / +-60 deg; success 0.10 m / 6 deg held 1 s; 40 s episodes at every level. These are not the
turn-in-place starts (one robot behind, one in front).

Schedule (`--level-mix`, fixed, not adaptive, so every run sees the same exposure): weights L0/L1/L2 0.5/0.5/0 from
iteration 0, 0.3/0.4/0.3 from 800, 0.2/0.3/0.5 from 1600. Object masses are drawn once per env at startup, so at
each phase change every env is reassigned a level and its object mass is redrawn inside that level's window (one
`set_const`); the log prints the realized mass range and distance per level (`[level mix]`).

Evaluation: `pair_eval.py --turn 60 --horizon 40` at 20 kg / 1 m, 40 kg / 2 m and 60 kg / 3 m (`sa-heavy-<run>-*`),
swapped starts, arm ablation and solo_1 / solo_2. For the solo run, solo_1 is the trained condition.

### Results (seed 0, 4000 iterations; `evals/sa-heavy-*`, 120 episodes per cell, swapped starts, 40 s)

| task | pair, arms trained | same checkpoint, arms locked | pair, arms stowed (trained so) | solo control (trained alone) |
|---|---|---|---|---|
| 20 kg, 1 m | 99.2% | 100% | 100% | 100% |
| 40 kg, 2 m | **73.3%** | 43.3% | 40.8% | 0% (object moved 0.7 m of 2) |
| 60 kg, 3 m | 0% (moved 0.50 m of 3) | 0% (0.33 m) | 0% (0.31 m) | 0% (0.10 m) |

- One trained robot does the light task alone (100%), so the light pilot never required teamwork. At 40 kg / 2 m
  the solo policy fails every time and the pairs succeed: the second robot is what makes the heavier task possible.
- On the heavier task the role split disappears: both robots are on the object for about 41% of the episode each, and
  no episode has one robot idle (light task: up to 43 of 120 per seed).
- Arms at 40 kg: arms trained 73.3% vs arms-stowed training 40.8%; locking the arms of the same checkpoint drops it
  to 43.3% (paired: 50 tasks lost, 14 gained). Mostly robot 2's arm (only robot 2's arm free: 70.0%; only robot 1's:
  47.5%). Arm contact is rare (<0.5% of the episode) but forceful (robot 2 mean arm force 28 N vs 8 N for robot 1).
  One seed; check the videos before claiming a mechanism (bracing / yaw correction vs posture).
- 60 kg / 3 m is out of reach in 40 s for every configuration at this budget.

Light ±60° task, all seeds (120 episodes per mode): arms trained MAPPO 99.2 / 100 / 92.5%, IPPO 100 / 97.5%; arms
stowed MAPPO 81.7 / 96.7%, IPPO 90.0 / 100%; locking a trained arm changes nothing (92.5-100%). The one-robot role split
recurs (MAPPO learned s2: 43 of 120). Standard evaluator (long object, 20 / 40 kg): IPPO arms trained 29 / 8%, stowed
90 / 22%, so none of the light-task Spot-arm policies transfer to 40 kg.

Turn in place seed 1 (16 per direction): stowed 94%, PPO hands 100% (seed 0: 84%), demonstrations + PPO 91%; hand
contact 0-5% in every case, so seed 1 confirms seed 0: the learned policies turn with the trunk, not the hands.

## Arm mechanism, torso, release (2026-11-17; `slurm/submit_spot_integration.sh`, no training)

Pusher: `sa_heavy_learned_s0` (iteration 4000), unchanged. Task: the heavy-transport evaluation's (long object,
40 kg, 2 m, goal heading 0 / +-60 deg, 40 s, 20 placements per turn, each with starts exchanged: 120 episodes per cell).

**Torso interface** (`SpotArmActionCfg.torso`, env option `torso=True`). Two outputs after the arm outputs: pitch
(a x 0.2 rad) and height (0.52 m at 0, 0.40 at -1, 0.55 at +1: the posture walker's training range); roll 0;
rate-limited to 0.5 rad/s and 0.15 m/s; action 0 = RAI's default posture exactly. Inputs (4, last in the actor and
state groups): the applied pitch and height - 0.52, and the tracking error (base height - commanded height,
projected-gravity x - sin(commanded pitch)). Older checkpoints load through `marl.expand_state` (new inputs zero
weight, new outputs zero rows): `scripts/spot_arm/torso_compat_check.py` checks the expanded actor's outputs against
the original's every step and that the applied torso stays (0, 0, 0.52); `pair_eval.py --torso-interface` compares
whole episodes. Each robot's command history, torso state and walker state are its own action term's.

1. **Compatibility first** (sweep): the fixed pusher with each walker (RAI, `push_ft_s2_posture`,
   `push_ft_s3_handload`; later `push_ft_s3_ctrl`) and scripted torso commands (`--torso P,H`: default; height
   0.47 / 0.43; pitch 0.1 at 0.52 / 0.47): success, object position and heading error, falls, walking, and 5 s of
   continued control after success. A stronger walker may answer the same high-level commands differently; matched
   pusher fine-tunes only after this.
2. **Arm mechanism** (original walker only, so the system whose arm advantage is explained stays the same): normal
   learned arms; both stowed (`none`); each robot's arm alone (`only_1`, `only_2`); both arms held at RAI's "out" pose
   (`hold_out`) and at each arm's own mean pose while touching the object (`hold_mean`, pose from the first run's
   `arm_pose.json`): does configuration alone explain the benefit?; learned motion with arm-object collisions off
   (`--arm-object-collide off`: only collision bits change, arm mass, inertia and actuation as before; arms still
   collide with the ground and robots): is direct arm contact needed? Each with starts exchanged; per-robot columns.
3. **Completion and release** (original walker): after success, 5 s of continued policy, zero base velocity with the
   arm held where it is, or the arm retracted (stowed, rate-limited) with a 0.2 m/s back-off for 2 s. Retention
   (still within 0.10 m / 6 deg at the end), object displacement and heading change during release, falls. At 40 kg
   2 m and at 20 kg 1 m. Scripted first; training only for a failure that remains.
4. **Next training** after `push_ft_s3_ctrl` (the continuation without applied forces; same parent, budget and
   masses): similar strength without the walking loss -> prefer the simpler continuation; applied forces add strength
   but cost mobility -> more free-walk rehearsal or a gentler load curriculum; force training also helps real
   contact and release -> a focused cooperative task (one pushes, one stabilizes / corrects heading, one object).

### Results (2026-11-18; 120 episodes per cell, 40 kg, 2 m, long object)

**Arm mechanism, RAI walker** (`sa-mech-rai-*`): learned arms 73.3%; both stowed 40.0%; only robot 1's arm 48.3%,
only robot 2's 70.8% (similar with starts exchanged: the effect belongs to actor 2, not a side); held out 0.0%
(the arms block the object); each arm held at its own mean pose 78.3%; learned arms with arm-object collisions off
74.2%. Arm-object contact is 0.0-0.5% of steps with learned arms. The mean poses keep the arm folded (shoulder
pitch / elbow at the stowed values) and yaw it (robot 1 -30 deg, robot 2 +78 deg). Supported: the arm
configuration is sufficient for most of the advantage; direct arm contact and arm motion are not needed. **Not
yet shown:** that it works by shifting the centre of mass (measure CoM, foot loading, trunk attitude, slip before
claiming it). Repeated with s3 (`sa-mech-s3-*`, job 29543942): a stronger walker may shrink the arm advantage.

**Torso sweep** (`sa-sweep-*`, success; rerun spread about +-5 points, RAI default 69-74% over four jobs):

| torso | RAI | s2 | s3 (load-trained) | s3_ctrl (same continuation, no forces) |
|---|---|---|---|---|
| default | 69% | 78% | 94% | 75% |
| height 0.47 | 81% | 87% | 96% | 85% |
| height 0.43 | 79% | 92% | 96% | 78% |
| pitch 0.1, height 0.52 | 55% | 76% | 94% | 57% |
| pitch 0.1, height 0.47 | 66% | 77% | 90% | 66% |

s3's advantage over s3_ctrl supports the load-training regimen (hand and trunk forces with loading / unloading
segments; hand force alone not isolated) over extra training alone. Ramp test (`evals/walker_load/rai_s3_s3ctrl.md`):
held force s3 151-176 N, s3_ctrl 89-108 N, RAI 69-73 N; s3's free-walk velocity error 0.16-0.25 m/s (RAI 0.06-0.09).

**Release, first run: horizon bug.** The evaluator ran 40 s in total including the 5 s release, so a success after
35 s could not finish its window: those episodes counted as not retained with NaN displacement (40 kg: 4 / 87
continued policy, 8 / 83 zero command, 7 / 89 retract), and the zero-command run had one release fall. Fixed in
`pair_eval.py`: success only inside `--horizon`, simulation continues `--release-s` longer, `release_complete`
recorded, rates over complete episodes, and both "inside at the end" and "inside throughout" the window. The first
run's percentages (continued policy 27-49% retained; zero / retract 88-93%) are qualitative only. Rerun with RAI and
s3 as `sa-release-v2-{rai,s3}-*` (jobs 29543940, 29543941).

**Arm mechanism, s3 walker** (`sa-mech-s3-*`): learned arms 95.0%; stowed 90.8% (-4.2 [-10.8, +2.5]); only robot 1's
arm 92.5%, only robot 2's 95.8%; held out 0.8%; mean pose 93.3%; collisions off 96.7%. With the load-trained walker
the arm advantage (RAI: +33 points over stowed) is mostly gone: arm configuration compensates for a weaker
locomotion controller.

**Release, corrected** (`sa-release-v2-*`; every success completed its 5 s window; rates: inside at end / inside
throughout / median displacement / falls in release):

| walker, task | continued policy | zero base command, arm held | retract + back-off |
|---|---|---|---|
| RAI 40 kg 2 m | 42% / 32% / 0.090 m / 3.6% | 100% / 100% / 0.003 m / 0% | 100% / 100% / 0.002 m / 0% |
| RAI 20 kg 1 m | 30% / 3% / 0.136 m / 0% | 97% / 97% / 0.009 m / 0% | 97% / 97% / 0.008 m / 0% |
| s3 40 kg 2 m | 53% / 28% / 0.092 m / 1.8% | 77% / 77% / 0.015 m / 0.9% | 95% / 95% / 0.003 m / 0% |
| s3 20 kg 1 m | 26% / 3% / 0.145 m / 0% | 57% / 54% / 0.042 m / 0.9% | 81% / 81% / 0.011 m / 0% |

Continued control rarely keeps the object in place throughout. With RAI either scripted release holds it; s3 does
not stand still on a zero command (its stop-command velocity error 0.115 m/s vs RAI 0.008 in the ramp test) and
nudges the object, worst at 20 kg: retract + back-off is needed with s3, and still loses 5-19%.

## Spot-arm through the ANYmal pipeline (2026-11-19; `slurm/submit_spot_pipeline.sh`)

Walker: `push_ft_s3_handload` (model_2999; held force 151-176 N on the ramp test, about an ANYmal's 150-165 N in
`evals/beam-push`). Same steps as ANYmal: one robot learns to push the ten objects to their goals, then pairs start
from it.

1. **Solo pusher** `sp_solo_s0` (IPPO, `--solo-agent 0`: partner parked; from scratch; arm learned, hand inputs,
   partner map, r7; ten objects; 6000 iterations). Fixed level mix:
   - L0: 1-1.5 m, 5-20 kg;
   - L1: 1.5-2.5 m, 5-30 kg;
   - L2: 2-3.5 m, 5-40 kg;
   - weights 0.6/0.4/0 from 0, 0.3/0.4/0.3 from 1000, 0.2/0.3/0.5 from 2500.
   Masses match ANYmal's single-robot training (Stage 1b / 2: 5-40 kg, cap rising 15 -> 40 kg).
2. **Shared start:** the solo actor is copied to both robots (`scripts/make_shared_ckpt.py ... spotarm1`, as B0 + B0)
   -> `logs/shared_init/SP_solo_6000.pt`.
3. **Pairs from it, one after the other:** `sp_pair_mappo_s0`, then `sp_pair_ippo_s0` (`--init-actors`, 100
   critic-only iterations, 6000 iterations). Fixed level mix:
   - L0: 1.5-2.5 m; L1: 2-3 m; L2: 2-4 m; 20-80 kg uniform at every level (as ANYmal's ten-object pair runs,
     `--train-mass 20,80`), evaluated at 20 / 40 / 60 / 80 kg;
   - same weights schedule as the solo run.

Jobs (resubmitted with the ANYmal masses): check 29611752, solo 29611753, init 29611754, MAPPO 29611755, IPPO 29611756
(each after the previous).
Not yet queued: the ten-object benchmark evaluation of each stage (eval_coop2 with a Spot task bank).

## Rerun with goal credit and 20 objects (2026-11-19)

`sp_solo_s0` plateaued near 73% (arch 5-15%, dumbbell 8-27%, cylinder 35-50%, the rest 90%+), stopped using the arm
(arm contact 29% -> 2%, trunk 20%) and often walked off the object. Cause in the reward: r7's push_credit paid only
with the trunk's front within 8 cm of the object and only for travel, never for turning, so an arm push and a turn
earned nothing. Cancelled at iteration 3580.

Rerun (`slurm/submit_spot_pipeline.sh`, TAG _gc): `--goal-credit` (`mdp.goal_motion_credit`: the object's motion
toward its goal pose, travel and turning through its radius, x (1 + cos) for the right direction, paid while any part
of the robot, the arm included, touches it with 5 N+; nothing for staying or leaving) and `--arm-bonus 0.25`. The
single robot (`sp_solo20_gc_s0`) trains on the 20 objects of `docs/spot_low_tall.md` (low and tall ones 60%); the
pairs (`sp_pair_{mappo,ippo}_gc_s0`) start from it on the ten objects.

## Restart from the ten-object solo (2026-11-19, runs `sp_*_ft_*`)

`sp_solo20_gc_s0` (from scratch, 20 objects, low/tall 60%) was cancelled at iteration ~2080:
- success ~3% (never above 7%); cube 10%, sphere 49% -> 15% (forgetting); `sp_solo_s0` was at 77% by the same point;
- 30% of episodes ended with the object tipped; arm contact 4%;
- action noise fell to 0.28 by iteration 520, then rose back to its 0.6 cap as learning stalled; the actor learning
  rate sat at its 1e-5 floor while the value loss grew 0.003 -> 1.3;
- jerky motion: 10-20% of the mean actions past their range (bang-bang commands); the action-rate penalty (-0.05)
  cost ~0.12 per episode, too small to matter.

Cause: a from-scratch policy given mostly objects it cannot yet move never learned basic pushing.

Restart (`slurm/submit_spot_pipeline.sh`, TAG _ft):
- `--init-from logs/marl2/sp_solo_s0/model_3800.pt` (~73% on the ten objects); the iteration count carries over, so
  the solo runs 3800 -> 9800;
- the 20 objects drawn evenly (`LOWTALL_BIAS=1.0`; raise once the easy objects hold);
- `--action-rate-w 0.2` (was 0.05), `--action-limit-w 0.1` (was 0.02), `--std-cap 0.4` (was 0.6);
- goal credit and `--arm-bonus 0.25` as before.

`ARM=hand_rate` (`sp_solo20_hr_ft_s0`, `SOLO_ONLY=1`): only the 3 base outputs load from the joint-arm checkpoint
(`expand_state` keeps the base rows when the output shrinks); the 4 arm outputs start at 0 with noise 0.6, capped at
0.4. The pairs (`sp_pair_{mappo,ippo}_ft_s0`) start from the joint-arm solo.

Heading the whole way (same day, before the restart ran): `--yaw-gate 0 --yaw-w 2.0`. `yaw_progress` (signed: paid
for turning the object toward its goal heading, charged for turning it away) used to apply only within 1.5 m of the
goal, at weight 1 (a radian worth 1/3 m of travel); in `sp_solo20_gc_s0` it was ~4% of the progress reward. It now
applies at every distance at weight 2. Only the joint-arm pipeline runs (one GPU for Spot); the hand_rate solo is
not queued. Jobs: check 29717633 (passed), solo 29717634, init 29717635, MAPPO 29717636, IPPO 29717637.

## Arm shaping and 20-object pairs (2026-11-20, runs `sp_*_arm_*`)

Two additions, both from the RAI comparison (their tire-rolling RL policy is rewarded for bringing the torso and end
effector to positions computed from the object's geometry; contacts are otherwise not prescribed):
- `--arm-self-cost 1.0`: contact sensor `self_<robot>` (arm subtree vs body, hips, legs; adjacent links are filtered
  by MuJoCo), cost 1 per second while touching; logged as `Arm/self_touch_<robot>`.
- `--hand-shaping 1.0`: `mdp.hand_target` = the surface point on the side away from the goal (nearest point to one
  radius + 0.3 m behind the object, on the true body-height slice), at 35% of the object's height (0.12-0.40 m: low on
  tall objects so they do not tip, the edge of low ones); `hand_approach` pays the decrease of the hand's distance to it
  (potential-based: leaving takes it back); the actor and critic get the hand -> target vector and distance (4, last);
  logged as `Arm/hand_target_dist_<robot>`.

The pairs now train on the solo's 20 objects at its light masses (5-20 / 5-30 / 5-40 kg levels), so they compare
directly with the single robot (`PAIR_SET=ten` restores the ten objects at 20-80 kg). Jobs: check 29737405 (passed), solo
29737407 (held until the presentation videos are queued), init 29737409, MAPPO 29737410, IPPO 29737412.
