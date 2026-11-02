#!/bin/bash
# Stages 3-4: ANYmal C + Spot push one Stage 2 object together (train_coop2.py).
# Models from evals/models.yaml. A job continues its run if it has checkpoints (so a requeued or
# resubmitted job picks up where it stopped) and stops at ITERS total.
#
#   ALGO=mappo SEED=0 sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   ALGO=ippo  SEED=0 sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   slurm/submit_coop2_first.sh       # both, plus the baseline evaluations and the final evaluations
#   Stage 4 (push from assigned contacts, two ANYmal C, success tolerance curriculum):
#   ALGO=mappo SEED=0 RUN_NAME=s4_aa_s0 EXTRA="--pair anymal --partner-map --reward r7 --contacts --kl-ref 0.05 \
#     --kl-ramp 1000 --need-frac 0.5 --critic-warmup 500 --max-actor-lr 1e-4" \
#     sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Stage 4b (contacts re-chosen every 3-6 s, 30% random starts), continuing a Stage 4 run: copy its last
#   checkpoint into logs/marl2/s4b_aa_s0/ first, then
#   ALGO=mappo SEED=0 RUN_NAME=s4b_aa_s0 ITERS=6000 EXTRA="--pair anymal --partner-map --reward r7 --contacts \
#     --reselect-s 3,6 --random-start 0.3 --need-frac 0.5 --max-actor-lr 1e-4" \
#     sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Stage 4c (no deadlines, no ending for being off contact: pulled to the contact, cost per second off it;
#   train_coop2.py's default --off-contact soft), continuing Stage 4b: copy its model_6000.pt into
#   logs/marl2/s4c_aa_s0/ first, then
#   ALGO=mappo SEED=0 RUN_NAME=s4c_aa_s0 ITERS=9000 EXTRA="--pair anymal --partner-map --reward r7 --contacts \
#     --reselect-s 3,6 --random-start 0.3 --need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 100" \
#     sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
# Optional: VARIANT (b|ctrl), ITERS (3000), NUM_ENVS (4096), LOGGER (wandb|tensorboard), RUN_NAME,
# EXTRA (more train_coop2.py args).
#SBATCH -J qc-coop2
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
ALGO=${ALGO:?set ALGO=mappo or ippo}
SEED=${SEED:-0}
VARIANT=${VARIANT:-b}
SUFFIX=""
if [[ "$VARIANT" == ctrl ]]; then SUFFIX=_ctrl; fi
RUN=${RUN_NAME:-${ALGO}${SUFFIX}_s${SEED}}
echo "run $RUN: $ALGO, variant $VARIANT, seed $SEED, to ${ITERS:-3000} iterations"
nvidia-smi --query-gpu=name,memory.total --format=csv
python train_coop2.py --algo "$ALGO" --variant "$VARIANT" --seed "$SEED" --run-name "$RUN" --resume \
    --num-envs "${NUM_ENVS:-4096}" --max-iterations "${ITERS:-3000}" --logger "${LOGGER:-wandb}" ${EXTRA:-}
