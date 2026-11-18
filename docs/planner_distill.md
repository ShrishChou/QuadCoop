# Distilling the contact planner into the shared pair policy (S4)

Status (2026-11-18): code written; smoke test queued. Goal: every object above 60% on the benchmark (S4 at 6100:
arch 40-41%, cylinder 40-44%, dumbbell 57-59%, plus 58-60%; all collapse at 60-80 kg).

**Why.** On arch the S4 robots rarely push at the same time (median co-push share 0% at 40 kg and above, against
34-41% on long and cylinder), and when both push their contacts are about 0.36 m apart (0.55-1.0 m on other
objects): they crowd one spot. The contact planner (expert rule + the Stage 4 contact-conditioned executor
`logs/keep/marl2/turn_debug/model_15000.pt`) assigns separate contacts and reaches 88 / 88 / 65% on arch at 20 / 40 /
60 kg on the four standard scenarios, starting behind, 80 s horizon. The S4 benchmark also uses 80 s
(`eval_coop2.py` default); on its standard formation S4 gets 71 / 62 / 21% on arch at matched masses (different task
seeds). At 40 s (from the recorded success times) the planner gets 81 / 68 / 32% on arch and S4 62 / 33 / 0%: the
planner leads on arch at both horizons; S4 leads on dumbbell (80 s: 100 / 88 / 50 vs 82 / 64 / 52) and is close on
long. A direct comparison on the benchmark's own tasks (all ten objects, 20-80 kg, start behind, seeds 7100 and
7500): `planner-bench-{7100,7500}-expert` (jobs 29561834-5). The S4 actor already sees its partner (position, heading, velocity, last
command; partner footprint on the top map), so the first step teaches it the planner's behaviour rather than adding
inputs.

## Demonstrations (`scripts/distill/collect_planner_demos.py`)

- Teacher: planner expert rule (contacts re-chosen in the env as trained) + the contact executor; robots start
  behind and walk to their contacts; nominal geometry (the planner's tables are built from it).
- Student inputs are a prefix of the teacher's: actor_<a> = the teacher's first 51 numbers (42 own + 9 partner),
  top_<a> (object, partner footprint) and front are identical groups. Recorded: student inputs and the teacher's
  action (clamped to [-1, 1]) every N steps.
- DAgger-style mixing: half the envs are driven by the S4 student (6100), the teacher only labels there, so the data
  covers the student's own states.
- Tasks: hard objects (arch, cylinder, dumbbell, plus), 20-80 kg, random goal distance 2-5 m, direction
  -150..150 deg, heading change +-90 deg (capped by symmetry); seed 9100 (not an evaluation seed).

## Training (`train_coop2.py --bc-data`)

From S4 6100's shared actor (`--init-actors ... --shared-actor`, normalizers kept: `--bc-keep-norm`), fresh critics,
critic-only iterations, behaviour-cloning pretraining (pooled over both robots), then PPO on all ten objects with an
imitation loss on the demonstrations that fades to 0 (`--bc-coef`, `--bc-iters`, counted from the run's start), and
the single-robot KL anchor weakened to 0.01 (the anchor pulls toward the single-robot pushing spot; distillation
would fight it).

Changes to the trainer: pretraining and the fade count from the run's start iteration (`bc_origin`, saved), not
iteration 0; `--bc-keep-norm`; pooled pretraining for the shared actor. Earlier runs (starting at 0) unchanged.

## Read

Per-object success (arch, cylinder, dumbbell, plus by mass) against S4 at matched iterations and the weak-anchor
arm (`asS4_kl001_s0`, same start, no demonstrations); co-push share and contact spread on arch; whether success on
the other six objects holds. Benchmark (seed 7100) and fresh tasks (seed 7500).
