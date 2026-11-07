#!/bin/bash
# Submit every component evaluation at once (they are independent; Slurm runs them as GPUs free up).
# Run from ~/quadcoop on the login node:   bash slurm/submit_component_evals.sh
# Model: the minimal-reward contact executor (hvB, iteration 13500), kept copy. Skip parts with SKIP="fsweep allpairs ...".
#
#   fsweep    test 1, force limit 150 / 250 / 350 N           -> evals/pp-fsweep
#   allpairs  every contact pair fixed, 40 and 80 kg (10 jobs) -> evals/game-hvB-allpairs   (then contact_game.py, below)
#   immov     test 2a: an immovable object (5000 kg)            -> evals/t2-immov-expert, -wrench (push force a robot sustains)
#   share     test 2b: the standard tasks from the contacts     -> evals/t2-share-expert     (does each robot push its share?)
#   turn      test 3: turn in place, three planner variants     -> evals/t3-base-expert, t3-nofinish-expert, t3-force-expert
#
# When everything has finished:
#   python scripts/contact_game.py --sweep evals/game-hvB-allpairs
#   git add evals/pp-fsweep evals/game-hvB-* evals/t2-* evals/t3-* && git commit -m "component evals" && git push
set -euo pipefail
CK=logs/keep/marl2/hvB_aa_s0/model_13500.pt
[[ -f "$CK" ]] || { echo "missing $CK (copy it into logs/keep first)"; exit 1; }
SKIP=" ${SKIP:-} "
S4="--executor stage4 --checkpoint $CK --videos 0"
sub() { echo "+ $*"; env "$@"; }

if [[ "$SKIP" != *" fsweep "* ]]; then
  sub NAME=pp-fsweep ARGS="--fmax 150,250,350" sbatch slurm/planner_physics_test.sbatch
fi
if [[ "$SKIP" != *" allpairs "* ]]; then
  for m in 40 80; do for objs in cube,long,sphere cylinder,arch,dumbbell t_shape,beam,l_shape asym,u_channel,plus; do
    sub MASSES=$m RULES=allpairs REPS=3 PREFIX=game-hvB ARGS="$S4 --objects $objs" sbatch slurm/contact_test.sbatch
  done; done
fi
if [[ "$SKIP" != *" immov "* ]]; then
  sub MASSES=5000 RULES=expert,wrench REPS=1 PREFIX=t2-immov ARGS="$S4 --horizon 20" sbatch slurm/contact_test.sbatch
fi
if [[ "$SKIP" != *" share "* ]]; then
  for m in 20 40 60 80; do
    sub MASSES=$m RULES=expert REPS=3 PREFIX=t2-share ARGS="$S4" sbatch slurm/contact_test.sbatch
  done
fi
if [[ "$SKIP" != *" turn "* ]]; then
  sub RULES=expert REPS=3 PREFIX=t3-base ARGS="$S4 --tasks turn --horizon 30 --trace 1" sbatch slurm/contact_test.sbatch
  sub RULES=expert REPS=3 PREFIX=t3-nofinish ARGS="$S4 --tasks turn --horizon 30 --trace 1 --set finish_dist=0" sbatch slurm/contact_test.sbatch
  sub RULES=expert REPS=3 PREFIX=t3-force ARGS="$S4 --tasks turn --horizon 30 --trace 1 --set robot_push_force=320" sbatch slurm/contact_test.sbatch
fi
squeue -u "${USER:-$(whoami)}"
