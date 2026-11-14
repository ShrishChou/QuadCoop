# Ten-object IPPO restart: iteration 3000 → 4000

Status (2026-11-14): done. Iteration 4000 is the common parent of the next-wave arms (`docs/next_wave.md`).

## Run
- `ippo_aa_kl_ten_s0`, from `ippo_aa_kl_s0/model_3000.pt`, trained to iteration 4000 (job 29054248, 1 h 44 min).
- Settings:
  - ten objects; beam and asym excluded;
  - level 4 held (`--fixed-difficulty`, with the `push2_curriculum` fix);
  - 20–80 kg, equal shape weights;
  - r7 reward, KL anchor 0.05.
- Logged to wandb as `ippo_aa_kl_ten_s0`.

## Evaluation
Both checkpoints were evaluated on the same 480 tasks (seed 7100): `ten-ippo-source-dev7100` and
`ten-ippo-it4000-dev7100`.

Each checkpoint was evaluated a second time, in the recovery logging pass:
- the same tasks again, with logging only;
- that pass gave a different outcome on 82/480 tasks (iteration 3000) and 68/480 (iteration 4000);
- GPU simulation is not bit-reproducible.

Iteration 3000 against 4000 differs on 90 tasks, about the same as a rerun. So single-run "gained / lost" counts are
mostly noise. The table uses the mean of the two runs per task.

Full report: `evals/ten_restart/compare_it4000_vs_it3000.md` (`scripts/restart_compare.py --ref2 --new2`).

| tasks | iteration 3000 | iteration 4000 | change, per-task two-run means [95% CI] |
|---|---|---|---|
| all ten | 63.7% | 65.2% | +1.5 [−1.3, +4.3] points |
| l_shape (newly trained) | 67.7% | 80.2% | +12.5 [+5.2, +19.8] |
| plus (newly trained) | 51.0% | 63.5% | +12.5 [+2.1, +22.9] |
| u_channel (newly trained) | 69.8% | 68.8% | −1.0 [−8.3, +6.2] |
| arch | 44.8% | 37.5% | −7.3 [−18.8, +5.2] |
| cylinder | 45.8% | 42.7% | −3.1 [−10.4, +3.1] |
| long | 78.1% | 72.9% | −5.2 [−12.5, +2.1] |
| sphere | 97.9% | 96.9% | −1.0 [−5.2, +3.1] |
| dumbbell | 55.2% | 58.3% | +3.1 [−7.3, +13.5] |
| t_shape | 64.6% | 70.8% | +6.2 [−2.1, +15.6] |
| cube | 62.5% | 60.4% | −2.1 [−8.3, +4.2] |

Single run (the main evaluation):
- **Successes:** 303 → 315 of 480.
- **Falls:** 67 → 52; paired change −3.1 points [−6.7, +0.6].
- **Final distance to the goal:** −0.07 m [−0.15, −0.00].
- **Plus falls:** 15 → 5.

**Reading:**
- **Overall:** not a clear improvement.
- **Where the gain comes from:** only L-shape and plus, both held out before this run and trained on in it. That
  explanation is available for the gain.
- **The other seven objects:** flat (−0.3 points, single run).
- **Targets:**
  - 70% overall (336/480) is not met.
  - At least 20/48 per object is not met on arch: 16/48 in the main run, 18/48 in the rerun.
- **Strong objects:** kept within the intervals, though long dipped (−5 points).
- **Arch:** lower in both runs. Arch is the coordination object to watch in the next wave.

**Training curve** (episodes ending in each iteration):
- about 0.65 success over 3100–3300, drifting to about 0.58 by 4000;
- falls dropped from about 0.15 to 0.07;
- the first 100 iterations read high because only short episodes end that early.

**Parent decision**, by the rule set in advance:
- Iteration 4000 is not clearly worse, has fewer falls, and keeps the strong objects within noise. It is chosen.
- It has also already adapted to the ten-shape mix. The arms' differences will then reflect what each arm changes,
  not catching up on the three newly trained shapes.
- Iteration 3000 remains the fallback.
