# Three ANYmals: transfer from the pair, then joint training (MAPPO, IPPO)

Status (2026-11-17): code done and checked; transfer evaluations and training queued (`slurm/submit_three_anymal.sh`).

**Question.** Do three robots that already push and cooperate as a pair do better than two, especially at the heavy
masses, and what does joint training add over the transferred trio?

## How a team of three is built (`--pair anymal3`, slots anymal1-3)

No fixed sub-pairs. Every robot keeps the pair policy's inputs, so the pair's trained actors drive the trio unchanged:

- **Partner inputs (9 numbers):** the nearest teammate's, chosen per env and step (`pairs.NEAREST`).
- **Partner map channel:** every teammate's footprint (the pair's one partner box becomes the union of two).
- **Starts:** training: `--start-around`, robots evenly spaced at random around the object (120 deg apart +-30 deg, so
  neighbours are at least 60 deg apart), which robot gets which place is random. Evaluation: the standard formation
  for three (behind-left, behind, behind-right at -50 / 0 / +50 deg) on the benchmark tasks.
- **Robot-robot contact and crowding:** one contact sensor per pair; `robots_touch` is 1 when any two touch;
  `robots_close` uses the closest pair.
- **Critic:** MAPPO's central critic sees all three robots' states and maps (1052 inputs); IPPO has one critic per robot.
- **Actors from the pair:** anymal1 and anymal2 take the pair's actors, anymal3 a copy of anymal1's
  (`marl.source_slot`, observation-group names in the weights renamed).
- **Not for three robots:** the contact planner (`--contacts` is rejected with more than two robots).
- Two-robot runs are unchanged: a re-evaluation of the trained MAPPO pair (cube, 40 kg, the 12 benchmark tasks)
  gives 12/12, against 11/12 in each of the two earlier runs (reruns differ by GPU nondeterminism).

## Checks

- `scripts/three_wiring.py` (job 29452943): ALL PASS. A robot commanded forward for 2 s travels 1.10-1.22 m while the
  others stay at their zero-action creep (0.11-0.20 m; action 0 is not exactly "stand"); each robot's partner inputs
  equal its nearest teammate's; 3 robot-robot sensors, 3 fall terminations, 3 walker action terms.
- `train_coop2.py --check`, MAPPO and IPPO (job 29451191): build, actor transfer, 2 iterations, checkpoint with 3 actors.
- Physics buffer: a trio needs about 4000 constraint rows (njmax 4500; the pair uses 1500).

## Runs (`bash slurm/submit_three_anymal.sh`)

| step | MAPPO | IPPO |
|---|---|---|
| transfer: pair actors as a trio, benchmark + 100 / 120 kg | `trio-transfer-mappo` | `trio-transfer-ippo` |
| the pairs at 100 / 120 kg (they have 20-80 kg) | `team-aa-mappo-it4000-dev7100-heavy` | `team-aa-ippo-it4000-dev7100-heavy` |
| training from the pair actors, 4000 -> 6000 iterations | `trio_mappo_s0` | `trio_ippo_s0` |
| trained trio, benchmark + 100 / 120 kg | `trio-mappo-it6000-dev7100` | `trio-ippo-it6000-dev7100` |

Training recipe = the pair's ten-object restart (`docs/three_teams.md`) with three robots: r7 + KL anchor 0.05 to the
single-robot policies, actor lr cap 1e-4, ten objects, level 4 held, masses 20-120 kg (pair: 20-80), critic-only for
the first 300 iterations, random starts around the object.

**Main comparison:** the original benchmark (480 seed-7100 tasks, 20-80 kg), two against three robots; then 100 and
120 kg for both team sizes. Smoke test (8 tasks at 40 kg) of the transferred trio: 5/8, but robots touched each
other 81% of the time: crowding is the first thing to watch.
