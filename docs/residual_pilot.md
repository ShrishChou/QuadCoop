# Beam-focused residual execution pilot

Status: implemented; 2-iteration check passed (job 28878832: base weights unchanged, correction updated); pilot training launched. Written 2026-11-12, before any training. Changes after results go
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

(none)
