#!/usr/bin/env bash
# Regret-minimizing subgoal planner over the ANYmal MAPPO pair (docs/subgoal_planner.md): a short check, then
# (after it) the Exp3 training passes and the fixed-arm comparators in parallel, then the test of the trained planner.
#   bash slurm/submit_subgoal.sh
#   PASSES=5 bash slurm/submit_subgoal.sh                  # more learning passes
#   TAG=sg2 SGARGS="--subgoal-look 2.0" bash slurm/submit_subgoal.sh   # a variant (own output names)
set -euo pipefail
cd "$(dirname "$0")/.."
export TAG=${TAG:-sg} PASSES=${PASSES:-3} SGARGS=${SGARGS:-}
chk=$(KIND=check sbatch --parsable -J qc-sg-check -t 00:40:00 slurm/subgoal_job.sbatch)
tr=$(KIND=train sbatch --parsable -J qc-sg-train --dependency=afterok:$chk slurm/subgoal_job.sbatch)
fx=$(KIND=fixed sbatch --parsable -J qc-sg-fixed --dependency=afterok:$chk slurm/subgoal_job.sbatch)
te=$(KIND=test sbatch --parsable -J qc-sg-test --dependency=afterok:$tr slurm/subgoal_job.sbatch)
echo "check $chk -> train $tr (then test $te), fixed arms $fx"
