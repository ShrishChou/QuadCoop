#!/bin/bash
# Scripted contacts (scripts/contact_test.py): hand-assigned contact rules on the pair-evaluation tasks.
# Stats -> evals/<PREFIX>-<rule>/eval/pair/ (one folder per rule), videos -> logs/evals/<PREFIX>-<rule>/pair/videos/.
#
#   sbatch slurm/contact_test.sbatch                                   # two ANYmal C, rules centre/adjacent/spread
#   PAIR=mixed sbatch slurm/contact_test.sbatch                        # ANYmal C + Spot
#   PREFIX=contact-aa-re4 ARGS="--reassign-s 4" sbatch slurm/contact_test.sbatch
#   ARGS="--executor policy" sbatch slurm/contact_test.sbatch                     # hand-off test -> handoff-aa-<rule>
#   PREFIX=handoff-aa-free ARGS="--executor policy --return-dist 0" sbatch slurm/contact_test.sbatch   # never pulled back
# Masses can be split over jobs with the same PREFIX: each job merges its masses into the same results, and
# results are saved after every mass (a job that hits the time limit keeps the masses it finished), e.g.
#   for m in 40 60 80; do MASSES=$m PREFIX=handoff-aa-free ARGS="--executor policy --return-dist 0" sbatch slurm/contact_test.sbatch; done
# Optional: PAIR (anymal), PREFIX (contact-<aa|mx|ss>), RULES (centre,adjacent,spread), MASSES (20,40,60,80),
# REPS (3), ARGS (more contact_test.py args).
#SBATCH -J qc-contact
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH --requeue
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
EXTRA=()
if [[ -n "${PREFIX:-}" ]]; then EXTRA+=(--prefix "$PREFIX"); fi
python scripts/contact_test.py --pair "${PAIR:-anymal}" --rules "${RULES:-centre,adjacent,spread}" \
  --masses "${MASSES:-20,40,60,80}" --reps "${REPS:-3}" "${EXTRA[@]}" ${ARGS:-}
