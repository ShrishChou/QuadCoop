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
