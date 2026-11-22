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

## Four-robot validation (2026-11-22, `k4-check`: seed 1001, 60 and 100 kg, 40 tasks each)

`scripts/chain4_branch.py`; the pair pushes from t = 0, robot 3 joins at 8 s (k3) or 20 s (k3b), robot 4 at 20 s after
robot 3 at 8 s (k4). The first attempt overflowed the constraint buffer (7946 rows at the initial pose against 7500);
njmax is now 10000 for four robots (e353bc2).

- Wiring (`QUADCOOP_PAIR=anymal4 scripts/three_wiring.py`): all four robots move only on their own command, partner
  inputs are the nearest teammate's, 6 robot-robot sensors and 4 fall terms. PASS.
- Joint search: one helper 45-76 ms per env, feasible 91-94%; two helpers (bounded, top 8 contacts each)
  101-108 ms per env, feasible 71%. About 9 of the 24 minutes per mass.
- Helpers press about as often as robot 3 does: fraction of time pressing, robot 3 / robot 4 in k4, 0.29 / 0.21
  at 60 kg and 0.53 / 0.43 at 100 kg (robot 3 in k3: 0.25, 0.52).
- Robot 4 adds no falls: any robot fell in 12% (60 kg) and 33% (100 kg) of k4 episodes, against 12% and 38% in k3.
  Robot 3 joining early does raise the pair's falls at 100 kg (any fall 38% in k3, 35% in k3null, 7% with the pair).

| mass | pair (k2) | + robot 3 at 20 s (k3b) | trio (k3) | + robot 4 (k4) | k3b - k2 | k4 - k3 | k3null - k3 (null) |
|---|---|---|---|---|---|---|---|
| 60 | 75% | 75% | 75% | 60% | +0.0 [-15, +15] | -15.0 [-32, +2] | -5.0 [-20, +8] |
| 100 | 10% | 28% | 20% | 22% | +17.5 [+8, +30] | +2.5 [-15, +18] | +7.5 [-2, +18] |

Reading: four-robot execution works (no overflow, search mostly feasible, helpers press, no extra falls), but on
average a fourth robot is worth about nothing at 20 s. So the 3 -> 4 question is whether a rule can find the few
tasks where it helps, and "always stay" is the baseline to beat. Full trees queued: seeds 1001-1003 (training) and
8201-8202 (test, untouched), all ten objects, 5 masses, 3 reps, split by mass into `k4-s<seed>a` (20, 40, 60 kg) and
`k4-s<seed>b` (80, 100 kg).

## Confirmation results (2026-11-22; fresh seeds 8101-8106, frozen file sha256 55451fd2121b, evaluated once)

3388 eligible decisions (the pair still pushing at t2) of 3600 starts. Nothing refitted. Full output:
`logs/evals/k-confirm/`.

| endpoint | development (7100 + 7900) | confirmation (8101-8106) | placebo | verdict |
|---|---|---|---|---|
| A: net deliveries per 100 calls at 10%, mass-then-delta minus mass + object | +1.9 [-11.5, +14.6] | +3.1 [-3.7, +10.0] | +0.3 [-4.2, +5.0] | not shown (needed ~416 seeds; expected) |
| B: within a mass, uplift of top half of delta minus bottom half (pp) | +9.2 [+3.9, +15.3] | **+11.9 [+9.0, +15.2]** | -0.5 [-3.3, +2.1] | confirmed |
| C: each team alone, ask rule (delta > 0.087) minus mass rule (payoff pp, cost 0.1) | +1.9 [+0.4, +3.3] | **+1.5 [+0.7, +2.4]** | | confirmed |

- Endpoint C uses fewer helpers: the ask rule calls for 49% of pairs and the mass rule for 80%. Success is 63.4% vs
  65.0%, and net deliveries are +20.2 vs +14.3 per 100 calls. The ask rule also beats always recruiting (-3.3 pp for
  that) and always staying (-5.0 pp).
