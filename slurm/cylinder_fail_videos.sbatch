#!/bin/bash
# Videos of the two-robot contact planner's cylinder failures (the planner-bench setup: expert rule 4, the Stage 4
# executor turn_debug/model_15000.pt, start behind, 80 s, 20-80 kg, 4 scenarios x 3 reps, seeds 7100 and 7500, the
# old isotropic force model). Every cylinder episode is filmed; the successes' videos are then removed, so the folder
# holds only failures. Videos + index.html: logs/evals/cyl-fail-<seed>-expert/pair/videos/.
#   sbatch slurm/cylinder_fail_videos.sbatch
#SBATCH -J qc-cylvid
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
for s in 7100 7500; do
  V=logs/evals/cyl-fail-$s-expert/pair/videos
  if ! ls $V/*.mp4 >/dev/null 2>&1; then
    python scripts/contact_test.py --pair anymal --executor stage4 --checkpoint logs/keep/marl2/turn_debug/model_15000.pt \
      --rules expert --start behind --objects cylinder --masses 20,40,60,80 --reps 3 --seed "$s" --horizon 80 \
      --slow-min-s 1.0 --prefix "cyl-fail-$s" --videos 1 --video-objects cylinder --video-masses 20,40,60,80 \
      --video-scenarios all --video-reps all
  fi
  python - "$V" <<'PY'
import sys
from pathlib import Path
sys.path.insert(0, "scripts")
from contact_test import _video_index
v = Path(sys.argv[1])
gone = 0
for f in v.glob("*__success.mp4"):
    f.unlink()
    j = v / (f.name.split("__")[0] + ".json")
    if j.exists():
        j.unlink()
    gone += 1
_video_index(v)
print(f"{v}: removed {gone} success videos, kept {len(list(v.glob('*.mp4')))} failures")
PY
done
