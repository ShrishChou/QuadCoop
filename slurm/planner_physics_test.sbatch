#!/bin/bash
# Test 1, the planner's force model against the physics (scripts/planner_physics_test.py): no robots,
# no learning; the planner's pushes applied as forces at the contacts of every object x mass x motion.
# Stats -> evals/<NAME>/ (committed), every case -> logs/evals/<NAME>/cases.csv.
#
#   sbatch slurm/planner_physics_test.sbatch                                     # 250 N, 20-80 kg -> evals/pp-test
#   NAME=pp-fsweep ARGS="--fmax 150,250,350" sbatch slurm/planner_physics_test.sbatch   # how much the force limit matters
#SBATCH -J qc-pptest
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
nvidia-smi --query-gpu=name,memory.total --format=csv
python scripts/planner_physics_test.py --name "${NAME:-pp-test}" ${ARGS:-}
