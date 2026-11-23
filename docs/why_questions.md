# Why questions: joint training, the planner's wins and losses, and when one more robot helps

Status 2026-11-22. Three questions, each with the runs that answer it. The corrected 3 -> 4 transfer trees
(docs/k_dispatch.md) keep running alongside.

## 1. What does joint training buy? (existing runs, CPU: `scripts/joint_benefit.py`)

Matched ten-object benchmark (`pres-*`, seed 7100). 480 tasks = 10 objects x 4 masses x 4 placements x 3 repeats,
identical for every system. Runs per task: solo 2, frozen pair 2, IPPO 1, MAPPO 1, planner 2. Output:
`logs/evals/joint-benefit/` (summary.md, figure_data.json).

| mass | solo | frozen pair (2 x solo) | IPPO | MAPPO | planner |
|---|---|---|---|---|---|
| 20 kg | 86% | 71% | 88% | 88% | 82% |
| 40 kg | 78% | 57% | 83% | 81% | 77% |
| 60 kg | 32% | 38% | 62% | 66% | 62% |
| 80 kg | 12% | 19% | 28% | 24% | 42% |
| all | 52% | 46% | 65% | 65% | 66% |

Gain over solo, paired over tasks (pp, 95% CI):
- 20 kg: frozen pair -15.4 [-22.9, -7.9]; IPPO +2.1 [-3.8, +7.9]; planner -4.6 [-12.5, +3.3].
- 60 kg: frozen pair +5.4 [-2.1, +12.9]; IPPO +29.2 [+19.6, +38.8]; MAPPO +33.3; planner +29.6.
- 80 kg: frozen pair +6.2 [+2.1, +10.8]; IPPO +15.0 [+8.3, +22.5]; MAPPO +11.7; planner +29.2 [+21.2, +37.1].

A robot fell in 37.3% of frozen-pair episodes, against 7.5% for solo, 11.7% for IPPO and 3.3% for the planner. The
joint policy driving one robot alone is far below solo: IPPO 15%, MAPPO 9% overall. Joint training does not make a
better single pusher; it makes a policy that depends on its partner.

Why one robot is enough at low mass (failure anatomy, eval_coop2 columns):
- At 20 and 40 kg, solo's failures are mostly "within 0.5 m but heading still off by more than 6 degrees": 88% and 65%
  of its failures. Its timeouts end 0.2 m away but about 50 degrees off. That is a steering or finishing limit;
  solo starts the object moving in 3-4 s.
- At 60 and 80 kg, solo's failures are mostly "moved, then stopped more than 0.5 m short": 56% and 70%. The first 0.25 m
  takes 8.5 and 17.8 s, against 3-6 s for any pair. That is a force limit, which a second pusher relieves.
- The frozen pair's failures are mostly falls: 66-80% at every mass. An extra body without a joint policy collides.

Not in these logs: the fraction of the episode making progress, and goal-directed force per robot. Those come from
the probe runs in section 2.

## 2. Why does the planner win on the arch and lose on the long object?

Benchmark: arch, planner 73% vs MAPPO 31%; long, planner 54% vs MAPPO 77%. The planner's loss on the long object is
not only in turning: straight-ahead 67% vs MAPPO 92%; 60 kg 38% vs 83%.

A. Observe the pushes (queued). `quadcoop/push_probe.py` gives every system the same per-robot measurements, split
   into transport (more than 0.5 m from the goal) and alignment:
   - goal-directed force;
   - turning moment about the centre of mass, signed by the heading still needed, at the robot's front point;
   - |moment|;
   - which side it touches;
   - touching and repositioning seconds;
   - progress and heading gained per phase.

   Arch and long, 20-80 kg, 4 placements x 10 repeats, seed 7100:
   - planner (`logs/evals/probe-planner-expert`, job 30093317);
   - IPPO (`logs/evals/probe-ippo`, 30093312);
   - MAPPO (`logs/evals/probe-mappo`, 30093313).

   The tasks match across systems, but are not the benchmark's exact placements: those depend on the object list.

