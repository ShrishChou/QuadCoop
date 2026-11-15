#!/bin/bash
# Spot-arm turn pilot evaluation (scripts/spot_arm/pair_eval.py): held-out starts, arm ablation, videos. ~15 min.
#   CK=logs/marl2/sa_mappo_learned_s0/model_2000.pt NAME=sa-pilot-sa_mappo_learned_s0 sbatch slurm/spot_arm_eval.sbatch
#SBATCH -J qc-saeval
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -t 01:00:00
#SBATCH --exclude=node4207
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
python scripts/spot_arm/pair_eval.py --checkpoint "${CK:?}" --name "${NAME:?}" ${ARGS:-}
