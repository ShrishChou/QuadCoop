#!/bin/bash
# Spot walker sweep: one actuator / gait-prior profile per job (quadcoop/robots/spot.py):
#   pose    v1 gains (kp 500, kd 1), knee pose prior relaxed 0.15 -> 0.4
#   soft    ANYmal-style gains kp 197, kd 12.6, relaxed knee prior
#   damped  Menagerie gains kp 500, kd 40, relaxed knee prior
# Run name walker_spot/<date>_<profile>. Preemptable-safe: a requeued or resubmitted job
# continues that profile's newest checkpoint and stops at ITERS total.
#   PROFILE=soft sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_spot_walker.sbatch
# Fine-tune an existing walker instead of starting from scratch (same gains required, so
# v1/pose for the original walker): INIT_RUN=<run folder in walker_spot> [INIT_CKPT=model_N.pt]
# with ITERS = number of fine-tuning iterations, and RUN_TAG to name the run apart, e.g.
#   PROFILE=v1 RUN_TAG=ft INIT_RUN=2026-10-19_11-45-37_seed0 ITERS=2000 QUADCOOP_PUSH_FORCE=1 \
#     QUADCOOP_PUSH_MAX_FRAC=0.3 sbatch slurm/train_spot_walker.sbatch
#SBATCH -J qc-spotwalk
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
PROFILE=${PROFILE:?set PROFILE=v1|rai|pose|soft|damped}
export QUADCOOP_SPOT_PROFILE=$PROFILE
ITERS=${ITERS:-6000}
NAME=${PROFILE}${RUN_TAG:-}
EXP=logs/rsl_rl/walker_spot
ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}" --agent.seed "${SEED:-0}"
      --agent.run-name "$NAME" --agent.logger "${LOGGER:-wandb}"
      --video True --video-length 300 --video-interval "${VIDEO_INTERVAL:-5000}")
PREV=""
for d in $(ls -d "$EXP"/2*_"$NAME"/ 2>/dev/null | sort -r); do
  if ls "$d"model_*.pt >/dev/null 2>&1; then PREV=$(basename "$d"); break; fi
done
if [[ -n "${INIT_RUN:-}" ]]; then
  # fine-tune: checkpoints continue the numbering of INIT_CKPT, so the target is START + ITERS
  CK=${INIT_CKPT:-$(basename "$(ls "$EXP/$INIT_RUN"/model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2)")}
  START=$(echo "$CK" | sed -E 's/model_([0-9]+)\.pt/\1/')
  if [[ -n "$PREV" ]]; then
    LAST=$(ls "$EXP/$PREV"/model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1/' | sort -n | tail -1)
    LEFT=$(( START + ITERS - LAST ))
    if (( LEFT <= 1 )); then echo "$EXP/$PREV fine-tune done (at $LAST)"; exit 0; fi
    ARGS+=(--agent.resume True --agent.load-run "$PREV" --agent.load-checkpoint "model_$LAST.pt"
           --agent.max-iterations "$LEFT")
    echo "continuing fine-tune $EXP/$PREV from $LAST for $LEFT more iterations"
  else
    ARGS+=(--agent.resume True --agent.load-run "$INIT_RUN\$" --agent.load-checkpoint "$CK"
           --agent.max-iterations "$ITERS")
    echo "fine-tuning $EXP/$INIT_RUN/$CK for $ITERS iterations"
  fi
elif [[ -n "$PREV" ]]; then
  LAST=$(ls "$EXP/$PREV"/model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1/' | sort -n | tail -1)
  LEFT=$(( ITERS - LAST ))
  if (( LEFT <= 1 )); then echo "$EXP/$PREV already at iteration $LAST (target $ITERS)"; exit 0; fi
  ARGS+=(--agent.resume True --agent.load-run "$PREV" --agent.load-checkpoint "model_$LAST.pt"
         --agent.max-iterations "$LEFT")
  echo "continuing $EXP/$PREV from $LAST for $LEFT more iterations"
else
  ARGS+=(--agent.max-iterations "$ITERS")
fi
nvidia-smi --query-gpu=name,memory.total --format=csv
echo "profile=$PROFILE args=${ARGS[*]}"
python train.py QuadCoop-Walker-Spot "${ARGS[@]}"