- Measured rescue minus disruption rate rises across quintiles of delta at every mass. Q5 - Q1 within a mass (pp):

  | mass | 20 kg | 40 kg | 60 kg | 80 kg | 100 kg |
  |---|---|---|---|---|---|
  | Q5 - Q1 | +14.9 [+2, +28] | +17.5 [+7, +28] | +8.1 [-4, +21] | +36.8 [+25, +48] | +38.7 [+30, +47] |

  Pooled: +28.3 [+22.8, +33.3].
- "Most likely to fail" is worse than random: +8.0 vs +11.7 net per 100 calls at 10%, 27 rescues out of 339 calls.
  The pushes that are failing are mostly ones a third robot cannot rescue.
- At 10% every call lands at 80 kg, so endpoint A only tests the within-80 kg order, against the object table.
- Descriptive, not an endpoint: delta alone (no mass ordering) gives the most net deliveries at 20-50% budgets, for
  example +190 vs +176 (mass + object) at 20% and +243 vs +214 (mass) at 30%.

Claim for the paper: at 2 -> 3, observing the push identifies which pairs a third robot will rescue, beyond the
mass. The rule confirmed within mass (B) and as a per-team ask rule that beats the mass rule with fewer calls (C). We
did not show that it beats a mass + object lookup table at a fixed 10% budget (A).

## Full four-robot trees, development look (2026-11-22; training seeds 1001-1003 only, test seeds 8201-8202 unopened)

`k_transfer.py`, trained on 1001-1002 and tested on 1003:
- At 3 -> 4, robot 4 for every trio still pushing changes success by -13.3 [-17.5, -9.1] pp (null -0.9).
- The transferred 2 -> 3 ranking has a within-mass gap of -2.8 [-12.3, +6.2].
- The transferred threshold calls robot 4 for 27% of trios and loses 6.2 pp to always staying. The in-domain rule
  learns never to call.

Across 1001-1003 (1391 trio decisions):
- Robot 4 lowers success at every mass: -18, -12, -22, -18 and -6 pp at 20-100 kg. The null is between -2.3 and 0.
- 270 disruptions against 62 rescues. Only 42% of the disruptions include a fall.

Suspected cause (an implementation defect, not crowding): the bounded two-helper search draws the helpers' contacts
from the top 8 by score. A helper's current contact need not be among them, and helpers pay no stop cost, so robot 3
could be moved off a contact it was pushing at when robot 4 joined. The trio search ranges over all K contacts and can
always keep it. Fix: the current, still-valid contact of each present helper is always a candidate. Episodes now log
contact switches per robot from t2 (`switches1-4`).

Check: `k4-check2` (seed 1001, 20 / 60 / 100 kg, 1 rep). Identical to `k4-check` up to t2 and per-mass seeded, so its
k4 arm is a paired comparison of the old and new search. The full trees are rerun only if the fix removes the harm.
The 8201-8202 trees from the old code are not analysed.

### Paired check result (k4-check2) and mechanism

The fix did not remove the harm. Robot 4 changed success by +4.5 (20 kg, n = 22), -26.7 (60 kg) and -12.5 pp (100 kg),
with the null between 0 and +6. Robot 3 switches contacts about as often with robot 4 as without (60 kg: 7.3 vs 9.5
switches after t2). Every robot, the pair included, switches about every 5 s in both arms; that is the planner's
normal re-planning schedule. (Two runs of the same code agree on the trio arm in only 76% of tasks: the GPU solver is
not bitwise reproducible and runs diverge after t2, so cross-run comparisons are not exactly paired.)

On the training trees, 157 of the 270 disruptions ended at the horizon, with a median final position error of
0.18 m (success needs 0.10 m and 6 degrees). The robots touch each other twice as often (23% vs 11% of the time), and
successes are slower (35.8 vs 33.2 s median). Four robots bring the object close to the goal but crowd each other
during the final alignment; no helper ever withdraws. This is a limit of the current controller, not of the
bookkeeping.

