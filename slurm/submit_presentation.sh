#!/usr/bin/env bash
# Presentation set (docs/presentation.md): every system on the same 480 seed-7100 ten-object tasks, filmed on the same
# preselected tasks (every outcome), plus a second run of the baselines (rerun noise) and each trained actor alone.
#   P=mit_preemptable bash slurm/submit_presentation.sh      # partition (default mit_preemptable: 4 GPUs, requeued)
set -euo pipefail
cd "$(dirname "$0")/.."
P=${P:-mit_preemptable}
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
VOBJ=arch,cylinder,long,sphere,l_shape,dumbbell; VM=40,80; VS=A_straight,D_far_turn
VT="$VOBJ/$VM/$VS/0"
BASE="--objects $shapes --seed 7100"
IPPO=logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt
MAPPO=logs/marl2/nwB_mappo_uniform_s0/model_5000.pt
PLAN=logs/keep/marl2/turn_debug/model_15000.pt
for f in $IPPO $MAPPO $PLAN; do [[ -s $f ]] || { echo "missing $f" >&2; exit 1; }; done
ev() { sbatch --parsable -p "$P" --exclude=node4207 slurm/eval_coop2.sbatch; }
ids=()
# systems, filmed
ids+=($(NAME=pres-solo-anymal MODE=solo-anymal1 ARGS="--pair anymal $BASE --videos 1 --video-tasks $VT" ev))
ids+=($(NAME=pres-frozen-pair MODE=frozen ARGS="--pair anymal $BASE --videos 1 --video-tasks $VT" ev))
ids+=($(NAME=pres-ippo-it4000 CK=$IPPO SOLO= ARGS="$BASE --videos 1 --video-tasks $VT" ev))
ids+=($(NAME=pres-mappo-B-it5000 CK=$MAPPO SOLO= ARGS="$BASE --videos 1 --video-tasks $VT" ev))
ids+=($(PREFIX=pres-planner RULES=expert ARGS="--executor stage4 --checkpoint $PLAN --start behind $BASE --videos 1 \
  --video-objects $VOBJ --video-masses $VM --video-scenarios $VS --video-reps 0" \
  sbatch --parsable -p "$P" --exclude=node4207 slurm/contact_test.sbatch))
# second runs of the baselines (the trained pairs have one in their placement evaluations' standard rows)
ids+=($(NAME=pres-solo-anymal-r2 MODE=solo-anymal1 ARGS="--pair anymal $BASE --videos 0" ev))
ids+=($(NAME=pres-frozen-pair-r2 MODE=frozen ARGS="--pair anymal $BASE --videos 0" ev))
ids+=($(PREFIX=pres-planner-r2 RULES=expert ARGS="--executor stage4 --checkpoint $PLAN --start behind $BASE --videos 0" \
  sbatch --parsable -p "$P" --exclude=node4207 slurm/contact_test.sbatch))
# each trained actor alone (partner parked far away)
for who in anymal1 anymal2; do
  ids+=($(NAME=pres-ippo-it4000-solo-$who CK=$IPPO SOLO=$who ARGS="$BASE --videos 0" ev))
  ids+=($(NAME=pres-mappo-B-it5000-solo-$who CK=$MAPPO SOLO=$who ARGS="$BASE --videos 0" ev))
done
echo "presentation jobs on $P: ${ids[*]}"
