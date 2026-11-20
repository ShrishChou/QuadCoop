#!/bin/bash
# Regret-minimizing subgoal planner above the ANYmal MAPPO pair (quadcoop/coop2/subgoal.py; slurm/submit_subgoal.sh
# submits these). KIND:
#   check  2 objects, 40 kg, 1 rep, 30 s, exp3: the hook runs and the planner learns / saves
#   train  Exp3 learning passes on training placements (seeds 1001.., not the benchmark's 7100), each pass starting
#          from the previous pass's planner state -> logs/evals/sg-train-s<seed>/pair/subgoal_planner.pt
#   fixed  every arm alone on the benchmark (seed 7100): the comparators; fixed:direct is the pair on its own
#   test   the trained planner on the benchmark: frozen (no learning, no exploration) and online (keeps learning)
# Benchmark = the 480-task set of the 66% MAPPO result: 10 training shapes x 4 positions x 3 reps x 20/40/60/80 kg.
# A pass whose episodes.csv exists is skipped, so a requeued job continues where it stopped.
#SBATCH -J qc-subgoal
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
CK=${CK:-logs/marl2/nwB_mappo_uniform_s0/model_5000.pt}
OBJ=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
TAG=${TAG:-sg}
SG=${SGARGS:-}
run() {  # name, then eval_coop2 args
  local name=$1; shift
  if [[ -s logs/evals/$name/pair/episodes.csv ]]; then echo "skip $name (done)"; return 0; fi
  python scripts/eval_coop2.py --name "$name" --checkpoint "$CK" --objects $OBJ --videos 0 "$@" $SG || echo "!! $name failed"
}
case "${KIND:?set KIND}" in
  check)
    rm -rf logs/evals/$TAG-check
    run $TAG-check --objects cube,beam --masses 40 --reps 1 --horizon 30 --seed 1001 --subgoal exp3
    cat logs/evals/$TAG-check/pair/subgoal_planner.md ;;
  train)
    prev=${LOAD:-}
    for s in $(seq 1001 $((1000 + ${PASSES:-3}))); do
      run $TAG-train-s$s --masses 20,40,60,80 --reps 3 --seed $s --subgoal exp3 ${prev:+--subgoal-load $prev}
      prev=logs/evals/$TAG-train-s$s/pair/subgoal_planner.pt
    done
    cat "$(dirname "$prev")/subgoal_planner.md" ;;
  fixed)
    for arm in ${ARMS_LIST:-direct straight translate rotate arc_left arc_right}; do
      run $TAG-fixed-$arm-dev7100 --masses 20,40,60,80 --reps 3 --seed 7100 --subgoal fixed:$arm
    done ;;
  test)
    st=${LOAD:-logs/evals/$TAG-train-s$((1000 + ${PASSES:-3}))/pair/subgoal_planner.pt}
    [[ -s $st ]] || { echo "no planner state $st"; exit 1; }
    run $TAG-frozen-dev7100 --masses 20,40,60,80 --reps 3 --seed 7100 --subgoal frozen --subgoal-load $st
    run $TAG-online-dev7100 --masses 20,40,60,80 --reps 3 --seed 7100 --subgoal exp3 --subgoal-load $st ;;
  *) echo "unknown KIND"; exit 1 ;;
esac
