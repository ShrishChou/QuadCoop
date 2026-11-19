#!/bin/bash
# Rolling-cylinder planner model (CoopPush2CommandCfg.roll_ratio, docs/planner_cylinder.md): one job.
#   1. planner physics test (no robots), cylinder only: does the planner's push move it as asked, with the old
#      isotropic model (roll 0) against rolling models (0.05, 0.1, 0.2)?
#   2. the planner on the benchmark's cylinder tasks (as planner-bench-*: start behind, 80 s, 20-80 kg, seeds 7100
#      and 7500) with roll 0.1 and 0.2; the roll-0 baseline is evals/planner-bench-{7100,7500}-expert.
#   sbatch slurm/cylinder_roll_test.sbatch
#SBATCH -J qc-cylroll
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 04:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
for r in 0 0.05 0.1 0.2; do
  [[ -s evals/pp-cyl-roll$r/summary.md ]] && continue
  python scripts/planner_physics_test.py --name "pp-cyl-roll$r" --objects cylinder --fmax 150,250 --roll-ratio "$r"
done
for r in 0.1 0.2; do
  for s in 7100 7500; do
    [[ -s evals/cyl-roll$r-$s-expert/eval/pair/summary.md ]] && continue
    python scripts/contact_test.py --pair anymal --executor stage4 --checkpoint logs/keep/marl2/turn_debug/model_15000.pt \
      --rules expert --start behind --objects cylinder --masses 20,40,60,80 --reps 3 --seed "$s" --horizon 80 \
      --slow-min-s 1.0 --videos 0 --prefix "cyl-roll$r-$s" --set "roll_ratio=$r"
  done
done