Cheap checks before B and C (planner, the same objects and probe; queued):
- Mirrored goals: `--tasks mirror`, direction and turn negated (`probe-planner-mirror-expert`). Left/right asymmetry
  points to a sign or wrapping bug.
- Turn in place: `--tasks turn`, the object at the goal position and its heading off by +15, -30, +60 and -90 degrees
  (`probe-planner-turn-expert`). Compares turning each way.
- Robot-index swap: `--swap-actors`, robot 1 runs robot 2's network (`probe-planner-swap-expert`).
- Torque sign: from the probe, the realised moment's sign against the heading actually gained, per phase.

B (intervene on contact choice) and C (direct-force pushes) are not started. They follow the cheap checks.

## 3. When does one more robot help: weight, usable contact space, or interference?

Original footprint: the corrected chain4 trees (`k4c-s*`, docs/k_dispatch.md) have 2 -> 3 and 3 -> 4 branches at
20-100 kg, seeds 1001-1003 (development) and 8401-8402 (test).

Enlarged footprint (`chain4_branch.py --scale 1.5`), fixed in advance:
- Horizontal size factors x 1.5, heights kept. The cylinder scales its length only. The sphere scales its radius, so it
  grows in height too; that is flagged in the analysis.
- At 1.5, faces of 1 m or more fit one more robot at the planner's 0.85 m standing-point spacing.
- Mass unchanged. Inertia stretched to match: pseudo_inertia d1/d2 = ln 1.5, which also scales the centre-of-mass
  offset. Exact for the cube and long; approximate where bar thickness stays fixed.
- The contact-separation rule (standing points at least 0.85 m apart) is recomputed at the new size
  (`scaled_sep`). The nominal table would hide the room the enlargement adds.
- Logged per episode: object radius, mass, Izz; free compatible contacts at each request (n_free, free_best); joined
  or not; arrival and press times; robot-robot contact; falls.

Design: masses 20, 60 and 100 kg; the same seeds as the original-footprint trees (1001-1003, then 8401-8402); the
same arms (stay at k, request k + 1, repeat stay). Validation job 30092686 runs 6 objects at 60 kg, at 1.5 and at 1.0.
The full trees are queued after it passes.

Primary number in every cell: success after the request minus success after staying. Questions:
- At the same mass, does enlarging raise that gain?
- At the same footprint, does more mass raise it?
- Mechanism: feasible joins and arrivals (room), incumbent force and robot-robot contact while the helper enters
  (approach interference), the helper's goal force (useful force), and heading and alignment failures (finishing).

## 4. What the recruitment rule learned

Kept for after section 3 data:
- always stay, always request, mass + shape + footprint, and a learned rule that also sees the push and the free
  contacts;
- fresh seeds at the same helper budget;
- full-feedback fit first, then a bandit with chosen-action feedback only.
Four robots maximum for the class paper.

## Section 2 cheap checks: first results (planner, 2026-11-22)

Arch and long, 20-80 kg, 4 placements x 10 repeats, seed 7100 (320 tasks per run). Paired over matched tasks.
- Mirrored goals (`probe-planner-mirror-expert`): 67% vs 66%, -1.2 pp [-7.5, +5.0]. Arch -3.8 [-11.9, +4.4], long
  +1.2 [-8.1, +10.0]. Per-scenario shifts of 10-17 pp sit inside the noise of 40 tasks. No sign or wrapping bug shows.
- Robot-index swap (`probe-planner-swap-expert`): -5.9 pp [-11.6, -0.3]. The two actor networks are a little
  specialised to their index; not large enough to explain the long-object loss.
- Turn in place (`probe-planner-turn-expert`): arch 82-92% at every size. Long: 98% (+15 deg), 75% (-30), 82%
  (+60), 45% (-90). The -90 task is set to -81 deg, the clamp. The long -90 failures are by mass: 20 kg 70%,
  40 kg 80%, 60 kg 30%, 80 kg 0%. 22 failures, none fell; 21 ended 44-83 deg off, so the object barely turned.
  A heavy long object cannot be turned far in place.
  Next: whether that is the direction or the size. `--tasks turn_mirror` negates the turns, so +90 is run as well
  (job 30114359).
