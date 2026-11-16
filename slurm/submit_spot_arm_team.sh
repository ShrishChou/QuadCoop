#!/usr/bin/env bash
# Spot-arm teamwork sweep (docs/spot_arm_pair.md, "Teamwork sweep"): IPPO / MAPPO x arms stowed / joint-target arms
# on the +-60 deg task of the hand wave (slurm/spot_arm_hand.env TURN60: 1 m, long object 18-22 kg, 0 / +-60 deg),
# seeds 0-2. MAPPO seed 0 is H2 / H3 (sa_mappo_{stowed,learned}60_s0) and is not rerun. Every run is followed by
# scripts/spot_arm/pair_eval.py --turn 60: arm ablation (joint arms) and solo_1 / solo_2 (partner parked).
#   bash slurm/submit_spot_arm_team.sh                      # the 10 new runs
#   SEEDS="1" ALGOS="ippo" ARMS="learned" bash slurm/submit_spot_arm_team.sh
set -euo pipefail
cd "$(dirname "$0")/.."
source slurm/spot_arm_hand.env
ITERS=${ITERS:-2000}
NORMAL=${NORMAL:-"sa_ippo_stowed60_s0 sa_ippo_learned60_s0"}  # the two mit_normal_gpu slots: finish seed 0 first
for seed in ${SEEDS:-0 1 2}; do
  for algo in ${ALGOS:-ippo mappo}; do
    for arm in ${ARMS:-stowed learned}; do
      run=sa_${algo}_${arm}60_s${seed}
      [[ -e logs/marl2/$run/model_$ITERS.pt ]] && { echo "$run: done, skipped"; continue; }
      part="-p mit_preemptable --requeue -t 12:00:00"
      [[ " $NORMAL " == *" $run "* ]] && part="-p mit_normal_gpu -t 06:00:00"
      t=$(ALGO=$algo SEED=$seed RUN_NAME=$run ITERS=$ITERS LOGGER=wandb EXTRA="--arm $arm $TURN60" \
          sbatch --parsable $part --exclude=node4207 slurm/train_coop2.sbatch)
      e=$(CK=logs/marl2/$run/model_$ITERS.pt NAME=sa-team-$run ARGS="--turn 60" sbatch --parsable \
          -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 --dependency=afterok:$t slurm/spot_arm_eval.sbatch)
      echo "$run: train $t ($part), eval $e"
    done
  done
done
