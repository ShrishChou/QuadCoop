#!/bin/bash
# Contact planner + helper robot (scripts/helper_test.py, docs/planner_helper.md). Stats -> evals/<PREFIX>/.
#   PREFIX=helper-7100 ARGS="--seed 7100" sbatch slurm/helper_test.sbatch
#   PREFIX=helper-smoke ARGS="--objects cube,long --masses 80 --reps 1 --horizon 10" sbatch -t 00:30:00 slurm/helper_test.sbatch
#SBATCH -J qc-helper
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 05:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
python scripts/helper_test.py --prefix "${PREFIX:-helper}" ${ARGS:-}
