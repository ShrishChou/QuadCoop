#!/usr/bin/env bash
# Spot-arm turn in place (docs/spot_arm_pair.md, "Turn in place"): three matched MAPPO runs, same task, reward, starts,
# seed and 2000 iterations; settings in slurm/spot_arm_turn.env. Each is followed by its held-out evaluation.
#   T1 sa_turn_stowed_s0   arms stowed
#   T2 sa_turn_hand_s0     persistent hand targets, PPO alone
#   T3 sa_turn_bc_s0       persistent hand targets, cloned from the scripted maneuver, then PPO + fading imitation
# Requires the demonstrations (slurm/spot_arm_turn_prep.sbatch -> logs/demos/turn40.pt).
#   bash slurm/submit_spot_arm_turn.sh        RUNS="T3" SEED=1 bash slurm/submit_spot_arm_turn.sh
set -euo pipefail
cd "$(dirname "$0")/.."
source slurm/spot_arm_turn.env
[[ -s $DEMOS ]] || { echo "no demonstrations at $DEMOS: sbatch slurm/spot_arm_turn_prep.sbatch"; exit 1; }
SEED=${SEED:-0}; ITERS=${ITERS:-2000}
declare -A CFG=([T1]="stowed stowed" [T2]="hand hand_rate" [T3]="bc hand_rate")
for r in ${RUNS:-T1 T2 T3}; do
  set -- ${CFG[$r]}; nm=$1; arm=$2; run=sa_turn_${nm}_s${SEED}
  extra=""; [[ $nm == bc ]] && extra="$BC"
  part="-p mit_preemptable --requeue -t 12:00:00"
  [[ "${NORMAL:-T3}" == *"$r"* ]] && part="-p mit_normal_gpu -t 06:00:00"
  t=$(ALGO=mappo SEED=$SEED RUN_NAME=$run ITERS=$ITERS LOGGER=wandb EXTRA="--arm $arm $TURN $extra" \
      sbatch --parsable $part --exclude=node4207 slurm/train_coop2.sbatch)
  e=$(CK=logs/marl2/$run/model_$ITERS.pt NAME=sa-turn-$run sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue \
      --exclude=node4207 --dependency=afterok:$t slurm/spot_arm_turn_eval.sbatch)
  echo "$r $run: train $t ($part), eval $e"
done
