# Beam-focused residual execution pilot

Status: **closed without adoption (2026-11-13)**; see "Pilot 2 outcome" at the end. Pilot 1 (1,500 iterations) was found invalid on review (see Amendments). The frozen turn_debug executor stays the reference; seeds 5000–5002 remain unused. Written 2026-11-12, before any training. Changes after results go
under "Amendments", with a reason.

## Why beam, and what fails

Case selection uses `scripts/exec_failures.py` on the reference e1s-Aw traces, with 12 episodes per object × mass.
A sample counts as **requested** when the planner wants motion, the robot is on its contact, and its commanded
share is ≥ 0.15. This replaces the geometric "push" label.

| requested samples | beam 20 / 40 / 60 / 80 kg | protected (arch, cube, sphere), 20 → 80 kg |
|---|---|---|
| success | 0.75 / 0.42 / 0.00 / 0.00 | 0.33–1.00 |
| force along the push (N) | 29 / 45 / 54 / 57 | 21–149, rising with mass |
| share of requested time off contact | 0.29 / 0.34 / 0.54 / 0.60 | 0.05–0.25 |
| object speed ÷ wanted speed | 1.38 / 0.73 / 0.25 / 0.06 | 0.22–2.36 |
| falls (of 12) | 0 / 1 / 5 / 9 | ≤ 1 |

**Beam fails by losing contact and falling under load, with low useful force.** Force-share error (≈0.4) is the
same on every object, protected ones included, so it does not explain beam.

The next vulnerable group fails differently:
- **cylinder:** turns, 5 of 12 turn failures at 20 and 40 kg;
- **T-shape and plus:** stalls under load (T-shape 9 of 12 at 80 kg).

## Frozen

- walker v1 and current physics;
- the hand-written expert planner (`contact_mix expert:1`) with replanning as deployed (`reselect_s` 3–6);
- push directions and the force split;
- the base executor: turn_debug `logs/keep/marl2/turn_debug/model_15000.pt`.

## Policy

Per robot: action = base(obs) + gate × 0.3 × tanh(MLP(inputs)).

**Base:**
- the frozen turn_debug actor;
- deterministic.

**Correction:**
- **Network:** a new MLP with hidden layers (128, 64).
- **Start:** the last layer is initialised to zero, so the mean equals the base at iteration 0.
- **Exploration:** a Gaussian with a learned scalar std, starting at 0.15 and floored at 0.05.
- **Inputs:** the actor inputs plus `resid_<robot>` (41 numbers):
  - own and partner force on the object, and force along each push;
  - both commanded shares;
  - wanted and actual object velocity and yaw rate;
  - own base velocity;
  - push direction and the contact point relative to the front;
  - contact distance, heading error, and both on-contact flags;
  - a 0.4 s history at 10 Hz of own force along the push, the partner's, object speed along the wanted motion,
    and own on-contact.

**Gate (`resid_gate`):** 1 for objects with the correction enabled. With gate 0 the deterministic action is exactly
the base, so disabled objects keep the baseline by construction.

**Critic and curriculum:** both carried over from turn_debug.

## Training (seed 0, declared budget)

```
ALGO=mappo SEED=0 RUN_NAME=resid_beam_s0 ITERS=1500 EXTRA="--pair anymal --partner-map --contacts --guide --push-cmd \
  --contact-mix expert:1 --reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 \
  --reselect-s 3,6 --random-start 0.5 --need-frac 0.5 --reward rmin --turn-frac 0.3 \
  --residual logs/keep/marl2/turn_debug/model_15000.pt --resid-scale 0.3 --resid-std 0.15 --min-std 0.05 \
  --shape-bias beam:8,cylinder:1.5,t_shape:1.5,plus:1.5,asym:0 --actor-lr 3e-4 --max-actor-lr 3e-4 \
  --critic-warmup 50" sbatch -p mit_normal_gpu -t 06:00:00 slurm/train_coop2.sbatch
```

