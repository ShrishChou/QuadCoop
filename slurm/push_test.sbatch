#!/bin/bash
# Scripted push test (scripts/push_test.py): no policy, both robots push straight, side by side,
# one per contact surface, vs each robot alone. Stats -> evals/push-test/, videos ->
# logs/evals/push-test/videos/. About 15-20 minutes.
#
#   sbatch slurm/push_test.sbatch
#   MASSES=60,90 ARGS="--objects beam,arch,dumbbell" sbatch slurm/push_test.sbatch
# Optional: NAME (push-test), MASSES (40,60,80,90), REPS (2), HORIZON (20), ARGS (more options).
#SBATCH -J qc-pushtest
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
python scripts/push_test.py --name "${NAME:-push-test}" --masses "${MASSES:-40,60,80,90}" --reps "${REPS:-2}" \
    --horizon "${HORIZON:-20}" ${ARGS:-}
