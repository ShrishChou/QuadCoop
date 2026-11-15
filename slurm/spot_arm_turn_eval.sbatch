#!/bin/bash
# Spot-arm turn in place: held-out evaluation with arm and partner ablations (scripts/spot_arm/turn_inplace.py).
#   CK=logs/marl2/sa_turn_bc_s0/model_2000.pt NAME=sa-turn-sa_turn_bc_s0 sbatch slurm/spot_arm_turn_eval.sbatch
#SBATCH -J qc-saturnev
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -t 00:45:00
#SBATCH --exclude=node4207
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
python scripts/spot_arm/turn_inplace.py --checkpoint "${CK:?}" --out "evals/${NAME:?}" ${ARGS:-}
