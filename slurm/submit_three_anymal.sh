#!/usr/bin/env bash
# Three ANYmals (docs/three_anymal.md): transfer first, then joint training, MAPPO and IPPO.
#   1. wiring check (scripts/three_wiring.py); everything below waits for it to pass
#   2. transfer: the pair's trained actors run as a trio (anymal3 takes anymal1's actor), on the original benchmark
#      (480 seed-7100 tasks, 20-80 kg) plus 100 and 120 kg; the pairs themselves at 100 and 120 kg (they have 20-80)
#   3. training from the pair actors: ten objects, level 4 held, 20-120 kg, r7 + KL anchor 0.05, actor lr cap 1e-4,
#      critic-only for 300 iterations, robots started at random around the object (--start-around), 2000 iterations
#   4. the trained trio on the same tasks
#   bash slurm/submit_three_anymal.sh
set -euo pipefail
cd "$(dirname "$0")/.."
SH=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
EV="--objects $SH --seed 7100 --videos 0"
ANY="-p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207"
w=${WIRE:-$(sbatch --parsable $ANY -J qc-3wire -G l40s:1 -c 4 --mem=32G -t 00:30:00 -o logs/slurm/%x-%j.out \
    --wrap "source .venv/bin/activate && export MUJOCO_GL=egl && python scripts/three_wiring.py")}  # WIRE=<job>: reuse one
echo "wiring check $w"
ev() { NAME="$1" CK="$2" SOLO= MASSES="$3" REPS=3 ARGS="$EV $4" sbatch --parsable $ANY --dependency="afterok:$5" slurm/eval_coop2.sbatch; }
for algo in mappo ippo; do
  pair=logs/marl2/${algo}_aa_kl_ten_s0/model_4000.pt
  e1=$(ev trio-transfer-$algo $pair 20,40,60,80,100,120 "--pair anymal3" $w)
  e2=$(ev team-aa-$algo-it4000-dev7100-heavy $pair 100,120 "" $w)
  run=trio_${algo}_s0
  t=$(ALGO=$algo SEED=0 RUN_NAME=$run ITERS=6000 LOGGER=wandb EXTRA="--pair anymal3 --init-actors $pair \
--critic-warmup-resume 300 --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,120 --train-shapes $SH --start-around" \
      NUM_ENVS=2048 sbatch --parsable -p mit_preemptable --requeue -t 12:00:00 --exclude=node4207 --dependency=afterok:$w slurm/train_coop2.sbatch)
  e3=$(ev trio-$algo-it6000-dev7100 logs/marl2/$run/model_6000.pt 20,40,60,80,100,120 "" $t)
  echo "$algo: transfer eval $e1, pair heavy eval $e2, training $t ($run, iterations 4000 -> 6000), trained eval $e3"
done
