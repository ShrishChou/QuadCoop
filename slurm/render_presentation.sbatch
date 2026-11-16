#!/bin/bash
# HD presentation renders, stage by stage, with the best checkpoint of each (src/quadcoop/render_hd.py:
# 1920x1080, 8x MSAA, CRF 16, low three-quarter camera). Raw renders -> logs/evals/hd-*/, eval_videos/hd-*/;
# then scripts/collect_presentation.py copies the chosen clips into presentation_export/hd/ (git-ignored).
#   sbatch slurm/render_presentation.sbatch
#   STAGES="coop planner" sbatch slurm/render_presentation.sbatch       # a subset
#   QUADCOOP_HD_CAM="60,-18,0.7" STAGES=walkers sbatch ...               # another camera angle
# Stages: walkers (ANYmal, Spot), push (single-robot push policies), coop (ANYmal alone, frozen pair, IPPO, MAPPO,
# ANYmal + Spot, Spot + Spot), planner (contact planner + executor), spotarm (transport, turn in place).
#SBATCH -J qc-render
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 04:00:00
#SBATCH --exclude=node4207
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_HD=1 QUADCOOP_SHAPES=v2
STAGES=${STAGES:-walkers push coop planner spotarm}
run() { echo ">> $*"; "$@" || echo "!! failed ($?): $*"; }
has() { [[ " $STAGES " == *" $1 "* ]]; }

if has walkers; then  # free walking, a 25% body-weight push, walking into a 30 kg cube
  for w in walker-anymal-v1:QuadCoop-Walker-AnymalC walker-spot-rai-falcon:QuadCoop-Walker-Spot; do
    id=${w%%:*}
    ( eval "$(python scripts/methods.py env --id $id)"; unset QUADCOOP_PUSH_FORCE
      run python scripts/eval_walker.py --task ${w#*:} --checkpoint logs/evals/$id/model.pt --masses 30 --bearings 0 \
        --num-envs 4 --video --out-dir logs/evals/hd-$id )
  done
fi
if has push; then  # Stage 2b push policies (the ones the teams start from), long object 40 kg, three goals
  for id in s2b-anymal-term80 s2b-spot-falcon; do
    run python scripts/showcase.py --id $id --name hd-$id --objects long --masses 40
  done
fi
if has coop; then  # the 480-task benchmark's long object, 40 / 80 kg, straight 3 m and 5 m with a 90 deg turn
  V="--objects long --masses 40,80 --reps 1 --seed 7100 --videos 1 --video-tasks long/40,80/A_straight,D_far_turn/0"
  run python scripts/eval_coop2.py --name hd-anymal-alone --solo anymal1 --pair anymal $V
  run python scripts/eval_coop2.py --name hd-frozen-pair --frozen-pair --pair anymal $V
  run python scripts/eval_coop2.py --name hd-ippo-anymal-pair --checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt $V
  run python scripts/eval_coop2.py --name hd-mappo-anymal-pair --checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt $V
  run python scripts/eval_coop2.py --name hd-mappo-anymal-spot --checkpoint logs/marl2/mappo_mx_kl_ten_s0/model_4000.pt $V
  run python scripts/eval_coop2.py --name hd-ippo-spot-pair --checkpoint logs/marl2/ippo_ss_kl_ten_s0/model_4000.pt $V
fi
if has planner; then
  run python scripts/contact_test.py --pair anymal --rules expert --prefix hd-planner --executor stage4 \
    --checkpoint logs/keep/marl2/turn_debug/model_15000.pt --start behind --objects long --masses 40,80 --reps 1 \
    --seed 7100 --videos 1 --video-objects long --video-masses 40,80 --video-scenarios A_straight,D_far_turn --video-reps 0
fi
if has spotarm; then  # transport (arms active / locked / partner parked); turn in place: learned and scripted
  run python scripts/spot_arm/pair_eval.py --checkpoint logs/marl2/sa_mappo_learned60_s0/model_2000.pt \
    --name hd-sa-transport --turn 60 --reps 1
  run python scripts/spot_arm/turn_inplace.py --checkpoint logs/marl2/sa_turn_stowed_s0/model_2000.pt --reps 1 \
    --out logs/evals/hd-sa-turn-stowed
  run python scripts/spot_arm/turn_inplace.py --checkpoint logs/marl2/sa_turn_bc_s0/model_2000.pt --reps 1 \
    --conds both_hands --out logs/evals/hd-sa-turn-bc
  run python scripts/spot_arm/turn_inplace.py --conds both_hands --reps 1 --out logs/evals/hd-sa-turn-script
fi
python scripts/collect_presentation.py
