#!/bin/bash
# Evaluate a Stage 1b pushing policy on a fixed task grid with a mass ablation.
#
#   ROBOT=anymal_c sbatch slurm/eval_push.sbatch      # newest pushhard + newest walker checkpoints
#   ROBOT=spot     sbatch slurm/eval_push.sbatch
#   ROBOT=spot CKPT=<pushhard model.pt> WALKER=<walker model.pt> sbatch slurm/eval_push.sbatch
#   ROBOT=anymal_c EVAL_ARGS="--objects cube,arch --masses 10,40" sbatch slurm/eval_push.sbatch
#   ROBOT=spot STAGE=1c sbatch slurm/eval_push.sbatch    # the Stage 1c (v2) retrain
#
# Results go to eval_<checkpoint>/ next to the checkpoint: episodes.csv, summary.md,
# summary.json, vs_mass.png, snapshots/ (open snapshots/index.html).
#SBATCH -J qc-eval-push
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 04:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl   # snapshots / videos render on the GPU

ROBOT=${ROBOT:-anymal_c}
STAGE=${STAGE:-1b}   # 1b = QuadCoop-PushHard-*, 1c = QuadCoop-PushHard2-* (the v2 retrain)
V=""; [[ "$STAGE" == "1c" ]] && V=2
case "$ROBOT" in
  anymal_c) TASK=QuadCoop-PushHard${V}-AnymalC ;;
  spot)     TASK=QuadCoop-PushHard${V}-Spot ;;
  *) echo "ROBOT must be anymal_c or spot"; exit 1 ;;
esac
ARGS=(--task "$TASK")
[[ -n "${CKPT:-}" ]] && ARGS+=(--checkpoint "$CKPT")      # else newest pushhard_<robot> run
[[ -n "${WALKER:-}" ]] && ARGS+=(--walker "$WALKER")      # else newest walker_<robot> run
unset QUADCOOP_WALKER_CKPT QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT
python scripts/eval_push.py "${ARGS[@]}" ${EVAL_ARGS:-}
