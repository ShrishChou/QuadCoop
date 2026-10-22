#!/bin/bash
# Submit N chained copies of the coop training array, each starting when the previous
# one has ended (each job resumes its run), so runs can go past the 6 h limit.
#
#   slurm/chain_coop.sh 3            # array 0-5, three 6 h rounds
#   slurm/chain_coop.sh 2 0,3        # only MAPPO seed 0 and IPPO seed 0, two rounds
#   EFFORT=0.5 slurm/chain_coop.sh 2 0  # environment variables pass through
set -euo pipefail
N=${1:-3}
ARRAY=${2:-0-5}
prev=""
for i in $(seq 1 "$N"); do
  dep=()
  [[ -n "$prev" ]] && dep=(--dependency=afterany:"$prev")
  prev=$(sbatch --parsable "${dep[@]}" --array="$ARRAY" slurm/train_coop.sbatch)
  prev=${prev%%;*}
  echo "round $i: job $prev (array $ARRAY)"
done
