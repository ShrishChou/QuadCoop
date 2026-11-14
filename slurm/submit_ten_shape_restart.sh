#!/usr/bin/env bash
# From the cluster checkout: bash slurm/submit_ten_shape_restart.sh
# Submit the original checkpoint's evaluation alongside its fine-tune, then the
# final checkpoint evaluation. Both evaluations use the same ordered task list.
set -euo pipefail
cd "$(dirname "$0")/.."
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
source_ck=logs/marl2/ippo_aa_kl_s0/model_3000.pt
run=ippo_aa_kl_ten_s0
final_ck=logs/marl2/$run/model_4000.pt
args="--objects $shapes --seed 7100 --videos 0"
extra="--init-from $source_ck --pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 --train-mass 20,80 --train-shapes $shapes"

[[ -s "$source_ck" ]] || { echo "Missing source checkpoint: $source_ck" >&2; exit 1; }
mkdir -p logs/slurm
train_id=$(ALGO=ippo SEED=0 VARIANT=b NUM_ENVS=4096 RUN_NAME="$run" ITERS=4000 EXTRA="$extra" \
    sbatch --parsable slurm/train_coop2.sbatch)
echo "Fine-tune: $train_id"
eval_arm() {
    local name=$1 ck=$2
    shift 2
    NAME="$name" CK="$ck" SOLO= MASSES=20,40,60,80 REPS=3 ARGS="$args" \
        sbatch --parsable "$@" slurm/eval_coop2.sbatch
}
echo "Source and final evaluation jobs follow"
eval_arm ten-ippo-source-dev7100 "$source_ck"
eval_arm ten-ippo-it4000-dev7100 "$final_ck" --dependency="afterok:${train_id%%;*}"
