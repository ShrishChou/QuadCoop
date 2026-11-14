#!/bin/bash
# Mixed-start bank (docs/mixed_start.md), no training: a copy of the next-wave bank with 2 of 16 tasks per slot in the
# flank formation and 2 in goal_behind (one of each with the robots exchanged), every other field unchanged; built
# under the arms' env, every column re-recorded and replay-checked (twice), placements checked against the bearings.
#   PARENT=logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt sbatch slurm/mixed_start_bank.sbatch
#SBATCH -J qc-mixbank
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 01:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
PARENT=${PARENT:?set PARENT=<trainer checkpoint>}
SRC=${SRC:-logs/next_wave/bank_ten_s0_k16.pt}
OUTB=${OUTB:-logs/next_wave/bank_ten_s0_k16_mix.pt}
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
ARM="--pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
  --train-mass 20,80 --train-shapes $shapes --init-actors $PARENT --critic-warmup-resume 100 --seed 0 --video-interval 0"
python train_coop2.py --algo ippo --run-name chk_mixbank --num-envs 4096 $ARM --task-bank-file "$OUTB" \
  --bank-remix "$SRC" --bank-mix flank:2,goal_behind:2 --bank-mix-seed 9200
