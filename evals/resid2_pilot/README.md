# Residual pilot 2 (resid2_beam_s0): close-out evidence

Decision and reading: `docs/residual_pilot.md`, section "Pilot 2 outcome".

- `learning_curves.csv`: every logged scalar, iterations 1–600, exported from wandb run `resid2_beam_s0`.
- `learning_curves_by50.md`: 50-iteration means of the main curves.
- `reset_counts_it1-300.json`, `reset_counts_it301-600.json`: episode starts by shape and 10 kg bin. The counter
  restarts on resume. All starts are beam, 20–80 kg.
- `push_endings.md`: output of
  `python scripts/push_endings.py r2dev-base:4000,4001,4002 r2dev-resid:4000 r2dev-resid600:4001,4002 --objects=beam`.
  It shows why requested joint pushes end, and the force delivered in sustained joint pushes.
- `heavy.py`, `heavy_s4000.md`: the first 80 kg check. **Superseded**: it used the raw 10 Hz force and the
  on_contact flag, and its "no sustained joint pressing" reading is retracted (see the script docstring).

Evaluations: `logs/evals/r2dev-base-s400{0,1,2}-expert`, `r2dev-resid-s4000-expert` (checkpoint 300) and
`r2dev-resid600-s400{1,2}-expert` (checkpoint 600).
