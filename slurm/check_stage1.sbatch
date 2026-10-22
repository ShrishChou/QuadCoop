#!/bin/bash
# GPU check of the Stage 1 env with your trained walkers (a few minutes).
#
#   WALKER_ANYMAL=<anymal model.pt> WALKER_SPOT=<spot model.pt> sbatch slurm/check_stage1.sbatch
#SBATCH -J qc-check-push
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 00:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
QUADCOOP_WALKER_CKPT="$WALKER_ANYMAL" python scripts/check_stage1.py --task QuadCoop-Push-AnymalC --envs 64
QUADCOOP_WALKER_CKPT="$WALKER_SPOT"   python scripts/check_stage1.py --task QuadCoop-Push-Spot   --envs 64
