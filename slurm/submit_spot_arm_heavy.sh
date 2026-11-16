#!/usr/bin/env bash
# Spot-arm heavy transport (docs/spot_arm_pair.md, "Heavy transport"): three matched MAPPO runs, seed 0, from scratch,
# same reward (r7), rollout budget, level rows and level-mix schedule:
#   sa_heavy_learned_s0   two Spot-arms, policy-controlled (joint-target) arms
#   sa_heavy_stowed_s0    the same two bodies, arms held stowed
#   sa_heavy_solo_s0      solo control: spotarm1 alone (partner parked 40 m away, zero actions, falls ignored),
#                         trainable arm, the same task draws
# Level rows (11 columns as --pilot-level; randomized rear-side starts, each robot within +-25 deg of behind, at
# least 60 deg apart, 0.3-0.9 m gap; goal heading change 0 / +-60 deg; 0.10 m / 6 deg held 1 s):
#   L0  1 m,        18-22 kg   (the light pilot task: retention)
#   L1  1.5-2.5 m,  38-42 kg
#   L2  2-3 m,      40-60 kg
# Schedule (iterations: weights L0,L1,L2): 0: .5,.5,0 | 800: .3,.4,.3 | 1600: .2,.3,.5. 40 s episodes for every level.
# Each run is followed by pair_eval --turn 60 on the three task sizes (40 s horizon, swapped starts, arm ablation,
# solo_1 / solo_2).
#   bash slurm/submit_spot_arm_heavy.sh
#   RUNS="sa_heavy_solo_s0" bash slurm/submit_spot_arm_heavy.sh
set -euo pipefail
cd "$(dirname "$0")/.."
ITERS=${ITERS:-4000}
ROW="25,0,10,60,0.10,6,1.0"
HEAVY="--scratch --partner-map --reward r7 --mean-clip 1.1 --bound-coef 0.01 --entropy-coef 0.003 --hand-obs \
--train-shapes long --fixed-difficulty --fixed-level 0 --dyaw-choices --pilot-episode-s 40 \
--pilot-level 1.0,1.0,$ROW,22,18 --extra-levels 1.5,2.5,$ROW,42,38;2.0,3.0,$ROW,60,40 \
--level-mix 0:0.5,0.5,0;800:0.3,0.4,0.3;1600:0.2,0.3,0.5"
declare -A OPT=([sa_heavy_learned_s0]="--arm learned" [sa_heavy_stowed_s0]="--arm stowed"
                [sa_heavy_solo_s0]="--arm learned --solo-agent 0")
for run in ${RUNS:-sa_heavy_learned_s0 sa_heavy_stowed_s0 sa_heavy_solo_s0}; do
  [[ -e logs/marl2/$run/model_$ITERS.pt ]] && { echo "$run: done, skipped"; continue; }
  t=$(ALGO=mappo SEED=0 RUN_NAME=$run ITERS=$ITERS LOGGER=wandb EXTRA="--pair spot_arm ${OPT[$run]} $HEAVY" \
      sbatch --parsable -p mit_preemptable --requeue -t 12:00:00 --exclude=node4207 \
      slurm/train_coop2.sbatch)
  evals=""
  for task in "20 1" "40 2" "60 3"; do
    set -- $task
    e=$(CK=logs/marl2/$run/model_$ITERS.pt NAME=sa-heavy-$run-${1}kg-${2}m \
        ARGS="--turn 60 --mass $1 --dist $2 --horizon 40" sbatch --parsable -p mit_normal_gpu,mit_preemptable \
        --requeue --exclude=node4207 --dependency=afterok:$t slurm/spot_arm_eval.sbatch)
    evals="$evals $e"
  done
  echo "$run: train $t, evals$evals"
done