- **Planner:** the only change from turn_debug's settings is the contact rule, from the training mix (spread /
  random / wrench) to the deployed expert planner.
- **Shape mix:** beam is about 8 / 18.5 ≈ 43% of draws; cylinder, T-shape and plus 1.5 each; the other protected
  objects 1 each (retained examples); asym is not drawn (deferred). Heavy wide objects (`need_frac` 0.5) and turn
  practice (0.3) are as in turn_debug.
- **Starts:** a mix of contact starts and normal approach starts, as turn_debug (`random_start` 0.5,
  `contact_start_at` 0.7).
- **Reward:** `rmin`, unchanged. It contains:
  - pose progress, precise progress, success, failure and own fall;
  - the pull to the assigned contact;
  - contact work: force along the push × the object's motion along the wanted motion. It pays only when the push
    moves the object usefully, so force or contact alone earns nothing.
- **Budget:** 1,500 iterations × 4,096 envs × 24 steps ≈ 147M env steps, about 4 h. One seed.
- **Correction during training:** enabled on every drawn object.
- **Checkpoint rule:** `model_1500.pt`, the final checkpoint. Intermediate checkpoints are not selected.

## Deployment and evaluation

Evaluation uses `contact_test.py` with the standard tasks: 12 objects × 4 scenarios, 20–80 kg, start behind,
`--reselect-s auto`, 80 s horizon. Reference and residual run on identical placement seeds.

1. **Development (seed 4000, 3 reps):**
   - correction enabled on beam, cylinder, T-shape and plus (`--resid-objects beam,cylinder,t_shape,plus`);
   - the baseline is turn_debug on the same seed.

   These results decide the deployment gate. Beam is enabled. Each of cylinder, T-shape and plus is added only if
   its development success − baseline > 0 with falls not higher. The gate is fixed in this file before step 2.
2. **Held-out (seeds 5000–5002, 3 reps each):** the fixed gate against the baseline, all 12 objects. The same
   window and metrics as E1: success, precise, falls, capped time, contact acquisition.

**Acceptance (all on the held-out evaluation):**
- beam success > 40% over 20–80 kg;
- falls overall non-inferior to the baseline, margin 2 points; beam falls not higher;
- protected objects (gate off) success and precise non-inferior on matched placements, margin 5 points. They run
  the identical base policy, so this checks only that nothing else changed;
- gains measured on complete episodes from normal starts, not on segments.

## Amendments

**2026-11-12, after training (review of 082c5a2): the pilot is not a valid test of the intended repair.**
- **Beam and plus were never trained.** The inherited eligibility mask (`TRAIN_NAMES` in
  `src/quadcoop/stage2/shapes.py`) admits only cube, long, sphere, cylinder, arch, dumbbell and T-shape.
  `--shape-bias` reweights after that mask, so the "beam ≈ 43% of draws" statement in Training is wrong. Beam got 0%.
- **The correction can be powerless on saturated commands.** It is added to the raw base output, and the walker
  interface then clips to [-1, 1]. A base output beyond 1.3 cannot be changed by a ±0.3 correction. How often
  this happens in this checkpoint has not been measured.
- **It was active in every phase on every drawn object**, including approach and repositioning, not only during
  contact acquisition and maintenance.
- The development evaluation (seed 4000) was cancelled before any results. `resid_beam_s0/model_1500.pt` is not
  evaluated or deployed. No held-out seeds were used, so 5000–5002 stay reserved.

## Pilot 2: the corrected test (written before its training)

What changed from pilot 1, one item per review finding:

1. **Beam is actually trained.** `--train-shapes beam` replaces the Stage 2 eligibility mask for this run, so
   beam is the only object drawn. The protected objects are not trained and keep the frozen base. The sampler
   counts episode starts by object × 10 kg mass bin (`reset_counts`). The trainer logs the per-iteration
   object shares to wandb (`Resets/frac_<shape>`) and writes the cumulative object × mass table to
   `reset_counts.json` with every checkpoint. The distribution is read from these counts, never inferred from
   weights. Beam is no longer a held-out object for this executor.
