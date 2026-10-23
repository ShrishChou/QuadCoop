#!/bin/bash
# Standard evaluation of a registered method (scripts/eval_method.py); results go to
# evals/<ID>/eval/<SUITE>/ and evals/README.md is rebuilt afterwards.
#   ID=s2b-anymal SUITE=standard sbatch slurm/eval_method.sbatch
#   for m in $(python scripts/methods.py list | awk '$2=="stage2"{print $1}'); do ID=$m SUITE=h80 sbatch slurm/eval_method.sbatch; done
#SBATCH -J qc-evalm
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
unset QUADCOOP_WALKER_CKPT QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT QUADCOOP_PUSH_FORCE
python scripts/eval_method.py --id "${ID:?set ID=<method id>}" --suite "${SUITE:-standard}" || echo "eval returned $?"
python scripts/report.py > /dev/null && echo "updated evals/README.md"