- Torque sign (front-point definition): the sign of the moment agrees with the heading actually gained in 86% of
  transport phases and 60% of alignment phases (turn-in-place alignment 93%). No moment-sign error.

Probe correction: the first version labelled sides by the bounding box. On the arch, the pillar faces lie inside
the feet's box, so a push from behind read as a side touch. The side now comes from the outward surface normal at
the nearest point of the true shape, and the moment is taken at that point (`g.surface_geometry`). Runs on the new
definition, for the cross-system comparison: `probe2-planner-expert` (30114284), `probe-ippo` (30099479),
`probe-mappo` (30099480). The cheap checks above keep the first definition; they only compare planner runs with
each other.

## Section 2B: does revising the contact ranking after failed turns help? (planner ablation, frozen robots)

What the code does now (verified):
- `_propose_expert` adds `stall_penalty` to `j_cur` only. The argmin is still taken over the unpenalised J, so the
  current pair can win again: the penalty moves the threshold, not the ranking.
- Inside the finishing zone a stall sets `c_fin`, not `c_stalled`, so no penalty applies. A switch is allowed only
  when the current pair's residual exceeds `finish_resid`.
- In `probe-planner-turn-expert`, all ten 80 kg long-object -81 deg failures logged 27-38 finishing stalls and 0
  switches (38 is nearly every 2 s window of the episode).

Change (`coop2/mdp.py`, `fail_mem`, episode-local):
J_updated(a) = J_geometry+travel+switching(a) + lambda * sum_j w_j K(a, a_j).
- The penalty goes into the candidate table before the argmin. Keep-or-switch uses the same table with the usual
  margin.
- Evidence is counted once per non-overlapping 2 s window, only during a near-goal turn: within 0.5 m and
  |heading error| > 15 deg at the window's start. Both robots must push on their contacts through the whole window.
- Evidence = 1 - (heading gained / 3 deg), clipped to [0, 1], so slow turning earns partial credit.
- A productive window halves all evidence. A change of turn direction clears it. Reset clears it.
- The penalty applies only during a turn in the direction the evidence was collected for.
- Repeated stalls (evidence >= 2 on the current exact pair) allow the comparison inside the finishing zone.
- Robot identity is kept.

