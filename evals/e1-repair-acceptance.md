# E1 execution-repair round: acceptance criteria

Written 2026-11-11 10:31 ET, before any repair-arm results (R-T, R-TP, R-TE) existed. Changes after results must be
listed under "Amendments" with a reason.

## Fixed for this round

Walker (v1), planner (`QUADCOOP_PLANNER=ends`, expert rule), and replanning (`--reselect-s auto`, as trained) stay as they are.
`QUADCOOP_CONTACT=train`, `QUADCOOP_CMD_IF=raw`, executor `logs/keep/marl2/turn_debug/model_15000.pt`, start behind.
Standard tasks: 12 objects x 4 scenarios x 3 reps x 4 masses = 576 tasks per arm.

## Arms

| arm | recipe flags (all: `--recipe share --recipe-scope push`) | window |
|---|---|---|
| A-w (reference) | none (executor only) | `--settle-s 5` |
| R (done, e1s-R) | open-loop speed, recipe stops inside 10 cm / 6 deg | none |
| R-T | `--recipe-track 2` | `--settle-s 5` |
| R-TP | `--recipe-track 2 --recipe-finish precise` | `--settle-s 5` |
| R-TE | `--recipe-track 2 --recipe-finish exec` | `--settle-s 5` |

The success metric is unchanged: 10 cm / 6 deg held for 1 s, within 80 s. `--settle-s 5` adds a 5 s observation
window after each success, using the same controller. It records `settled`: precise at rest (10 cm / 3 deg, object
still) at any time up to the window's end. It also records the pose error at the window's end and any fall during the
window. Nothing measured inside the window changes any other metric. A-w and every repair arm use the same window.

## Reported for every arm (overall and per mass)

Report these together:
- success;
- unconditional precise (up to success, as before);
- unconditional settled (within the window);
- precise given success and settled given success;
- falls;
- horizon-capped completion time.

A conditional rate is never read without its unconditional rate.

## Statistics

Paired differences use a bootstrap 95% CI over tasks: 2,000 resamples, task = object x mass x scenario x rep
(`scripts/e1_report.py`).

Margin rules for a candidate vs A-w:
- **Non-inferiority (NI) to margin m:** the CI lower bound of (candidate - A-w) is above -m, or the upper bound is
  below +m for harms such as falls.
- **Inconclusive:** the CI crosses the margin.
- **Fail:** the whole CI lies beyond the margin.

## Criteria for adopting a candidate (all must hold vs A-w)

1. **80 kg success:** NI with margin 5 points.
2. **Falls:**
   - overall NI with margin 3 points;
   - 80 kg NI with margin 5 points.
3. **20 + 40 kg success (pooled):** CI lower bound > 0. The light-object gain must survive.
4. **Settled, unconditional, overall:** NI with margin 5 points.
5. **Precise, unconditional, overall:** NI with margin 5 points.
6. **Capped completion time, overall:** NI with margin 3 s.

If any criterion is inconclusive and none fails, the result is **inconclusive**: no adoption. The next step is more
reps on the deciding stratum, not a new variant. With 144 tasks per mass, an 80 kg success interval is about
±7 points, so criterion 1 can come out inconclusive.

## Mechanism comparisons (explanation, not adoption)

| comparison | question | read as |
|---|---|---|
| R-T vs R, 80 kg | does tracking remove the heavy regression? | success and falls CI; mechanism checks below |
| R-TP vs R-T | does the 3 deg stopping target restore settling? | settled (unconditional and given success), precise |
| R-TE vs R-T | does the executor finish better? | same |

R has no window. R-T vs R uses only metrics defined without the window.

## If tracking does not remove the 80 kg regression

Check these at 80 kg, R-T vs R vs A-w (`scripts/repair_diag.py`), before attributing the cause:
- **(a)** whether commands reach the walker limit while both robots press;
- **(b)** whether force along the push direction increases;
- **(c)** whether the object moves faster while both press, and whether its yaw rate has the wanted sign;
- **(d)** whether contact retention improves: exits per pressing-second and falls per exit.

How to read the outcomes:
- Commands not reaching the limit means the command repair was ineffective.
- Commands at the limit without more useful force or motion points to force allocation or contact geometry.
- Neither outcome alone points at the planner or justifies walker training.

## Amendments

(none)

## Closure (2026-11-11)

The recipe branch is closed. Nothing was adopted.

| item | status |
|---|---|
| Recipe variants R (standard, e1s-R) and turn-only (e1t-R); segment arms e6-equal/share (v1, v2), e6r-share | **Evaluated, not adopted** |
| R-T, R-TP, R-TE (tracking / finishing repairs) | **Cancelled before producing results: unevaluated.** These criteria were never applied. |
| Execution backend for the next experiment | turn_debug executor (`logs/keep/marl2/turn_debug/model_15000.pt`), walker v1, current physics, `QUADCOOP_PLANNER=ends`, expert planner settings as trained. All frozen. |

What the evaluated recipe variants showed:
- **Translation gains:** e1s-R vs e1s-A, success +11 points at 20 kg and +9 at 40 kg; e1t-R vs e1t-A, success +5.7 [+1.9, +9.4].
- **Regressions:**
  - 80 kg success −12 [−19, −5], with more falls;
  - unconditional precise 0.49 → 0.34 (standard) and 0.61 → 0.32 (turn-only);
  - worse move-and-turn segments, and with replanning it falls below the executor on segments (−5.4 [−9.4, −0.7]).

Reference stopping behaviour (e1s-Aw, 5 s post-success window):
- success 0.57;
- settled 0.53 overall, 0.93 given success;
- only 0.58 of successes still within 10 cm / 6 deg when the window ends.

So the reference executor often reaches precise rest but does not reliably stay at the goal. Comparisons must keep this limitation in view and must not describe the backend as solved.
