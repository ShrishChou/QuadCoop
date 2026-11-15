#!/bin/bash
# Spot + arm pilot step 2 (docs/spot_arm.md): CPU search for any constant command that pushes 20/40/60 kg.
#SBATCH -J qc-spotcap
#SBATCH -p mit_normal
#SBATCH -c 8
#SBATCH --mem=16G
#SBATCH -t 01:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
python scripts/spot_arm/push_capability.py --judo "${JUDO:-$HOME/ext/judo}" --samples "${SAMPLES:-150}" --workers 8
