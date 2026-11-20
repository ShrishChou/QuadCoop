#!/bin/bash
# Deploy the contact game's regret picks (scripts/contact_game.py picks.json) in the contact system: the hvB executor
# (iteration 13500, the payoff sweep's) on fresh placements (seed 7100), 12 objects x 4 positions x REPS, 40 and 80 kg.
#   KIND=fixed   rules regret, spread, random: one contact pair held the whole episode (the one-shot game)
#   KIND=expert  the expert planner on the same tasks (re-plans its contacts during the episode)
#SBATCH -J qc-regret
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
CK=logs/keep/marl2/hvB_aa_s0/model_13500.pt
OBJ=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus
C="--pair anymal --executor stage4 --checkpoint $CK --objects $OBJ --masses 40,80 --reps ${REPS:-5} --seed 7100 --videos 0"
case "${KIND:?}" in
  fixed)  python scripts/contact_test.py $C --rules regret,spread,random --regret-picks ${PICKS:-evals/game-hvB-picks/picks.json} \
            --regret-learner ${LEARNER:-rm_plus} --prefix regret-hvB-7100 ;;
  expert) python scripts/contact_test.py $C --rules expert --prefix regret-hvB-7100 ;;
esac
