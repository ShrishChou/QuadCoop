#!/usr/bin/env bash
# Spot-arm on the load-trained walker (push_ft_s3_handload), taken through the ANYmal pipeline:
#   1. one robot learns to push the ten objects to their goals (partner parked: --solo-agent 0), from scratch, with a
#      fixed level-mix curriculum over distance and mass (light, short first);
#   2. that robot's actor is copied to both robots (scripts/make_shared_ckpt.py, as B0 + B0 for ANYmal);
#   3. MAPPO pair from it, then IPPO pair from it, one after the other (same tasks, heavier masses).
# Masses match the ANYmal runs, so the two robots compare directly: solo 5-40 kg with the cap rising 20 -> 30 -> 40 kg
# (ANYmal Stage 1b / 2: 5-40 kg, cap 15 -> 40 kg); pairs 20-80 kg uniform at every level (ANYmal ten-object pair runs:
# --train-mass 20,80), evaluated at 20 / 40 / 60 / 80 kg.
#
#   bash slurm/submit_spot_pipeline.sh            # submit all three trainings and the init step
#   SOLO_ITERS=6000 PAIR_ITERS=6000 bash slurm/submit_spot_pipeline.sh
# Reward (since 2026-11-19, runs sp_*_gc_*): r7 with --goal-credit: each robot is paid for the object's motion toward
# its goal pose (travel and turning), x (1 + cos) for the right direction, while any part of it (the arm included)
# touches the object. r7's push_credit paid only with the trunk's front on the object, so an arm push earned nothing
# and the first run (sp_solo_s0) stopped using the arm. TAG= (empty) restores the old reward and names.
# Objects (since 2026-11-19): the single robot trains on the 20 objects of docs/spot_low_tall.md (QUADCOOP_SHAPE_SET=
# spot20: the ten below + beam, asym + 4 low + 4 tall that body-height pushing handles badly), the low and tall ones
# drawn 60% of the time, with x 1.25 pay while the arm touches (--arm-bonus 0.25), so it learns to use the arm. The
# pairs then train on the ten objects (comparable with ANYmal). Inputs do not depend on the object set.
# ARM=hand_rate (default learned = joint targets): the arm is driven by a hand target that each action moves relative to
# where it is (a x 0.6 m/s in the robot's body frame) plus an extension rate, turned into joint targets by IK
# (spot_arm_term.py); runs are named with _hr. SOLO_ONLY=1: submit only the check and the single-robot run.
# Restart (2026-11-19, runs sp_*_ft_*): the from-scratch 20-object solo (sp_solo20_gc_s0) stalled at ~3% success by
# iteration 2000 (60% of episodes on low/tall objects it could not do; 30% tipped; noise back at its 0.6 cap). The solo
# now starts from the ten-object Spot solo (sp_solo_s0, model_3800, ~73%) with --init-from (iteration count carried,
# so it runs to 3800 + SOLO_ITERS), on the 20 objects drawn evenly (LOWTALL_BIAS=1.0, raise later), with smoother
# actions: --action-rate-w 0.2 (was 0.05), --action-limit-w 0.1 (was 0.02), noise capped at --std-cap 0.4 (was 0.6).
# Heading (same day): --yaw-gate 0 --yaw-w 2.0: the signed heading progress is paid and charged at every distance,
# not only within 1.5 m of the goal, at twice the weight.
# With ARM=hand_rate only the base outputs load (the arm interface differs); the arm outputs start fresh.
set -euo pipefail
cd "$(dirname "$0")/.."
W=logs/rsl_rl/walker_spot_arm
S3=$(ls -d $W/*push_ft_s3_handload | tail -1)/model_2999.pt
[[ -s "$S3" ]] || { echo "missing s3 walker: $S3" >&2; exit 1; }
export QUADCOOP_SPOT_ARM_WALKER=$S3
TAG=${TAG-_ft}
ARM=${ARM:-learned}
CREDIT=""; [[ -n "$TAG" ]] && CREDIT="--goal-credit --arm-bonus ${ARM_BONUS:-0.25}"
[[ "$ARM" == hand_rate ]] && TAG="_hr$TAG"
export QUADCOOP_SHAPE_SET=spot20
SH20=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus,low_slab,low_bar,low_plus,\
low_roller,tall_box,tall_column,tall_wall,top_heavy
B=${LOWTALL_BIAS:-1.0}
SOLO_OBJ="--train-shapes $SH20 --shape-bias low_slab:$B,low_bar:$B,low_plus:$B,low_roller:$B,tall_box:$B,\
tall_column:$B,tall_wall:$B,top_heavy:$B"
SOLO_INIT=${SOLO_INIT:-logs/marl2/sp_solo_s0/model_3800.pt}
[[ -s "$SOLO_INIT" ]] || { echo "missing $SOLO_INIT" >&2; exit 1; }
SOLO_START=$(basename "$SOLO_INIT" .pt); SOLO_START=${SOLO_START#model_}
SMOOTH="--action-rate-w ${RATE_W:-0.2} --action-limit-w ${LIMIT_W:-0.1} --std-cap ${STD_CAP:-0.4}"
# heading paid and charged the whole way (was only within 1.5 m of the goal), a radian worth 2/3 m of travel (was 1/3)
HEADING="--yaw-gate 0 --yaw-w 2.0"
SOLO_ITERS=${SOLO_ITERS:-6000}
PAIR_ITERS=${PAIR_ITERS:-6000}
TEN=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
ROW="25,0,10,60,0.10,6,1.0"   # spread, behind offset, start yaw, goal turn (deg), tol 0.10 m / 6 deg, hold 1 s
BASE="--pair spot_arm --arm $ARM --hand-obs --partner-map --reward r7 $CREDIT --mean-clip 1.1 --bound-coef 0.01 \
$SMOOTH $HEADING --entropy-coef 0.003 --fixed-difficulty --fixed-level 0 --dyaw-choices --pilot-episode-s 40"
# columns: d_lo, d_hi, ROW, max mass, min mass
SOLO_LV="--pilot-level 1.0,1.5,$ROW,20,5 --extra-levels 1.5,2.5,$ROW,30,5;2.0,3.5,$ROW,40,5 \
--level-mix 0:0.6,0.4,0;1000:0.3,0.4,0.3;2500:0.2,0.3,0.5"
SOLO_LV="$SOLO_OBJ $SOLO_LV"
PAIR_LV="--train-shapes $TEN --pilot-level 1.5,2.5,$ROW,80,20 --extra-levels 2.0,3.0,$ROW,80,20;2.0,4.0,$ROW,80,20 \
--level-mix 0:0.5,0.5,0;1000:0.3,0.4,0.3;2500:0.2,0.3,0.5"
PART="-p mit_preemptable --requeue -t 1-00:00:00 --exclude=node4207"
SOLO=sp_solo20${TAG}_s0
chk=$(ALGO=ippo SEED=0 RUN_NAME=${SOLO}_check ITERS=2 LOGGER=wandb WANDB_MODE=disabled NUM_ENVS=512 \
      EXTRA="$BASE --init-from $SOLO_INIT --solo-agent 0 $SOLO_LV --check" \
      sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 -t 00:30:00 slurm/train_coop2.sbatch)
echo "check: $chk"
SOLO_END=$((SOLO_START + SOLO_ITERS))
solo=$(ALGO=ippo SEED=0 RUN_NAME=$SOLO ITERS=$SOLO_END LOGGER=wandb \
       EXTRA="$BASE --init-from $SOLO_INIT --solo-agent 0 $SOLO_LV" sbatch --parsable $PART --dependency=afterok:$chk slurm/train_coop2.sbatch)
echo "solo pusher $SOLO: $solo"
[[ "${SOLO_ONLY:-0}" == 1 ]] && exit 0
INIT=logs/shared_init/SP_solo20${TAG}_${SOLO_END}.pt
mk=$(sbatch --parsable -p mit_normal_gpu,mit_preemptable --exclude=node4207 -c 2 --mem=8G -t 00:10:00 \
     -J qc-spinit -o logs/slurm/%x-%j.out --dependency=afterok:$solo \
     --wrap "source .venv/bin/activate && python scripts/make_shared_ckpt.py logs/marl2/$SOLO/model_$SOLO_END.pt spotarm1 $INIT")
echo "shared init $INIT: $mk"
prev=$mk
for algo in mappo ippo; do
  run=sp_pair_${algo}${TAG}_s0
  t=$(ALGO=$algo SEED=0 RUN_NAME=$run ITERS=$PAIR_ITERS LOGGER=wandb \
      EXTRA="$BASE --init-actors $INIT --critic-warmup-resume 100 $PAIR_LV" \
      sbatch --parsable $PART --dependency=afterok:$prev slurm/train_coop2.sbatch)
  echo "pair $run: $t (after $prev)"
  prev=$t
done
