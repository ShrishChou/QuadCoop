# What can the frozen stack control while pushing? Command-to-force probe

Status: step 1 done (2026-11-13). Result: mixed by mass. Steps 2–3 (tracker, response test) are not started;
decision at the end. No training, no walker change, no extra robots.

**Why.** The request-tracking pilot (`docs/request_tracking.md`) failed, but a failed learner doesn't show what the
stack can control. The scripted beam tests showed that some commands move the beam. They didn't show that changing
the commands redistributes force. Before any tracker, this measures the local response: how one robot's forward
command changes the force it and its partner deliver.

## Design (`contact_test.py --cmd-probe robot,vx,partner_vx`; analysis `scripts/cmd_force_probe.py`)

- **Stack:** the frozen executor (turn_debug `model_15000.pt`) and frozen walker, reference planner with feedback off,
  contacts fixed (`--reselect-s 0`), engaged start (`--start contact`).
- **Task:** a new 4 m straight segment `S_long`, added last to the segment set, so earlier tasks are unchanged. It
  gives a long window before the goal.
- **Load:** beam, 40 and 60 kg, friction 0.5, 3 reps, seed 4300 (unused before). Horizon 15 s; measured over
  2–12 s while live.
- **Commands:**
  - each episode, the probe robot's walker forward command is fixed at 0.8 / 0.6 / 0.4 / 0.2 / 0.0 m/s;
  - its partner's is fixed at 0.8 m/s, the executor's usual saturated level;
  - lateral and heading commands are the executor's own, a consistent control law.
- **Matching:** each level runs with identical resets, tasks and contacts. Both robots take the probe role in turn,
  giving 6 matched tasks per mass and level.
- **Measured:**
  - each robot's force along its push direction, averaged over the window, which spans many gait cycles;
  - the probe robot's share of the force;
  - touching (each robot, and both at once) and on-contact share;
  - beam speed, largest heading change, falls;
  - the applied forward command (it matched the override exactly in every run).

Evidence: `evals/command_force/probe.md` (tables, paired CIs, every task) and the per-run episode files.

## Results

| mass | probe vx | probe force N | partner force N | probe share | probe touching | both touching | beam speed m/s | beam yaw deg | falls |
|---|---|---|---|---|---|---|---|---|---|
| 40 | 0.8 | 77 | 79 | 0.50 | 0.52 | 0.31 | 0.55 | 26 | 2/6 |
| 40 | 0.6 | 78 | 85 | 0.48 | 0.53 | 0.30 | 0.52 | 39 | 0/6 |
| 40 | 0.4 | 63 | 89 | 0.42 | 0.52 | 0.30 | 0.43 | 57 | 0/6 |
| 40 | 0.2 | 40 | 94 | 0.30 | 0.46 | 0.28 | 0.28 | 77 | 1/6 |
| 40 | 0.0 | 0 | 105 | 0.00 | 0.00 | 0.00 | 0.19 | 78 | 1/6 |
| 60 | 0.8 | 116 | 128 | 0.47 | 0.73 | 0.57 | 0.27 | 20 | 0/6 |
| 60 | 0.6 | 122 | 110 | 0.54 | 0.79 | 0.61 | 0.22 | 18 | 0/6 |
| 60 | 0.4 | 118 | 120 | 0.50 | 0.78 | 0.56 | 0.15 | 13 | 1/6 |
| 60 | 0.2 | 102 | 122 | 0.46 | 0.79 | 0.63 | 0.12 | 20 | 1/6 |
| 60 | 0.0 | 0 | 120 | 0.00 | 0.00 | 0.00 | 0.03 | 10 | 3/6 |

Paired change against the 0.8 m/s level (mean [95% CI], 6 tasks):

