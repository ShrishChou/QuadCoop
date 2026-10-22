#!/bin/bash
# GPU check of the Stage 1b env with your walkers (a few minutes).
#
#   WALKER_ANYMAL=<anymal walker.pt> WALKER_SPOT=<spot walker.pt> sbatch slurm/check_stage1b.sbatch
#SBATCH -J qc-check-hard
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 00:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
QUADCOOP_WALKER_CKPT="$WALKER_ANYMAL" python scripts/check_stage1b.py --task QuadCoop-PushHard-AnymalC --envs 256
QUADCOOP_WALKER_CKPT="$WALKER_SPOT"   python scripts/check_stage1b.py --task QuadCoop-PushHard-Spot   --envs 256
