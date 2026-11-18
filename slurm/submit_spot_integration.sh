#!/usr/bin/env bash
# Spot-arm integration evaluations (docs/spot_arm_pair.md, "Arm mechanism, torso, release"); no training.
# Pusher: the 40 kg heavy-transport checkpoint (sa_heavy_learned_s0, MAPPO, learned joint-target arms), unchanged.
# Task: long object, 40 kg, 2 m, goal heading 0 / +-60 deg, 40 s, 20 placements per turn, each with starts exchanged
# (120 episodes per cell), seed 7100 (the heavy-transport evaluation's tasks).
#   mech      original walker (RAI). Modes both / only_1 / only_2 / none (stowed) / hold_out, then hold_mean (each
#             arm held at its own mean pose while touching, from the first run), then learned arms with arm-object
#             collisions off (both / only_1 / only_2).
#   sweep     fixed pusher x walker (RAI, push_ft_s2_posture, push_ft_s3_handload; WALKERS overrides) x torso
#             (default; height 0.47 / 0.43; pitch 0.1 at 0.52 / 0.47), mode both, release = continued policy 5 s.
#   release   original walker, mode both, after success 5 s of: continued policy / zero base velocity, arm held /
#             arm retracted with 2 s back-off; at 40 kg 2 m and at 20 kg 1 m (more successes to release).
#   PARTS="mech sweep release" bash slurm/submit_spot_integration.sh
set -euo pipefail
cd "$(dirname "$0")/.."
CK=${CK:-logs/marl2/sa_heavy_learned_s0/model_4000.pt}
W=logs/rsl_rl/walker_spot_arm
S2=$W/2026-11-17_14-26-35_push_ft_s2_posture/model_2999.pt
S3=$(ls -d $W/*push_ft_s3_handload | tail -1)/model_2999.pt
WALKERS=${WALKERS:-"rai=  s2=$S2  s3=$S3"}
MECH_WALKERS=${MECH_WALKERS:-"rai="}   # mech and release parts: one job per walker
REL_WALKERS=${REL_WALKERS:-"rai="}
H="--object long --turn 60 --horizon 40 --reps 20 --videos 0 --seed 7100"
H40="$H --mass 40 --dist 2"
H20="$H --mass 20 --dist 1"
ANY="-p mit_normal_gpu,mit_preemptable --requeue --exclude=node4207 -G l40s:1 -c 8 --mem=48G"
PE="python scripts/spot_arm/pair_eval.py --checkpoint $CK"
pre="source .venv/bin/activate && export MUJOCO_GL=egl && set -e"
for part in ${PARTS:-mech sweep release}; do
  case "$part" in
    mech)
      for wv in $MECH_WALKERS; do
        wn=${wv%%=*}; wp=${wv#*=}
        j=$(sbatch --parsable $ANY -t 04:00:00 -J qc-samech -o logs/slurm/%x-%j.out --wrap "$pre && \
export QUADCOOP_SPOT_ARM_WALKER=$wp && \
$PE --name sa-mech-$wn-40kg-2m --modes both,only_1,only_2,none,hold_out $H40 && \
$PE --name sa-mech-$wn-holdmean-40kg-2m --modes hold_mean --hold-pose-from sa-mech-$wn-40kg-2m $H40 && \
$PE --name sa-mech-$wn-nocollide-40kg-2m --modes both,only_1,only_2 --arm-object-collide off $H40")
        echo "mech $wn: job $j"
      done ;;
    sweep)
      for wv in $WALKERS; do
        wn=${wv%%=*}; wp=${wv#*=}
        cmds="$pre && export QUADCOOP_SPOT_ARM_WALKER=$wp"
        for tor in default 0,0.47 0,0.43 0.1,0.52 0.1,0.47; do
          tag=${tor//,/_}; targ=$([[ $tor == default ]] && echo "" || echo "--torso $tor")
          cmds="$cmds && $PE --name sa-sweep-$wn-t$tag-40kg-2m --modes both $targ --release policy $H40"
        done
        j=$(sbatch --parsable $ANY -t 05:00:00 -J qc-sasweep -o logs/slurm/%x-%j.out --wrap "$cmds")
        echo "sweep $wn: job $j"
      done ;;
    release)
      for wv in $REL_WALKERS; do
        wn=${wv%%=*}; wp=${wv#*=}
        cmds="$pre && export QUADCOOP_SPOT_ARM_WALKER=$wp"
        for task in "40kg-2m:$H40" "20kg-1m:$H20"; do
          tn=${task%%:*}; ta=${task#*:}
          for r in policy zero retract; do
            cmds="$cmds && $PE --name sa-release${RTAG:-}-$wn-$r-$tn --modes both --release $r --release-s 5 $ta"
          done
        done
        j=$(sbatch --parsable $ANY -t 05:00:00 -J qc-sarel -o logs/slurm/%x-%j.out --wrap "$cmds")
        echo "release $wn: job $j"
      done ;;
    *) echo "unknown part $part" >&2; exit 1 ;;
  esac
done
