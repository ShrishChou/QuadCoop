#!/bin/bash
# Heavy-transport evaluation over objects (scripts/spot_arm/pair_eval.py, one call per object x task):
#   the long object at 20 kg / 1 m, 40 kg / 2 m, 60 kg / 2 m and 60 kg / 3 m (20 placements per turn x swap), and
#   every other trained object at 40 kg / 2 m (6 placements). 40 s horizon, +-60 deg, arm ablation, solo modes.
#   CK=logs/marl2/<run>/model_4000.pt RUN=<run> sbatch slurm/spot_arm_eval_multi.sbatch
#SBATCH -J qc-saevalm
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH -G 1
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -t 03:00:00
#SBATCH --exclude=node4207
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
ev() {  # object mass dist reps
  local name=sa-heavy-${RUN:?}-$1-${2}kg-${3}m
  [[ -e evals/$name/summary.md ]] && return 0
  python scripts/spot_arm/pair_eval.py --checkpoint "${CK:?}" --name "$name" --object "$1" --turn 60 --mass "$2" \
    --dist "$3" --horizon 40 --reps "$4" || echo "!! failed: $name"
}
ev long 20 1 20; ev long 40 2 20; ev long 60 2 20; ev long 60 3 20
for o in ${OBJECTS:-cube sphere cylinder arch dumbbell t_shape l_shape u_channel plus}; do ev "$o" 40 2 6; done
