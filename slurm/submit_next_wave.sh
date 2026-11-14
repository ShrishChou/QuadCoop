#!/usr/bin/env bash
# Next-wave arms (docs/next_wave.md), from one common parent, on one fixed task bank, reward fixed except E:
#   A  IPPO   uniform        B  MAPPO  uniform
#   C  IPPO   SGS            D  MAPPO  SGS
#   E  MAPPO  uniform, push_credit removed (team return only for pushing)
# Each arm: actors from PARENT (normalizers, noise), fresh critics trained alone for 100 iterations, 1000
# iterations in all (ITERS overrides the stop iteration), then the matched 480-task seed-7100 evaluation.
# At most two arms per call (two GPUs); AFTER=<job id> holds this call's training until that job ends.
#
#   PARENT=logs/marl2/ippo_aa_kl_s0/model_3000.pt ARMS="A B" bash slurm/submit_next_wave.sh
# Refuses unless slurm/next_wave_checks.sbatch passed for PARENT (transfer into both algorithms, bank replay).
set -euo pipefail
cd "$(dirname "$0")/.."
PARENT=${PARENT:?set PARENT=<trainer checkpoint>}
ARMS=${ARMS:?set ARMS, e.g. \"A B\"}
TAG=$(basename "$(dirname "$PARENT")")_$(basename "$PARENT" .pt)
OUT=logs/next_wave
BANK=${BANK:-$OUT/bank_ten_s0_k16.pt}
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
read -r -a arms <<< "$ARMS"
(( ${#arms[@]} <= 2 )) || { echo "at most two arms per call (two GPUs)" >&2; exit 1; }
[[ -s "$PARENT" && -s "$BANK" ]] || { echo "missing $PARENT or $BANK" >&2; exit 1; }
for f in "$OUT/obs_${TAG}.ippo.json" "$OUT/obs_${TAG}.mappo.json" "${BANK%.pt}.check.json"; do
  python3 -c "import json,sys; sys.exit(0 if json.load(open('$f'))['pass'] else 1)" 2>/dev/null \
    || { echo "preflight not passed: $f (run slurm/next_wave_checks.sbatch with PARENT=$PARENT)" >&2; exit 1; }
done
pit=$(source .venv/bin/activate && python -I -c "import torch; print(int(torch.load('$PARENT', map_location='cpu', weights_only=False)['iter']))")
ITERS=${ITERS:-$((pit + 1000))}
COMMON="--pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,80 --train-shapes $shapes --init-actors $PARENT --critic-warmup-resume 100 --task-bank-file $BANK"
dep=()
[[ -n "${AFTER:-}" ]] && dep=(--dependency="afterany:${AFTER}")
for arm in "${arms[@]}"; do
  case "$arm" in
    A) algo=ippo;  extra="--task-bank uniform"; what=ippo-uniform ;;
    B) algo=mappo; extra="--task-bank uniform"; what=mappo-uniform ;;
    C) algo=ippo;  extra="--task-bank sgs";     what=ippo-sgs ;;
    D) algo=mappo; extra="--task-bank sgs";     what=mappo-sgs ;;
    E) algo=mappo; extra="--task-bank uniform --drop-rewards push_credit"; what=mappo-uniform-nocredit ;;
    *) echo "unknown arm $arm" >&2; exit 1 ;;
  esac
  run="nw${arm}_${what//-/_}_s0"
  tid=$(ALGO=$algo SEED=0 VARIANT=b NUM_ENVS=4096 RUN_NAME="$run" ITERS="$ITERS" LOGGER=wandb EXTRA="$COMMON $extra" \
        sbatch --parsable "${dep[@]}" slurm/train_coop2.sbatch)
  eid=$(NAME="nw-${arm}-${what}-it${ITERS}-dev7100" CK="logs/marl2/$run/model_${ITERS}.pt" SOLO= MASSES=20,40,60,80 REPS=3 \
        ARGS="--objects $shapes --seed 7100 --videos 0" sbatch --parsable --dependency="afterok:${tid%%;*}" slurm/eval_coop2.sbatch)
  echo "arm $arm ($algo, $what): train $run job $tid (to iteration $ITERS) -> eval job $eid"
done
