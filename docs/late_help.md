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