2. **The correction acts on the clipped base.** mean = clip(base, −1, 1) + gate × 0.3 × tanh(MLP)
   (`resid_compose: clipped`; the walker clips again). A correction can now pull a saturated command back into
   range.
   - **Action history (review of 9bacf23).** The executor reads its previous raw action (`last_action`), so the
     wrapper must not replace a raw 4 with a clipped 1.
     - **Env action:** per component, wherever the corrected command equals the base's applied command (gate off,
       zero correction, or a push further into saturation), the env receives the base's raw output itself.
       Otherwise it receives the corrected in-range command.
     - **The base's history:** in residual envs, the base's `last_action` input (actor and critic groups) is
       `resid_base_last`. It holds the base's own raw output from the previous step and is zeroed at reset. Where
       the correction is off this equals the walker term's raw action, so the base's inputs and outputs are
       identical to running alone, step after step.
     - **Overridden actions:** in `contact_test.py`, robots whose action is overridden (idle, recipe, replay) get
       the action actually sent as their history.
   - Checkpoints without `resid_compose` (pilot 1) still load with the raw composition and their original action
     history.
3. **Phase gate.** Per robot, the gate is object ∈ `resid_objects` (beam) **and** front-to-contact distance
   ≤ 0.6 m (`--resid-gate-dist 0.6`; on-contact is 0.25 m). That covers the final approach, pressing, and
   recovery after slipping off, but not the walk around the object or repositioning to a far contact.
   - Where the gate is off, the robot runs the base deterministically in training too (no exploration noise).
   - Those samples are left out of the actor loss and the KL estimate.
4. **Fixed difficulty.** Level 4 (distances 3–6 m, turns up to 180°) with the finest tolerance (10 cm / 3°) are
   held, and the first episodes also start there. Mass is drawn from a fixed 20–80 kg window (the evaluation
   range) instead of the level's 50–90 kg. There are no replayed lower levels, and shape weights stay uniform.
   - **Mass:** the physical per-env masses are drawn in that window at startup (uniform in mass, consistent
     inertia scaling), and every training draw asserts that the selected object is eligible and inside the window.
   - **Level and tolerance:** `--fixed-difficulty` requires `--fixed-level`. Level and finest tolerance are set
     before the first episodes are drawn and re-applied after the warm start, which restores the checkpoint's
     curriculum. Every running episode is asserted to use them.
   - Turn practice 0.3 and contact starts 0.5 are as before. The wide-heavy (`need_frac`) episodes are off, since
     they draw other shapes.

### Logged to wandb every iteration (`Resid/*`, per robot)

- the share of rows with the gate on;
- on gated rows:
  - the share of base components past ±1 and past ±1.3, overall and per axis;
  - the mean applied command change of the deterministic and the sampled action;
- on ungated rows: the largest applied change, which must be 0.

### Preflight (`--resid-check 400`, 512 envs, 400 steps per pass)

One short preflight replaces the earlier check. It fails on any missing coverage.

**Zero correction:**
- an independently built turn_debug actor, fed the same observation, gives bitwise the env action sent;
- the walker term received exactly that;
- the applied command is unchanged;
- after every step, the `last_action` the base reads equals what it would read without the wrapper (reset rows
  included).

**±0.2 correction:**
- every in-range component, and every saturated component the correction pulls back, changes its applied
  command;
- the base's history stays its own raw output;
- ungated rows are bitwise the base, and so is their next `last_action`.

**Draw:** only eligible shapes, and only inside 20–80 kg.

**Coverage:** each pass needs at least 1,000 gated and 1,000 ungated rows, 1,000 in-range components, 100
pulled-back components, and 1,000 protected-object rows when protected objects are eligible.

It runs twice:
- **A:** the training flags (beam only), job 28909676;
- **B:** the same flags with all seven protected objects also eligible and gated off, job 28909677.

