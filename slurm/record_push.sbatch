#!/bin/bash
# Record videos of a trained pushing policy at a chosen curriculum level.
#
#   ROBOT=anymal_c WALKER=<walker model.pt> CKPT=<push model.pt> LEVEL=3 sbatch slurm/record_push.sbatch
#
# Videos land next to the push checkpoint (videos/play/).
#SBATCH -J qc-push-video
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
  anymal_c) TASK=QuadCoop-Push-AnymalC ;;
  spot)     TASK=QuadCoop-Push-Spot ;;
esac
: "${WALKER:?set WALKER}"; : "${CKPT:?set CKPT}"
export QUADCOOP_WALKER_CKPT="$WALKER" QUADCOOP_PUSH_LEVEL="${LEVEL:-2}"
python play_push.py "$TASK" --checkpoint-file "$CKPT" --num-envs 4 \
    --video True --video-length 1000
EOF