#!/bin/bash
# Stage 1: train the high-level pushing policy on top of a frozen Stage 0 walker.
#
#   ROBOT=anymal_c WALKER=logs/rsl_rl/walker_anymal_c/<run>/model_5999.pt sbatch slurm/train_push.sbatch
#   ROBOT=spot     WALKER=logs/rsl_rl/walker_spot/<run>/model_5999.pt     sbatch slurm/train_push.sbatch
#
# Resume after the 6 h limit: add RESUME=1 (newest run of logs/rsl_rl/push_<robot>).
# Optional: NUM_ENVS (4096), SEED (0), ITERS (5000), RUN_NAME, LOGGER (wandb|tensorboard),
# VIDEO (1|0), VIDEO_INTERVAL (env steps, default 5000).
#SBATCH -J qc-push
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl

ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in
  anymal_c) TASK=QuadCoop-Push-AnymalC ;;
  spot)     TASK=QuadCoop-Push-Spot ;;
  *) echo "ROBOT must be anymal_c or spot"; exit 1 ;;
esac
: "${WALKER:?set WALKER=path/to/the Stage 0 model_<iter>.pt for this robot}"
[[ -f "$WALKER" ]] || { echo "walker checkpoint not found: $WALKER"; exit 1; }
export QUADCOOP_WALKER_CKPT="$WALKER"

ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}"
      --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-5000}"
      --agent.run-name "${RUN_NAME:-seed${SEED:-0}}"
      --agent.logger "${LOGGER:-wandb}")
if [[ "${VIDEO:-1}" == "1" ]]; then
  ARGS+=(--video True --video-length 500 --video-interval "${VIDEO_INTERVAL:-5000}")
fi
if [[ "${RESUME:-0}" == "1" ]]; then
  ARGS+=(--agent.resume True)
fi

nvidia-smi --query-gpu=name,memory.total --format=csv
echo "task=$TASK walker=$WALKER args=${ARGS[*]}"
python train_push.py "$TASK" "${ARGS[@]}"
EOF