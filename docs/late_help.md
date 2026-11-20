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
