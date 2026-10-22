#!/bin/bash
# Stage 2: ANYmal C + Spot push one object together, IPPO or MAPPO.
#
# One array task per (algorithm, seed):  0-2 = MAPPO seeds 0-2, 3-5 = IPPO seeds 0-2.
#
#   sbatch --array=0-5 slurm/train_coop.sbatch          # all six runs (as many at once as you have GPUs)
#   sbatch --array=0,3 slurm/train_coop.sbatch          # just seed 0 of each
#   slurm/chain_coop.sh 3 0-5                           # six runs, each continued for 3 x 6 h
#
# Every job continues its run if it has checkpoints (logs/marl/<algo>_seed<seed>/), so
# resubmitting the same array continues it. First job: actors warm-started from the
# newest pushhard2_<robot> (Stage 1c) run, else pushhard_<robot> (Stage 1b).
# Optional: NUM_ENVS (4096), ITERS (6000), LOGGER (wandb|tensorboard), EFFORT (0),
# EXTRA (more train_coop.py args), ALGO/SEED (to run one without an array).
#SBATCH -J qc-coop
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%A_%a.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_SHAPES=v2

ID=${SLURM_ARRAY_TASK_ID:-0}
ALGOS=(mappo mappo mappo ippo ippo ippo)
SEEDS=(0 1 2 0 1 2)
ALGO=${ALGO:-${ALGOS[$ID]}}
SEED=${SEED:-${SEEDS[$ID]}}
RUN="${ALGO}_seed${SEED}"
[[ "${EFFORT:-0}" != "0" ]] && RUN="${RUN}_effort${EFFORT}"

nvidia-smi --query-gpu=name,memory.total --format=csv
echo "array task $ID -> $RUN"
python train_coop.py --algo "$ALGO" --seed "$SEED" --run-name "$RUN" --resume \
    --num-envs "${NUM_ENVS:-4096}" --max-iterations "${ITERS:-6000}" \
    --effort-cost "${EFFORT:-0}" --logger "${LOGGER:-wandb}" ${EXTRA:-}