### Frozen 3 -> 4 transfer test (stated 2026-11-22 before opening 8201-8202)

System: the chain4 trees as generated (code before 9feaa6f, for training and test alike). Script `scripts/k_transfer.py`,
unchanged since ce2ccaa (sha256 5120f7e37d55...).

    python scripts/k_transfer.py --train logs/evals/k4-s100{1,2,3}{a,b} --test logs/evals/k4-s820{1,2}{a,b} --out logs/evals/k-transfer

Endpoints, on the test seeds' 3 -> 4 decisions:
1. Ranking transfer: the within-mass top-half minus bottom-half uplift for the transferred 2 -> 3 rule.
   Development value -2.8 [-12.3, +6.2]; expected about 0, which would mean no transfer.
2. Threshold transfer: the payoff of the transferred ask rule minus always staying (the best fixed choice
   on the training trees). Development value -6.2 [-8.9, -3.6]; expected negative, meaning the 2 -> 3 rule calls a
   fourth robot that does harm.
3. Secondary: the same for the in-domain 3 -> 4 rule, to show what is learnable at 3 -> 4.
Run once.

### Result (run once, 2026-11-22; train 1001-1003, test 8201-8202; 913 trio decisions, 954 pair decisions)

At 3 -> 4, robot 4 for every trio still pushing: -13.9 [-17.2, -10.8] pp (placebo -2.1).

| endpoint | development (1003) | test (8201-8202) | placebo | verdict |
|---|---|---|---|---|
| 1. transferred 2 -> 3 ranking, within-mass top minus bottom | -2.8 [-12.3, +6.2] | **-11.9 [-17.3, -4.6]** | -3.1 | does not transfer; reversed |
| 2. transferred ask rule minus always stay (payoff pp) | -6.2 [-8.9, -3.6] | **-10.0 [-12.3, -7.9]** | | overcalls: 33% of trios |
| 3. in-domain 3 -> 4 ranking, within-mass top minus bottom | +6.1 [-2.8, +15.0] | +16.2 [+9.2, +22.8] | +2.9 | learnable at 3 -> 4 |

- The trios the 2 -> 3 rule rates most in need of help are the ones robot 4 harms most.
- The in-domain 3 -> 4 rule learns never to call; its ask rule matches always staying.
- At a 10% budget every rule loses deliveries. Best is in-domain at -3.3 per 100 calls; random -13.9, transferred -29.9.
- Same trees, 2 -> 3 (a different design from the kc trees: the pair pushes from t = 0, robot 3 at 20 s). The
  in-domain within-mass gap is +13.7 [+7.0, +19.2] (placebo -3.4), so endpoint B replicates. The in-domain ask rule
  does not beat the mass rule here: payoff 0.535 vs 0.540. Both beat always recruiting.

Reading: a dispatcher learned at one team size must not be reused at the next without retraining. The value of one
more robot changes sign between 2 -> 3 and 3 -> 4 in this system, and the 2 -> 3 rule's signal for "this team needs
help" points the wrong way at 3 -> 4. The harm comes from crowding during the final alignment, with a controller in
which helpers never withdraw. Whether a fourth robot can pay with a controller that lets helpers step back is not
tested.

## Step 1: does robot 4 hurt because it stays too long? (protocol written 2026-11-22, before any run)

The question: did robot 4 do harm because it never leaves, crowding the final alignment, or was its arrival already
counterproductive?

Tree (`chain4_branch.py --withdraw 0.75,0.5,0.3`): the pair from t = 0, robot 3 at t1 = 8 s. At t2 = 20 s the unfinished
trio branches into:
- k3: stay at three.
- k3null: a copy of k3.
- k4: robot 4 joins and stays.
- k4w75 / k4w50 / k4w30: robot 4 joins and withdraws for good once the object's position error first drops below
  0.75 / 0.5 / 0.3 m.

