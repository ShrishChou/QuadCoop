#!/usr/bin/env bash
# Spot-arm turn pilot (docs/spot_arm_pair.md): two arm-equipped Spots on RAI's frozen walker, from scratch,
# IPPO / MAPPO x arms stowed / learned, same tasks, reward, seed and step budget:
#   A sa_ippo_stowed_s0   B sa_ippo_learned_s0   C sa_mappo_stowed_s0   D sa_mappo_learned_s0
# Resumable (the sbatch passes --resume; a requeued job continues from its last checkpoint). Run the wiring test
# first (slurm/spot_arm_wiring.sbatch). Then each run's evaluation on held-out starts (slurm/spot_arm_eval.sbatch).
#   bash slurm/submit_spot_arm_pilot.sh            # all four, seed 0
#   RUNS="B D" SEED=1 bash slurm/submit_spot_arm_pilot.sh
set -euo pipefail
cd "$(dirname "$0")/.."
source slurm/spot_arm_pilot.env
[[ -s evals/spot_arm/pair_wiring/report.json ]] && grep -q '"pass": true' evals/spot_arm/pair_wiring/report.json || {
  echo "wiring test has not passed (evals/spot_arm/pair_wiring/report.json): sbatch slurm/spot_arm_wiring.sbatch"; exit 1; }
SEED=${SEED:-0}; ITERS=${ITERS:-2000}
declare -A CFG=([A]="ippo stowed" [B]="ippo learned" [C]="mappo stowed" [D]="mappo learned")
for r in ${RUNS:-A B C D}; do
  set -- ${CFG[$r]}; algo=$1; arm=$2; run=sa_${algo}_${arm}_s${SEED}
  # the first two on the normal partition (2 GPUs per user, 6 h), the others on preemptable (requeued jobs resume)
  part="-p mit_preemptable --requeue -t 12:00:00"
  [[ "${NORMAL:-B D}" == *"$r"* ]] && part="-p mit_normal_gpu -t 06:00:00"
  t=$(ALGO=$algo SEED=$SEED RUN_NAME=$run ITERS=$ITERS LOGGER=wandb EXTRA="--arm $arm $PILOT" \
      sbatch --parsable $part --exclude=node4207 slurm/train_coop2.sbatch)
  e=$(CK=logs/marl2/$run/model_$ITERS.pt NAME=sa-pilot-$run sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue \
      --exclude=node4207 --dependency=afterok:$t slurm/spot_arm_eval.sbatch)
  echo "$r $run: train $t ($part), eval $e"
done
