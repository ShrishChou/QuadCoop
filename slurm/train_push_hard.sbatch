#!/bin/bash
# Stage 1b: harder push-to-pose with ten shapes, warm-started from the Stage 1 policy.
#
#   ROBOT=anymal_c WALKER=<walker model.pt> INIT=<stage1 push model.pt> sbatch slurm/train_push_hard.sbatch
#   ROBOT=spot     WALKER=<walker model.pt> INIT=<stage1 push model.pt> sbatch slurm/train_push_hard.sbatch
#
# With INIT it first converts the Stage 1 checkpoint (scripts/warmstart_push.py) and
# starts from it. Without INIT it trains from scratch. RESUME=1 continues the newest
# Stage 1b run (after the 6 h limit). Optional: NUM_ENVS (4096), SEED, ITERS (8000),
# RUN_NAME, LOGGER (wandb|tensorboard), VIDEO (1|0), VIDEO_INTERVAL.
#SBATCH -J qc-pushhard
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
  anymal_c) TASK=QuadCoop-PushHard-AnymalC ;;
  spot)     TASK=QuadCoop-PushHard-Spot ;;
  *) echo "ROBOT must be anymal_c or spot"; exit 1 ;;
esac
: "${WALKER:?set WALKER=path/to/the Stage 0 walker model_<iter>.pt for this robot}"
[[ -f "$WALKER" ]] || { echo "walker checkpoint not found: $WALKER"; exit 1; }
export QUADCOOP_WALKER_CKPT="$WALKER"

ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}"
      --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-8000}"
      --agent.run-name "${RUN_NAME:-seed${SEED:-0}}"
      --agent.logger "${LOGGER:-wandb}")
if [[ "${VIDEO:-1}" == "1" ]]; then
  ARGS+=(--video True --video-length 750 --video-interval "${VIDEO_INTERVAL:-5000}")
fi

if [[ "${RESUME:-0}" == "1" ]]; then
  ARGS+=(--agent.resume True)            # newest dated run sorts after 0000_warmstart
elif [[ -n "${INIT:-}" ]]; then
  [[ -f "$INIT" ]] || { echo "Stage 1 checkpoint not found: $INIT"; exit 1; }
  python scripts/warmstart_push.py --task "$TASK" --init "$INIT"
  ARGS+=(--agent.resume True --agent.load-run 0000_warmstart --agent.load-checkpoint model_0.pt)
fi

nvidia-smi --query-gpu=name,memory.total --format=csv
echo "task=$TASK walker=$WALKER init=${INIT:-none} args=${ARGS[*]}"
python train_push_hard.py "$TASK" "${ARGS[@]}"
