#!/bin/bash
# Output saturation of the existing high-level policies (scripts/action_stats.py): Stage 1b
# (pushhard), Stage 1c (pushhard2) and the Stage 2 control, newest run of each, both robots.
# ~15 min. Decides which checkpoint is a sound warm start for the fixed Stage 2 runs.
#   sbatch slurm/action_stats.sbatch
#SBATCH -J qc-actstats
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -t 01:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
newest_ckpt() {
  local run; run=$(ls -d $1/ 2>/dev/null | sort | tail -1)
  [[ -n "$run" ]] || return 1
  ls "$run"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2
}
for ROBOT in anymal_c spot; do
  case "$ROBOT" in anymal_c) R=AnymalC ;; spot) R=Spot ;; esac
  # the original walker (not a Spot sweep run: those use other joint gains)
  WRUN=$(ls -d logs/rsl_rl/walker_$ROBOT/2*/ | grep -vE '_(pose|soft|damped)/$' | sort | tail -1)
  export QUADCOOP_WALKER_CKPT=$(ls "$WRUN"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2)
  export QUADCOOP_SPOT_PROFILE=v1
  for pair in "pushhard:QuadCoop-PushHard-$R" "pushhard2:QuadCoop-PushHard2-$R" "push2ctrl:QuadCoop-Push2ctrl-$R"; do
    EXP=${pair%%:*}; TASK=${pair#*:}
    CK=$(newest_ckpt "logs/rsl_rl/${EXP}_$ROBOT/2*") || { echo "(no $EXP run for $ROBOT)"; continue; }
    QUADCOOP_SHAPES=$([[ $EXP == pushhard ]] && echo v1 || echo v2) \
      python scripts/action_stats.py --task "$TASK" --checkpoint "$CK" 2>&1 | tail -7
  done
done
