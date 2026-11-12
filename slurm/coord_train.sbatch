#!/bin/bash
# Learned coordinator (scripts/coord_train.py). CMD = the coord_train.py arguments, e.g.
#   CMD="collect --out logs/coord/bc0 --seeds 100-103 --reps 12" sbatch slurm/coord_train.sbatch
#SBATCH -J qc-coord
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH --requeue
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_PLANNER=ends QUADCOOP_CONTACT=train QUADCOOP_CMD_IF=raw
if [[ -n "${CMD:-}" ]]; then python scripts/coord_train.py $CMD; fi
if [[ -n "${CMD2:-}" ]]; then python scripts/coord_train.py $CMD2; fi
if [[ -n "${CMD3:-}" ]]; then python scripts/coord_train.py $CMD3; fi
if [[ -n "${EVAL:-}" ]]; then python scripts/contact_test.py $EVAL; fi
# EVAL_ARGS + EVAL_SEEDS + EVAL_PREFIX: one contact_test.py run per seed, prefix <EVAL_PREFIX>-s<seed>
for s in ${EVAL_SEEDS:-}; do python scripts/contact_test.py $EVAL_ARGS --seed "$s" --prefix "${EVAL_PREFIX}-s$s"; done
