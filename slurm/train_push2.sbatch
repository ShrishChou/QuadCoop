#!/bin/bash
# Stage 2 (shape profiles): VARIANT=a (object-frame top + front images), b (robot-frame
# top map at 10 Hz + front), ctrl (same task, no images). Resumes the newest
# push2<VARIANT>_<robot> run that has checkpoints; otherwise builds the warm start from
# INIT (default: newest pushhard2_<robot> (Stage 1c), else pushhard_<robot>) with
# scripts/warmstart_push2.py (image weights zero, so it starts as that policy).
# Logs a 20 s training video to W&B every 500 iterations.
#   VARIANT=a ROBOT=anymal_c sbatch slurm/train_push2.sbatch
#   VARIANT=b ROBOT=spot sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_push2.sbatch
#SBATCH -J qc-push2
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
case "$VARIANT" in a|b|ctrl) ;; *) echo "VARIANT must be a, b or ctrl"; exit 1 ;; esac
TASK=QuadCoop-Push2${VARIANT}-$R
newest_ckpt() {
  local run; run=$(ls -d "$1"/2*/ 2>/dev/null | sort | tail -1)
  [[ -n "$run" ]] || { echo "no runs in $1" >&2; return 1; }
  ls "$run"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2
}
WALKER=${WALKER:-$(newest_ckpt logs/rsl_rl/walker_$ROBOT)}
export QUADCOOP_WALKER_CKPT="$WALKER"
unset QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT
EXP=logs/rsl_rl/push2${VARIANT}_$ROBOT
ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}" --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-6000}" --agent.run-name "seed${SEED:-0}"
      --agent.logger "${LOGGER:-wandb}"
      --video True --video-length "${VIDEO_LEN:-1000}" --video-interval "${VIDEO_EVERY:-12000}")
PREV=""
for d in $(ls -d "$EXP"/2*/ 2>/dev/null | sort -r); do
  if ls "$d"model_*.pt >/dev/null 2>&1; then PREV=$(basename "$d"); break; fi
done
nvidia-smi --query-gpu=name,memory.total --format=csv
if [[ -n "$PREV" ]]; then
  ARGS+=(--agent.resume True --agent.load-run "$PREV"); echo "continuing $EXP/$PREV"
else
  # warm start: newest Stage 1c run (pushhard2_<robot>, same falls/masses/episode length)
# if there is one, else the Stage 1b run (pushhard_<robot>); INIT=<model_N.pt> overrides
INIT=${INIT:-$(newest_ckpt logs/rsl_rl/pushhard2_$ROBOT 2>/dev/null || newest_ckpt logs/rsl_rl/pushhard_$ROBOT)}
  echo "warm start from $INIT"
  python scripts/warmstart_push2.py --task "$TASK" --init "$INIT" --device cuda:0
  ARGS+=(--agent.resume True --agent.load-run 0000_warmstart --agent.load-checkpoint model_0.pt)
fi
echo "task=$TASK walker=$WALKER map_hz=$QUADCOOP_MAP_HZ args=${ARGS[*]}"
python train_push2.py "$TASK" "${ARGS[@]}"
