#!/bin/bash
# Stage 2 (shape profiles): VARIANT=a (object-frame top + front images), b (robot-frame
# top map at 10 Hz + front), ctrl (same task, no images).
#
# Each run is push2<VARIANT>_<robot>/<date>_<RUN_NAME> (default RUN_NAME s<SEED>_v2). A job
# continues the newest run with that name that has checkpoints and stops at ITERS total,
# so requeued / chained jobs never train past ITERS. Otherwise it builds the warm start
# from INIT (default: newest pushhard2_<robot> (Stage 1c), else pushhard_<robot>) with
# scripts/warmstart_push2.py (image weights zero, so it starts as that policy).
# Logs a 20 s training video to W&B every 500 iterations.
#
# Spot: SPOT_PROFILE=<profile> selects the walker's actuator profile (quadcoop/robots/spot.py)
# and, unless WALKER is given, the newest walker_spot/*_<profile> run.
#
#   VARIANT=a ROBOT=anymal_c SEED=0 sbatch slurm/train_push2.sbatch
#   # continue an existing run with longer episodes (env vars pass through to the env):
#   VARIANT=b ROBOT=anymal_c RUN_NAME=ep90 INIT_RUN=<run folder> ITERS=3000 QUADCOOP_EPISODE_S=90 sbatch ...
#   VARIANT=b ROBOT=spot SPOT_PROFILE=soft sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_push2.sbatch
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
SEED=${SEED:-0}
RUN=${RUN_NAME:-s${SEED}_v2}
ITERS=${ITERS:-6000}
case "$ROBOT" in anymal_c) R=AnymalC ;; spot) R=Spot ;; *) echo "ROBOT must be anymal_c or spot"; exit 1 ;; esac
case "$VARIANT" in a|b|ctrl) ;; *) echo "VARIANT must be a, b or ctrl"; exit 1 ;; esac
TASK=QuadCoop-Push2${VARIANT}-$R
newest_ckpt() {  # newest run dir matching $1 (glob) -> its highest model_N.pt
  local run; run=$(ls -d $1/ 2>/dev/null | sort | tail -1)
  [[ -n "$run" ]] || { echo "no runs matching $1" >&2; return 1; }
  ls "$run"model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2
}
WGLOB="logs/rsl_rl/walker_$ROBOT/2*"
if [[ "$ROBOT" == spot && -n "${SPOT_PROFILE:-}" ]]; then
  export QUADCOOP_SPOT_PROFILE=$SPOT_PROFILE
  WGLOB="logs/rsl_rl/walker_spot/2*_$SPOT_PROFILE"
fi
WALKER=${WALKER:-$(newest_ckpt "$WGLOB")}
export QUADCOOP_WALKER_CKPT="$WALKER"
unset QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT
EXP=logs/rsl_rl/push2${VARIANT}_$ROBOT
ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}" --agent.seed "$SEED" --agent.run-name "$RUN"
      --agent.logger "${LOGGER:-wandb}"
      --video True --video-length "${VIDEO_LEN:-1000}" --video-interval "${VIDEO_EVERY:-12000}")
PREV=""
for d in $(ls -d "$EXP"/2*_"$RUN"/ 2>/dev/null | sort -r); do
  if ls "$d"model_*.pt >/dev/null 2>&1; then PREV=$(basename "$d"); break; fi
done
nvidia-smi --query-gpu=name,memory.total --format=csv
if [[ -n "${INIT_RUN:-}" ]]; then
  # continue an existing Stage 2 run of the same variant under a new name (e.g. with longer
  # episodes): checkpoints continue its numbering, so the target is START + ITERS
  CK=${INIT_CKPT:-$(basename "$(ls "$EXP/$INIT_RUN"/model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1 &/' | sort -n | tail -1 | cut -d' ' -f2)")}
  START=$(echo "$CK" | sed -E 's/model_([0-9]+)\.pt/\1/')
  if [[ -n "$PREV" ]]; then
    LAST=$(ls "$EXP/$PREV"/model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1/' | sort -n | tail -1)
    LEFT=$(( START + ITERS - LAST ))
    if (( LEFT <= 1 )); then echo "$EXP/$PREV done (at $LAST)"; exit 0; fi
    ARGS+=(--agent.resume True --agent.load-run "$PREV" --agent.load-checkpoint "model_$LAST.pt"
           --agent.max-iterations "$LEFT")
    echo "continuing $EXP/$PREV from $LAST for $LEFT more iterations"
  else
    ARGS+=(--agent.resume True --agent.load-run "$INIT_RUN\$" --agent.load-checkpoint "$CK"
           --agent.max-iterations "$ITERS")
    echo "continuing from $EXP/$INIT_RUN/$CK for $ITERS iterations as run $RUN"
  fi
elif [[ -n "$PREV" ]]; then
  LAST=$(ls "$EXP/$PREV"/model_*.pt | sed -E 's/.*model_([0-9]+)\.pt$/\1/' | sort -n | tail -1)
  LEFT=$(( ITERS - LAST ))
  if (( LEFT <= 1 )); then echo "$EXP/$PREV is already at iteration $LAST (target $ITERS)"; exit 0; fi
  ARGS+=(--agent.resume True --agent.load-run "$PREV" --agent.load-checkpoint "model_$LAST.pt"
         --agent.max-iterations "$LEFT")
  echo "continuing $EXP/$PREV from $LAST for $LEFT more iterations"
else
  # warm start: newest Stage 1c run (pushhard2_<robot>, same falls/masses/episode length)
  # if there is one, else the Stage 1b run (pushhard_<robot>); INIT=<model_N.pt> overrides
  INIT=${INIT:-$(newest_ckpt "logs/rsl_rl/pushhard2_$ROBOT/2*" 2>/dev/null || newest_ckpt "logs/rsl_rl/pushhard_$ROBOT/2*")}
  WS=0000_warmstart_$RUN
  echo "warm start from $INIT -> $EXP/$WS"
  python scripts/warmstart_push2.py --task "$TASK" --init "$INIT" --device cuda:0 --out "$EXP/$WS/model_0.pt"
  ARGS+=(--agent.resume True --agent.load-run "$WS\$" --agent.load-checkpoint model_0.pt
         --agent.max-iterations "$ITERS")
fi
echo "task=$TASK walker=$WALKER map_hz=$QUADCOOP_MAP_HZ args=${ARGS[*]}"
python train_push2.py "$TASK" "${ARGS[@]}"