Both passed (`logs/marl2/resid2_preflight_{beam,mixed}/resid_check.json`):

| | A (beam only) | B (mixed) |
|---|---|---|
| gated / ungated rows, zero pass | 311k / 98k | 40k / 370k (356k protected) |
| every exact-equality check | 0.0 difference | 0.0 difference |
| in-range components changed (±) | 1.00 / 1.00 | 1.00 / 1.00 |
| pulled-back saturated changed (±) | 1.00 / 1.00 | 1.00 / 1.00 |
| raw composition would have changed those | 0.12 / 0.24 | 0.13 / 0.24 |
| base past ±1.3 on gated rows | 0.36 (vx 0.57, vy 0.35, wz 0.16) | 0.37 |
| episodes drawn | 95, all beam, all in 20–80 kg | 216, eligible shapes only, all in window |

So on gated beam rows, the turn_debug base is past ±1.3 on 36% of command components. Under pilot 1's
composition, only 12–24% of the saturated components a correction pulls back would have moved.

### Training check

```
ALGO=mappo SEED=0 RUN_NAME=resid2_beam_s0 ITERS=300 EXTRA="--pair anymal --partner-map --contacts --guide \
  --push-cmd --contact-mix expert:1 --reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 \
  --reselect-s 3,6 --random-start 0.5 --reward rmin --turn-frac 0.3 \
  --residual logs/keep/marl2/turn_debug/model_15000.pt --resid-scale 0.3 --resid-std 0.15 --min-std 0.05 \
  --resid-objects beam --resid-gate-dist 0.6 --train-shapes beam --train-mass 20,80 --fixed-difficulty \
  --fixed-level 4 --actor-lr 3e-4 --max-actor-lr 3e-4 --critic-warmup 50" \
  sbatch -p mit_normal_gpu -t 02:00:00 slurm/train_coop2.sbatch
```

- **Budget:** 300 iterations ≈ 29M env steps, under 1 h, logged to wandb. Checkpoint: `model_300.pt`.
- **Measurement against the frozen baseline:** beam only, standard tasks, 20–80 kg, start behind, seed 4000,
  3 reps, `--trace 2`. `scripts/exec_failures.py --objects=beam` on both trace sets gives:
  - useful force (force along the push while requested);
  - contact loss (share of requested time off contact);
  - falls;
  - success.
- **Extend** the budget on matched success and falls (success up, falls not higher). Contact retention and
  useful force explain the result but are not required to rise: better positioning can move the object with
  less force. The pilot 1 acceptance criteria and held-out seeds (5000–5002) are unchanged and come after
  that.

## Pilot 2 outcome (closed 2026-11-13, written after the results)

Evidence: `evals/resid2_pilot/` (learning curves 0–600, reset counts, `push_endings.md`, the superseded `heavy.py`
with its output). wandb: `resid2_beam_s0` (one run, 600 iterations).

**Results against the frozen baseline (matched beam tasks, 20–80 kg, start behind, 3 reps)**

| checkpoint | seeds | tasks | success base → resid | paired Δ success [95% CI] | falls base → resid | paired Δ falls [95% CI] |
|---|---|---|---|---|---|---|
| 300 | 4000 | 48 | 14 → 18 (29.2% → 37.5%) | +8.3 [−6.2, +22.9] | 18 → 14 | −8.3 [−22.9, +8.3] |
| 600 (preselected) | 4001, 4002 | 96 | 25 → 25 (26.0% → 26.0%) | +0.0 [−7.3, +7.3] | 32 → 27 | −5.2 [−13.5, +3.1] |

