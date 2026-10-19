#!/bin/bash
# Stage 0 gate on a trained walker (newest checkpoint of the newest run by default).
#
#   ROBOT=anymal_c sbatch slurm/validate.sbatch
#   ROBOT=spot CKPT=logs/rsl_rl/walker_spot/<run>/model_3000.pt sbatch slurm/validate.sbatch
#
# Writes validation.json next to the checkpoint; the job log ends with PASSED / NOT PASSED.
#SBATCH -J qc-validate
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 00:45:00
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

if [[ -z "${CKPT:-}" ]]; then
  RUN=$(ls -td logs/rsl_rl/walker_"$ROBOT"/*/ | head -1)
  # Highest iteration number, not newest mtime.
  CKPT=$(ls "$RUN"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2)
fi
echo "validating $CKPT"
python scripts/validate_walker.py --task "$TASK" --checkpoint "$CKPT" --num-envs 256
