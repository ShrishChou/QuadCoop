#!/bin/bash
# GPU smoke test: both walkers build, forces and boxes behave, two-robot scene works.
#   sbatch slurm/smoke.sbatch
#SBATCH -J qc-smoke
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 00:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
nvidia-smi --query-gpu=name,memory.total,driver_version --format=csv
python scripts/smoke_test.py
