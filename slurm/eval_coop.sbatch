#!/bin/bash
# Evaluate two-robot pushing: ANYmal alone, Spot alone, both single-robot policies
# together (no coordination training), and a trained IPPO/MAPPO run, on one task grid
# with object masses 20-120 kg.
#
#   RUN=mappo_seed0 sbatch slurm/eval_coop.sbatch                     # all four conditions
#   RUN=ippo_seed0 CONDITIONS=trained sbatch slurm/eval_coop.sbatch   # just the trained policy
#   RUN=mappo_seed0 EVAL_ARGS="--masses 40,80 --videos 2" sbatch slurm/eval_coop.sbatch
#
# Results: logs/marl/<run>/eval_model_<N>/ (episodes.csv, summary.md with M50 per
# condition and object, summary.json, vs_mass.png, videos/).
#SBATCH -J qc-eval-coop
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 04:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_SHAPES=v2
: "${RUN:?set RUN=<algo>_seed<seed> (a folder in logs/marl)}"
python scripts/eval_coop.py --run "$RUN" --conditions "${CONDITIONS:-anymal,spot,pair,trained}" ${EVAL_ARGS:-}