On withdrawal, robot 4 stops pushing and walks straight out from the object, avoiding teammates. It counts as released
1.5 m beyond the object's radius, or after 8 s. The trio re-plans its contacts at once with the trio search. Nothing
else differs between arms. The corrected contact search (9feaa6f) is used everywhere.

Logged per episode:
- t_region: the first time the position error is below 0.5 m (the near-goal region, fixed now).
- Success: 10 cm and 6 degrees held for 1 s.
- helper4_s: robot 4's seconds from joining until released or the end.
- The position error at 30, 40, 50 and 60 s.
- The withdrawal and release times.

Eligible decisions: tasks where the trio is still pushing at t2.

Development (seeds 1001-1003, all ten objects, 5 masses, 3 reps): choose the trigger. The rule is the highest success
over all eligible decisions; within 1 pp, the larger radius wins (earlier release, fewer helper-seconds). Then confirm on
fresh seeds 8301-8302 with arms k3, k3null, k4 and the chosen k4w, evaluated once.

Reported on the confirmation seeds, by arm, over all eligible starts:
- The share entering the region.
- Restricted mean time to the region over the horizon, with never-entered (timeouts, falls) counted as 80 s.
- Success.
- Robot 4's helper-seconds.
- Matched rescues and disruptions against k3. Paired 95% bootstrap over tasks.

Readings, fixed now:
- Finishing interference is supported if k4 enters the region at least as often and as fast as k3 but succeeds less,
  and the chosen k4w recovers success relative to k4.
- If k4 is already slower to the region than k3, the harm is in approach or contact assignment, not in finishing.
- Worth pursuing (justifies calling at all): k4w - k3 success > 0 with the CI above 0, in all masses or in the heavy
  regime (80 + 100 kg); or k4w within 2 pp of k3 on success with a lower restricted mean time to success.
- Merely beating k4 is a controller improvement, not a reason to call.

Amendment (2026-11-22, before any results): three separate findings, each with its own comparison on the same starts.
1. Release improves the controller: success k4w - k4.
2. Calling a fourth robot can pay: success k4w - k3, in all masses or the heavy regime (80 + 100 kg pooled; group size
   checked equal to the sum of its masses).
3. Later, only if 2 holds: a frozen dispatcher using these gains beats a mass + object rule at the same helper budget
   on fresh tasks.

Trios already within a release radius at t2 get a robot 4 that is called and sent away at once, without ever
pushing. Per arm, the analysis counts those starts and the starts where robot 4 never pressed. Every comparison is
also reported on the starts not yet within the largest radius (0.75 m) at t2, alone and in the heavy regime, where
every arm's robot 4 has a transport phase. Analysis: `scripts/k_withdraw.py`.

## Correction (2026-11-22): a planner bug behind part or all of "robot 4 hurts"

In the first k4 trees, a called helper with no feasible assignment at the moment of the call never activated. The
team size still went to k + 1, so the team kept planning around a robot that never came. Its contacts had to be
compatible with the absent robot's planned contact, and the plan's time cost included the arrival time of a robot
that never moved. That happened in 25% of the 3 -> 4 calls (348 of 1391, training seeds). Those tasks lost
-14.4 [-19.3, -9.5] pp, as much as the tasks where robot 4 joined (-15.1 [-17.9, -12.3]).

So the "fourth robot hurts" result, the crowding reading, and the 3 -> 4 transfer result above (f435c68) are not
evidence about four robots. They are superseded and will be redone on fixed trees.

Fixed in chain4_branch: a called helper with no feasible assignment does not join. It returns to parking and the team
keeps its size. The 2 -> 3 confirmation (kc trees, chain_branch) has the same pattern in 4.3% of its decisions
(144 of 3388). Robot 3's effect in those is +5.6 pp, with no sign of harm, so the confirmed 2 -> 3 result stands.

The step-1 development runs were restarted on the fixed code. The withdrawal arms otherwise end a phantom as well,
mixing the bug fix with withdrawal.
