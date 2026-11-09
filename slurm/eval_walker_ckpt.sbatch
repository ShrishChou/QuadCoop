#!/bin/bash
# Evaluate the newest checkpoint of an ANYmal walker run, found when the job starts (so it can be
# chained after a training job with --dependency=afterok:<train job>).
#
#   MODE=wt   : walker acceptance test, v1 (original) vs the run         -> evals/wt-<RUN_NAME>/
#   MODE=pair : Stage 4 pair eval (expert rules, start behind) on the run -> evals/fair-td-<RUN_NAME>-behind-expert/
#
#   RUN_NAME=v1_nocreep2 MODE=wt QUADCOOP_CONTACT=nocreep sbatch --dependency=afterok:<job> slurm/eval_walker_ckpt.sbatch
#SBATCH -J qc-wevalck
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 03:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
RUN_DIR=$(ls -d logs/rsl_rl/walker_anymal_c/*_"${RUN_NAME:?set RUN_NAME}" | tail -1)
CKPT=$PWD/$(ls "$RUN_DIR"/model_*.pt | sort -V | tail -1)
echo "run=$RUN_DIR ckpt=$CKPT contact=${QUADCOOP_CONTACT:-train}"
case "${MODE:?set MODE=wt|pair}" in
  wt)   python scripts/walker_test.py --walkers "v1=logs/evals/walker-anymal-v1/model.pt,$RUN_NAME=$CKPT" \
          --name "wt-$RUN_NAME" ${ARGS:-} ;;
  pair) QUADCOOP_WALKER_OVERRIDE_ANYMAL_C=$CKPT python scripts/contact_test.py --pair anymal --rules expert \
          --masses 20,40,60,80 --reps 3 --prefix "fair-td-$RUN_NAME-behind" \
          --executor stage4 --checkpoint logs/keep/marl2/turn_debug/model_15000.pt --start behind ;;
  *) echo "MODE must be wt or pair"; exit 1 ;;
esac
