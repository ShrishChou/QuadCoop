#!/bin/bash
# Talk media renders (6.7980 talk; composed by scripts/talk/compose_talk.py). One GROUP per job:
#   A0..A6  12-object grid per method (A0 = A1 at 20 kg) (one episode per object, the same 12 starts for every method)
#   B1 B2 B3 B5  before/after starts, two runs per arm (B4 and B6 reuse existing films)
# Every step writes to <name>.part and is renamed to <name> only when the script exits cleanly, so a requeued job
# skips finished steps and reruns a step that was killed mid-write.
#   GROUP=A1 sbatch scripts/talk/render_talk.sbatch      (scripts/talk/submit_talk.sh submits them all)
# No policy, checkpoint or planner setting differs from the runs each step reproduces.
#SBATCH -J qc-talk
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH --exclude=node4207,node2902
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_HD=1 QUADCOOP_SHAPES=v2
: "${GROUP:?set GROUP}"

IPPO=logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt
MAPPO=logs/marl2/nwB_mappo_uniform_s0/model_5000.pt
EXEC=logs/keep/marl2/turn_debug/model_15000.pt
NOKL=logs/marl2/mappo_aa_nokl_s0/model_3000.pt
KL=logs/marl2/mappo_aa_kl_s0/model_3000.pt
TEN=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus     # pres-* layout (B1)
ALL=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus
# the original planner: the config of the 1,920-trial benchmark (pres-planner-{20,40,60,80}kg-expert: no --set,
# fail_mem 0). The failed-contact penalty appears only in B4, which reuses the fm-test-{A,B2}-turn_mirror films.
PLAN="--pair anymal --rules expert --executor stage4 --checkpoint $EXEC --start behind"
# Part A: the benchmark layout (12 objects x 4 goals x 10 reps, seed 7100); rep picked once by
# random.Random(6798).randrange(10) = 9 (scripts/talk/compose_talk.py PART_A_REP)
REP=9
GOALS=("cube,long,sphere:A_straight" "cylinder,arch,dumbbell:B_left" "t_shape,beam,l_shape:C_backright"
       "asym,u_channel,plus:D_far_turn")
GA="--objects all --reps 10 --seed 7100 --videos 1"

done_() { [[ -s logs/evals/$1/summary.json || -s logs/evals/$1/pair/summary.json ]]; }
clear_() {  # remove a stale partial output (logs/evals/<d> and evals/<d>)
  local d
  for d in "logs/evals/$1" "evals/$1"; do [[ -e "$d" ]] && rm -rf -- "${d:?}"; done
  return 0
}
commit_() {  # commit_ PART FINAL: rename logs/evals/PART (and evals/PART) to FINAL
  clear_ "$2"
  mv -- "logs/evals/$1" "logs/evals/$2" && { [[ -e "evals/$1" ]] && mv -- "evals/$1" "evals/$2"; true; }
}
step() {  # step KIND NAME args...   KIND: ev (eval_coop2), ct (contact_test), hl (helper_test), br (chain4_branch)
  local kind=$1 n=$2; shift 2
  local fin=$n part=$n.part
  [[ $kind == ct ]] && { fin=$n-expert; part=$n.part-expert; }
  done_ "$fin" && { echo "== skip $n"; return; }
  clear_ "$part"; clear_ "$fin"
  echo ">> $kind $n $*"
  case $kind in
    ev) python scripts/eval_coop2.py --name "$n.part" "$@" ;;
    ct) python scripts/contact_test.py --prefix "$n.part" $PLAN "$@" ;;
    hl) python scripts/helper_test.py --prefix "$n.part" "$@" ;;
    br) python scripts/chain4_branch.py --prefix "$n.part" "$@" ;;
  esac
  local rc=$?
  if [[ $rc == 0 ]] && done_ "$part"; then commit_ "$part" "$fin"; else echo "!! failed ($rc): $n"; fi
}
ev() { step ev "$@"; }
ct() { step ct "$@"; }
hl() { step hl "$@"; }

