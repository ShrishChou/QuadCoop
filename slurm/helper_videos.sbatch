#!/bin/bash
# Videos of the contact planner with the helper robot (scripts/helper_test.py --video-only): all twelve benchmark
# objects x the four scenarios, rep 0, at 80 and 100 kg, seed 7100 (helper arm only; no statistics).
# Videos + index.html: logs/evals/helper-videos/videos/.
#   sbatch slurm/helper_videos.sbatch
#SBATCH -J qc-helpvid
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 05:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
python scripts/helper_test.py --prefix helper-videos --seed 7100 --arms helper --reps 1 --masses 80,100 \
  --objects cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus \
  --videos 1 --video-only 1 --video-arms helper --video-objects all --video-masses 80,100 --video-scenarios all \
  --video-reps 0 ${ARGS:-}
