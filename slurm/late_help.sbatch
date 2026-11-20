#!/bin/bash
# Late-help branching experiment (scripts/branch_help.py, docs/late_help.md).
#   KIND=check  clone fidelity (twins stay solo after the copy; divergence printed), 2 objects, 40 kg, 1 rep
#   KIND=run    PROBE s solo probe, then solo vs help branches: 12 objects x 4 positions x REPS x 20-80 kg, seed 7100
#SBATCH -J qc-latehelp
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
case "${KIND:?}" in
  check) python scripts/branch_help.py --name lh-check --objects cube,beam --masses 40 --reps 1 --probe-s 5 --check ;;
  run)   python scripts/branch_help.py --name lh-p${PROBE:-8} --probe-s ${PROBE:-8} --reps ${REPS:-5} ;;
esac
