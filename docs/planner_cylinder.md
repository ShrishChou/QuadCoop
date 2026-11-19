# Teaching the contact planner that a lying cylinder rolls

Status (2026-11-19): the physics test passes at roll 0.1-0.2, but in closed loop the planner's cylinder success does
not improve (roll 0.1: 38 / 23% vs 31 / 38%). Job 29610362 still running (roll 0.2, seed 7500).

**Why.** On the benchmark tasks (start behind, 80 s, seeds 7100 and 7500 pooled) the planner reaches 34% on the cylinder,
against 52-92% on the other sliding objects, and its success barely depends on mass (20 / 40 / 60 / 80 kg: 50 / 25 /
29 / 33%). So force is not the limit there. Failed cylinder episodes end 0.59 m from the goal with the axis 38 deg
off, both robots pushing together only 13% of the time, and the robots usually off the object
(`evals/planner-bench-*-expert`).

The cylinder lies with its axis along the object's y axis (`stage2/shapes.py`, radius 0.30 m, length 1.20 m). Pushed
across the axis it rolls, with almost no resistance; along the axis, and in yaw (the ends must slip sideways along the
rolling direction), it slides. The planner's force model (`_split`, `_pair_strength`, `_pair_residuals`) uses one
isotropic ellipsoidal limit surface for every object. For the cylinder it therefore:
- rates same-side pushes at the two ends as a good way to turn it (they only roll it);
- overestimates the force a cross-axis push needs.

## Change (`src/quadcoop/coop2/mdp.py`; off by default)

`CoopPush2CommandCfg.roll_ratio` (0 = the old model). When > 0, shapes whose grounded parts are all lying cylinders
get resistance `roll_ratio x mu m g` across the axis (object frame x) and `mu m g` along it, with the yaw term
unchanged. That surface is (Fx / rho)^2 + Fy^2 + (tau / cg)^2 = 1. In the scaled coordinates F' = (Fx / rho, Fy,
tau / cg) it is the unit sphere, and the wrench is parallel to the scaled motion (rho vx, vy, cg wz). The fit is
therefore the existing one with:
- the cone edges' x column divided by rho;
- the wanted x velocity multiplied by rho.

Force sizes stay physical (`_roll_scale`; per env `roll_factor()`; passed as `roll=` to every call of the three fits,
and in `contact_test.py`'s reference split and `planner_physics_test.py --roll-ratio`).

CPU check (toy cylinder, two contacts; residual 0 = can make the motion exactly, 1 = cannot):

| wanted motion | same side, both ends | couple (one behind at one end, one in front at the other) |
|---|---|---|
| pure turn, old model | 0.46 | 0.03 |
| pure turn, roll 0.1 | **0.98** | 0.03 |
| roll + turn, old model | **0.08** | 0.67 |
| roll + turn, roll 0.1 | 0.78 | **0.03** |
| pure roll, both models | 0.00-0.09 | 0.13-0.79 |

The rolling model sends a turn to a couple, and a roll-plus-turn to a couple with slightly unequal forces. The old
model picks same-side pushes, which in the simulator only roll the cylinder.

## Test (`sbatch slurm/cylinder_roll_test.sbatch`)

1. `planner_physics_test.py --objects cylinder --fmax 150,250`, roll 0 / 0.05 / 0.1 / 0.2 (`evals/pp-cyl-roll*`):
   with no robots, do the planner's chosen pushes move the cylinder as asked?
2. The planner on the benchmark's cylinder tasks, as `planner-bench` (start behind, 80 s, 20-80 kg, 3 reps, seeds 7100
   and 7500), roll 0.1 and 0.2 (`evals/cyl-roll*-expert`). Baseline: roll 0 = `evals/planner-bench-*-expert`
   (cylinder 34%, 48 tasks per seed).

Read: cylinder success against the baseline, matched tasks; whether the planner now uses couples (contact pair
geometry in the episode logs); final heading error.

## Results

**1. Physics test** (`evals/pp-cyl-roll*`): share of the planner's workable pushes that moved the cylinder as asked,
150 N / 250 N per robot:

| roll_ratio | 150 N | 250 N |
|---|---|---|
| 0 (old model) | 0.62 | 0.75 |
| 0.05 | 0.60 | 0.75 |
| 0.1 | 0.80 | **1.00 (PASS)** |
| 0.2 | 0.87 | **1.00 (PASS)** |

The rolling model fixes the force model: every failure left at roll 0.2 is a pure turn at 60-80 kg with 150 N.

**2. Closed loop** (cylinder tasks of the benchmark, 48 matched tasks per seed, success %):

| | seed 7100 | seed 7500 |
|---|---|---|
| roll 0 (baseline) | 31 | 38 |
| roll 0.1 | 38 | 23 |
| roll 0.2 | 27 | (running) |

Final heading error is unchanged (about 25-33 deg mean) and both robots push together 15-19% of the time either way.

**Reading.** The planner now asks for the right pushes (couples to turn), but the Stage 4 executor does not deliver
them. Most likely it was trained mostly on contacts on the same side of the object, rarely on one robot pushing behind at one end while
the other pushes in front at the other, so the couple does not form. The limit on the cylinder is the executor, not
the plan. Next step: fine-tune the executor on cylinder tasks with roll_ratio 0.1, so it trains on the couples the
planner now asks for.

## Executor fine-tune and failure videos (2026-11-19)

- `cyl_ft_s0` (`slurm/submit_cylinder_ft.sh`, job 29661847): turn_debug's recipe from `model_15000.pt`, 2000 more
  iterations, `--roll-ratio 0.1` (new `train_coop2.py` flag) and `--shape-bias cylinder:6` (about half the
  episodes). Evaluate on the cylinder tasks with `contact_test.py --set roll_ratio=0.1`.
- Videos of the two-robot planner's cylinder failures (old model, seeds 7100 / 7500): `slurm/cylinder_fail_videos.sbatch`
  -> `logs/evals/cyl-fail-<seed>-expert/pair/videos/index.html` (successes removed).
