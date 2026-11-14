# Next wave: matched IPPO / MAPPO arms on a fixed task bank

Status (2026-11-14): components built; preflight passed for the iteration-3000 parent (job 29055494: transfer into IPPO and MAPPO and both bank replays, all with difference 0; 65,536 tasks, 6,450-6,702 per shape). No arm has trained yet. The parent is chosen from the
ten-object restart's matched evaluation (see Parent, below).

**Question.** Can the robots learn when one should yield or reposition? Arms A–D cross the algorithm with the
reset sampler, and the reward stays fixed. Arm E removes only the individual push credit: does a robot make room for
its partner more readily when it can earn team return without pushing itself?

| arm | algorithm | resets | reward |
|---|---|---|---|
| A | IPPO | uniform over the bank | r7 |
| B | MAPPO | uniform over the bank | r7 |
| C | IPPO | SGS over the bank | r7 |
| D | MAPPO | SGS over the bank | r7 |
| E | MAPPO | uniform over the bank | r7 without `push_credit` (`--drop-rewards push_credit`) |

**Common to every arm:**
- the parent's actors;
- fresh critics, trained alone for 100 iterations (`--critic-warmup-resume 100`);
- the ten-object restart's settings: level 4, 20–80 kg, ten shapes, KL anchor 0.05, actor LR cap 1e-4;
- seed 0, 4096 envs, 1000 iterations;
- then the same 480-task seed-7100 evaluation as the restart.

Launch: `PARENT=<ck> ARMS="A B" bash slurm/submit_next_wave.sh`. It takes at most two arms per call, and refuses to
run unless the preflight passed for that parent.

## Actor transfer (`MarlTrainer.init_actors`, `train_coop2.py --init-actors`)

- **What carries over:** both actors are copied from a trainer checkpoint of either algorithm, strictly. That covers
  weights, observation normalizers and the action noise parameter, plus noise caps, adapted learning rates, the
  iteration count and the curriculum state.
- **What starts fresh:** the critics (IPPO's two per-robot critics, or MAPPO's central critic) and every optimizer.
  `--init-from` and `--resume` can't do this, because they require the same algorithm and copy the critics.
- **Check** (`--transfer-check OBS_FILE`, before any update):
  - Observations: three batches (at the start, then after 50 and 200 steps under the source policy), collected
    once and saved.
  - Comparison: the IPPO and the MAPPO arm are each compared with an independently built reference, the evaluation
    loader (`PairPolicy`) on the source checkpoint, run through the same mean-clamp sampling path.
  - Quantities: the sampling mean and std the rollout records, the deterministic mean, and every actor tensor.
  - Pass: largest difference ≤ 1e-6. The reports go to `logs/next_wave/obs_<parent>.{ippo,mappo}.json`.

## Task bank (`quadcoop/coop2/task_bank.py`, `--task-bank uniform|sgs --task-bank-file`)

**What a task is.** A task is (env slot, column).
- **The slot fixes the physics.** Object masses, friction and sizes are startup draws, one per slot and object for
  the whole run.
- **The column fixes one training-rule draw on that slot:**
  - shape, object pose, goal;
  - each robot's bearing, gap and yaw noise;
  - the turn and heavy-pair flags.
- **What stays random:** only the walker's joint noise at reset.

**The bank:**
- 4096 slots × 16 columns = 65,536 tasks, drawn with the command's own sampling (seed 9100).
- It is saved with a snapshot of what each task produced in the simulation, and drawn once. Every arm loads the same
  file.
- At startup each arm checks that its slots carry the bank's physics, so a mismatched env build stops the run.

**Sampling at a slot's reset:**
- **Uniform:** uniform over the slot's 16 tasks.
- **SGS:** weight max(4p(1−p), 0.05), where p is the task's success estimate (EMA 0.3 over its own attempts, 0.5
  untried). Tasks the policy sometimes solves are practised most; solved and hopeless tasks keep a floor.
- On CPU with a synthetic bank:
  - uniform drew each column about 25% of the time;
  - SGS drew the two mixed-outcome tasks 49% and 41%, and the solved and failed ones about 5% each.

**What is logged:**
- **Every iteration** (wandb `Bank/*`): draw share by shape, the success of episodes that ended, the mean p of drawn
  tasks, the share of tasks tried, and draw entropy.
- **Every checkpoint:** `bank_<iter>.pt` holds each task's tries, successes and p. A difference between arms can
  then be traced to which tasks were practised.

**Replay check** (`--bank-make` / `--bank-check`):
- Columns 0 and 15 are replayed on every slot, twice, through full env resets.
- Compared with the bank's record: shape, mass, friction, size, object pose, goal, and both robots' placed poses.
- Pass: ≤ 1e-4. The check runs under the IPPO and the MAPPO env build.
- Report: `logs/next_wave/bank_ten_s0_k16.check.json`.

**Evaluation stays separate.** `scripts/eval_coop2.py` builds its own env (play mode, nominal sizes, one mass per
build, scripted placements) and never loads the bank.

## Preflight (`slurm/next_wave_checks.sbatch`, one GPU, no training)

1. Transfer into IPPO.
2. Transfer into MAPPO.
3. Draw the bank, then replay-check it under IPPO.
4. Replay-check the bank under MAPPO.

Queued after the iteration-3000 reference evaluation, with `PARENT=model_3000`. If iteration 4000 becomes the parent,
the job is rerun with that `PARENT`: the transfer checks run again and the existing bank is replay-checked again.

## Parent

The parent is chosen from `scripts/restart_compare.py`: iteration 4000 vs 3000, paired on the 480 seed-7100 tasks.
- **Use iteration 4000** if it improves transport while keeping the strong objects (sphere, long).
- **Use iteration 3000** if iteration 4000 clearly regresses. Iteration 3000 remains a viable parent.
