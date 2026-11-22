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
