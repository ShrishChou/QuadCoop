#!/bin/bash
# Regret minimization inside the contact planner's re-planning (RegretCoordinator, docs/regret_replanning.md): the
# expert planner + turn_debug executor (the presentation system, robots starting behind the object), with each
# re-plan chosen by Exp3 among {expert's pick, keep, 2nd, 3rd cheapest}. KIND:
#   check   2 objects, 40 kg, 1 rep, 30 s
#   train   PASSES learning passes on training placements (seeds 1001..), each continuing the previous state
#   expert  the expert alone on the test (seed 7100)          frozen / online  the trained state on the same test
#SBATCH -J qc-rr
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
CK=logs/keep/marl2/turn_debug/model_15000.pt
OBJ=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus
C="--pair anymal --rules expert --executor stage4 --checkpoint $CK --start behind --objects $OBJ --videos 0"
D=logs/evals/rr-state
mkdir -p $D
done_() { [[ -s evals/$1-expert/eval/pair/episodes.csv ]]; }
case "${KIND:?}" in
  check)
    python scripts/contact_test.py $C --objects cube,beam --masses 40 --reps 1 --horizon 30 --seed 1001 --prefix rr-check \
      --coordinator regret --regret-save $D/check.pt && cat $D/check.md ;;
  train)
    prev=""
    for s in $(seq 1001 $((1000 + ${PASSES:-3}))); do
      if ! done_ rr-train-s$s || [[ ! -s $D/train-s$s.pt ]]; then
        python scripts/contact_test.py $C --masses 20,40,60,80 --reps 3 --seed $s --prefix rr-train-s$s \
          --coordinator regret ${prev:+--regret-state $prev} --regret-save $D/train-s$s.pt || echo "!! pass $s failed"
      fi
      prev=$D/train-s$s.pt
    done
    cat ${prev%.pt}.md ;;
  expert)
    python scripts/contact_test.py $C --masses 20,40,60,80 --reps 5 --seed 7100 --prefix rr-test-base ;;
  frozen|online)
    st=$D/train-s$((1000 + ${PASSES:-3})).pt
    [[ -s $st ]] || { echo "no state $st"; exit 1; }
    mode=$([[ $KIND == frozen ]] && echo frozen || echo exp3)
    python scripts/contact_test.py $C --masses 20,40,60,80 --reps 5 --seed 7100 --prefix rr-test-$KIND \
      --coordinator regret --regret-mode $mode --regret-state $st --regret-save $D/test-$KIND.pt ;;
esac
