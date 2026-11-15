#!/bin/bash
# Spot + arm port acceptance (docs/spot_arm.md step 1): RAI's walker in mjlab / MuJoCo Warp, one GPU, minutes.
#SBATCH -J qc-spotport
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 00:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
python scripts/spot_arm/warp_check.py --copies "${COPIES:-16}"
