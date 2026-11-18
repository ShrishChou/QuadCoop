#!/usr/bin/env bash
# Actor-schedule experiments (docs/actor_schedule.md), IPPO, from the ten-object parent's two actors:
#   S0  joint        both actors learn every iteration (the matched control)
#   S1  alt:100      A (anymal1) and B (anymal2) take turns, 100-iteration blocks, A first
#   S2  only:anymal1 A learns, B stays exactly B0
#   S3  only:anymal2 B learns, A stays exactly A0
#   S4  shared       one actor on both robots (--shared-actor), from the shared start SHARED (B0 + B0: closest to the
#                    parent on the 2880-episode shared-start evaluation, docs/actor_schedule.md), joint updates
# Common: --init-actors PARENT (weights, normalizers, noise), fresh critics, 100 critic-only iterations, then 2000
# actor-training iterations (4000 -> 6100); uniform over the fixed task bank, start tuples exchanged with
# probability 0.5 after replay (--swap-starts); r7, partner map, KL anchor 0.05, actor lr cap 1e-4, level 4,
# 20-80 kg, ten objects, seed 0, 4096 envs. Then the benchmark (480 seed-7100 tasks) in the standard, flank and
# goal-behind formations, each with the starts exchanged too (--swap).
#   ARMS="S0 S1 S2 S3" AFTER=<check job> bash slurm/submit_actor_schedule.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PARENT=${PARENT:-logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt}
SHARED=${SHARED:-logs/shared_init/BB_ippo_ten_4000.pt}
BANK=${BANK:-logs/next_wave/bank_ten_s0_k16.pt}
ITERS=${ITERS:-6100}
SH=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
read -r -a arms <<< "${ARMS:?set ARMS, e.g. \"S0 S1 S2 S3\"}"
COMMON="--pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,80 --train-shapes $SH --critic-warmup-resume 100 \
--task-bank uniform --task-bank-file $BANK --swap-starts"
dep=()
[[ -n "${AFTER:-}" ]] && dep=(--dependency="afterok:${AFTER}")
ANY="-p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207"
for arm in "${arms[@]}"; do
  case "$arm" in
    S0) sch=joint;        what=joint ;;
    S1) sch=alt:100;      what=alt100 ;;
    S2) sch=only:anymal1; what=onlyA ;;
    S3) sch=only:anymal2; what=onlyB ;;
    S4) sch=joint;        what=shared ;;
    *) echo "unknown arm $arm" >&2; exit 1 ;;
  esac
  run="as${arm}_${what}_s0"
  tid=$(ALGO=ippo SEED=0 VARIANT=b NUM_ENVS=4096 RUN_NAME="$run" ITERS="$ITERS" LOGGER=wandb \
        EXTRA="$COMMON --init-actors $([[ $arm == S4 ]] && echo "$SHARED --shared-actor" || echo "$PARENT") --actor-schedule $sch" sbatch --parsable $ANY -t 06:00:00 "${dep[@]}" slurm/train_coop2.sbatch)
  eid=$(NAME="as-${arm}-${what}-it${ITERS}-dev7100" CK="logs/marl2/$run/model_${ITERS}.pt" SOLO= MASSES=20,40,60,80 REPS=3 \
        ARGS="--objects $SH --seed 7100 --videos 0 --swap --formations standard,flank,goal_behind" \
        sbatch --parsable $ANY -t 06:00:00 --dependency="afterok:${tid}" slurm/eval_coop2.sbatch)
  echo "arm $arm ($sch): train $run job $tid (to $ITERS) -> eval job $eid"
done
