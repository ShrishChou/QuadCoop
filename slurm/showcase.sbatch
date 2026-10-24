#!/bin/bash
# Final per-object videos of a registered method into eval_videos/<NAME>/ (git-ignored), stats
# into evals/<ID>/eval/showcase/ (committed). See scripts/showcase.py.
#   ID=s2b-anymal-term80 NAME=s2b_anymal sbatch slurm/showcase.sbatch
#SBATCH -J qc-showcase
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
python scripts/showcase.py --id "${ID:?set ID=<method id>}" --name "${NAME:?set NAME=<folder in eval_videos>}" ${ARGS:-}
