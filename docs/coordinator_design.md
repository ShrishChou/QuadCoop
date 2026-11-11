# Learned contact-and-participation coordinator: interface design

Status: interfaces 1–3 implemented and verified by a teacher-controlled integration smoke run (§7). Withdrawal
(stage W) and the trainer are not built yet.

## 0. Frozen for the first learning experiment

Execution stack:
- walker v1;
- turn_debug executor (`logs/keep/marl2/turn_debug/model_15000.pt`);
- current physics;
- `QUADCOOP_CONTACT=train`, `QUADCOOP_CMD_IF=raw`, `QUADCOOP_PLANNER=ends`.

Planner settings stay as trained, including `reselect_s` (3, 6) and the expert's triggers.

The push-direction and force-split calculation (`_update_push`, `_split`) is unchanged. The only learned change is
which contact each robot takes, and in stage W whether it takes part at all.

Known backend limitation, carried into every comparison: the reference often reaches precise rest, but only 0.58 of
its successes are still within 10 cm / 6 deg 5 s later (`evals/e1-repair-acceptance.md`, closure).

## 1. Interfaces in `src/quadcoop/coop2/mdp.py`

| # | interface | code | contract |
|---|---|---|---|
| 1 | request a decision | `_update_command` re-selection block (unchanged schedule) | It picks the eligible envs (`run`): timer, no progress, weak pair, finish, slow arrival, plus the start-up re-plan at 0.1 s; all of them settled and farther than `reselect_min_dist` from the goal. If `g.coordinator` is set, expert-rule envs in `run` go to `g.coordinator(g, ids)`, and other rules keep `_reselect`. |
| 2 | propose | `_propose_expert(ids) -> dict` | The expert's decision, computed with **no state change**. Returns `new`, `cur`, the candidate geometry `p` / `nn` / `pre`, the ordered-pair validity `use`, each robot's route time `t_route`, and `need_more`. This is the teacher label. |
| 3 | apply | `apply_assignment(ids, new, p, nn, pre, t_route)` | The one place an assignment changes state, for the teacher and the learner alike: contact ids, geometry and push direction of changed robots; engagement reset; drift and free timers; reach limit = 1.5 x route time + 2 s; relock record; switch count. It clears the stalled / weak / finish flags of every decided env, including a keep. |

`_reselect_expert` is now `_propose_expert` followed by `apply_assignment`. The computation is identical, with one
exception. The reach limit of a newly assigned contact now uses the route time without the relock penalty. The old
code used the relock-penalised time, which only matters if the expert picks a contact it left less than 3 s ago,
and its 1e6 s penalty makes that practically impossible.

## 2. Action space and joint validity

The actions for each robot are indices into the env's candidate list:
- `0..K-1`: take contact k;
- `K`: withdraw (stage W only, masked out until then).

**KEEP is choosing your current contact.** It is always valid: the current pair is added to the joint mask even when
geometry would now reject it, so no decision can force a switch.

The joint mask is `use[i, j]`: both contacts valid, standing points separated, and robot order kept
(`valid & sep & _order_mask`), plus the current pair. The teacher's remaining rules are its policy, not validity:
- relock (3 s);
- the switch margin (0.15);
- the finishing-zone hold.

The learner may learn them or not.

**Joint sampling is autoregressive** (`coord.py`):
- robot 1 samples from its marginal mask, `joint.any(2)`: contacts with at least one valid partner;
- robot 2 samples from `joint[a1]`, the row fixed by robot 1's choice;
- so every sampled pair is valid. The joint log-probability is the sum of the two conditional log-probabilities.

In stage W, the withdraw row and column are valid for any partner contact, and "both withdraw" is masked out.

**Recorded per decision for PPO:**
- the full joint mask (K x K bool; K ≤ 22) and both conditional masks;
- the sampled actions, the joint log-probability and the value estimate;
- the decision time.

The PPO update recomputes log-probabilities under exactly these masks. `coord.DecisionLog` already records the
time, time since the previous decision, the current / teacher / chosen pairs, the number of valid pairs and the
log-probability for every decision, and `contact_test.py --coordinator` writes `decisions_<mass>kg.csv.gz`.

## 3. Policy (MAPPO)

**Actors:** one network per robot role, or a shared network with a role id. Robot 2's actor also sees robot 1's
sampled action. Each actor scores the K candidates (plus withdraw) with a per-candidate head over candidate
features, so one network handles the different candidate counts per shape.

**Per-candidate features:**
- contact point, normal and standing point in the object frame;
- route time from each robot;
- whether it is the robot's current contact or was left recently;
- the single-contact residual for the wanted motion.

**Shared features:**
- object pose and velocity relative to the goal, and the wanted motion `c_vdes` / `c_wdes`;
- mass class and object shape id;
- both robots' poses and velocities;
- current assignment, engagement, on-contact, and measured force along the push for each robot;
- time since the last decision and the decision cause (`c_plan_reason`).

**Centralized critic:** the shared features plus both robots' features, plus the current pair's residual and the
best pair residual.

## 4. Returns over variable decision intervals (semi-MDP)

Decisions arrive at irregular times. Transition d spans from decision time t_d to the env's next decision (or the
episode end), Δ_d = t_{d+1} − t_d.

- **Reward:** accumulated per env step and discounted by elapsed time, R_d = Σ_τ γ^(t_τ − t_d) r_τ, with γ defined
  per second.
