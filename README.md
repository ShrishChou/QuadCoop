# quadcoop — Stage 0: force-robust walkers for ANYmal C and Spot

Stage 0 of the 6.7980 project ("Learning to Cooperate Through Physical Interaction").
It trains one low-level walker per robot that tracks a commanded base velocity
`(vx, vy, ωz)` **while something pushes back**. That walker is then frozen, and the
pushing and cooperation policies of Stages 1–2 command it.

The disturbance design is a port of the torso force field from
[G1-Force-Movement](https://github.com/ShrishChou/g1-force-movement), adapted for a
robot that has to push objects. The mjlab revision is pinned to the same commit.

## What the walker sees and what it is trained against

| | |
|---|---|
| **Actor observation** | The stock mjlab velocity task's: IMU linear/angular velocity, gravity direction, joint positions/velocities, last action, velocity command. No object, no partner, no force. |
| **Critic observation (training only)** | All of the above, plus foot contacts/heights and **the applied push force** (privileged). |
| **Push force** (`mdp/push_force.py`) | Horizontal, applied at the front of the body (so it also pitches the robot, like a real push). 70% of loads oppose the commanded velocity, 30% come from a random direction (bumps). Each env runs gap → ramp → hold 1–3 s → ramp, repeated. Peak magnitude is 0.4 × body weight, reached over 2000 iterations. |
| **Real box** (`mdp/box_events.py`) | A 0.6 × 0.6 × 0.7 m box of 3–30 kg, dropped in the commanded path for 30% of placements, at reset and every 4–8 s. It gives the walker real contact, friction, and a load that moves away. Otherwise the box is parked out of reach. |
| **Commands** | mjlab defaults, plus 15% standing envs (bracing), with the speed curriculum capped at 1.5 m/s. |

Every knob is an environment variable; see the top of `src/quadcoop/walker_env_cfg.py`.

## Layout

```
src/quadcoop/
  robots/anymal_c.py   robots/spot.py   robots/box.py   robots/spec.py
  mdp/push_force.py    the force field (CommandTerm)
  mdp/box_events.py    box placement event
  walker_env_cfg.py    the task (built on mjlab's make_velocity_env_cfg)
  rl_cfg.py            PPO settings
  __init__.py          registers QuadCoop-Walker-AnymalC / QuadCoop-Walker-Spot
scripts/
  fetch_assets.py      robot models from pinned commits (Menagerie, mujocolab)
  smoke_test.py        build/step checks, force + box checks, two-robot scene
  validate_walker.py   the Stage 0 gate on a trained checkpoint
slurm/                 setup + sbatch files for Engaging
train.py  play.py      mjlab's train/play with our tasks registered
```

## Getting it onto Engaging

Pick one:

- **GitHub (recommended).** On your laptop, create an empty private repo, then from this
  folder run `git add -A && git commit -m init && git remote add origin <url> && git push -u origin main`.
  On Engaging, make a key with `ssh-keygen -t ed25519 -C "$USER@mit.edu"`, add the `.pub`
  file to GitHub, then run `git clone <url>`.
- **Copy the folder.** `scp -r quadcoop <kerb>@orcd-login.mit.edu:~/`

## One-time setup

```bash
ssh <kerb>@orcd-login.mit.edu          # Kerberos password + Duo
cd ~/quadcoop
bash slurm/setup_engaging.sh           # on the login node: needs internet, ~10-15 min
```

This creates `.venv/` (Python 3.12 through uv; no conda needed), installs mjlab at the
pinned commit plus this package, and downloads both robot models.

## Run order

```bash
# 1. GPU smoke test (~5 min): builds both walkers, checks the force field and box, and
#    builds ANYmal C + Spot + box in ONE scene (the Stage 2 risk, checked on day one).
sbatch slurm/smoke.sbatch
tail -f logs/slurm/qc-smoke-*.out        # ends with "All smoke checks passed."

# 2. Train both walkers (one L40S each, 6 h limit on mit_normal_gpu).
ROBOT=anymal_c sbatch slurm/train_walker.sbatch
ROBOT=spot     sbatch slurm/train_walker.sbatch
squeue --me

# 3. If a job hit the 6 h wall, continue from its newest checkpoint:
ROBOT=anymal_c RESUME=1 sbatch slurm/train_walker.sbatch

# 4. Stage 0 gate (newest checkpoint by default; or set CKPT=...):
ROBOT=anymal_c sbatch slurm/validate.sbatch
ROBOT=spot     sbatch slurm/validate.sbatch
tail logs/slurm/qc-validate-*.out        # PASSED / NOT PASSED, plus validation.json
```

**Gate tests** (`scripts/validate_walker.py`, 256 robots × 10 s each):

| Test | Setup | Pass if |
|---|---|---|
| A track | vx = 0.5 m/s, no disturbance | falls ≤ 2%, speed error ≤ 0.15 m/s |
| B resist | vx = 0.5 m/s into a constant opposing force of 0.25 × weight | falls ≤ 5%, keeps ≥ 50% of commanded speed |
| C push box | vx = 0.4 m/s into a 15 kg box placed just ahead | falls ≤ 5%, median box displacement ≥ 2 m |

Change the load with `--force-frac` or `--box-mass` to map where each robot's limits are.
That data also feeds the capability table in Stage 1.

## Working interactively

```bash
srun -p mit_normal_gpu -G l40s:1 -c 8 --mem=32G -t 02:00:00 --pty bash
source .venv/bin/activate
python scripts/smoke_test.py --quick
python train.py QuadCoop-Walker-AnymalC --env.scene.num-envs 1024 --agent.max-iterations 50
```

**Watching a policy.** mjlab's Viser viewer serves a web page. Start it on the compute
node:

```bash
python play.py QuadCoop-Walker-AnymalC --viewer viser --num-envs 4 \
    --checkpoint-file logs/rsl_rl/walker_anymal_c/<run>/model_5999.pt
```

Then, on your laptop, tunnel through the login node (replace `<node>` with the compute
node's hostname and use the port Viser prints):
`ssh -L 8080:<node>:8080 <kerb>@orcd-login.mit.edu`, and open http://localhost:8080.

**Training curves.** Logs are TensorBoard by default:
`tensorboard --logdir logs/rsl_rl --port 6006`, using the same tunnel trick. To use W&B,
run `wandb login` once and add `--agent.logger wandb` to the `train.py` arguments
(edit `ARGS` in the sbatch file).

Things to watch: `Metrics/push_force/force_frac_weight` (load actually reaching 0.4),
episode length (falls), and the linear-velocity tracking reward. Tracking will dip while
the force curriculum ramps; it should recover.

## Notes and known limits

- **Spot model.** Spot is built from Menagerie's model with the body collision kept,
  because the torso must push. Its PD gains and joint damping come from Velocity Hub's
  trainable mjlab Spot. If its gait is poor, tune those first (`robots/spot.py`).
- **Robot mass.** Robot mass is read from the compiled model at startup, and the force is
  scaled to it, so both robots get the same relative difficulty.
- **Force units.** The force in the critic is in units of body weight, so the critic input
  scale is the same for both robots.
- **Ablation.** `QUADCOOP_PUSH_FORCE=0` trains a plain walker for comparison.
- **Assets.** Assets are not committed; `scripts/fetch_assets.py` pins the source commits.
