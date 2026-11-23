#!/usr/bin/env bash
# MAPPO and IPPO with three and four ANYmals, with and without the KL anchor (docs/marl_teams.md).
# Everything waits for the jobs already queued (AFTER=<job ids, colon list>; default: all of this user's jobs).
#   0. smoke: four-robot wiring check, train_coop2 --check (MAPPO, IPPO) with four robots, and a 4-task eval of the
#      pair's actors run as four; every training below waits for it to pass
#   1. training from the ten-object pair actors (iteration 4000 -> 6000), the trio recipe of docs/three_anymal.md:
#      r7, actor lr cap 1e-4, ten objects, level 4 held, 20-120 kg, critic-only for 300 iterations, random starts
#      around the object. Arms: KL anchor 0.05 to the single-robot pushers (as every pair and the trio) or none.
#        trio KL 0.05 = the existing trio_{algo}_s0 (stopped at 5500 / 5600 by preemption), continued to 6000
#        trio KL 0    = trio_{algo}_nokl_s0        quad KL 0.05 = quad_{algo}_s0        quad KL 0 = quad_{algo}_nokl_s0
#   2. evaluation on the pairs' benchmark: ten objects x 4 scenarios x 3 reps, seed 7100, 20-120 kg (720 tasks),
#      two runs per trained model (run 1 films arch / long / cube / t_shape at 40 and 80 kg, straight and far turn,
#      rep 0, whatever the outcome); plus the pair actors run as four (transfer, one run)
#   bash slurm/submit_marl_teams.sh
set -euo pipefail
cd "$(dirname "$0")/.."
SH=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
AFTER=${AFTER:-$(squeue -u "$USER" -h -o %i | paste -sd:)}
DEP=${AFTER:+--dependency=afterany:$AFTER}
GPU="-G l40s:1 --exclude=node4207,node2902"
EV="--objects $SH --seed 7100"
VID="--video-tasks arch,long,cube,t_shape/40,80/A_straight,D_far_turn/0"

smoke=$(sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue $GPU -c 8 --mem=64G -t 01:30:00 $DEP \
  -J qc-quad-smoke -o logs/slurm/%x-%j.out --wrap "source .venv/bin/activate && export MUJOCO_GL=egl && set -e && \
QUADCOOP_PAIR=anymal4 python scripts/three_wiring.py && \
for al in mappo ippo; do python train_coop2.py --algo \$al --check --pair anymal4 --num-envs 2048 --run-name quad_check_\$al \
  --init-actors logs/marl2/\${al}_aa_kl_ten_s0/model_4000.pt --critic-warmup-resume 300 --partner-map --reward r7 --kl-ref 0.05 \
  --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 --train-mass 20,120 --train-shapes $SH --start-around --logger wandb; done && \
python scripts/eval_coop2.py --name quad-smoke --checkpoint logs/marl2/mappo_aa_kl_ten_s0/model_4000.pt --pair anymal4 \
  --objects cube --masses 40 --reps 1 --seed 7100 --videos 1")
echo "smoke $smoke"

ev() {  # name checkpoint pair-args dependency videos
  NAME="$1" CK="$2" MASSES=20,40,60,80,100,120 REPS=3 ARGS="$EV $3 $5" \
    sbatch --parsable -p mit_normal_gpu,mit_preemptable --requeue $GPU --dependency="afterok:$4" slurm/eval_coop2.sbatch
}
for algo in mappo ippo; do
  pair=logs/marl2/${algo}_aa_kl_ten_s0/model_4000.pt
  e=$(ev quad-transfer-$algo "$pair" "--pair anymal4" "$smoke" "$VID")
  echo "$algo: pair actors as four $e"
  for team in trio quad; do
    pa=anymal4
    if [ $team = trio ]; then pa=anymal3; fi
    for kl in 0.05 0; do
      nk=""; nd=""
      if [ "$kl" = 0 ]; then nk=_nokl; nd=-nokl; fi
      run=${team}_${algo}${nk}_s0
      # new runs: 300 critic-only iterations once (--warmup-once: a requeue does not repeat them); the existing trio
      # KL runs already had theirs (4000-4300) and continue from 5500 / 5600 with none
      warm="--critic-warmup-resume 300 --warmup-once"
      if [ $team = trio ] && [ $kl = 0.05 ]; then warm="--critic-warmup-resume 0"; fi
      t=$(ALGO=$algo SEED=0 RUN_NAME=$run ITERS=6000 LOGGER=wandb NUM_ENVS=2048 EXTRA="--pair $pa --init-actors $pair \
$warm --partner-map --reward r7 --kl-ref $kl --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,120 --train-shapes $SH --start-around" \
        sbatch --parsable -p mit_preemptable --requeue $GPU -t 12:00:00 -J qc-$run --dependency=afterok:$smoke \
          slurm/train_coop2.sbatch)
      r1=$(ev $team-$algo$nd-it6000-dev7100 logs/marl2/$run/model_6000.pt "" "$t" "$VID")
      r2=$(ev $team-$algo$nd-it6000-dev7100-r2 logs/marl2/$run/model_6000.pt "" "$t" "--videos 0")
      echo "$algo $team KL $kl: training $t ($run), evals $r1 $r2"
    done
  done
done