- At checkpoint 300, 8 failures became successes and 4 successes were lost; 10 falls were avoided and 6 were new.
- At checkpoint 600, 7 failures became successes and 7 successes were lost; 11 falls were avoided and 6 were new.
- At checkpoint 600, 80 kg had no successes in either arm, and 60 kg went from 0/24 to 1/24.
- After the settling window, 14 of 25 checkpoint-600 successes stayed in tolerance, against 12 of 25 for the baseline.
- The two checkpoints were evaluated on different seeds, so this doesn't show that 300 → 600 made the policy worse.
- Decision: checkpoint 600 doesn't beat its matched baseline and stays below the >40% beam target. The pilot closes
  without adoption: no further extension, and no confirmation evaluation on 5000–5002.

**Training curves (`learning_curves_by50.md`)**
- Iterations 301–600 repeat the shape of iterations 1–300. Early success is high (biased toward episodes that end
  quickly) and settles at 0.35–0.37 (iterations 251–300 and 551–600).
- Falls settle at 0.13–0.16 per robot.
- The policy std reached its 0.05 floor by about iteration 250 and stayed there.
- The mean command change kept creeping up (0.060 → 0.069).
- Reading: success had plateaued with exploration at its floor. The curves alone can't separate a plateau from a
  reward that pays for the wrong behaviour.

**Why requested joint pushes end (`scripts/push_endings.py`, existing traces, CPU only)**

Denominator: time when the planner wants motion and engages both robots, each with a commanded share ≥ 0.15.
Time when only one robot is wanted is excluded.

Definitions matter here:
- The raw 10 Hz contact force pulses with the gait, roughly on and off every 0.3–0.5 s.
- Robots often press 0.25–0.4 m from their assigned point, outside on_contact's 0.25 m drift radius. That happens
  27% of the time at 20 kg and 63% at 80 kg, so the on_contact flag flickers while force is delivered.
- `push_endings.py` therefore uses physical contact and force, each averaged over 1 s.
- The earlier `heavy.py` reading ("both robots press only 3–6% of the time, never longer than 1 s") came from the
  raw signals and is retracted.

With those definitions, for the baseline on seeds 4000–4002:
- **Sustained joint pushing happens on heavy beams.** Both robots press together for 31% of the requested time at
  60 kg and 45% at 80 kg. Pushes of 2 s or more fill 22% and 38% of it, with a 90th-percentile bout of 3.4 s and
  7.2 s. On 80 kg beams that is about 16 s of sustained joint pushing per episode.
- **When joint pushes end, a robot has mostly lost touch.** That accounts for 70–81% of endings at every mass. A
  robot's force drops while it is still touching in 6–21%. Planner reassignment, falls and request changes
  contribute little. During 76–91% of joint-push time at 40–80 kg, at least one robot is off its assigned point.
- **Delivered force levels off.** Inside sustained joint pushes, total force along the command is 184 / 209 / 222 N
  (median) at 40 / 60 / 80 kg, with a 90th percentile of 255 / 293 / 294 N.
- **Per robot, force stays near 120 N at the command limit.** With the forward command held at the walker's 0.8 m/s
  limit, each robot delivers 114–121 N (median) and 167–171 N (90th percentile) at 60–80 kg. About 14% of the force
  is lost to misalignment.
- **Comparison with friction.** Beam friction is randomised over 0.4–0.6, so sliding needs about 235–353 N at 60 kg
  and 314–471 N at 80 kg. The beam moves (≥ 0.03 m/s) in 41% of sustained-push samples at 80 kg, against 98% at
  40 kg.
- Checkpoint 600 shows the same pattern: 225 N median at 60 and 80 kg, and per-robot 118–122 N at the limit.

Reading, narrowed:
- At 60–80 kg, failures happen despite sustained joint pushes. Those pushes deliver less force than sliding needs.
- That force is what the frozen walker produces through its velocity-command interface at its forward limit, in
  these behaviours. It is not the robot's physical capacity, and a walker or interface trained to push harder could
  do more.
- Contact maintenance is still a real loss: lost touch ends most joint pushes, and robots press off their assigned
  points.
- At 80 kg, though, better contact maintenance alone would at best deliver about 2 × 170 N, the bottom of the
  required range.

