#!/bin/bash
# 1. Full two-robot penalty benchmark: original planner (A, fail_mem 0.5 = unchanged decisions, logs the decisions the
#    memory would change) vs exact-pair penalty after repeated failures (B2: fail_mem 1, fail_act 2). The 480
#    ten-object tasks of pres-planner (seed 7100), frozen walkers and executor. Two runs per arm (GPU simulation is
#    not run-to-run deterministic); run 1 films every task's rep 0.
# 2. B2 added to the frozen turning test (seed 7300, beside A-D).
# 3. 3 -> 4 size-and-entry trees (chain4_branch --place 1): k3 / k4 walk-in / k4p placed, at scale 1.0 and 1.5,
#    20 / 60 / 100 kg, development seeds 1001-1003 and test seeds 8401-8402.
# bench140: the benchmark with a 140 s horizon (2:20) instead of 80 s.
# Usage: bash slurm/submit_penalty_place.sh [bench|bench140|turn|place]...
set -e
cd "$(dirname "$0")/.."
SB="sbatch --parsable ${DEP:+--dependency=$DEP} -p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207,node2902 -G l40s:1 -c 8 --mem=32G -o logs/slurm/%x-%j.out"
PRE="source .venv/bin/activate && export MUJOCO_GL=egl &&"
CT="python scripts/contact_test.py --pair anymal --rules expert --executor stage4 --checkpoint logs/keep/marl2/turn_debug/model_15000.pt --start behind"
TEN="cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus"
for what in "$@"; do
  case $what in
    bench)
      for arm in A:fail_mem=0.5 B2:fail_mem=1,fail_act=2; do
        name=${arm%%:*}; set_=${arm#*:}
        for r in 1 2; do
          vid="--videos 0"
          [ $r = 1 ] && vid="--videos 1 --video-objects $TEN --video-masses 20,40,60,80 --video-scenarios all --video-reps 0"
          $SB -t 04:00:00 -J qc-olp-$name-r$r --wrap "$PRE $CT --objects $TEN --masses 20,40,60,80 --reps 3 --seed 7100 --probe $vid --set $set_ --prefix olp-$name-r$r"
        done
      done ;;
    bench140)  # the same benchmark with a 140 s horizon (2:20) instead of 80 s
      # run 1's films are hard-linked (full quality) into presentation_export: A -> 07, B2 -> 08
      for arm in A:fail_mem=0.5:07_longer_planner_contact B2:fail_mem=1,fail_act=2:08_penalizing_longer_planner_contact; do
        name=${arm%%:*}; rest=${arm#*:}; set_=${rest%%:*}; pe=presentation_export/${rest#*:}
        for r in 1 2; do
          vid="--videos 0"; post=""
          [ $r = 1 ] && vid="--videos 1 --video-objects $TEN --video-masses 20,40,60,80 --video-scenarios all --video-reps 0" \
            && post=" && mkdir -p $pe && cp -al logs/evals/olp140-$name-r$r-expert/pair/videos/. $pe/"
          $SB -t 07:00:00 -J qc-olp140-$name-r$r --wrap "$PRE $CT --objects $TEN --masses 20,40,60,80 --reps 3 --seed 7100 --probe --horizon 140 $vid --set $set_ --prefix olp140-$name-r$r$post"
        done
      done ;;
    turn)
      for t in turn turn_mirror; do
        $SB -t 02:00:00 -J qc-fm-test-B2-$t --wrap "$PRE $CT --objects arch,long --seed 7300 --masses 60,80 --reps 10 --probe --videos 1 --video-objects arch,long --video-masses 60,80 --video-scenarios all --video-reps 0,1 --tasks $t --set fail_mem=1,fail_act=2 --prefix fm-test-B2-$t"
      done ;;
    place)
      for s in 1001 1002 1003 8401 8402; do
        for sc in 1.0 1.5; do
          tag=$( [ $sc = 1.0 ] && echo s10 || echo s15 )
          $SB -t 05:00:00 -J qc-k4p-$tag-$s --wrap "$PRE python scripts/chain4_branch.py --place 1 --masses 20,60,100 --seed $s --scale $sc --film-max 4 --prefix k4p-$tag-s$s"
        done
      done ;;
  esac
done
