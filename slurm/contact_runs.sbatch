#!/bin/bash
# Several scripts/contact_test.py runs in sequence (one GPU job): RUN1 .. RUN9, each a full argument string.
#   COMMON="--pair anymal ..." RUN1="--prefix a" RUN2="--prefix b --set fb_on=1" sbatch slurm/contact_runs.sbatch
#SBATCH -J qc-runs
#SBATCH -p mit_normal_gpu
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 03:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl QUADCOOP_PLANNER=ends QUADCOOP_CONTACT=train QUADCOOP_CMD_IF=raw
for i in 1 2 3 4 5 6 7 8 9; do
    v="RUN$i"
    if [[ -n "${!v:-}" ]]; then echo "=== run $i: ${!v}"; python scripts/contact_test.py ${COMMON:-} ${!v}; fi
done
