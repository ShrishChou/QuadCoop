#!/bin/bash
# Integration check of a compliant walker inside the two-robot env (scripts/walker_coop_check.py): inputs (order,
# size, normalizer), force wiring against an independent recomputation, partner / ground exclusion, smoke run.
#
#   E=logs/rsl_rl/walker_anymal_c_compliant
#   V22K=$(ls $(ls -d $E/*_v22_k1000 | tail -1)/model_*.pt | sort -V | tail -1)
#   WALKER=$V22K NAME=wiring-v22k sbatch slurm/walker_coop_check.sbatch
#SBATCH -J qc-wiring
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 01:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
nvidia-smi --query-gpu=name,memory.total --format=csv
python scripts/walker_coop_check.py --walker "${WALKER:?set WALKER=<compliant walker model.pt>}" --name "${NAME:-wiring-check}" ${ARGS:-}
