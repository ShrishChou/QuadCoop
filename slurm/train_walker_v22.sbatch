#!/bin/bash
# Train walker v2.2 (task QuadCoop-Walker-AnymalC-Compliant-v22, src/quadcoop/walker_env_cfg.py) on one L40S:
# the same network, resumed from walker v2.1's final checkpoint (v2.1's commands, curriculum and force filter):
#   - no synthetic bumper load (v2.1's field pushed against any commanded direction at the nose; sideways and
#     slow-backward walking regressed). Real objects are the contact practice, the stock kicks the disturbances
#   - k = 500 N per m/s (0.1 m/s -> 50 N, 0.3 m/s -> 150 N) and the retreat bounded along the force (0.1 m/s)
#   - fine tracking planar-only and yaw-only on a ~0.4 s smoothed velocity (the stock function in v2/v2.1's
#     track_fine also counted vertical velocity: stepping with bounce scored below standing still)
#
#   sbatch slurm/train_walker_v22.sbatch                    # from v2.1's newest checkpoint, ITERS (3000) more
#   QUADCOOP_OBJ_MASS=<v2.1's final max_mass>,3000 sbatch slurm/train_walker_v22.sbatch   # resume the mass curriculum
#   RESUME=1 ITERS=<left> sbatch slurm/train_walker_v22.sbatch   # continue the newest v2.2 run
#   FROM=compliant sbatch slurm/train_walker_v22.sbatch    # start from v2 instead of v2.1
#
# Early gate (do not wait for the end): after ~500 iterations (about an hour; checkpoints every 100), test the
# newest checkpoint on free walking only:
#   E=logs/rsl_rl/walker_anymal_c_compliant; C=$(ls $(ls -d $E/*_v22 | tail -1)/model_*.pt | sort -V | tail -1)
#   WALKERS="v22=$C" NAME=wt-v22-early ARGS="--groups free --k v22=500 --videos side,back,yaw" sbatch slurm/walker_test.sbatch
# Continue only if sideways / slow-backward walking is back and turning on the spot clearly responds.
#
# Optional: FROM (v21 | compliant: which earlier run to start from; default v21), FROM_RUN / FROM_CKPT (explicit
# folder / checkpoint), ITERS, NUM_ENVS (4096), SEED (0), LOGGER (wandb|tensorboard), VIDEO (1|0), any QUADCOOP_* knob.
#SBATCH -J qc-walker22
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
[[ -f .venv/bin/activate ]] && source .venv/bin/activate
export MUJOCO_GL=egl
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=name,memory.total --format=csv

TASK=QuadCoop-Walker-AnymalC-Compliant-v22
EXP=logs/rsl_rl/walker_anymal_c_compliant
newest_ckpt() { ls "$1"/model_*.pt 2>/dev/null | sort -V | tail -1 | xargs -r basename; }
newest_run_with_ckpt() {  # $1 = folder suffix
  for d in $(ls -d "$EXP"/*_"$1" 2>/dev/null | sort -r); do
    if [[ -n "$(newest_ckpt "$d")" ]]; then basename "$d"; return; fi
  done
}

ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}"
      --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-3000}"
      --agent.run-name v22
      --agent.logger "${LOGGER:-wandb}")
[[ -n "${EXTRA_ARGS:-}" ]] && ARGS+=(${EXTRA_ARGS})
if [[ "${VIDEO:-1}" == "1" ]]; then
  ARGS+=(--video True --video-length 300 --video-interval "${VIDEO_INTERVAL:-5000}")
fi
if [[ "${RESUME:-0}" == "1" ]]; then
  RUN=$(newest_run_with_ckpt v22)
  CKPT=$(newest_ckpt "$EXP/$RUN")
else
  RUN=${FROM_RUN:-$(newest_run_with_ckpt "${FROM:-v21}")}
  CKPT=${FROM_CKPT:-$(newest_ckpt "$EXP/$RUN")}
fi
[[ -n "$RUN" && -n "$CKPT" && -f "$EXP/$RUN/$CKPT" ]] || { echo "no checkpoint to start from (RUN=$RUN CKPT=$CKPT) in $EXP"; exit 1; }
echo "starting from $EXP/$RUN/$CKPT"
ARGS+=(--agent.resume True --agent.load-run "^${RUN}\$" --agent.load-checkpoint "^${CKPT}\$")
echo "task=$TASK args=${ARGS[*]}"
python train.py "$TASK" "${ARGS[@]}"
