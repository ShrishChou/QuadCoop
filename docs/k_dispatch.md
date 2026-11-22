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

## Results (2026-11-21; trained on seeds 1001-1003, tested on 7100 + 7900)

Full tables: `logs/evals/k-dispatch/summary.md`, `logs/evals/k-budget/summary.md`.

**The tree.** All nulls fall between -4.6 and +2.5, and every one of their CIs crosses 0.

| | 1 robot | 2 robots | 3 robots | robot 3 at t2 (k3 - k2a) |
|---|---|---|---|---|
| 20 kg | 16% | 78% | 87% | +9.6 [+3.3, +15.4] |
| 40 kg | 8% | 79% | 84% | +5.0 [-0.4, +10.8] |
| 60 kg | 8% | 71% | 74% | +2.9 [-3.3, +9.2] |
| 80 kg | 4% | 29% | 53% | +24.6 [+18.3, +30.8] |
| 100 kg | 3% | 13% | 22% | +8.8 [+4.6, +13.3] |

- With the scripted solo pusher (8% success alone), the 1 -> 2 decision is close to trivial, so 2 -> 3 is the test.
- The need for a third robot is not monotone in mass.

**Dispatch without the mass**, payoff vs the given-mass table (pp):

| lam | no-mass fitted-Q | estimated mass -> table |
|---|---|---|
| 0.05 | -0.3 [-1.9, +1.2] | +0.2 [-1.1, +1.4] |
| 0.1 | -1.3 [-3.4, +0.9] | -2.4 [-4.4, -0.4] |
| 0.2 | -1.2 [-3.3, +0.8] | -3.0 [-4.6, -1.3] |

- Adding the mass to the same fitted-Q predictor changes payoff by -0.6 to +0.7 pp, with every CI crossing 0.
- The blind mass estimate is exact in 39% (t1) and 64% (t2, pair) of tasks. Going through an estimated mass loses;
  predicting the gain directly does not.

**Regret per task.** Hedge's 0.010-0.018 is full information. The other two learners see only the path they took:

| learner | regret per task |
|---|---|
| Hedge | 0.010-0.018 |
| causal EXP4 | 0.055-0.090 |
| Exp3 over whole rules | 0.077-0.19 |

**Cross-K transfer.** The 1 -> 2 threshold is "always add", because the solo pusher is weak.
- At lam = 0.1 it transfers to 2 -> 3 at -0.8 [-2.7, +1.2].
- At lam = 0.2 it fails, at -8.3 [-11.1, -5.6].

This shows the 1 -> 2 data carries no information about when to stop adding robots. It does not show that a common
rule fails.

**Budget-matched 2 -> 3 (`k_budget.py`), 1120 test decisions.**
- Every rule is near the mass rule at the same budget. The one significant gain over it is "mass, then response" at
  a 10% budget: +0.9 [+0.2, +1.6] pp (39 vs 29 extra objects).
- Response only: -0.7 to 0.0.
- Within a mass, the push ranks the tasks. Robot 3's uplift among the top half of the response + mass ranking, minus
  the bottom half:

  | mass | top - bottom | placebo |
  |---|---|---|
  | 20 kg | +4.5 | |
  | 40 kg | +5.2 | |
  | 60 kg | +8.1 | |
  | 80 kg | +16.5 [+4.2, +28.8] (34 vs 17) | -1.7 |
  | 100 kg | +11.7 [+2.2, +21.3] | -0.9 |
  | mean over masses | +9.2 [+3.7, +14.8] | -3.3 [-7.6, +0.8] |

- **Caveat:** the pooled row and the "mass, then response" ranker were added after seeing the per-mass table on these
  test seeds. They need a fresh test tree before they are claimed.

## Confirmation protocol: selective recruitment at 2 -> 3 (frozen 2026-11-21, before any fresh run)

The paper makes two claims, each with its own test:
1. **Selective recruitment (main).** Given a working pair, does the dispatcher predict which pushes benefit from a
   third robot?
2. **Transfer across team sizes.** Can a rule trained at 2 -> 3 make useful 3 -> 4 decisions without retraining? This
   needs a four-robot executor, which is in progress.

**The system:**

| component | decision | how |
|---|---|---|
| Dispatcher | at 20 s, stay at k or recruit one more | learned from simulated outcomes: P(delivery \| h, stay) and P(delivery \| h, recruit), logistic models fitted on both branches; delta(h) is their difference |
| Contact planner | where each robot pushes | model-based search over candidate contacts. The pair planner scores force/moment, travel and contact breaking; the trio planner searches joint triples (`helper_branch.py`) |
| Executor and walker | reach the contact and push | the frozen learned pair executor; robot 3 is a scripted contact controller |
| Hedge / EXP4 / Exp3 | which dispatch rule to trust | the online-learning comparison: full feedback vs the path taken |

Search enumerates contact assignments under an approximate physics score. Full feedback means the dispatcher is
trained on both simulated futures; at deployment it sees only what is observable before the decision. Both branches
keep the planner's normal replanning, and the recruit branch pays the helper's staging and travel.

**Benchmark and inputs:**
- All ten objects at their original dimensions: cube, long prism, sphere, cylinder, arch, dumbbell, T, L, U-channel
  and plus.
- 20 / 40 / 60 / 80 / 100 kg, 4 goal scenarios, 3 placements: 600 starts per seed.
- Delivery: within 10 cm and 6 degrees, held 1 s, by 80 s.
- Inputs: the t2 response features. The mass and object identity are given, and this is declared.

**Data roles:**
- Models are fitted on seeds 1001-1003.
- The baseline and the ask threshold are chosen on 7100 / 7900. Those seeds informed the ranker's design, so they
  are development data.
- The frozen file is `frozen/k_confirm_2to3.json`, and its sha256 is recorded in the commit message. Evaluation on
  the fresh seeds 8101-8106 refits nothing.

**Endpoints:**
- **A (the protocol's primary):** net extra deliveries per 100 helper calls at a 10% budget, "mass, then delta"
  minus the strongest validation baseline. That baseline is mass + object, chosen over random, mass, and most likely
  to fail alone.
  - On the development seeds: +1.9 [-11.5, +14.6].
  - At two-thirds of that effect, 80% power needs about 416 seeds. A is reported regardless, but it cannot confirm.
- **B (the powered test that delta learned about this push):** robot 3's uplift among the top half of delta minus
  the bottom half, within a mass, averaged over the masses.
  - On the development seeds: +9.2 [+3.9, +15.3], placebo -3.3. 4 seeds are needed.
- **C (each team decides alone):** the payoff at cost 0.1 of "recruit iff delta > tau" (tau = 0.087) minus the mass
  rule.
  - On the development seeds: +1.9 [+0.4, +3.3]; tau is in-sample there. 6 seeds are needed.
- **Also reported:**
  - success over all starts and over eligible decisions;
  - rescues, disruptions, calls and helper-seconds;
  - the k2null placebo;
  - one helper per ten teams;
  - the budget curve;
  - delta quintiles (pooled and within mass);
  - object x mass counts, including weak and negative cells.

**On the development seeds, "most likely to fail alone" is worse than random at a 10% budget** (+8 vs +11 net per
100 calls). The hardest pushes are often ones a helper cannot rescue.

**1 -> 2:** the learned-solo late-help result (+9.0 pp) is the supporting evidence. The scripted-solo chain (8% alone)
is labelled separately, as a weak test of selective recruitment.
