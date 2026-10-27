#!/bin/bash
# Pair / solo evaluation on fixed tasks (scripts/eval_coop2.py). Stats -> evals/<NAME>/eval/pair/,
# videos -> logs/evals/<NAME>/pair/videos/.
#
#   NAME=pair-frozen MODE=frozen sbatch slurm/eval_coop2.sbatch
#   NAME=solo-anymal MODE=solo-anymal sbatch slurm/eval_coop2.sbatch
#   NAME=mappo-s0-it3000 CK=logs/marl2/mappo_s0/model_3000.pt sbatch slurm/eval_coop2.sbatch
#   NAME=pair-frozen-anymal MODE=frozen ARGS="--pair anymal" sbatch slurm/eval_coop2.sbatch   # two ANYmal C
#   NAME=mappo-aa_r7-s0-it3000-solo-anymal1 CK=logs/marl2/mappo_aa_r7_s0/model_3000.pt SOLO=anymal1 \
#       sbatch slurm/eval_coop2.sbatch     # one trained actor alone (the other robot parked)
# Optional: MASSES (20,40,60,80), REPS (3), ARGS (more eval_coop2.py args).
#SBATCH -J qc-evalc2
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
: "${NAME:?set NAME=<output id>}"
if [[ -n "${CK:-}" ]]; then
  [[ -f "$CK" ]] || { echo "checkpoint not found: $CK"; exit 1; }
  SRC=(--checkpoint "$CK")
  if [[ -n "${SOLO:-}" ]]; then SRC+=(--solo "$SOLO"); fi
else
  case "${MODE:?set MODE=frozen, solo-anymal or solo-spot (or CK=<checkpoint>)}" in
    frozen) SRC=(--frozen-pair) ;;
    solo-anymal) SRC=(--solo anymal) ;;
    solo-spot) SRC=(--solo spot) ;;
    solo-*) SRC=(--solo "${MODE#solo-}") ;;
    *) echo "MODE must be frozen, solo-anymal or solo-spot"; exit 1 ;;
  esac
fi
python scripts/eval_coop2.py --name "$NAME" "${SRC[@]}" --masses "${MASSES:-20,40,60,80}" --reps "${REPS:-3}" ${ARGS:-}
