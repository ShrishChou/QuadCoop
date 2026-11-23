# MAPPO and IPPO with three and four robots, and whether the KL anchor helps

Status (2026-11-23): queued behind every earlier job (`slurm/submit_marl_teams.sh`). Results for pairs and the
existing trios are below. Four-robot and no-KL rows follow when their runs finish.

**Questions.**
1. Do learned teams of three or four beat the learned pair on the pairs' benchmark, and how do they compare with the
   contact planner's teams?
2. Does the KL anchor to the single-robot pushers help, and does it still help once the robots start from actors that
   already cooperate as a pair?

## Design (fixed before the new results)

Every team starts from the ten-object pair actors at iteration 4000 (`{mappo,ippo}_aa_kl_ten_s0/model_4000.pt`):
- robots 3 and 4 copy robot 1's and robot 2's actors;
- critics start fresh;
- 300 critic-only iterations, then training to 6000.

The rest is the trio recipe of docs/three_anymal.md: r7 reward, actor learning-rate cap 1e-4, ten objects, level 4
held, 20-120 kg, random starts around the object. One seed per cell.

| team | KL 0.05 (as every pair) | no KL |
|---|---|---|
| 3 robots | `trio_{algo}_s0`: the existing run, stopped by pre-emption at 5500 / 5600, continued to 6000 | `trio_{algo}_nokl_s0` |
| 4 robots | `quad_{algo}_s0` | `quad_{algo}_nokl_s0` |

**Evaluation:** the pairs' benchmark.
- Tasks: ten objects × 4 scenarios × 3 reps, seed 7100, 20-120 kg (720 tasks).
- Runs: two per trained model (`<team>-<algo>[-nokl]-it6000-dev7100[-r2]`).
- Films (run 1): arch, long, cube and T shape at 40 and 80 kg, straight and far-turn scenarios, rep 0, filmed
  whatever the outcome (the same tasks for every model).
- Baseline: the pair actors run as four with no training (`quad-transfer-{algo}`). The trio version already exists.

Start formations: pairs at ±35° behind the object; three robots at −50 / 0 / +50°; four at −66 / −22 / +22 / +66°.

**Reading rules.**
- Compare models paired by task, using the mean of the two runs.
- Report 20-60 and 80-120 kg separately: extra robots can only pay off where two are too weak.
- The KL effect is the within-team-size difference (same team size and algorithm, KL 0.05 vs none).

**Code added for this:**
- `--pair anymal4` in `train_coop2.py` and `scripts/eval_coop2.py` (the environment already had four-robot slots),
  plus a four-robot start formation.
- `--warmup-once` (`MarlConfig.warmup_once`). Without it, every resume, including a pre-emption requeue, ran the
  300 critic-only iterations again, and the run still stopped at 6000. An arm pre-empted more often would get fewer
  actor updates. Default off, so existing workflows are unchanged.

**Smoke test (job 30233340)** runs before any training:
- the four-robot wiring check;
- `train_coop2.py --check` with four robots, for MAPPO and IPPO;
- a one-task eval of the pair actors as four.

## Results so far

### Learned trios vs learned pairs (existing runs, one eval each, paired by task)

| | 20-60 kg | 80-120 kg |
|---|---|---|
| MAPPO pair | 76.7% | 19.2% |
| MAPPO trio, pair actors copied (no training) | 54.7% (−21.9 [−27.8, −16.1]) | 22.8% (+3.6 [−0.6, +7.8]) |
| MAPPO trio, trained to 5600 | 58.1% (−18.6 [−24.4, −13.1]) | 24.7% (**+5.6 [+0.6, +10.6]**) |
| IPPO pair | 78.3% | 18.3% |
| IPPO trio, pair actors copied | 48.6% (−29.7 [−35.3, −24.2]) | 13.3% (−5.0 [−9.2, −0.8]) |
| IPPO trio, trained to 5500 | 55.6% (−22.8 [−28.6, −17.2]) | 16.4% (−1.9 [−5.0, +1.4]) |

- A third learned robot costs 19-23 points at 20-60 kg.
- Only MAPPO gains at 80-120 kg, and only +5.6.
- Joint training recovers 3-7 points of what copying the pair actors loses.
- For comparison, the contact planner's third robot, added mid-task in the branched trees, gives 65.1% vs 55.1% for
  the pair overall. Its gain is largest at 80 and 100 kg (+19 and +16) but it is positive at 20 kg too (+10)
  (docs/why_questions.md section 3). The two designs differ: the planner's helper is called at 8 s into a running
  push, while the learned trio starts as three.

### KL anchor, pairs (existing runs, MAPPO, paired by task)

| comparison | n | success | difference |
|---|---|---|---|
| no KL → KL 0.05, seed 0 | 576 | 35.1% → 57.8% | **+22.7 [+18.6, +26.9]** |
| no KL → KL 0.05, seed 1 | 576 | 35.1% → 59.2% | +24.1 [+19.8, +28.3] |
| KL 0.02 → 0.05 | 576 | 55.9% → 57.8% | +1.9 [−1.7, +5.6] |
| KL 0.2 → 0.05 | 576 | 49.7% → 57.8% | +8.2 [+4.2, +12.0] |
| KL 0.05 seed 0 → seed 1 (seed noise) | 576 | 57.8% → 59.2% | +1.4 [−1.9, +4.9] |
| anchor faded out → kept, baseline observations | 480 | 22.9% → 65.0% | **+42.1 [+37.1, +47.1]** |
| anchor faded out → kept, geometry observations | 480 | 29.8% → 64.8% | +35.0 [+29.8, +40.2] |

Falls drop from 23% with no KL to 16% at 0.05; 0.2 raises them to 34%.

- **Helpful, and by a wide margin.** Without the anchor, the pair forgets how to push: 35% vs 58%, and 23% vs 65%
  when the anchor is removed after training.
- **Not sensitive to the exact weight.** 0.02 and 0.05 tie, and 0.2 is too strong.
- **Limits.** MAPPO only, one no-KL seed, training that starts from the single-robot pushers. The team runs above test
  the open cases: IPPO, and teams that start from actors that already cooperate.