case $GROUP in
A0|A1|A2|A3|A4)
  M=60
  case $GROUP in
    A0) SRC=(--solo anymal1 --pair anymal); M=20 ;;  # G0: G1 at 20 kg
    A1) SRC=(--solo anymal1 --pair anymal) ;;
    A2) SRC=(--frozen-pair --pair anymal) ;;
    A3) SRC=(--checkpoint $IPPO) ;;
    A4) SRC=(--checkpoint $MAPPO) ;;
  esac
  for i in 0 1 2 3; do
    o=${GOALS[$i]%%:*}; s=${GOALS[$i]##*:}
    ev talk-$GROUP-g$i "${SRC[@]}" $GA --masses $M --video-tasks "$o/$M/$s/$REP"
  done ;;
A5)
  for i in 0 1 2 3; do
    o=${GOALS[$i]%%:*}; s=${GOALS[$i]##*:}
    ct talk-A5-g$i --objects all --reps 10 --seed 7100 --masses 60 --videos 1 \
      --video-objects "$o" --video-masses 60 --video-scenarios "$s" --video-reps $REP
  done ;;
A6)  # the helper arm of slurm/helper_videos.sbatch, at 80 kg
  for i in 0 1 2 3; do
    o=${GOALS[$i]%%:*}; s=${GOALS[$i]##*:}
    hl talk-A6-g$i --seed 7100 --arms helper --reps 10 --masses 80 --objects $ALL \
      --videos 1 --video-only 1 --video-arms helper --video-objects "$o" --video-masses 80 --video-scenarios "$s" \
      --video-reps $REP
  done ;;
B1)  # pres-* layout: 10 objects, 3 reps, seed 7100
  B="--objects $TEN --reps 3 --seed 7100 --videos 1"
  for r in 1 2; do
    for arm in solo copies mappo; do
      case $arm in
        solo) SRC=(--solo anymal1 --pair anymal) ;;
        copies) SRC=(--frozen-pair --pair anymal) ;;
        mappo) SRC=(--checkpoint $MAPPO) ;;
      esac
      ev talk-B1-$arm-a-r$r "${SRC[@]}" $B --masses 80 --video-tasks "long,l_shape/80/A_straight/0"
      ev talk-B1-$arm-b-r$r "${SRC[@]}" $B --masses 60 --video-tasks "t_shape/60/A_straight/0"
      ev talk-B1-$arm-c-r$r "${SRC[@]}" $B --masses 60 --video-tasks "u_channel/60/B_left/2"
    done
  done ;;
B2)  # KL anchor: the mappo-aa_*-s0-it3000 evaluations (12 objects, 3 reps, seed 0)
  B="--objects all --reps 3 --seed 0 --videos 1"
  for r in 1 2; do
    for arm in nokl kl; do
      [[ $arm == nokl ]] && CK=$NOKL || CK=$KL
      ev talk-B2-$arm-a-r$r --checkpoint $CK $B --masses 60 --video-tasks "long,u_channel/60/A_straight/0"
      ev talk-B2-$arm-b-r$r --checkpoint $CK $B --masses 40 --video-tasks "dumbbell,t_shape/40/A_straight/0"
    done
  done ;;
B3)  # MAPPO pair vs the original contact planner, benchmark layout (12 objects, 10 reps, seed 7100)
  for r in 1 2; do
    ev talk-B3-mappo-a-r$r --checkpoint $MAPPO $GA --masses 60 --video-tasks "arch/60/A_straight/8"
    ev talk-B3-mappo-b-r$r --checkpoint $MAPPO $GA --masses 60 --video-tasks "asym/60/B_left/9"
    ev talk-B3-mappo-c-r$r --checkpoint $MAPPO $GA --masses 80 --video-tasks "u_channel/80/A_straight/8"
    ct talk-B3-plan-a-r$r --objects all --reps 10 --seed 7100 --masses 60 --videos 1 --video-objects arch \
      --video-masses 60 --video-scenarios A_straight --video-reps 8
    ct talk-B3-plan-b-r$r --objects all --reps 10 --seed 7100 --masses 60 --videos 1 --video-objects asym \
      --video-masses 60 --video-scenarios B_left --video-reps 9
    ct talk-B3-plan-c-r$r --objects all --reps 10 --seed 7100 --masses 80 --videos 1 --video-objects u_channel \
      --video-masses 80 --video-scenarios A_straight --video-reps 8
  done ;;
B5)  # 2 -> 3 robots, cloned states (k4c defaults: seed 1001, t1 8 s, t2 20 s), the two objects with the largest
     # k3 - k2 gain at 80 kg; side-by-side k2 (pair continues) | k3b (robot 3 called at t2 from the same state)
  export QUADCOOP_HD_SIZE=1280x720
  for r in 1 2; do
    step br talk-B5-r$r --objects t_shape,cube --masses 80 --reps 3 --seed 1001 \
      --film-pairs k2:k3b --film-max 8 --film-size 1280x720
  done ;;
*) echo "unknown GROUP $GROUP"; exit 1 ;;
esac
echo "done $GROUP"
