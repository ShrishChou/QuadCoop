#!/bin/bash
# Stage 0 gate + object sweep + videos on a trained walker (newest checkpoint of the newest run by default).
#
#   ROBOT=anymal_c sbatch slurm/validate.sbatch
#   ROBOT=spot CKPT=logs/rsl_rl/walker_spot/<run>/model_3000.pt sbatch slurm/validate.sbatch
#
# Writes validation.json and eval_<ckpt>/{eval.json,videos/} next to the checkpoint and logs the
# sweep to W&B; the job log ends with PASSED / NOT PASSED (EVAL_WANDB=0 to skip W&B).
#SBATCH -J qc-validate
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 01:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl

ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in
  anymal_c) TASK=QuadCoop-Walker-AnymalC ;;
  spot)     TASK=QuadCoop-Walker-Spot ;;
  *) echo "ROBOT must be anymal_c or spot"; exit 1 ;;
esac

if [[ -z "${CKPT:-}" ]]; then
  RUN=$(ls -td logs/rsl_rl/walker_"$ROBOT"/*/ | head -1)
  # Highest iteration number, not newest mtime.
  CKPT=$(ls "$RUN"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2)
fi
echo "validating $CKPT"
WB=(); [[ "${EVAL_WANDB:-1}" == "1" ]] && WB=(--wandb)
python scripts/eval_walker.py --task "$TASK" --checkpoint "$CKPT" --video "${WB[@]}"
python scripts/validate_walker.py --task "$TASK" --checkpoint "$CKPT" --num-envs 256
