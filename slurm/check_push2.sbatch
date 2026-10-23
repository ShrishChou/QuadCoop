#!/bin/bash
# Stage 2 input checks (obs shapes, sampler, geometry, profiles, map rate, ablation switches)
# and the warm-start equivalence check, for a, b and ctrl. ~10 min. Writes
# logs/check_push2/check_push2_{a,b}.png (render | top profile | front profile per shape).
#   ROBOT=anymal_c sbatch slurm/check_push2.sbatch
#SBATCH -J qc-check2
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=32G
#SBATCH -t 01:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_SHAPES=v2
ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in anymal_c) R=AnymalC ;; spot) R=Spot ;; *) echo "ROBOT must be anymal_c or spot"; exit 1 ;; esac
newest_ckpt() {
  local run; run=$(ls -d "$1"/2*/ 2>/dev/null | sort | tail -1)
  [[ -n "$run" ]] || { echo "no runs in $1" >&2; return 1; }
  ls "$run"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2
}
export QUADCOOP_WALKER_CKPT=${WALKER:-$(newest_ckpt logs/rsl_rl/walker_$ROBOT)}
unset QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT
mkdir -p logs/check_push2
python scripts/check_push2.py --robot "$ROBOT" --variants a,b --out logs/check_push2 --device cuda:0
# warm start: newest Stage 1c run (pushhard2_<robot>, same falls/masses/episode length)
# if there is one, else the Stage 1b run (pushhard_<robot>); INIT=<model_N.pt> overrides
INIT=${INIT:-$(newest_ckpt logs/rsl_rl/pushhard2_$ROBOT 2>/dev/null || newest_ckpt logs/rsl_rl/pushhard_$ROBOT)}
for V in a b ctrl; do
  python scripts/warmstart_push2.py --task QuadCoop-Push2${V}-$R --init "$INIT" --device cuda:0 \
    --out logs/check_push2/warmstart_${V}_$ROBOT.pt
done
echo "ALL STAGE 2 CHECKS PASSED"
