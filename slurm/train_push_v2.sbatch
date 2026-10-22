#!/bin/bash
# Stage 1c: single-robot pushing with the fixes (pose-based falls, uniform masses, 45 s
# episodes, v2 beam/arch). Resumes the newest pushhard2_<robot> run that has checkpoints;
# otherwise warm-starts from INIT (default: newest pushhard_<robot> checkpoint).
#   ROBOT=spot sbatch -p mit_preemptable --requeue -t 1-00:00:00 slurm/train_push_v2.sbatch
#SBATCH -J qc-pushv2
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
ROBOT=${ROBOT:-anymal_c}
case "$ROBOT" in
  anymal_c) TASK=QuadCoop-PushHard2-AnymalC ;;
  spot)     TASK=QuadCoop-PushHard2-Spot ;;
  *) echo "ROBOT must be anymal_c or spot"; exit 1 ;;
esac
newest_ckpt() {
  local run; run=$(ls -d "$1"/2*/ 2>/dev/null | sort | tail -1)
  [[ -n "$run" ]] || { echo "no runs in $1" >&2; return 1; }
  ls "$run"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2
}
WALKER=${WALKER:-$(newest_ckpt logs/rsl_rl/walker_$ROBOT)}
export QUADCOOP_WALKER_CKPT="$WALKER"
unset QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT
EXP=logs/rsl_rl/pushhard2_$ROBOT
ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}" --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-4000}" --agent.run-name "seed${SEED:-0}"
      --agent.logger "${LOGGER:-wandb}")
PREV=""
for d in $(ls -d "$EXP"/2*/ 2>/dev/null | sort -r); do
  if ls "$d"model_*.pt >/dev/null 2>&1; then PREV=$(basename "$d"); break; fi
done
if [[ -n "$PREV" ]]; then
  ARGS+=(--agent.resume True --agent.load-run "$PREV"); echo "continuing $EXP/$PREV"
else
  INIT=${INIT:-$(newest_ckpt logs/rsl_rl/pushhard_$ROBOT)}
  mkdir -p "$EXP/0000_warmstart"; cp "$INIT" "$EXP/0000_warmstart/model_0.pt"
  ARGS+=(--agent.resume True --agent.load-run 0000_warmstart --agent.load-checkpoint model_0.pt)
  echo "warm start from $INIT"
fi
nvidia-smi --query-gpu=name,memory.total --format=csv
echo "task=$TASK walker=$WALKER args=${ARGS[*]}"
python train_push_v2.py "$TASK" "${ARGS[@]}"
