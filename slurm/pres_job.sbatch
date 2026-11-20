#!/bin/bash
# One presentation job (slurm/submit_presentation_v2.sh submits them): KIND = walkers | solo | planner | pairs.
#   walkers  scripts/render_walkers.py for ANYmal (walker-anymal-v1) and Spot (walker-spot-rai-falcon): fleet corner +
#            flyover (training env, 256 robots, 40 s) and 4 single-robot clips each
#   solo     the best single-robot ANYmal pusher (s2b-anymal-term80, partner parked) at MASS: 12 objects x 4 positions
#            x 10 trials; the best trial per object x position filmed (HD)
#   planner  the contact planner (expert rule + turn_debug executor) at MASS, same tasks, best trial filmed with the
#            clear arrow overlay (--clear-marks)
#   pairs    IPPO (ippo_aa_kl_ten_s0 it 4000) and MAPPO (nwB_mappo_uniform_s0 it 5000), all masses, same tasks, no videos
#SBATCH -J qc-pres
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=96G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_HD=1 QUADCOOP_HD_CAM="${HD_CAM:-45,-30,1.0}"
KIND=${KIND:?set KIND}
OBJ=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus
REPS=${REPS:-10}
T="--objects $OBJ --reps $REPS --seed 7100"
case "$KIND" in
  walkers)
    for w in anymal:walker-anymal-v1:QuadCoop-Walker-AnymalC spot:walker-spot-rai-falcon:QuadCoop-Walker-Spot; do
      IFS=: read -r name id task <<< "$w"
      ( eval "$(python scripts/methods.py env --id $id)"
        python scripts/render_walkers.py --task $task --checkpoint logs/evals/$id/model.pt --name $name \
          --out logs/evals/pres-walkers --mode fleet --num-envs ${NUM_ENVS:-256} --seconds ${FLEET_S:-40} \
          || echo "!! $name fleet failed"
        unset QUADCOOP_PUSH_FORCE
        python scripts/render_walkers.py --task $task --checkpoint logs/evals/$id/model.pt --name $name \
          --out logs/evals/pres-walkers --mode single --single-seconds ${SINGLE_S:-12} || echo "!! $name single failed" )
    done ;;
  solo)
    M=${MASS:?set MASS}
    python scripts/eval_coop2.py --name pres-solo-${M}kg --solo anymal1 --pair anymal $T --masses $M \
      --videos 1 --video-tasks all/$M/all/all --video-best --video-size 1920x1080 ;;
  planner)
    M=${MASS:?set MASS}
    python scripts/contact_test.py --pair anymal --rules expert --prefix pres-planner-${M}kg --executor stage4 \
      --checkpoint logs/keep/marl2/turn_debug/model_15000.pt --start behind $T --masses $M \
      --videos 1 --video-objects all --video-masses $M --video-scenarios all --video-reps all \
      --video-size 1920x1080 --video-best --clear-marks ;;
  pairs)
    python scripts/eval_coop2.py --name pres-ippo --checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt $T \
      --masses 20,40,60,80 --videos 0 || echo "!! ippo failed"
    python scripts/eval_coop2.py --name pres-mappo --checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt $T \
      --masses 20,40,60,80 --videos 0 || echo "!! mappo failed" ;;
  *) echo "unknown KIND $KIND"; exit 1 ;;
esac
