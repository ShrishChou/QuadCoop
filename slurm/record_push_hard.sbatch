#!/bin/bash
# Videos of a Stage 1b policy at a level, optionally for one object.
#
#   ROBOT=anymal_c WALKER=<walker.pt> CKPT=<pushhard model.pt> LEVEL=4 OBJECT=arch sbatch slurm/record_push_hard.sbatch
#
# OBJECT: cube long sphere cylinder beam l_shape t_shape arch dumbbell asym (empty = mixed).
#SBATCH -J qc-pushhard-video
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 4
#SBATCH --mem=32G
#SBATCH -t 00:30:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in
  anymal_c) TASK=QuadCoop-PushHard-AnymalC ;;
  spot)     TASK=QuadCoop-PushHard-Spot ;;
esac
: "${WALKER:?set WALKER}"; : "${CKPT:?set CKPT}"
export QUADCOOP_WALKER_CKPT="$WALKER" QUADCOOP_PUSH_LEVEL="${LEVEL:-3}" QUADCOOP_PUSH_OBJECT="${OBJECT:-}"
python play_push_hard.py "$TASK" --checkpoint-file "$CKPT" --num-envs 4 \
    --video True --video-length 1500
