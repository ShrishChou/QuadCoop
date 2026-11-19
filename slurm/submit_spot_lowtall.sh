#!/usr/bin/env bash
# Spot-arm, low and tall objects, light masses: does coordination (and arm use) emerge? (docs/spot_low_tall.md)
# A separate project, queued after the Spot pipeline (slurm/submit_spot_pipeline.sh) finishes.
#   objects  20 (QUADCOOP_SHAPE_SET=spot20): the 12 existing (beam included) + 4 low (16-24 cm) + 4 tall (1.1 m; the
#            narrow ones tip when pushed at body height)
#   masses   5-25 kg at every level, the same for one robot and for pairs: coordination, not strength
#   reward   r7 (its success bonus already shrinks with time) + a team time cost (--time-cost) for short episodes
#   runs     solo pusher (IPPO, partner parked) -> its actor copied to both robots -> MAPPO pair -> IPPO pair
#   AFTER=<jobid> bash slurm/submit_spot_lowtall.sh     # start the solo run after that job (default: none)
set -euo pipefail
cd "$(dirname "$0")/.."
W=logs/rsl_rl/walker_spot_arm
S3=$(ls -d $W/*push_ft_s3_handload | tail -1)/model_2999.pt
[[ -s "$S3" ]] || { echo "missing s3 walker: $S3" >&2; exit 1; }
export QUADCOOP_SPOT_ARM_WALKER=$S3 QUADCOOP_SHAPE_SET=spot20
ITERS=${ITERS:-6000}
TIME_COST=${TIME_COST:-0.5}
SH20=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus,low_slab,low_bar,low_plus,\
low_roller,tall_box,tall_column,tall_wall,top_heavy
ROW="25,0,10,60,0.10,6,1.0"
BASE="--pair spot_arm --arm learned --hand-obs --partner-map --reward r7 --time-cost $TIME_COST --mean-clip 1.1 \
--bound-coef 0.01 --entropy-coef 0.003 --train-shapes $SH20 --fixed-difficulty --fixed-level 0 --dyaw-choices \
--pilot-episode-s 40"
LV="--pilot-level 1.0,1.5,$ROW,25,5 --extra-levels 1.5,2.5,$ROW,25,5;2.0,3.5,$ROW,25,5 \
--level-mix 0:0.6,0.4,0;1000:0.3,0.4,0.3;2500:0.2,0.3,0.5"
PART="-p mit_preemptable --requeue -t 1-00:00:00 --exclude=node4207"
SOLO=sp20_solo_s0
chk=$(ALGO=ippo SEED=0 RUN_NAME=${SOLO}_check ITERS=2 LOGGER=wandb WANDB_MODE=disabled NUM_ENVS=512 \
      EXTRA="$BASE --scratch --solo-agent 0 $LV --check" \
      sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 -t 00:30:00 slurm/train_coop2.sbatch)
echo "check: $chk"
dep="afterok:$chk${AFTER:+,afterany:$AFTER}"
solo=$(ALGO=ippo SEED=0 RUN_NAME=$SOLO ITERS=$ITERS LOGGER=wandb EXTRA="$BASE --scratch --solo-agent 0 $LV" \
       sbatch --parsable $PART --dependency=$dep slurm/train_coop2.sbatch)
echo "solo $SOLO: $solo (after $dep)"
INIT=logs/shared_init/SP20_solo_${ITERS}.pt
mk=$(sbatch --parsable -p mit_normal_gpu,mit_preemptable --exclude=node4207 -c 2 --mem=8G -t 00:10:00 \
     -J qc-sp20init -o logs/slurm/%x-%j.out --dependency=afterok:$solo \
     --wrap "source .venv/bin/activate && python scripts/make_shared_ckpt.py logs/marl2/$SOLO/model_$ITERS.pt spotarm1 $INIT")
echo "shared init $INIT: $mk"
prev=$mk
for algo in mappo ippo; do
  run=sp20_pair_${algo}_s0
  t=$(ALGO=$algo SEED=0 RUN_NAME=$run ITERS=$ITERS LOGGER=wandb \
      EXTRA="$BASE --init-actors $INIT --critic-warmup-resume 100 $LV" \
      sbatch --parsable $PART --dependency=afterok:$prev slurm/train_coop2.sbatch)
  echo "pair $run: $t (after $prev)"
  prev=$t
done
