#!/usr/bin/env bash
# Three teams, same recipe (docs/three_teams.md): ANYmal + ANYmal (exists), Spot + Spot, ANYmal + Spot (the current
# armless Spot), each with IPPO and MAPPO:
#   stage 1  from the two Stage 2 single-robot policies, r7 + KL anchor 0.05, 3000 iterations (as ippo_aa_kl_s0)
#   stage 2  ten-object restart, level 4 held, 20-80 kg, 1000 more iterations (as ippo_aa_kl_ten_s0)
#   eval     the 480 seed-7100 ten-object tasks, twice (rerun noise); frozen pair and solo Spot baselines
# Stage 1 runs on mit_preemptable (requeued jobs resume from their checkpoints); the rest wherever a GPU frees.
#   bash slurm/submit_three_teams.sh
set -euo pipefail
cd "$(dirname "$0")/.."
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
ANY="-p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207"
EV="--objects $shapes --seed 7100 --videos 0"
ev() { NAME="$1" CK="$2" SOLO= MASSES=20,40,60,80 REPS=3 ARGS="$EV" sbatch --parsable $ANY --dependency="afterok:$3" slurm/eval_coop2.sbatch; }
for team in mixed:mx spot:ss anymal:aa; do
  pair=${team%%:*}; tag=${team##*:}
  for algo in ippo mappo; do
    src=${algo}_${tag}_kl_s0; run=${algo}_${tag}_kl_ten_s0
    [[ "$run" == ippo_aa_kl_ten_s0 ]] && continue   # exists: the next-wave parent
    if [[ -s logs/marl2/$src/model_3000.pt ]]; then
      dep=""; echo "$src: stage 1 exists"
    else
      t1=$(ALGO=$algo SEED=0 RUN_NAME=$src ITERS=3000 LOGGER=wandb EXTRA="--pair $pair --partner-map --reward r7 --kl-ref 0.05" \
           sbatch --parsable -p mit_preemptable --requeue -t 12:00:00 --exclude=node4207 slurm/train_coop2.sbatch)
      dep="--dependency=afterok:$t1"; echo "$src: stage 1 job $t1"
    fi
    t2=$(ALGO=$algo SEED=0 RUN_NAME=$run ITERS=4000 LOGGER=wandb EXTRA="--init-from logs/marl2/$src/model_3000.pt --pair $pair \
--partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 --train-mass 20,80 --train-shapes $shapes" \
         sbatch --parsable $ANY $dep slurm/train_coop2.sbatch)
    e1=$(ev team-$tag-$algo-it4000-dev7100 logs/marl2/$run/model_4000.pt $t2)
    e2=$(ev team-$tag-$algo-it4000-dev7100-r2 logs/marl2/$run/model_4000.pt $t2)
    echo "$run: stage 2 job $t2, evals $e1 $e2"
  done
done
# baselines on the same tasks, two runs each (ANYmal's are in the presentation set)
for r in "" -r2; do
  b1=$(NAME=team-mx-frozen$r MODE=frozen ARGS="--pair mixed $EV" sbatch --parsable $ANY slurm/eval_coop2.sbatch)
  b2=$(NAME=team-ss-frozen$r MODE=frozen ARGS="--pair spot $EV" sbatch --parsable $ANY slurm/eval_coop2.sbatch)
  b3=$(NAME=team-solo-spot$r MODE=solo-spot1 ARGS="--pair spot $EV" sbatch --parsable $ANY slurm/eval_coop2.sbatch)
  echo "baselines$r: mixed frozen $b1, spot frozen $b2, solo spot $b3"
done
