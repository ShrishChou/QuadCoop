#!/usr/bin/env bash
# Fine-tune the Stage 4 executor (turn_debug/model_15000.pt) on the cylinder with the planner's rolling model
# (docs/planner_cylinder.md): the planner now asks for couples (one robot behind at one end, the other in front at the
# other); the executor rarely saw them. Same recipe as turn_debug, plus --roll-ratio 0.1 and the cylinder drawn about
# half the time (--shape-bias cylinder:6 over the six other training shapes). 2000 more iterations (15000 -> 17000).
# A 2-iteration check runs first.
#   bash slurm/submit_cylinder_ft.sh
set -euo pipefail
cd "$(dirname "$0")/.."
ITERS=${ITERS:-17000}
RUN=${RUN:-cyl_ft_s0}
S4="--pair anymal --partner-map --contacts --guide --push-cmd --contact-mix wrench:2,spread:1,random:1 \
--reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 --reselect-s 3,6 --random-start 0.5 \
--need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 300 --reward rmin --turn-frac 0.3 \
--roll-ratio 0.1 --shape-bias cylinder:6 --init-from logs/keep/marl2/turn_debug/model_15000.pt"
chk=$(ALGO=mappo SEED=0 RUN_NAME=${RUN}_check ITERS=2 LOGGER=wandb WANDB_MODE=disabled NUM_ENVS=512 \
      EXTRA="$S4 --check" sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 -t 00:30:00 \
      slurm/train_coop2.sbatch)
echo "check: $chk"
t=$(ALGO=mappo SEED=0 RUN_NAME=$RUN ITERS=$ITERS LOGGER=wandb EXTRA="$S4" \
    sbatch --parsable -p mit_preemptable --requeue -t 1-00:00:00 --exclude=node4207 --dependency=afterok:$chk \
    slurm/train_coop2.sbatch)
echo "fine-tune $RUN: $t (after $chk)"
