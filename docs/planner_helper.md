# The contact planner with a third, helper robot for heavy objects

Status (2026-11-19): tested (jobs 29612016-17, `evals/helper-{7100,7500}/summary.md`). The helper adds +7.5 to +13 pp
at 80-100 kg over the same pair, but costs 7.5-13 pp at 60 kg; overall not significant.

## Why: two ANYmals run out of force

Scripted engaged-start beam push (`scripts/beam_push_test.py`: the robots start against the beam and walk straight
into it, 20 s, friction 0.4 / 0.5 / 0.6):

| robots | mass | moved >= 1 m | beam travel (m, friction 0.4 / 0.5 / 0.6) | force delivered (N) | sliding force mu m g (N, at 0.5) |
|---|---|---|---|---|---|
| 2 (`evals/beam-push`) | 80 kg | 4/9 | 2.7-5.9 / 0.4-1.0 / 0.16-0.20 | 292-307 | 392 |
| 2 (`evals/beam-push2-heavy`) | 100 kg | 0/6 | 0.74-0.92 / 0.13-0.16 / 0.04-0.07 | 303-322 | 490 |
| 3 (`evals/beam-push3`) | 80 kg | **6/6** | 8.5-8.9 / 3.9-5.1 / 1.4-1.9 | 350-370 | 392 |
| 3 | 100 kg | 2/6 | 0.9-2.8 / 0.9-1.4 / 0.16-0.28 | 391-413 | 490 |
| 3 | 120 kg | 2/6 | 1.3-1.4 / 0.1-0.3 / 0.03-0.08 | 415-416 | 589 |

- Each ANYmal delivers at most about 150-165 N. The planner assumed 250 N (`robot_push_force`, "to be measured"), so
  it never flagged 80 kg as too heavy for a pair.
- Three robots deliver about 1.3x a pair's force (they are all in contact only 37-54% of the time), which is enough
  for 80 kg at every friction tested, and for 100-120 kg only at low friction.
- On the planner benchmark, success at 80 kg falls to 0-58% on every sliding object (cube 42, long 29, beam 0); the
  sphere, which rolls, stays at 92%.

## Change

The planner keeps planning a pair; the third robot is a helper outside that optimisation, so the planner's (n, 2)
buffers are unchanged.
- `quadcoop/coop2/mdp.py`: `PLAN = AGENTS[:2]`, the planner's two robots; per-robot loops in contact mode use it.
  `c_cap_mult` (per env) multiplies `robot_push_force` in `robot_cap` and in the contact pick. A third robot starts at
  its own placement.
- `quadcoop/coop2/env_cfg.py`: `make_coop2_env_cfg(helper=True)` (play only) allows three robots with contacts. The
  helper gets the plain, non-contact inputs, and its planner-based reward terms are not built.
- `quadcoop/coop2/pairs.py`: `QUADCOOP_HELPER=1` makes robots 1 and 2 each other's partner input (as trained), not
  the nearest teammate.
- `scripts/helper_test.py` drives robots 1 and 2 exactly as `planner-bench` does (expert rule 4 + the Stage 4
  executor `turn_debug/model_15000.pt`). The helper is the scripted `ContactController`:
  - **engage:** when the planner's own force model says the current pair cannot slide the object as wanted
    (`current_strength() < 1` for 0.5 s, with the measured 160 N); it then stays engaged;
  - **planner:** once engaged, the env's force limit is multiplied by 1.3 (measured above), so the pair plans with
    the team's force;
  - **contact:** a free candidate contact, not one of the pair's and with its standing point clear of theirs, whose
    push direction best matches the wanted motion, near the centre of friction unless a turn is wanted, never
    against the motion; re-chosen every 2 s; it walks there around the object and pushes along the normal.

## Test (`slurm/helper_test.sbatch`)

Arms, on the same tasks and in one env build per mass (the helper is parked 40 m away in the pair arms):
- **pair250:** the planner as in `planner-bench`;
- **pair160:** the same pair with the measured force limit;
- **helper:** pair160 plus the helper.

Tasks: the ten benchmark objects x 4 scenarios x 3 reps, 60 / 80 / 100 kg, start behind, 80 s, seeds 7100 and 7500.
Robots 1 and 2 use contact_test's seeded placements; the helper starts 1.2 m further out, straight behind the object.

Caveat: building a third robot changes the startup random draws (object friction), so pair250 matches `planner-bench`
statistically, not draw for draw. The paired comparisons are between arms inside this test.

Read:
- helper − pair160 and helper − pair250, per mass (paired bootstrap over tasks);
- per-object success at 80 kg (target: every object at or above 60%);
- how often the helper engages, its pushing time and force, helper falls, robot-robot contact.

## Results

Success % (all ten objects, 120 tasks per arm and mass per seed; seeds 7100 / 7500):

| arm | 60 kg | 80 kg | 100 kg |
|---|---|---|---|
| pair250 | 50 / 64 | 38 / 35 | 20 / 18 |
| pair160 | **68 / 78** | 32 / 28 | 10 / 10 |
| helper | 60 / 64 | **39 / 38** | **18 / 23** |

Paired differences (pp, 95% bootstrap):
- helper - pair160: 60 kg -7.5 [-18, +3] / -13.3 [-23, -2.5]; 80 kg +7.5 [-2.5, +17.5] / +10.0 [0, +20];
  100 kg +7.5 [+1.7, +13.3] / +13.3 [+6.7, +20].
- helper - pair250, all masses: +2.8 [-3, +9] on both seeds.
- pair160 - pair250: +17.5 / +13.3 at 60 kg, -8 to -10 at 100 kg.

Reading:
- **The measured force limit helps the pair at 60 kg** (+13-18 pp): a likely reason is that with 160 N the planner picks contacts that
  share the load instead of plans one robot cannot carry. At 100 kg it hurts, since no pair plan is strong enough.
- **The helper helps where force is short (80-100 kg) and hurts where it is not (60 kg).** It engages in 94-95% of
  60 kg episodes: with 160 N per robot and mu up to 0.6, the force model rates almost every 60 kg pair plan as too weak.
- **Falls.** With the helper, robot 1 falls about twice as often (60 kg: 5 -> 16 and 5 -> 7; 80 kg: 7 -> 16 and 4 -> 15),
  and the helper itself falls in 17 / 21 of 360 episodes. The helper walks into the pair.
- Success at 80 kg is still 38-39%, far from the 60% target; the beam test's 6/6 at 80 kg was an engaged start,
  straight push. The bottleneck at 80 kg is now reaching and holding contacts, not force.
- The cylinder is unchanged by the helper (8-50%), as expected: it is not force-limited.

Next, if pursued:
- engage only when force is really short (for example strength < 0.8, or stalled progress for 2 s), not on the
  model's verdict alone;
- keep the helper's standing point at least 0.8 m from both pair robots, and route it around them;
- use pair160 as the default limit for the pair below about 70 kg.

## Videos

`helper_test.py --videos 1 --video-only 1` films the helper arm's episodes (cyan / yellow posts: the pair's contacts;
magenta: the helper's, once engaged; caption: errors, pair strength, helper state). `slurm/helper_videos.sbatch`: all
twelve objects x four scenarios, rep 0, 80 and 100 kg, seed 7100 -> `logs/evals/helper-videos/videos/index.html`.
