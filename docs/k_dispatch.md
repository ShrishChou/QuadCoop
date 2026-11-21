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

**Step 1, given the mass:**
- a table per (decision, K, mass), chosen by backward induction;
- online learners over mass-threshold rules;
- fitted-Q with the mass as a feature.

**Step 2, no mass given.** The dispatcher sees how the object responds to the push:
- progress rate, speed and yaw rate;
- the robots' measured contact force and the time since the last progress;
- the distance and heading left;
- the object's shape.

It uses this in three ways:
- **est-mass:** estimate the mass from the response, then apply the table.
- **fitted-Q:** logistic success predictors with and without the next robot.
- **Online learners** over struggle rules. A rule adds a robot when rho = (distance left / progress rate) / time left
  exceeds tau.

## Analyses (all CPU, on the five queued trees)

1. **The tree, with a null per comparison.** Each matched effect is shown next to its own null:
   - k2a - k1 and k2b - k1 against k1null - k1;
   - k3 - k2a against k2null - k2a.

   Every leaf is a single rollout.
2. **Dispatch without being given the mass.** Compare the no-mass policies with the given-mass table on payoff.
   - The fair test of what the mass contributes is the same fitted-Q predictor with and without the mass feature.
   - The accuracy of the mass estimate is reported separately. Matching the table on payoff does not show that the
     team inferred the mass: it may only have recognised that progress was enough to finish.
3. **Regret minimization, causal.** Three learners use the same threshold rules:
   - **Hedge** sees every rule's payoff (full information, from the tree).
   - **Exp3** samples one whole rule per task, runs it on its own path and sees only its final payoff.
   - **EXP4** draws the t1 action from the rules' advice at t1. Only the t2 state of the branch taken is revealed,
     and the t2 action comes from the rules' advice on that state.

   Neither bandit learner sees a state the team would not have seen. The gap between Hedge and the bandits is what
   partial feedback costs. The frozen rules are readable thresholds.
4. **Cross-K transfer, at the same time.** At t2 (60 s left), fit a struggle threshold on 1 -> 2 decisions only, freeze
   it, and apply it to held-out 2 -> 3 decisions. Compare it with:
   - the threshold fitted on 2 -> 3;
   - one fitted on both;
   - always keep / always add.

   Report payoff, success and robots sent, with paired differences and the null for that comparison. The reverse
   direction is reported too.
   - **Transfer close to the in-domain rule, and better than the fixed choices:** a reusable K -> K+1 rule.
   - **Transfer fails:** a struggling pair needs help differently from a struggling solo robot, for example because a
     third contact adds crowding.

5. **The main dispatch test: when should a working pair call robot 3? (`scripts/k_budget.py`)** The decision is at
   t2, with the pair still pushing. The solo-robot decision is close to trivial with the scripted solo pusher (8%
   success alone), so the 1 -> 2 step is not the test. Every ranker sends helpers to the same fraction of decisions:
   - **Rankers:** random; the mass rule (training uplift per mass); mass + object; the observed push alone (T-learner);
     push + mass; and the mass order across masses with the push order within a mass.
   - **Scoring:** extra objects at the goal, with paired CIs against the mass rule.
   - **Placebo:** each allocation is also scored with the k2null copy in place of robot 3, so the true value is 0.
   - **Within each mass:** the uplift among the top half of the push ranking against the bottom half. This is the
     question of which 80 kg pushes a helper can rescue.

## Wording for the paper

- The headline is **dispatch without being given the mass**, not "the team infers the mass".
- **Attribution:** the second-robot effect is the gain from dispatching the implemented pair system. The solo robot is
  a scripted pusher and the pair runs a different controller, so the effect cannot be attributed to team size alone,
  and the direction of that bias is unknown.
- **Noise:** each comparison carries its own null; there is no single noise figure.
- **If the no-mass dispatcher loses,** the conclusion is that the tested signals and rules fell short under these
  conditions.
- **Organizing question:** can the same observable sign of struggle tell us when to send the next robot? The runs can
  separate three answers:
  - yes, across both team sizes;
  - yes, but with separate rules;
  - only when the dispatcher knows more about the task.
