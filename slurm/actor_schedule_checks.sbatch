#!/bin/bash
#SBATCH -J qc-schedchk
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 01:30:00
#SBATCH -o logs/slurm/%x-%j.out
# Checks for docs/actor_schedule.md, before any arm trains:
#   1. --schedule-check: only:anymal2, alt:2, joint, shared (from the A0+A0 checkpoint): after every iteration,
#      exactly the scheduled actors changed (weights, normalizer, noise, optimizer steps, lr); shared: identical
#   2. bank replay with --swap-starts: every slot places each robot where the bank put the other one exactly when
#      swapped, about half the slots swapped
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl WANDB_MODE=disabled
P=logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt
SH=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
C="--algo ippo --pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,80 --train-shapes $SH --seed 0 --video-interval 0 --logger wandb --swap-starts"
tag=$SLURM_JOB_ID
python train_coop2.py $C --run-name chk_only_$tag --num-envs 1024 --init-actors $P --critic-warmup-resume 1 --actor-schedule only:anymal2 --schedule-check 4
python train_coop2.py $C --run-name chk_alt_$tag --num-envs 1024 --init-actors $P --critic-warmup-resume 2 --actor-schedule alt:2 --schedule-check 9
python train_coop2.py $C --run-name chk_joint_$tag --num-envs 1024 --init-actors $P --critic-warmup-resume 1 --actor-schedule joint --schedule-check 3
python train_coop2.py $C --run-name chk_shared_$tag --num-envs 1024 --init-actors logs/shared_init/AA_ippo_ten_4000.pt --critic-warmup-resume 1 --actor-schedule joint --shared-actor --schedule-check 4
python train_coop2.py $C --run-name chk_swapbank_$tag --num-envs 4096 --init-actors $P --critic-warmup-resume 100 \
  --task-bank uniform --task-bank-file logs/next_wave/bank_ten_s0_k16.pt --bank-check
echo "== all actor-schedule checks passed"
