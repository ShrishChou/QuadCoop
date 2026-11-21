# When to add a robot: K -> K+1 dispatch

Question: a team of K robots is pushing an object; is one more robot worth sending, and can the planner tell
without being told the object's weight?

## The system (one planner for every K)

The contact planner (expert rule 4 + the Stage 4 executor `turn_debug/model_15000`) runs every team:

- K = 1: robot 1 alone. Robot 2 is parked, out of the push group (`c_in_group`), and stands idle.
- K = 2: robot 2 appears 3 m behind the object and joins the pair. Its contact is re-planned at once.
- K = 3: the scripted helper appears and the planner chooses all three contacts together (the joint planner of
  `helper_branch.py`, which beat the add-on helper at 80 kg on two seeds, docs/late_help.md).

The dispatcher sits above it and decides twice: at t1 = 8 s whether to add robot 2, and at t2 = 20 s whether to add
the next robot (robot 2 if it waited, robot 3 if it already has two).

## Data: a branching tree per task (`scripts/chain_branch.py`)

    t1: k1 --+-- wait  k1  -- t2 --+-- wait  k1    (1 robot)
             |                     +-- add   k2b   (2, the second at t2)
             +-- add   k2a -- t2 --+-- wait  k2a   (2, the second at t1)
                                   +-- add   k3    (3)
    nulls: k1null (k1 copied at t1), k2null (k2a copied at t2): the simulator's noise floor

Every branch is a full state copy, so every dispatch policy is scored exactly on the same tasks.

Runs: 10 objects x 4 starts x 3 reps x 20 / 40 / 60 / 80 / 100 kg. Training seeds 1001-1003; test seeds 7100 and
7900 (new placements). `kc-check` is the smoke test.

## The dispatcher (`scripts/k_dispatch.py`)

Payoff = success - lam x robots added, with lam = 0 / 0.05 / 0.1 / 0.2.

**Weight-aware (step 1):**
- a table per (decision, K, mass), chosen by backward induction;
- Hedge and EXP4 over mass-threshold experts;
- Exp3 per mass over the four plans.

**Weight-blind (step 2)** sees only how the object responds to the push:
- progress rate, speed, yaw rate, the robots' measured contact force, time since the last progress, and the
  distance and heading left;
- the object's shape, which the planner knows anyway.

The blind methods:
- **est-mass:** estimates the weight from the response, then uses the aware table.
- **fitted-Q:** logistic models of success with and without the extra robot.
- **Hedge / EXP4:** run over struggle-threshold experts. An expert adds a robot when the time the object would still
  need at its current progress rate exceeds tau times the time left. Hedge gets full feedback and EXP4 bandit
  feedback.
- **Exp3:** run over the plans, separately in each struggle bin.

The online learners are trained on the training seeds, frozen, and scored on the test seeds. Results are compared
against the aware table and the hindsight oracle, along with the regret curves.

## How regret minimization fits

The tree gives every branch's outcome. Hedge is therefore the full-information learner. EXP4 and Exp3 see only the
branch they played, which is what a deployed system would see. Their gap measures what bandit feedback costs. The
experts are interpretable rules, so the frozen choice states the dispatch rule directly. An example is "add a second
robot at 8 s if the object would need more than 0.5x the remaining time at its current pace".
