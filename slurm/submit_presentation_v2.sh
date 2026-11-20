#!/usr/bin/env bash
# Presentation set v2 (presentation_export/01-05; scripts/assemble_presentation.py builds the folders afterwards):
# walkers (1 job), the single-robot ANYmal pusher and the contact planner (one job per mass each, 20/40/60/80 kg,
# best-of-10 HD videos), IPPO + MAPPO metrics (1 job, no videos). Every job is slurm/pres_job.sbatch.
#   bash slurm/submit_presentation_v2.sh
#   KINDS="solo planner" MASSES="80" bash slurm/submit_presentation_v2.sh     # a subset
set -euo pipefail
cd "$(dirname "$0")/.."
KINDS=${KINDS:-walkers solo planner pairs}
MASSES=${MASSES:-20 40 60 80}
for k in $KINDS; do
  case "$k" in
    walkers|pairs) echo "$k: $(KIND=$k sbatch --parsable -J qc-pres-$k slurm/pres_job.sbatch)" ;;
    solo|planner) for m in $MASSES; do
        echo "$k ${m} kg: $(KIND=$k MASS=$m sbatch --parsable -J qc-pres-$k$m slurm/pres_job.sbatch)"; done ;;
    *) echo "unknown kind $k" >&2; exit 1 ;;
  esac
done
