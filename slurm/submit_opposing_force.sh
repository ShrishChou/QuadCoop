#!/usr/bin/env bash
# Opposing-force arms (docs/opposing_force.md): S0's settings (docs/actor_schedule.md: the ten-object parent's two
# actors, fresh critics, 100 critic-only iterations, 2000 actor iterations to 6100, uniform bank, --swap-starts,
# joint updates) plus two costs:
#   oppose_<robot>      per robot, OPPOSE x max(0, -(its wrench on the object . the wanted object twist) / 200 N)
#   force_cancellation  team, CANCEL x (sum |F_i| - |sum F_i|) / 200 N x (1 - turning share of the wanted motion)
# Arms: OFi (IPPO, against S0 = asS0_joint_s0), OFm (MAPPO), OFm0 (MAPPO control without the costs: no matched MAPPO
# run exists under these settings). A check job (2 iterations at 4096 envs: the bank is drawn for 4096; reward terms
# finite) runs first; training waits for
# it and for AFTER (the S0-S4 trainings).
#   AFTER=<ids, colon-separated> bash slurm/submit_opposing_force.sh
set -euo pipefail
cd "$(dirname "$0")/.."
PARENT=${PARENT:-logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt}
BANK=${BANK:-logs/next_wave/bank_ten_s0_k16.pt}
OPPOSE=${OPPOSE:-0.5}
CANCEL=${CANCEL:-0.25}
ITERS=${ITERS:-6100}
SH=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
COMMON="--pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
--train-mass 20,80 --train-shapes $SH --init-actors $PARENT --critic-warmup-resume 100 \
--task-bank uniform --task-bank-file $BANK --swap-starts --actor-schedule joint"
COST="--oppose-cost $OPPOSE --cancel-cost $CANCEL"
ANY="-p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207"
chk=$(sbatch --parsable $ANY -G l40s:1 -c 8 --mem=64G -t 00:40:00 -J qc-ofchk -o logs/slurm/%x-%j.out --wrap \
  "source .venv/bin/activate && export MUJOCO_GL=egl WANDB_MODE=disabled && set -e && \
python train_coop2.py --algo ippo --run-name chk_of_ippo_\$SLURM_JOB_ID --num-envs 4096 $COMMON $COST --critic-warmup-resume 1 --seed 0 --video-interval 0 --logger wandb --check && \
python train_coop2.py --algo mappo --run-name chk_of_mappo_\$SLURM_JOB_ID --num-envs 4096 $COMMON $COST --critic-warmup-resume 1 --seed 0 --video-interval 0 --logger wandb --check")
echo "check: job $chk"
dep="afterok:$chk${AFTER:+,afterany:$AFTER}"
for arm in OFi OFm OFm0; do
  case "$arm" in
    OFi)  algo=ippo;  extra="$COST"; run=ofI_ippo_oppose_s0 ;;
    OFm)  algo=mappo; extra="$COST"; run=ofM_mappo_oppose_s0 ;;
    OFm0) algo=mappo; extra="";      run=ofM0_mappo_joint_s0 ;;
  esac
  tid=$(ALGO=$algo SEED=0 VARIANT=b NUM_ENVS=4096 RUN_NAME="$run" ITERS="$ITERS" LOGGER=wandb EXTRA="$COMMON $extra" \
        sbatch --parsable $ANY -t 06:00:00 --dependency="$dep" slurm/train_coop2.sbatch)
  eid=$(NAME="of-${arm}-it${ITERS}-dev7100" CK="logs/marl2/$run/model_${ITERS}.pt" SOLO= MASSES=20,40,60,80 REPS=3 \
        ARGS="--objects $SH --seed 7100 --videos 0 --swap --formations standard,flank,goal_behind" \
        sbatch --parsable $ANY -t 06:00:00 --dependency="afterok:${tid}" slurm/eval_coop2.sbatch)
  echo "arm $arm ($algo${extra:+, costs}): train $run job $tid -> eval job $eid"
done
