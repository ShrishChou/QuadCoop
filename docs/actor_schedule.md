# Actor schedules and a shared actor (two ANYmals, IPPO)

Status (2026-11-18): S0-S4 trained and evaluated (results below); S5 not implemented or tested. Follow-ups queued:
checkpoint trajectory, fresh-task confirmation, a second continuation seed, and the S4sep initialization control.

**Question.** The ten-object pair plateaus at about 315/480 (parent 315, IPPO continuation 315, MAPPO 316:
`docs/next_wave.md`). Does the way the two actors learn around each other limit it? Five treatments and a control,
all from the same parent, `logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt` (A = anymal1's actor, B = anymal2's).

| arm | what learns | starts from | question |
|---|---|---|---|
| S0 (control) | A and B every iteration | A0, B0 | the matched continuation under exactly these settings |
| S1 | A and B in turn, 100-iteration blocks, A first | A0, B0 | does learning around a temporarily fixed partner build complementary behaviour? |
| S2 | A only; B stays B0 | A0, B0 | how far can one actor improve with the existing B? |
| S3 | B only; A stays A0 | A0, B0 | mirror of S2 |
| S4 | one shared actor on both robots, both robots' samples pooled | the shared start (below) | does pooling make a better, interchangeable controller? |
| S5 | a shared learner with a frozen snapshot partner, promoted per generation | the same shared start | does a consistent partner help the shared policy? |

## Audit (what the code did before this change)

