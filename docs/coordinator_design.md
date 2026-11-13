# Learned contact-and-participation coordinator: interface design

Status: interfaces 1–3 implemented and verified by a teacher-controlled integration smoke run (§7). Slow-arrival
limit implemented (§1). Policy, rollout buffer, BC and PPO implemented (`src/quadcoop/coop2/coord_learn.py`,
`scripts/coord_train.py`, §3, §6); not yet run at scale. Withdrawal (stage W) is not built.

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

**Slow-arrival limit (approved in review of f6e0f39):** `slow_min_s` (config; `contact_test.py --slow-min-s`).
After a decision taken while a robot was overdue, the slow-arrival trigger is suppressed for that env for
`slow_min_s` seconds. A KEEP leaves the overdue condition true, so without the limit the same question is asked
again on the next control step. Every other trigger and the timer are unchanged. Default 0 (as trained). The first
learning experiment uses 1.0 s for the teacher, the learner and the hand-written baseline alike.

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

## 3. Policy (centralized PPO over the joint assignment)

**Actor (implemented):** one score per ordered pair, s(i, j) = MLP(A·cand_i + B·cand_j + P·pair_ij + Z·shared).
The joint policy is the masked softmax over the K × K scores. It is sampled autoregressively: robot 1 from its
marginal (log-sum over valid partners), then robot 2 from the row fixed by robot 1's choice. The stored joint
log-probability equals robot 1's marginal plus robot 2's conditional log-probability, and PPO recomputes it
under the stored mask. This replaces the per-robot heads first proposed. It conditions robot 2 on robot 1's choice
exactly, and the teacher's own cost is defined per pair. With a third robot (K³ pairs) it would need a factored
form again. Withdraw will be one extra row and column.

**Pair features (implemented):** the expert's own intermediate quantities, exposed by `_propose_expert`:
- pair residual;
- J minus J of the current pair (clipped);
- the slower robot's arrival time;
- whether it is the current pair.

The teacher's decision itself is never an input.

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

Implementation (`scripts/coord_train.py`, `slurm/coord_train.sbatch`):
- rollouts run `contact_test.py --coordinator external` in-process, so success, failure and horizon are the
  evaluator's own;
- `collect` records teacher (or policy) rollouts with the teacher label at every decision;
- `bc` trains imitation plus a critic on discounted returns, with held-out seeds;
- `rl` runs PPO with semi-MDP GAE and a decaying teacher cross-entropy term. The budget and checkpoint rule are
  written to `run.json` before the first iteration, and a run will not resume under a different configuration;
- `contact_test.py --coordinator learned --coord-ckpt X` evaluates a policy greedily.

Imitation metrics (KEEP dominates teacher labels, so overall accuracy is not reported alone):
- exact pair accuracy, overall and on keeps;
- switch recall;
- exact accuracy on teacher switches;
- false-switch rate.

Switch decisions are up-weighted to 30% of the loss.

Declared task cells: long, arch, dumbbell × 4 standard scenarios × 20/40/60 kg, start behind. Pooled e1s-A + e1s-Aw
reference success is ≥ 25% for 35 of the 36 cells. Excluded: dumbbell / D_far_turn / 60 kg (0.17). Its episodes run
but are not recorded.


- **BC:** collect (context, teacher label) pairs from teacher-controlled rollouts on the training distribution, with
  keep/select only and both robots active. Because `_propose_expert` is pure, states the student visits can also be
  labelled (DAgger, 1–2 rounds). Report held-out agreement (exact pair; keep vs switch).
