# When is a second robot worth deploying? Late help by branching

Question: can early object motion tell a planner when committing a second robot will change the outcome?

Baseline already in hand (Benchmark B, choose on trials 0-4, score on 5-9): dispatching one robot or the IPPO pair
per object x mass uses 1.62 robots per task for 62.8 % success, against 2.00 and 63.3 % for always sending the pair.

## Step 1: does late help work at all? (scripts/branch_help.py)

Frozen pushers: the single-robot parent (s2b-anymal-term80, the policy the pair was initialized from, run through
the pair wrapper) and the IPPO pair (ippo_aa_kl_ten_s0, it 4000). Every Benchmark-B task (12 objects x 4 starts x
5 placements x 20/40/60/80 kg, seed 7100) starts solo, partner parked. After the probe (8 s; 15 s) the whole state
is cloned into a twin env:

* solo branch: the solo robot continues;
* help branch: the partner appears at a staging point 3 m behind the object (w.r.t. the goal), 0.8 m to the side
  away from the pushing robot, facing the object; both robots switch to the pair policy; the partner walks in.

Same deadline (80 s from the start) in both branches. Counted per branched task: rescue (solo fails, help succeeds),
disruption (solo succeeds, help fails), both, neither; by object x mass x start. The probe features (distance and
heading left, contact time, object speed and yaw rate) are saved for step 3. `--check` verifies the clone: both
twins stay solo after the copy and their divergence is reported.

## Step 2: room for a decision-maker

If the same object-mass groups contain both rescues and disruptions, interaction history has something to add over
shape and mass. If late help rarely rescues, keep dispatch at reset.

## Step 3 (only then): a help predictor

Trained on the branch outcomes from the probe features (+ shape, mass), compared against the object-mass rule and a
"call after stalled progress" rule, on fresh placements; main figure: success vs second-robot time committed.

## Pipeline as queued (2026-11-20)

| stage | jobs | output |
|---|---|---|
| 1 -> 2 clone check | 29809403 | log: CLONE CHECK divergence |
| 1 -> 2 test (seed 7100), probe 8 / 15 s | 29809404 / 29809405 | `logs/evals/lh-p8`, `lh-p15` |
| 1 -> 2 training (seeds 1001-1003), probes 8 + 15 s | 29809995-97 | `logs/evals/lh12-p{8,15}-s100x` |
| 2 -> 3 clone check (trio env, robot 3 parked) | 29809998 | log |
| 2 -> 3 test (seed 7100), probe 8 s, 20-120 kg | 29809999 | `logs/evals/lh23-p8-s7100` |
| 2 -> 3 training (seeds 1001-1003) | 29810000-02 | `logs/evals/lh23-p8-s100x` |
| trained trios on the benchmark (+100/120 kg) | 29810003 (IPPO 5500), 29810004 (MAPPO 5600) | `evals/trio-*-dev7100` |

2 -> 3 uses the same policy family: the IPPO pair pushes in the probe, the trio trained from it (trio_ippo_s0) acts
after the third robot is added; the placements are Benchmark B's (the pair draws), robot 3 parked during the probe.

## Analysis (CPU): scripts/dispatch_learn.py

    # basic + regret minimization on 1 -> 2
    python scripts/dispatch_learn.py --train logs/evals/lh12-p8-s1001 logs/evals/lh12-p8-s1002 logs/evals/lh12-p8-s1003 \
        --test logs/evals/lh-p8 --out logs/evals/dispatch-1to2-p8
    # scaling: rules learned on 1 -> 2 only, tested on 2 -> 3 (never seen); online learners adapt there
    python scripts/dispatch_learn.py --train logs/evals/lh12-p8-s100{1,2,3} --test logs/evals/lh23-p8-s7100 \
        --out logs/evals/dispatch-1to2-on-2to3
    # in-domain 2 -> 3 reference
    python scripts/dispatch_learn.py --train logs/evals/lh23-p8-s100{1,2,3} --test logs/evals/lh23-p8-s7100 \
        --out logs/evals/dispatch-2to3

Rules: never / always / object-mass table / stall threshold / predictor (two logistic models, team-size-agnostic
inputs) / oracle; online: Hedge (full information), EXP4 (bandit, the rules as experts), Exp3 (bandit, no inputs);
lam (price of helper time) swept. Checked on synthetic branches: rule ordering as constructed, Hedge regret 0.011
per task, EXP4 0.047, Exp3 0.152.

## Results: the third robot (2026-11-21)

Pair (planner) at 10 s, a scripted helper staged 3 m behind; nets vs the pair continuing alone, 95% paired bootstrap.

Joint direct search vs the add-on helper (hbj-7100 / hbj-7500):

| | 60 kg net | 80 kg net |
|---|---|---|
| null (noise floor) | +2.6 / -0.9 | +0.9 / +3.6 |
| add-on helper (h1) | -9.6 / -12.4 | -2.6 / -4.5 |
| joint planner | -2.6 / +0.9 | **+18.4 / +10.0** |

Re-planning all three contacts removes the add-on's disruption at 60 kg (where a third robot is not needed) and makes
the helper pay at 80 kg, on both seeds.

Move type at the helper's arrival (`movetype_learn.py`, train seeds 1001-1003 = 650 decisions, test seed 7900 = 213):

| test success | 60 kg | 80 kg | all |
|---|---|---|---|
| pair alone | 73.4% | 24.0% | 49.3% |
| add-on helper | 63.3% | 18.3% | 41.3% |
| direct search (move type by score) | 70.6% | 52.9% | 62.0% |
| per-mass table = Hedge (frozen: keep at both) | 78.9% | 54.8% | 67.1% (+5.2 [-1.4, +11.7] vs direct) |
| Exp3 (frozen: move both) | 71.6% | 47.1% | 59.6% |
| net-force score (jnet) | 75.2% | 49.0% | 62.4% |
| best group per task (hindsight) | 89.9% | 72.1% | 81.2% |

- Direct search picks "keep" in only 13-18% of tasks, but keeping the incumbents is the best fixed rule: the contact
  score overvalues moving a robot that is already pushing. Learned "keep" gains +8.3 [0.0, +16.5] at 60 kg.
- Hedge regret 0.033 per decision, Exp3 0.027; with bandit feedback Exp3 still froze to the wrong group (move both).
- The net-force score adds nothing over the per-contact score (+0.5 overall).
- The hindsight gap (+19 pp) is not reachable with mass as the only context.
- Interference: the add-on helper's robot contact is mostly after it arrives (11.5 s / 13.0 s per episode touching after
  vs 2.4 / 2.6 s before); every planned variant cuts the after-arrival touching to 3.5-7 s and halves the incumbent losses
  while touching. The problem is formation, not the approach route.
