#!/bin/bash
# Evaluate a two-robot training run at several iterations (when did it get better or worse?), and
# optionally each trained actor alone (did the single-robot skill survive?). One eval job each,
# same tasks as every other pair evaluation; stats in evals/<name>/eval/pair/.
#
#   RUN=mappo_aa_r7_s0 slurm/eval_coop2_iters.sh                       # iterations 100 500 1000 2000 3000
#   RUN=mappo_aa_r7_s0 ITERS="0 250 500 1000" slurm/eval_coop2_iters.sh
#   RUN=mappo_aa_r7_s0 SOLO=1 slurm/eval_coop2_iters.sh                # + each robot alone at every iteration
#   RUN=mappo_aa_r7_s0 SOLO=last slurm/eval_coop2_iters.sh             # + each robot alone at the last one
#
# Names: <algo>-<tag>-s<seed>-it<N> (as the automatic final evals), + -solo-<robot>.
# iteration 0 = the warm-started policies before any update (= the untrained pair).
# Missing checkpoints are skipped. Job ids: logs/slurm/eval_iters_<RUN>.txt.
set -euo pipefail
: "${RUN:?set RUN=<logs/marl2 run folder name>, e.g. mappo_aa_r7_s0}"
ITERS=${ITERS:-"100 500 1000 2000 3000"}
EVAL_PART=${EVAL_PART:-"-p mit_normal_gpu,mit_preemptable -t 06:00:00"}
EXCLUDE=${EXCLUDE:---exclude=node3006}
DIR=logs/marl2/$RUN
[[ -d "$DIR" ]] || { echo "no run folder $DIR"; exit 1; }
PREFIX=${PREFIX:-$(echo "$RUN" | sed -E 's/^([a-z]+)_(.*)_s([0-9]+)$/\1-\2-s\3/')}
mkdir -p logs/slurm
LOG=logs/slurm/eval_iters_$RUN.txt
echo "evaluating $DIR at iterations: $ITERS (solo: ${SOLO:-no}) ($(date))" | tee "$LOG"
LAST=""
for N in $ITERS; do
  if [[ -f "$DIR/model_$N.pt" ]] && { [[ -z "$LAST" ]] || (( N > LAST )); }; then LAST=$N; fi
done
for N in $ITERS; do
  CK=$DIR/model_$N.pt
  if [[ ! -f "$CK" ]]; then echo "  skip iteration $N (no $CK)" | tee -a "$LOG"; continue; fi
  J=$(env -u SOLO NAME="$PREFIX-it$N" CK="$CK" sbatch --parsable $EVAL_PART $EXCLUDE -J "ev-$PREFIX-it$N" \
        slurm/eval_coop2.sbatch | cut -d';' -f1)
  echo "  $PREFIX-it$N: job $J" | tee -a "$LOG"
  if [[ "${SOLO:-}" == 1 || ( "${SOLO:-}" == last && "$N" == "$LAST" ) ]]; then
    SLOTS=$(python - "$CK" <<'PY'
import sys
import torch
sys.path.insert(0, ".")
from train_coop2 import robot_of
ck = torch.load(sys.argv[1], map_location="cpu", weights_only=False)
print(" ".join(robot_of(ck.get("cfg", {}).get("pair", "mixed"))))
PY
)
    for S in $SLOTS; do
      J=$(env NAME="$PREFIX-it$N-solo-$S" CK="$CK" SOLO="$S" sbatch --parsable $EVAL_PART $EXCLUDE \
            -J "ev-$PREFIX-it$N-$S" slurm/eval_coop2.sbatch | cut -d';' -f1)
      echo "  $PREFIX-it$N-solo-$S: job $J" | tee -a "$LOG"
    done
  fi
done
