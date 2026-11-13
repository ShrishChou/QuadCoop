#!/bin/bash
# Engaged-start beam push with the frozen walker (scripts/beam_push_test.py): two ANYmals, scripted commands.
# Stats -> evals/<NAME>/, full output -> logs/evals/<NAME>/. Default 27 cases (9 env builds), about 20-30 min.
#   NAME=beam-push sbatch slurm/beam_push_test.sbatch
#   NAME=beam-push-smoke ARGS="--speeds 0.6 --masses 60 --mus 0.5 --horizon 4" sbatch slurm/beam_push_test.sbatch
#SBATCH -J qc-beampush
#SBATCH -p mit_normal_gpu
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 01:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_PLANNER=ends QUADCOOP_CONTACT=train QUADCOOP_CMD_IF=raw
python scripts/beam_push_test.py --name "${NAME:-beam-push}" ${ARGS:-}
