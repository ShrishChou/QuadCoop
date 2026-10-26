#!/bin/bash
# First two-robot test: baselines + MAPPO and IPPO (seed 0) + their evaluations, in one go.
#
#   slurm/submit_coop2_first.sh               # ITERS=3000 by default
#   ITERS=6000 slurm/submit_coop2_first.sh
#   SKIP_BASELINES=1 slurm/submit_coop2_first.sh    # only the training runs and their evaluations
#   TAG=r4 SKIP_BASELINES=1 EXTRA="--partner-map --reward r4" slurm/submit_coop2_first.sh
#   TAG=r5 SKIP_BASELINES=1 EXTRA="--partner-map --reward r5" slurm/submit_coop2_first.sh
#   TAG=r6 SKIP_BASELINES=1 EXTRA="--partner-map --reward r5 --mean-clip 1.1 --bound-coef 0.01 --entropy-coef 0.003" \
#       slurm/submit_coop2_first.sh       # r6: r5 rewards + exploration in saturated outputs + entropy bonus
#   TAG=scratch ITERS=20000 SKIP_BASELINES=1 \
#       EXTRA="--scratch --partner-map --reward r5 --mean-clip 1.1 --bound-coef 0.01 --entropy-coef 0.003" \
#       slurm/submit_coop2_first.sh       # same as r6 but from the walkers only (random initial policies)
#   TAG=r7scratch ITERS=20000 SKIP_BASELINES=1 \
#       EXTRA="--scratch --partner-map --reward r7 --mean-clip 1.1 --bound-coef 0.01 --entropy-coef 0.003" \
#       slurm/submit_coop2_first.sh       # r7 rewards (outcome-based), from the walkers only
#   TAG=r7 SKIP_BASELINES=1 EXTRA="--partner-map --reward r7 --mean-clip 1.1 --bound-coef 0.01 --entropy-coef 0.003" \
#       slurm/submit_coop2_first.sh       # r7 rewards, warm start from Stage 2b
#   TAG=aa_r7 SKIP_BASELINES=1 \
#       EXTRA="--pair anymal --partner-map --reward r7 --mean-clip 1.1 --bound-coef 0.01 --entropy-coef 0.003" \
#       slurm/submit_coop2_first.sh       # two ANYmal C, both from the ANYmal Stage 2b policy, r7 rewards
#   (their untrained baseline: NAME=pair-frozen-anymal MODE=frozen ARGS="--pair anymal" sbatch slurm/eval_coop2.sbatch)
#                                   # EXTRA: more train_coop2.py options for both runs
#
# Submits (job ids are saved in logs/slurm/coop2_<TAG>.txt):
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
LOG=logs/slurm/coop2_${TAG:-r3}.txt
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