- **Bootstrap:** γ^Δ_d · V(s_{d+1}).
- **GAE:** uses δ_d = R_d + γ^Δ_d V(s_{d+1}) − V(s_d) and per-transition weights (γλ)^Δ_d.
- **Proposed values:** γ = 0.98 / s (about 50 s effective horizon, against 80 s episodes) and λ = 0.95 / s.

Step reward r_τ, team-level only (no per-robot pressing or work terms):
- pose progress: decrease of `pose_error()` (position + scaled heading);
- success bonus, once, at the evaluator's success (10 cm / 6 deg held 1 s);
- time cost per second;
- fall and object-tip penalties, terminal;
- robot-robot collision cost;
- **deployed robot-seconds** cost λ_dep x (active robots) x dt. λ_dep = 0 while learning assignments, then one fixed
  declared value (stage W2).

## 5. Withdrawal (stage W): built only after keep/select works

Requirements and design:
- **State:** `c_active (n, 2)`. Withdraw sets it false. Selecting a contact sets it true, and the robot approaches
  from where it is.
- **Release and waiting location:** an inactive robot backs off its contact, then walks around the object
  (`guide` routing) to a waiting point. The point is on a circle of radius (object circumradius + 1.0 m) around the
  object, as far as possible from the goal direction (out of the swept path) and at least 1.0 m from the partner's
  standing point. It is recomputed when the goal direction changes by more than 45°.
- **Locomotion while withdrawn:** a scripted go-to-pose walker command (the frozen executor only knows how to approach
  and press contacts). It stops at the point.
- **Exclusions while inactive:**
  - its contact is left out of the force split (the active robot gets the full share, using `_split` with one
    contact);
  - readiness (go / hold) treats it as absent, like `c_in_group`;
  - no contact-following, drift or reach-limit triggers for it;
  - no slow-arrival re-plans on its account.
- **Accounting:** its travel distance and its approach / withdraw / wait time are counted separately. Deployed
  robot-seconds = time active.
- **Smoke check before RL uses it:** force withdrawal of robot 2 at a fixed time in a short run, then check:
  - contact released within 2 s;
  - waiting point reached within the reach limit;
  - stays at least 0.5 m clear of the object for the rest of the episode;
  - the partner continues, with share 1.0;
  - no falls.
- **Interpretation:** the teacher never withdraws, so imitation has no withdraw labels. That is not evidence that
  "both active" is optimal.

## 6. Initialization and training

- **BC:** collect (context, teacher label) pairs from teacher-controlled rollouts on the training distribution, with
  keep/select only and both robots active. Because `_propose_expert` is pure, states the student visits can also be
  labelled (DAgger, 1–2 rounds). Report held-out agreement (exact pair; keep vs switch).
- **RL:** MAPPO from the BC weights, with a decaying KL-to-teacher term (0 by the end of the first quarter of the
  budget). It is not tied to the old velocity policy.
- **Distribution:**
  - objects long, arch, dumbbell; 20–60 kg;
  - chosen from the E1 data: object × mass × scenario cells where the reference succeeds in at least 25% of episodes
    (this rule is declared before training);
  - curriculum:
    - **S1:** 1.5 m translations with turns up to 30°, starting at contacts;
    - **S2:** standard scenarios, starting behind;
    - **S3:** more objects and 80 kg (later).
  - Reassignment stays enabled in every stage.
- **Bounded experiment:** seed 0 first, with the env-step budget and checkpoint rule (final checkpoint; held-out
  placement seeds) declared in the run config before launch. If held-out performance improves, add seeds 1 and 2
  with the same setup.
- **Baselines on held-out placements** (same frozen backend):
  - hand-written planner;
  - each robot alone (needs stage W);
  - both always deployed (withdraw masked).

  Report success, settled / precise, falls, capped time **and** deployed robot-seconds; never reward alone.
- **If learning fails, check:**
  - whether the policy changes assignments (switch rate, agreement with the teacher);
  - whether chosen assignments execute (time to engagement, reach-limit hits);
  - whether returns differ between actions (advantage spread per decision).

## 7. Integration smoke run (2026-11-11)

Setup: long, arch, dumbbell; 20 and 40 kg; 4 scenarios x 2 reps; start behind; replanning as trained; traced.

| check | result |
|---|---|
| Teacher through the coordinator path vs the expert path | Identical assignments until the two simulations diverge. That happens at a median 1.8 s; in 33 of 48 episodes it is before the expert's first contact change, so the cause is physics nondeterminism, not the decisions. Success 36/48 (teacher path) vs 42/48 (expert path). The same 48 tasks in the two earlier reference runs (e1s-A, e1s-Aw): 37 and 38. So the expert smoke run was the high one. |
| Mask | 0 of 1,783 teacher decisions and 0 of 790 random decisions fell outside the joint mask. Valid joint pairs per decision: median 204, minimum 70. |
| Arbitrary valid assignments execute (random coordinator, 20 kg) | Success 0.62; one fall in 24 episodes. Contacts reached among assignments held at least 6 s: **0.60** (teacher **0.98**). Executing an arbitrary valid contact is therefore not guaranteed: distant or obstructed contacts often are not reached in time. The learner needs route time as an input, and "chosen but not reached" is a logged failure mode. |
| Decision rate | 40.8 decisions per episode (20 kg). **62% come less than 0.05 s after the previous one, and 62% are slow-arrival triggers.** The teacher keeps the pair in 92% of decisions. |

**Proposed scheduling change for the first learning experiment (awaiting approval):** slow-arrival decisions are limited to one per env
per 1.0 s. All other triggers and the timer are unchanged. The teacher-path baseline is re-run with the same limit so
the hand-written comparison uses an identical schedule.
