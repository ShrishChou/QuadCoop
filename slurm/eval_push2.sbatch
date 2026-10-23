#!/bin/bash
# Evaluate a Stage 2 policy: seen / unseen shapes, in / out-of-range sizes, and the
# ablations (heading_zero, heading_zero_map for b, profile_zero, profile_roll) plus the
# action-sensitivity probe. Results: eval2_<ckpt>/summary.md, episodes.csv,
# videos/index.html, next to the checkpoint (newest push2<VARIANT>_<robot> run by default).
#   VARIANT=a ROBOT=anymal_c sbatch slurm/eval_push2.sbatch
#   VARIANT=ctrl ROBOT=anymal_c CKPT=<model_N.pt> sbatch slurm/eval_push2.sbatch
#   VARIANT=b EVAL_ARGS="--objects arch,u_channel --conditions normal,heading_zero" sbatch slurm/eval_push2.sbatch
#SBATCH -J qc-eval2
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_SHAPES=v2
export QUADCOOP_MAP_HZ=${MAP_HZ:-10}
VARIANT=${VARIANT:-a}
ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in anymal_c) R=AnymalC ;; spot) R=Spot ;; *) echo "ROBOT must be anymal_c or spot"; exit 1 ;; esac
ARGS=(--task "QuadCoop-Push2${VARIANT}-$R")
[[ -n "${CKPT:-}" ]] && ARGS+=(--checkpoint "$CKPT")
[[ -n "${WALKER:-}" ]] && ARGS+=(--walker "$WALKER")
unset QUADCOOP_WALKER_CKPT QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT
python scripts/eval_push2.py "${ARGS[@]}" ${EVAL_ARGS:-}
