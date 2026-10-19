#!/bin/bash
# Train one walker on one L40S.
#
#   ROBOT=anymal_c sbatch slurm/train_walker.sbatch
#   ROBOT=spot     sbatch slurm/train_walker.sbatch
#
# mit_normal_gpu caps jobs at 6 h. If a run is cut off, resubmit with RESUME=1
# and it continues from the newest checkpoint of the newest run for that robot:
#
#   ROBOT=anymal_c RESUME=1 sbatch slurm/train_walker.sbatch
#
# Optional: NUM_ENVS (4096), SEED (0), ITERS (6000), RUN_NAME, and any
# QUADCOOP_* knob from src/quadcoop/walker_env_cfg.py, e.g. QUADCOOP_PUSH_MAX_FRAC=0.5.
#SBATCH -J qc-walker
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate

ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in
  anymal_c) TASK=QuadCoop-Walker-AnymalC ;;
  spot)     TASK=QuadCoop-Walker-Spot ;;
  *) echo "ROBOT must be anymal_c or spot"; exit 1 ;;
esac

ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}"
      --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-6000}"
      --agent.run-name "${RUN_NAME:-seed${SEED:-0}}")
if [[ "${RESUME:-0}" == "1" ]]; then
  ARGS+=(--agent.resume True)   # newest run + newest model_*.pt under logs/rsl_rl/walker_$ROBOT
fi

nvidia-smi --query-gpu=name,memory.total --format=csv
echo "task=$TASK args=${ARGS[*]}"
python train.py "$TASK" "${ARGS[@]}"
