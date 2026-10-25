#!/bin/bash
# Train a Stage 2 policy from scratch on a registered walker and evaluate it, as one chain of jobs.
#
#   slurm/chain_push2_scratch.sh                       # defaults: Spot 2b on walker-spot-rai-falcon
#   ROBOT=anymal_c WALKER_ID=walker-anymal-v1 ID=s2b-anymal-fs slurm/chain_push2_scratch.sh
#   DRY=1 slurm/chain_push2_scratch.sh                 # print the sbatch commands only
#
# Phase A ("hold" success rule, 45 s episodes, curriculum from level 0) in segments that each
# continue the run to the next milestone: MILESTONES="10000 20000 32000". After each segment the
# newest checkpoint is registered as <ID>-it<iteration> and evaluated with the h80 suite, so the
# learning curve shows up in evals/README.md while training goes on.
# Phase B continues the run for FINAL_ITERS (4000) with the terminate rule and 80 s episodes (as
# s2b-anymal-term80 was), and only starts if phase A reached its last milestone.
# The final model is registered as <ID> and gets the h80, precise and standard suites + showcase.
#
# Training segments share one job name with --dependency=singleton: they run one at a time, in
# order, and a preempted + requeued segment finishes before the next one starts.
# Options (env): ROBOT (spot), VARIANT (b), WALKER_ID (walker-spot-rai-falcon), RUN (fs),
# ID (s2b-spot-fs), SHOWCASE (s2b_spot_fs), MILESTONES, FINAL_ITERS, TRAIN_PART, EVAL_PART, EXCLUDE.
set -euo pipefail
ROBOT=${ROBOT:-spot}
VARIANT=${VARIANT:-b}
WALKER_ID=${WALKER_ID:-walker-spot-rai-falcon}
RUN=${RUN:-fs}
ID=${ID:-s2b-spot-fs}
SHOWCASE=${SHOWCASE:-${ID//-/_}}
MILESTONES=${MILESTONES:-10000 20000 32000}
FINAL_ITERS=${FINAL_ITERS:-4000}
TRAIN_PART=${TRAIN_PART:-"-p mit_preemptable --requeue -t 2-00:00:00"}
EVAL_PART=${EVAL_PART:-"-p mit_normal_gpu,mit_preemptable -t 06:00:00"}
EXCLUDE=${EXCLUDE:---exclude=node3006}
case "$ROBOT" in anymal_c) R=AnymalC ;; spot) R=Spot ;; *) echo "ROBOT must be anymal_c or spot"; exit 1 ;; esac
TASK=QuadCoop-Push2${VARIANT}-$R
EXP=logs/rsl_rl/push2${VARIANT}_$ROBOT
JOB=tr-$ID  # all training segments + phase B: one name, run one at a time (singleton)

python scripts/methods.py list | grep -q "^$WALKER_ID " || { echo "walker $WALKER_ID is not registered"; exit 1; }
if ls -d "$EXP"/2*_"$RUN"/ >/dev/null 2>&1; then
  echo "note: $EXP already has a run named $RUN; the chain continues it (pick another RUN for a new one)"
fi
mkdir -p logs/slurm
LOG=logs/slurm/chain_$ID.txt

# submit SCRIPT as job NAME after DEP, with VAR=VALUE settings; variables from earlier runs in your
# shell that would change the job (warm start, continuation, success rule, ...) are cleared first
CLEAR=(-u INIT -u INIT_RUN -u INIT_CKPT -u REQUIRE_ITERS -u WALKER -u SPOT_PROFILE -u SCRATCH
       -u START_LEVEL -u QUADCOOP_SUCCESS_MODE -u QUADCOOP_EPISODE_S -u QUADCOOP_ACTION_FIX
       -u QUADCOOP_START_LEVEL -u QUADCOOP_WALKER_CKPT -u QUADCOOP_SPOT_PROFILE -u QUADCOOP_WALKER_HISTORY)
launch() {  # launch NAME DEPENDENCY PARTITION SCRIPT [VAR=VALUE ...]
  local name=$1 dep=$2 part=$3 script=$4; shift 4
  if [[ "${DRY:-0}" == "1" ]]; then
    echo "env $* sbatch $part $EXCLUDE -J $name --dependency=$dep $script" >&2; echo "DRY$RANDOM"; return
  fi
  # shellcheck disable=SC2086
  env "${CLEAR[@]}" "$@" sbatch --parsable $part $EXCLUDE -J "$name" --dependency="$dep" "$script" | cut -d';' -f1
}

echo "chain $ID ($(date)): $TASK on $WALKER_ID, run $RUN, milestones $MILESTONES, then +$FINAL_ITERS terminate/80 s" | tee "$LOG"
BASE=(VARIANT=$VARIANT ROBOT=$ROBOT WALKER_ID=$WALKER_ID)
EVAL=(EXP=$EXP ID=$ID WALKER_ID=$WALKER_ID TASK=$TASK)
for M in $MILESTONES; do
  T=$(launch "$JOB" singleton "$TRAIN_PART" slurm/train_push2.sbatch "${BASE[@]}" SCRATCH=1 RUN_NAME="$RUN" ITERS="$M")
  E=$(launch "ev-$ID-$M" "afterany:$T" "$EVAL_PART" slurm/eval_checkpoint.sbatch "${EVAL[@]}" RUN="$RUN" SUITES=h80 \
        NOTE="$ID: from scratch on $WALKER_ID (hold rule, 45 s)")
  echo "  train to $M: job $T   -> h80 eval: job $E" | tee -a "$LOG"
  LAST=$M
done
B=$(launch "$JOB" singleton "$TRAIN_PART" slurm/train_push2.sbatch "${BASE[@]}" RUN_NAME="${RUN}_term80" INIT_RUN="$RUN" \
      REQUIRE_ITERS="$LAST" ITERS="$FINAL_ITERS" QUADCOOP_SUCCESS_MODE=terminate QUADCOOP_EPISODE_S=80)
echo "  phase B (+$FINAL_ITERS, terminate, 80 s): job $B" | tee -a "$LOG"
F=$(launch "ev-$ID-final" "afterok:$B" "$EVAL_PART" slurm/eval_checkpoint.sbatch "${EVAL[@]}" RUN="${RUN}_term80" FINAL=1 \
      SUITES=h80 SHOWCASE="$SHOWCASE" NOTE="$ID: from scratch on $WALKER_ID, then terminate rule and 80 s")
echo "  final: register $ID + h80 + showcase eval_videos/$SHOWCASE: job $F" | tee -a "$LOG"
for S in precise standard; do
  J=$(launch "ev-$ID-$S" "afterok:$F" "$EVAL_PART" slurm/eval_method.sbatch ID="$ID" SUITE="$S")
  echo "  final $S: job $J" | tee -a "$LOG"
done
echo "job ids saved in $LOG; watch with: squeue --me" | tee -a "$LOG"