- Two separate actors and optimizers (`MarlTrainer`); MAPPO changes only the critic.
- Both ANYmal actors started from the same single-robot policy, then trained apart (the parent's A and B differ).
- Training starts are not side-fixed: the two bearings are drawn independently from the same distribution and pushed
  apart symmetrically (`mdp.py`, reset), the goal's world direction is random. So "one robot always on one side" does
  not explain the plateau.
- The task bank replays saved bearings / gaps / yaw noise per task, so a sampler change alone would not reach banked
  training; the evaluation's standard formation does fix sides (anymal1 left, anymal2 right); `--swap` exchanges them.
- No robot-ID input; the actors differ by their own weights and observation-group names only.

## Common settings (every arm)

- IPPO, two ANYmals, frozen walkers; r7, partner map, KL anchor 0.05 to the single-robot policy, actor lr cap 1e-4,
  level 4 held, 20-80 kg, ten objects; seed 0; 4096 envs.
- `--init-actors`: actor weights, observation normalizers and action noise exactly as saved; fresh critics and
  optimizers; 100 critic-only iterations; then 2000 actor-training iterations (4000 -> 6100).
- Resets uniform over the fixed bank (`logs/next_wave/bank_ten_s0_k16.pt`, as next-wave arm A), no SGS.
- **Start balance (`--swap-starts`):** at every reset, with probability 0.5, the robots' complete start tuples
  (bearing, gap, yaw noise) are exchanged, after any bank replay, so each actor starts from either place of every
  task. A balance safeguard, not a fix of a proven bug. The bank replay check verifies it
  (`--bank-check --swap-starts`: every robot sits where the bank put the other exactly when swapped; 45-55% swapped).
- Observations unchanged: 42 own inputs + 9 partner inputs (relative position, heading sin/cos, partner velocity in
  this robot's frame, the partner's previous clipped command: history, not its current action) + top and front maps.
- Rewards unchanged: team terms + the robot's own terms.
- Evaluation: the 480 seed-7100 tasks in the standard, flank and goal-behind formations, each also with starts
  exchanged (`--swap`).

## S1-S3: the schedule (`--actor-schedule`)

`joint` | `alt:<N>` | `only:<agent>`. An actor outside the active set gets no forward pass in the update, so no
optimizer step, no Adam state change, no adaptive-lr change, no noise clamp, no KL-anchor or imitation update; its
normalizer is fixed anyway (warm-started actors keep theirs). It still acts with its stochastic policy in the
rollouts (switching it to deterministic would be another treatment). Both critics keep learning. Blocks count from
the first actor-training iteration (`sched_origin`, saved in the checkpoint), so a requeued job continues the same
block and does not repeat the critic-only phase. Rollouts are fresh every iteration (no reuse across blocks).
An actor reactivated continues from its own latest weights and optimizer state.

Logged per iteration: `Schedule/active_<agent>`, `Schedule/actor_updates_<agent>` (at equal env steps each S1 actor
gets about half the updates of S0's; S2 / S3's learner as many as S0's).

**Check (`--schedule-check N`):** after every iteration, the changed actors must be exactly the active ones
(weights, normalizer, noise, Adam step count, lr), and the shared actor must stay identical across robots.

**Block checkpoints.** Checkpoints are saved every 100 iterations (`save_interval`) and the blocks start at 4100,
so every S1 block boundary has its checkpoint: 4100 = (A0, B0) with warmed critics, 4200 = (A1, B0), 4300 = (A1, B1),
4400 = (A2, B1), ... 6100. All are kept (nothing prunes `logs/marl2/<run>/model_*.pt`); S0, S2, S3 have the same
iterations for matched comparisons.

**Evaluations beyond the final one** (after training): S1 at every block boundary (smaller task set, both
assignments); cross pairings of S2's A with S3's B and with S1's B at selected checkpoints.

## S4, S5: the shared actor (`--shared-actor`)

- One actor: every robot's actor uses anymal1's parameters and buffers (tied tensors; `MarlTrainer.tie_actors`),
  each robot reads its own observation groups (`actor_<a>`, `top_<a>`, `front`; the same features from its own
  point of view, map channels in the same order, the partner footprint included) and samples its own action;
  walker states, previous actions and physics stay separate.
- Update: each robot's samples with their own old log-probabilities and advantages; the loss is the mean over both
  robots' samples (equal counts), one backward pass, one optimizer step, one adaptive learning rate (mean KL).
  Not "the same model object in both dict entries" (that would step it twice through slot-specific paths).
- IPPO's two critics stay. No robot-ID input.
- **Shared start.** There is no exact conversion of two actors into one. `scripts/make_shared_ckpt.py` writes
  A0 + A0 and B0 + B0 checkpoints (`logs/shared_init/`); they are evaluated like the parent (A0 + B0), with both
  starting assignments. If one keeps the parent's performance, it is the start of S4 and S5; if both lose much, a
  balanced distillation from A and B (observations from both assignments) comes first, evaluated as shared +
  shared before any PPO. No weight averaging. Any conversion loss is reported separately.
- **S5 (to implement after the shared start is chosen):** learner plus frozen snapshot, assigned to the robots at
  random per episode and fixed for it; training only on the learner's samples (half S4's samples per env step);
  generations of 100 iterations; promotion decided by new + new on a development task set (weak objects weighted,
  overall success and falls as regression guards; rule fixed before the run), new + old in both assignments and
  old + old reported; on promotion weights, normalizer and noise copied into the snapshot, at a synchronized reset.
  The promotion tasks are used again and again, so they are a development set: they come from their own seed
  (not 7100), and the final S5 result is reported on an untouched test set (seed 7100 benchmark and a fresh seed),
  never on the promotion tasks.
  KL reference stays the single-robot policy. No partner pool, no SGS in the first run.

## Shared start: result (2880 episodes each: 480 tasks x standard / flank / goal-behind x starts exchanged)

| pair | success | weakest object (arch) | cylinder | standard / exchanged | flank / exchanged | goal-behind / exchanged |
|---|---|---|---|---|---|---|
| parent A0 + B0 | 64.0% | 37% | 40% | 66.0 / 66.2% | 65.4 / 61.7% | 64.2 / 60.6% |
| A0 + A0 | 62.8% | 25% | 38% | 62.9 / 65.0% | 62.1 / 61.5% | 63.5 / 61.9% |
| B0 + B0 | 63.2% | 39% | 41% | 64.2 / 64.2% | 62.9 / 64.2% | 62.7 / 60.8% |

B0 + B0 is the shared start: 0.8 points below the parent overall (rerun level; the conversion loss, reported
apart from anything S4 / S5 do) and no loss on arch. A0 + A0 loses arch (37% -> 25%). No distillation needed. By mass
(parent / B0+B0): 20 kg 87 / 88%, 40 kg 82 / 82%, 60 kg 58 / 58%, 80 kg 29 / 24%.

## Reading the results

Per-object success and its minimum; object x mass (arch, cylinder, dumbbell especially); standard vs exchanged
starts; falls, robot contact, time to useful contact; object progress in single- and two-robot contact; actor
updates, learner samples and env steps per arm. One seed and GPU nondeterminism (~15% of episodes flip between
reruns): a few tasks' difference is not a gain; promising arms are confirmed on fresh task seeds and more training
seeds. Arch failures are inspected case by case (contacts, access, steering, contact loss, not finishing).

| S1-S3 outcome | to investigate |
|---|---|
| S2 and S3 improve | either actor can learn complementary behaviour around a stable partner |
| only one improves | the actors differ in adaptability or conventions |
| S2 / S3 improve, S1 regresses | successive adaptations undo useful conventions |
| none improves | partner nonstationarity alone does not explain the plateau |

## Runs

| arm | run | training job | evaluation |
|---|---|---|---|
| shared start: parent A0+B0, A0+A0, B0+B0 | - | - | `shared-init-{AB,AA,BB}-ippo-ten-it4000-dev7100` (29490671-3) |
| S0 joint | `asS0_joint_s0` | 29490997 | `as-S0-joint-it6100-dev7100` (29490998) |
| S1 alt:100 | `asS1_alt100_s0` | 29490999 | `as-S1-alt100-it6100-dev7100` (29491000) |
| S2 only A | `asS2_onlyA_s0` | 29491001 | `as-S2-onlyA-it6100-dev7100` (29491002) |
| S3 only B | `asS3_onlyB_s0` | 29491003 | `as-S3-onlyB-it6100-dev7100` (29491004) |
| S4 shared (from B0 + B0) | `asS4_shared_s0` | 29494696 | `as-S4-shared-it6100-dev7100` (29494697) |

## Result (2026-11-18; 2880 episodes each, seed-7100 tasks)

| run | success | arch | falls | paired vs S0 (gained / lost) |
|---|---|---|---|---|
| parent A0 + B0 | 64.0% | 37% | 14.0% | +245 / -256 |
| S0 joint | 64.4% | 32% | 13.1% | - |
| S1 alt:100 | 63.3% | 34% | 13.9% | +255 / -288 |
| S2 only A | 64.8% | 36% | 13.2% | +252 / -242 |
| S3 only B | 63.2% | 35% | 15.0% | +256 / -292 |
| S4 shared (from B0 + B0, 63.2%) | 65.9% | 41% | 12.1% | +264 / -222 |

S4 - S0 = +1.46 points; a paired bootstrap over tasks (the six formation / assignment variants of a task grouped)
gives [-0.07, +2.95] (5000 resamples of the 480 tasks; task uncertainty only, not training-seed variability). S4 also differs from S0 in its
start (B0 + B0, not A0 + B0): S4 is +2.7 over its own start.

**What it shows.** Under this warm start, reward, regularization (KL anchor 0.05, lr cap 1e-4), task bank and
budget (2000 actor iterations, about 197 M joint transitions; each S1 actor 1000 active iterations, S2 / S3's learner
the full 2000), these frozen-partner schedules did not improve the final checkpoint. That does not establish that a
changing partner is irrelevant to the plateau in general, nor convergence.

**Training diagnostics** (mean per bin, S0 / S1 / S2 / S4 alike): training success flat at about 0.59-0.60 from 4300
to 6100 in every arm (the higher 0.67-0.74 before 4300 is start-up bias: the first episodes to end are the quick
successes); actor KL per update about 0.003 with the learning rate at its 1e-4 cap throughout; KL to the
single-robot reference flat at about 0.38-0.48; noise std flat at about 0.79-0.80; no skipped updates; critic loss
falls 4.4 -> 2.3. About half of the actor's mean outputs are beyond +-1.1 (`Policy/out_of_range` 0.47-0.55; S4
0.47-0.52), with `--mean-clip` and `--bound-coef` off: the clipped outputs give the policy gradient nothing to act on,
the saturation problem this repository documented before. A candidate limit on improvement, not yet tested here.

## Follow-ups (queued 2026-11-18)

| what | runs / evaluations | jobs |
|---|---|---|
| checkpoint trajectory, seed 7100 | S0, S1, S4 at 4300 / 4700 / 5100 / 5500 (S1: after full cycles 1, 3, 5, 7) | 29543976-87 |
| fresh tasks, seed 7500 (unused before) | parent, B0 + B0, S0 and S4 at 6100 (`*-fresh7500`) | 29543988-91 |
| S4sep: B0 + B0, two separate actors, joint updates (isolates sharing from initialization) | `asS4sep_bbsep_s0` | 29543956; fresh-task eval 29543992 |
| second continuation seed (fine-tuning variability around this parent, not an independent parent) | `asS4_shared_s1`, `asS0_joint_s1` | 29543958, 29543960; fresh-task evals 29543993-4 |