- **RL:** centralized PPO over the joint assignment (one policy chooses both robots' contacts; sampling robot 1 then robot 2 does not make it decentralized MAPPO), from the BC weights, with a decaying KL-to-teacher term (0 by the end of the first quarter of the
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

**Scheduling change (approved):** slow-arrival decisions are limited to one per env per 1.0 s (`slow_min_s`, §1).

### 7b. Follow-up checks (same 48 tasks)

| check | result |
|---|---|
| Adapter parity (`--coordinator parity`): at every decision, snapshot every env-state tensor, run `_reselect_expert`, restore, run the coordinator path, compare | **0 differing state tensors in 13,131 env-decisions** (3,830 at 20 kg, 9,301 at 40 kg; as-trained schedule). Success 37/48. Scope: `_reselect_expert` itself now calls `_propose_expert` and `apply_assignment`, so this shows the coordinator adapter matches the current expert wrapper. It is **not** an independent comparison against the pre-refactor implementation. That rests on the code review in §1 (one known deviation: the reach limit's relock term). |
| Slow-arrival limit 1.0 s, teacher path | 18.5 decisions per episode (37.1 without), **0% within 0.05 s of the previous one (58%)**, KEEP 0.81 (0.92). Switches per episode 3.5 (2.9–3.5 without). Success 36/48 (36–37 without), precise 35. Masks: 0 outside. |

Caveats: the smoke uses three relatively favourable shapes at 20/40 kg, so its ~75% success is not comparable with
the full suite's 57%. The random coordinator samples uniformly at each conditional stage, which is not uniform
over joint pairs: it is a sampling smoke test, not a performance baseline.

### 7c. Training pipeline smoke (job 28735652, 2026-11-11)

Collect, BC, one PPO iteration and a greedy evaluation of the result, each on 12 episodes at 20 kg with a 30 s
horizon:
- all stages ran;
- 0 decisions fell outside the joint mask;
- the transitions closed and GAE was computed.

The BC policy (5 epochs on 105 decisions, effectively untrained) took 20 kg success to 0.17 (teacher 0.58–0.83 on the
same settings). An unimitated assignment policy is therefore harmful, so RL starts only from a BC policy with
adequate switch metrics.

## 8. Seeds (reserved 2026-11-11)

| use | placement seeds |
|---|---|
| BC data (teacher collection) | 100–104 train, 105 held out |
| Closed-loop BC vs teacher check | 2000 |
| PPO pilot rollouts | 200–223 |
| Smoke and pipeline tests (used; never for final results) | 0, 90, 91, 1000 |
| **Final comparison: teacher, BC, final PPO** | **3000–3002**, not used before the final evaluation |

## 9. Full-data BC (2026-11-11)

Data: teacher collection on seeds 100–105. That is 2,592 episodes, or 2,520 without the excluded cell, and 49,001
recorded decisions. Seeds 100–104 are used for training (41,145) and seed 105 is held out (7,856). Teacher
switch share: 0.17 overall (20 kg 0.26, 40 kg 0.17, 60 kg 0.12). Training ran 40 epochs, with switches weighted to
30% of the loss.

| held-out (seed 105) | n | exact pair | exact on keep | switch recall | exact on switch | false switch | critic R² |
|---|---|---|---|---|---|---|---|
| 20 kg | 2,129 | 0.977 | 0.982 | 0.987 | 0.960 | 0.018 | 0.70 |
| 40 kg | 2,688 | 0.987 | 0.991 | 0.987 | 0.969 | 0.009 | 0.60 |
| 60 kg | 3,039 | 0.993 | 0.997 | 0.978 | 0.965 | 0.003 | 0.47 |
| all | 7,856 | 0.987 | 0.991 | 0.985 | 0.964 | 0.009 | 0.60 |

**Closed-loop check:** seed 2000, identical tasks, 80 s horizon, `--slow-min-s 1.0`, greedy BC against the teacher.
Excluded cell removed: 210 episodes per arm. Intervals are paired bootstrap 95% CIs over tasks.

| | success | precise | fell | capped time (s) |
|---|---|---|---|---|
| teacher | 0.781 | 0.671 | 0.010 | 44.4 |
| BC | 0.748 | 0.590 | 0.014 | 44.3 |
| BC − teacher | −0.033 [−0.100, +0.029] | −0.081 [−0.171, +0.005] | | |

BC's on-policy agreement with the teacher's label, measured in BC's own states:
- 0.985 / 0.987 / 0.993 at 20 / 40 / 60 kg;
- switch recall ≥ 0.99;
- false switches ≤ 0.9%.

No collapse, so no DAgger round. The precise gap is not resolved at this sample size and is watched in the final
comparison.

**PPO pilot launched:** `logs/coord/rl_s0`, jobs 28767151 and 28767152 (chained resume). 24 iterations; each is one
mass × 144 episodes, cycling 20/40/60 kg on seeds 200–223. All other settings are frozen as in §0 and §1. The
reward is fixed per `RewardCfg`; the configuration and checkpoint rule are in `run.json`.

## 10. Final comparison: teacher vs BC vs PPO (seeds 3000–3002, 2026-11-12)

Setup: greedy policies, identical tasks and settings, 1,260 matched episodes per arm with the excluded cell removed.
Full table: `evals/coord-rl_s0/final_comparison.md` (`scripts/coord_compare.py`). Intervals are paired bootstrap
95% CIs over tasks.

| | success | precise | fell | capped time (s) |
|---|---|---|---|---|
| teacher | 0.752 | 0.652 | 0.024 | 44.3 |
| BC | 0.744 | 0.626 | 0.024 | 44.1 |
| PPO (final) | 0.737 | 0.629 | 0.024 | 44.6 |
| PPO − teacher | −1.6 [−4.4, +1.3] | −2.3 [−5.6, +1.0] | +0.0 [−1.2, +1.1] | +0.4 [−1.0, +1.8] |
| PPO − BC | −0.8 [−3.6, +1.9] | +0.2 [−3.2, +3.6] | | |

**Dumbbell (replicated on fresh seeds), vs the teacher:**
- BC: success −5.3 [−10.4, 0.0], precise −8.3 [−14.4, −2.0];
- PPO: success −5.6 [−10.9, 0.0], precise −6.3 [−12.6, −0.3].

Contact acquisition is unchanged across arms (0.78 of assignments reached), as are switches per episode (about 10).

The PPO training log (`evals/coord-rl_s0/log.jsonl`) shows the policy barely departed from BC:
- entropy 0.02–0.06 nats;
- sampled-action agreement with the teacher 0.96–0.99;
- KL per update about 0.001–0.002 and about 1% of samples clipped.

**Conclusion:** PPO did not improve contact selection over the teacher, and BC adds a dumbbell regression. The
contact-selection-only line is closed. No further contact-selection-only runs; the hand-written planner stays the
deployed assignment rule. Next (separate record): the beam-focused residual execution pilot, then solo-vs-pair
participation using the real Stage-2b solo policy.
