#!/bin/bash
# Walker transition test (scripts/walker_transition_test.py): start / stop / reverse in free space, position
# corrections with one fixed controller, and stop / restart / release under load, for any number of walkers.
#
#   E=logs/rsl_rl/walker_anymal_c_compliant
#   V21=$(ls $(ls -d $E/*_v21 | tail -1)/model_*.pt | sort -V | tail -1)
#   V22=$(ls $(ls -d $E/*_v22 | tail -1)/model_*.pt | sort -V | tail -1)
#   V22K=$(ls $(ls -d $E/*_v22_k1000 | tail -1)/model_*.pt | sort -V | tail -1)
#   WALKERS="v1=logs/evals/walker-anymal-v1/model.pt,v21=$V21,v22=$V22,v22k=$V22K" NAME=tt-walkers sbatch slurm/walker_transition_test.sbatch
#SBATCH -J qc-ttest
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
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
nvidia-smi --query-gpu=name,memory.total --format=csv
python scripts/walker_transition_test.py --walkers "${WALKERS:?set WALKERS=label=checkpoint,...}" --name "${NAME:-tt-test}" ${ARGS:-}
