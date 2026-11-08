#!/bin/bash
# Test A, can the frozen walker push at distinct, sustained force levels (scripts/walker_force_test.py):
# one ANYmal driven at fixed forward speeds into a cube face (immovable and movable), contact force measured.
# Stats -> evals/<NAME>/ (summary.md, summary.json, cases.csv; committed).
#
#   sbatch -G l40s:1 slurm/walker_force_test.sbatch                 # -> evals/wf-test
#SBATCH -J qc-wforce
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 02:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
nvidia-smi --query-gpu=name,memory.total --format=csv
python scripts/walker_force_test.py --name "${NAME:-wf-test}" ${ARGS:-}
