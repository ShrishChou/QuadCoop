#!/usr/bin/env bash
# Observation study (docs/obs_study.md): does explicit contact geometry and/or a short interaction history help the
# ordinary ANYmal MAPPO pair coordinate? Four matched arms, all MAPPO, all --init-from the same checkpoint
# (PARENT, default the final ten-object MAPPO pair nwB_mappo_uniform_s0/model_5000: actors, critics, noise, curriculum
# state; new input columns start at zero weight, so every arm starts from exactly the parent's behaviour):
#   A  matched baseline (no new inputs)      B  + contact geometry (--geom-obs, 14 inputs)
#   C  + interaction history (--hist-obs, 200 inputs)      D  both
# Everything else is the parent's recipe (slurm/submit_next_wave.sh arm B: r7, KL anchor 0.05, actor lr cap 1e-4,
# level 4, 20-80 kg, ten objects, uniform task bank); action-saturation handling identical in all arms (the parent's:
# none). Same budget: PARENT's iteration + ITERS_ADD (2000). A and B on mit_normal_gpu (2 GPUs), C and D on
# mit_preemptable (requeued and resumed from their last checkpoint if preempted). A short check (arm D's inputs, with
# the geometry / history self-test) runs first; training waits on it (afterok). Each arm is then evaluated on the
# 480-task benchmark (seed 7100, 20/40/60/80 kg, 3 reps), as the next-wave arms.
#
#   bash slurm/submit_obs_study.sh                 # all four
#   ARMS="B D" SEED=1 bash slurm/submit_obs_study.sh   # a second seed of two arms
set -euo pipefail
cd "$(dirname "$0")/.."
PARENT=${PARENT:-logs/marl2/nwB_mappo_uniform_s0/model_5000.pt}
BANK=${BANK:-logs/next_wave/bank_ten_s0_k16.pt}
ARMS=${ARMS:-A B C D}
SEED=${SEED:-0}
[[ -s "$PARENT" && -s "$BANK" ]] || { echo "missing $PARENT or $BANK" >&2; exit 1; }
pit=$(source .venv/bin/activate && python -I -c "import torch; print(int(torch.load('$PARENT', map_location='cpu', weights_only=False)['iter']))")
ITERS=$((pit + ${ITERS_ADD:-2000}))
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
COMMON="--pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,80 --train-shapes $shapes --task-bank uniform --task-bank-file $BANK --init-from $PARENT"
chk=$(ALGO=mappo SEED=$SEED VARIANT=b NUM_ENVS=4096 RUN_NAME=obs_study_check_s$SEED ITERS=2 LOGGER=wandb WANDB_MODE=disabled \
      EXTRA="$COMMON --geom-obs --hist-obs --check" \
      sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 -t 00:30:00 slurm/train_coop2.sbatch)
echo "check (arm D inputs): $chk"
for arm in $ARMS; do
  case "$arm" in
    A) extra="";                       what=base ;;
    B) extra="--geom-obs";             what=geom ;;
    C) extra="--hist-obs";             what=hist ;;
    D) extra="--geom-obs --hist-obs";  what=geom_hist ;;
    *) echo "unknown arm $arm" >&2; exit 1 ;;
  esac
  case "$arm" in
    A|B) part=(-p mit_normal_gpu -t 06:00:00) ;;
    *)   part=(-p mit_preemptable --requeue -t 12:00:00) ;;
  esac
  run="obs${arm}_mappo_${what}_s${SEED}"
  tid=$(ALGO=mappo SEED=$SEED VARIANT=b NUM_ENVS=4096 RUN_NAME="$run" ITERS="$ITERS" LOGGER=wandb EXTRA="$COMMON $extra" \
        sbatch --parsable "${part[@]}" --exclude=node4207 --dependency=afterok:$chk slurm/train_coop2.sbatch)
  eid=$(NAME="obs-${arm}-${what}-s${SEED}-it${ITERS}-dev7100" CK="logs/marl2/$run/model_${ITERS}.pt" SOLO= MASSES=20,40,60,80 \
        REPS=3 ARGS="--objects $shapes --seed 7100 --videos 0" \
        sbatch --parsable --exclude=node4207 --dependency="afterok:$tid" slurm/eval_coop2.sbatch)
  echo "arm $arm ($what): train $run job $tid (${part[1]}, to iteration $ITERS) -> eval job $eid"
done