| mass | probe vx | probe force N | probe share | probe touching | beam yaw deg |
|---|---|---|---|---|---|
| 40 | 0.4 | −13.7 [−28.8, +0.7] | −0.08 [−0.14, −0.01] | −0.00 [−0.08, +0.09] | +31 [+1, +59] |
| 40 | 0.2 | −37.5 [−56.1, −24.2] | −0.19 [−0.31, −0.09] | −0.06 [−0.22, +0.06] | +52 [+13, +75] |
| 60 | 0.4 | +1.7 [−13.4, +21.4] | +0.03 [−0.03, +0.08] | +0.05 [+0.02, +0.09] | −7 [−22, +9] |
| 60 | 0.2 | −15.9 [−29.7, +1.4] | −0.01 [−0.06, +0.03] | +0.04 [+0.00, +0.07] | +3 [−21, +27] |
| 60 | 0.0 | −113.9 [−127.5, −97.6] | −0.47 [−0.50, −0.44] | −0.73 [−0.76, −0.69] | −11 [−30, +8] |

**40 kg: graded and predictable, with contact kept, but the beam turns.**
- Lowering one robot's command from 0.8 to 0.2 m/s lowers its force monotonically (77 → 40 N) and its share
  (0.50 → 0.30).
- Its touching stays near the 0.8 m/s level, and its partner's force rises slightly.
- The asymmetric push turns the beam markedly: +31° at 0.4 m/s, +52° at 0.2 m/s. Lateral and heading control were
  the executor's, which doesn't compensate.
- At 0 m/s the robot drops off the beam: the beam moves on at 0.19 m/s without it.

**60 kg: flat while in contact; force falls only by breaking contact.**
- From 0.8 to 0.4 m/s the probe robot's force doesn't change (116 → 118 N, share 0.47 → 0.50), and its touching even
  rises slightly.
- At 0.2 m/s there is a small, uncertain drop (−16 N [−30, +1]); the share doesn't change.
- At 0 m/s contact breaks (touching 0), and 3 of 6 episodes end in a fall.
- Physically: at 60 kg the beam moves at 0.12–0.27 m/s, slower than any command ≥ 0.2 m/s, so both robots are
  load-limited. The walker then pushes at its own level (about 100–130 N, gait-averaged) regardless of the commanded
  speed.
- At 40 kg the beam moves at 0.3–0.55 m/s, about the commanded speed, so the command sets how hard the robot keeps
  up.
- Reading: the walker's forward velocity command regulates force only in the speed-limited regime (light objects).
  In the load-limited regime (heavy objects), force sharing through the forward command is not a usable primitive.

**Limits:**
- one friction (0.5), one partner level (0.8 m/s), 3 reps per robot role;
- straight broadside contacts only;
- the 1 s gait averaging is replaced here by 10 s window means;
- the beam's yaw changes the push geometry during the window, especially at 40 kg.

## Decision (the review's rules)

**40 kg: "command changes predictably alter force."**
- A measured tracker is possible there, mapping a requested share to the probe robot's command level using the
  table above, with small bounded feedback.
- It must also handle the yaw that unequal force creates: either keep the request consistent with a turn, or
  correct heading. The executor's lateral and heading outputs alone didn't.

**60 kg: "commands barely alter force across the tested range while contact stays stable," and below 0.2 m/s
"force changes only by breaking contact"**, with falls.
- Continuous force sharing through the forward velocity command is the wrong primitive for heavy beams with this
  walker.
- Investigate another control variable or primitive before any more executor training:
  - engagement decisions (which robots push, where, and when to release and re-engage);
  - contact position along the beam;
  - lateral or heading offset at the contact;
  - or the walker's command interface itself.

**Proposed next step, for review:**
- Do not build the share tracker yet: it would work at most for light beams, where coordination matters least.
- Run one bounded engagement-primitive probe at 60 kg, same stack:
  - which beam motions can be produced by choosing which robot pushes and where;
  - one robot vs both; inner vs end contacts;
  - with controlled release (command 0.2 m/s, not 0), to see whether release can be done without falls.
- If useful, those choices, not continuous force percentages, become the coordination primitive the planner adapts.