Arms (`contact_test.py --set fail_mem=...`):
- **A, 0.5:** current planner; evidence logged, never used.
- **B, 1:** penalty on the exact failed assignment.
- **C, 2:** similar pushes share the penalty. Per robot, the kernel is
  exp(-|dp / half extents|^2 / (2 x 0.25^2)) x ((1 + n . n') / 2)^8. Same face and direction share it; another face,
  even at the same corner, does not.
- **D, 3:** branch diagnostic. At the same trigger, every assignment with similarity > 0.3 to the stalled pair is
  excluded, and the best of the rest is taken once, without the margin.

All arms share lambda 0.25 per window, the trigger and the margin. The arms run identical trajectories until the
memory first changes a decision, if the simulation is deterministic. Check: A's and B's first verified stall times
(`fm_t_stall`) should match task by task.

Tasks: long and arch at 60 and 80 kg; `--tasks turn` and `turn_mirror` (+-15, +-30, +-60, +-81 deg); 10 repeats.
Controls: arch turns, and long turns of 15-30 deg.
- Development: seed 7100. Settings may change once after it.
- Test: fresh placements, seed 7300, settings frozen.

Outcomes:
- **Primary:** success, paired by task, B / C / D minus A.
- **Mechanism:** heading error 10 s and 20 s after the first verified stall (walking included); switches; the old
  and new assignments and their scores.
- **Orientation-flip check:** seconds commanded against the heading error (`*_wflip_s`).

Readings:
- D > A: the planner overvalued the incumbent pair.
- C > B: the similarity term earns its place.
- B, C and D no better than A: the candidate set lacks a usable turning push, or the executor cannot realise the
  torque.

### 2B development results (seed 7100, 2026-11-23)

Jobs 30143391-98; `logs/evals/fm-dev-{A,B,C,D}-{turn,turn_mirror}-expert`. 320 tasks per arm (long and arch,
60 and 80 kg, eight turns, 10 placements). Paired by task, 95% bootstrap over tasks.

Determinism check failed. Only 49 of 99 first-stall times match between A and B. Tasks where neither arm ever logged
evidence also end differently (0 of 88 identical final states), so the GPU simulation does not repeat itself. The arms
share placements, not trajectories. The comparison is a task-paired one, and D is not a true branch (that needs
`clone_envs`, as in chain4).

| success, gain over A (pp) | n | A | B exact pair | C similar pushes | D forced switch |
|---|---|---|---|---|---|
| all | 320 | 76% | +10.9 [+5.9, +16.2] | +11.2 [+6.2, +16.6] | +5.0 [+0.3, +10.0] |
| long, clockwise | 80 | 49% | +33.8 [+21.2, +46.2] | +32.5 [+20.0, +45.0] | +20.0 [+7.5, +32.5] |
| long, clockwise 60-81 deg | 40 | 18% | +62.5 [+45.0, +77.5] | +60.0 [+42.5, +75.0] | +47.5 [+30.0, +65.0] |
| long, counter-clockwise | 80 | 84% | +3.8 [-5.0, +12.5] | +5.0 [-3.8, +13.8] | +1.2 [-7.5, +10.0] |
| long, 15-30 deg | 80 | 85% | +5.0 [-2.5, +12.5] | +5.0 [-3.8, +13.8] | -2.5 [-11.2, +5.0] |
| arch | 160 | 86% | +3.1 [-2.5, +8.8] | +3.8 [-1.9, +10.0] | -0.6 [-5.6, +5.0] |

Per cell, A then B: long 80 kg -81 deg 0% -> 70%, -60 deg 0% -> 80%; long 60 kg -81 deg 30% -> 90%, -60 deg
40% -> 80%. The controls do not move beyond n = 10 noise.

Mechanism (120 tasks with a verified stall in A, compared on the same tasks in each arm):

| arm | success | memory switch | abs heading error at stall / +10 s / +20 s (deg, median) | finishing stalls |
|---|---|---|---|---|
| A | 62% | 0% | 58 / 47 / 33 | 13.4 |
| B | 87% | 55% | 59 / 50 / 17 | 6.8 |
| C | 86% | 61% | 60 / 50 / 27 | 6.6 |
| D | 73% | 60% | 59 / 54 / 29 | 8.1 |

What the switch is: on heavy clockwise long turns the planner holds the two diagonal corners (candidates 8 and 3,
corners -x+y and +x-y). That is a pure couple of 0.18 m per unit force. The memory's first switch is usually
(8, 3) -> (8, 4): one robot leaves the +x-y corner for the +x long face at y = -0.25, pushing straight in. It worked
in B in 20 of 21 cases. The alternative (9, 3) moves the other robot to the -x face. Both trade a 45 deg corner push for
a flat-face push with a larger lever (0.25 m).

Readings:
- D > A: the planner overvalued the incumbent pair.
- B, C > D: one forced switch is not enough. The memory must keep the stalled pair penalised, or the planner returns
  to it.
- C = B: the similarity kernel adds nothing here. In these tasks there is one alternative and the exact penalty finds it.

Robot-swap check (jobs 30149104/6, `turn-swap-*`, long only, the same tasks as A): clockwise 49% -> 50%, clockwise
60-81 deg 18% -> 20%, counter-clockwise 84% -> 56%.
- Pressing follows the network: at -60 deg, robot 1/2 press fraction 0.14/0.80 becomes 0.60/0.19 when swapped.
- Success does not move. At 80 kg -81 deg, both robots press 84-89% of the time in A and still fail, with 0 switches.
- The clockwise failure is the contact choice, not the walking policy. The counter-clockwise drop is index
  specialisation of the networks (cf. the -5.9 pp swap result).

Open: why the unmodified planner relocks clockwise but switches 6-12 times counter-clockwise. A tie-break by candidate
index (argmin takes the first) would treat mirrored pairs differently. Not yet checked.

Test (seed 7300, settings unchanged from development): jobs 30165806-20, `fm-test-*`.
Films: `presentation_export/05_contact_planner/failed_push_memory/`.

## Protocols fixed 2026-11-23 (before results)

### 2C. Penalty on ordinary deliveries (`slurm/submit_penalty_place.sh bench`)

The 480 ten-object tasks of `pres-planner` (seed 7100; 10 objects x 20/40/60/80 kg x 4 placements x 3 repeats), frozen
walkers and executor. Two runs per arm, because the GPU simulation does not repeat itself.
- **A** (`olp-A-r*`): fail_mem 0.5. Decisions are unchanged from the current planner. It logs every re-plan whose
  decision the memory would have changed.
- **B2** (`olp-B2-r*`): fail_mem 1 with fail_act 2. An assignment is penalised only once it has at least two failed
  windows of evidence. One productive window halves the evidence (below the threshold), so a pair that is moving the
  object keeps its contacts. This differs from the development B, which could act on a single window: in fm-dev B,
  28% of first switches came with evidence below 2.

Unchanged from 2B: evidence counts only near the goal while turning (within 0.5 m, |heading error| > 15 deg). Stalls in
transport are left to the existing stall logic.

Reported:
- Paired success, B2 - A, with tasks the unit (the mean of the two runs); overall and by object and by mass.
- Decisions the memory changes. Counterfactual at every re-plan: the same rule on the table with and without the
  memory (`fm_changed`; first change `fm_t_chg`, `fm_d_chg`, `fm_ae_chg`). Reported as the share of episodes with at
  least one change, and changes per episode, for A (would change) and B2 (did change).

Turning check: B2 is added to the seed 7300 test beside A-D (`fm-test-B2-*`).
Films: run 1 of each arm films every task's rep 0. Curated pairs go to
`presentation_export/06_contact_planner_online_learning/`.

### 3B. 3 -> 4: footprint x entry (`chain4_branch.py --place 1`; `slurm/submit_penalty_place.sh place`)

Leaves at t2 = 20 s, from one decision state per task:
- **k3:** stay at three.
- **k4:** robot 4 is called; the joint search assigns contacts and it walks in from staging.
- **k4p:** a copy of k4 taken right after that assignment. Only robot 4 moves, to the standing point of its assigned
  contact, if the footprint there is clear of the object (>= 2 cm) and of robots 1-3 (>= 5 cm). Otherwise it walks
  in, recorded as place_ok = 0.
- **k3null:** a second copy of k3, as the noise floor.

Scale 1.0 and 1.5; 20, 60 and 100 kg. Development seeds 1001-1003, test seeds 8401-8402. Controller version fixed
across all trees.

The k4s15 trees cannot supply k3 or k4 for this comparison: branches are matched only within one job, and across
jobs the decision states differ. They still give 2 -> 3 at 1.5 and a replication of k4 - k3.

Reported per mass and footprint:
- Delivery: k4 - k3, k4p - k3 and k4p - k4. k4p is reported as requested (every request; a stance that is not clear
  counts as requested) and over the clear stances.
- Entry: requests; joins (a feasible joint assignment); clear stances; arrivals and time to arrival.
- Force: incumbent goal-directed force (robots 1-3, from t2 on); robot 4's force.

Readings:
- k4p > k4 but both < k3: the approach costs, and staying at three is still right.
- k4p > k3 > k4: there is value to recover with a physical priority or routing planner.
- k4 > k3 at 1.5: the scaling result.

### 4B. Does the planner know when to ask? (after 3B)

Decision at t2 in the place trees: recruit robot 4 (k4, physical entry) or stay (k3). Both outcomes are simulated for
every task, so any rule is scored on the same tasks.
- **Rules:** always stay; always recruit; mass + shape + footprint (one threshold); the learned rule, which also sees
  the push and the free contacts (f2_*).
- **Fit and freeze:** rules are fitted and thresholds fixed on development seeds 1001-1003 (both footprints), then
  frozen and scored once on test seeds 8401-8402.
- **Comparison:** at the same helper budget. The mass + shape + footprint rule's threshold is set so it recruits in as
  many test tasks as the learned rule.
- **4 -> 5:** only if 3B shows a fourth robot can add value under at least one condition. The frozen 3 -> 4 rule is
  tried first. A rule refitted on 4 -> 5 data is reported separately.
