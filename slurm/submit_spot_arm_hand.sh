#!/usr/bin/env bash
# Spot-arm hand wave (docs/spot_arm_pair.md, "Hand-position control"): four MAPPO runs from scratch, same reward,
# seed, step budget and held-out evaluation as the turn pilot; settings in slurm/spot_arm_hand.env.
#   H1 sa_mappo_hand30_s0     hand position, 0 / +-30 deg   vs pilot D: the interface change alone
#   H2 sa_mappo_stowed60_s0   arms stowed,   0 / +-60 deg   body pushing on the larger turn
#   H3 sa_mappo_learned60_s0  joint targets, 0 / +-60 deg   does the larger turn alone bring arm use
#   H4 sa_mappo_hand60_s0     hand position, 0 / +-60 deg   vs H2: arm advantage; vs H3: interface advantage
# Each run is followed by its evaluation (slurm/spot_arm_eval.sbatch, --turn 30 or 60). Requires the hand preflight
# (slurm/spot_arm_hand_wiring.sbatch -> evals/spot_arm/hand_reach/report.json) to have passed.
#   bash slurm/submit_spot_arm_hand.sh            # all four, seed 0
#   RUNS="H4" SEED=1 bash slurm/submit_spot_arm_hand.sh
set -euo pipefail
cd "$(dirname "$0")/.."
source slurm/spot_arm_hand.env
[[ -s evals/spot_arm/hand_reach/report.json ]] && grep -q '"pass": true' evals/spot_arm/hand_reach/report.json || {
  echo "hand preflight has not passed (evals/spot_arm/hand_reach/report.json): sbatch slurm/spot_arm_hand_wiring.sbatch"; exit 1; }
SEED=${SEED:-0}; ITERS=${ITERS:-2000}
declare -A CFG=([H1]="hand 30" [H2]="stowed 60" [H3]="learned 60" [H4]="hand 60")
for r in ${RUNS:-H1 H2 H3 H4}; do
  set -- ${CFG[$r]}; arm=$1; turn=$2; run=sa_mappo_${arm}${turn}_s${SEED}
  args=$TURN30; [[ $turn == 60 ]] && args=$TURN60
  part="-p mit_preemptable --requeue -t 12:00:00"
  [[ "${NORMAL:-H2 H4}" == *"$r"* ]] && part="-p mit_normal_gpu -t 06:00:00"
  t=$(ALGO=mappo SEED=$SEED RUN_NAME=$run ITERS=$ITERS LOGGER=wandb EXTRA="--arm $arm $args" \
      sbatch --parsable $part --exclude=node4207 slurm/train_coop2.sbatch)
  e=$(CK=logs/marl2/$run/model_$ITERS.pt NAME=sa-hand-$run ARGS="--turn $turn" sbatch --parsable \
      -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 --dependency=afterok:$t slurm/spot_arm_eval.sbatch)
  echo "$r $run: train $t ($part), eval $e"
done
