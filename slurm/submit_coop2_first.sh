#!/bin/bash
# First two-robot test: baselines + MAPPO and IPPO (seed 0) + their evaluations, in one go.
#
#   slurm/submit_coop2_first.sh               # ITERS=3000 by default
#   ITERS=6000 slurm/submit_coop2_first.sh
#   SKIP_BASELINES=1 slurm/submit_coop2_first.sh    # only the training runs and their evaluations
#   TAG=r4 SKIP_BASELINES=1 EXTRA="--partner-map --reward r4" slurm/submit_coop2_first.sh
#                                   # EXTRA: more train_coop2.py options for both runs
#
# Submits (job ids are saved in logs/slurm/coop2_first.txt):
#   baselines now:  solo-anymal, solo-spot (each Stage 2b policy alone), pair-frozen (both, untrained together)
#   training:       mappo_<TAG>_s0 and ippo_<TAG>_s0 (TAG=r3 by default; preemptable, requeued
#                   automatically; each resumes itself)
#   after each:     its final checkpoint evaluated on the same tasks (<algo>-<TAG>-s0-it<ITERS>)
set -euo pipefail
ITERS=${ITERS:-3000}
TRAIN_PART=${TRAIN_PART:-"-p mit_preemptable --requeue -t 2-00:00:00"}
EVAL_PART=${EVAL_PART:-"-p mit_normal_gpu,mit_preemptable -t 06:00:00"}
EXCLUDE=${EXCLUDE:---exclude=node3006}
mkdir -p logs/slurm
LOG=logs/slurm/coop2_first.txt
python scripts/select_models.py --check
echo "coop2 runs ($(date)), $ITERS iterations, tag ${TAG:-r3}, options: ${EXTRA:-none}" | tee "$LOG"
sub() { sbatch --parsable "$@" | cut -d';' -f1; }
for M in $([[ "${SKIP_BASELINES:-0}" == 1 ]] || echo solo-anymal solo-spot frozen); do
  NAME=$([[ $M == frozen ]] && echo pair-frozen || echo $M)
  J=$(env NAME=$NAME MODE=$M sbatch --parsable $EVAL_PART $EXCLUDE -J ev-$NAME slurm/eval_coop2.sbatch | cut -d';' -f1)
  echo "  baseline $NAME: job $J" | tee -a "$LOG"
done
TAG=${TAG:-r3}  # run names <algo>_<TAG>_s0 (r2: divergence fix; r3: no entropy bonus, noise capped)
for ALGO in mappo ippo; do
  RUN=${ALGO}_${TAG}_s0
  T=$(env ALGO=$ALGO SEED=0 ITERS=$ITERS RUN_NAME=$RUN sbatch --parsable $TRAIN_PART $EXCLUDE -J tr-$ALGO-$TAG \
        slurm/train_coop2.sbatch | cut -d';' -f1)
  E=$(env NAME=$ALGO-$TAG-s0-it$ITERS CK=logs/marl2/$RUN/model_$ITERS.pt \
        sbatch --parsable $EVAL_PART $EXCLUDE -J ev-$ALGO-$TAG --dependency=afterok:$T slurm/eval_coop2.sbatch | cut -d';' -f1)
  echo "  train $RUN to $ITERS: job $T  -> eval: job $E" | tee -a "$LOG"
done
echo "watch: squeue --me ; training logs: logs/slurm/tr-<algo>-s0-<job>.out" | tee -a "$LOG"
