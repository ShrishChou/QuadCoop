#!/bin/bash
# Two-robot per-object videos (scripts/showcase_coop2.py) into eval_videos/<NAME>/ (git-ignored);
# stats into evals/<NAME>/eval/showcase/ (committed). About 30-60 min per policy.
#
#   NAME=mappo_aa_kl CK=logs/marl2/mappo_aa_kl_s0/model_3000.pt sbatch slurm/showcase_coop2.sbatch
#   NAME=pair_frozen_aa MODE=frozen PAIR=anymal sbatch slurm/showcase_coop2.sbatch
#   NAME=solo_anymal MODE=solo-anymal1 PAIR=anymal sbatch slurm/showcase_coop2.sbatch
# Optional: MASSES (40,60,80), PAIR (frozen / solo: mixed, anymal, spot), ARGS (more options).
# Then on the login node: python scripts/showcase_coop2.py --compare a,b,c --name cmp  (side by side)
#SBATCH -J qc-showc2
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
: "${NAME:?set NAME=<folder under eval_videos>}"
if [[ -n "${CK:-}" ]]; then
  [[ -f "$CK" ]] || { echo "checkpoint not found: $CK"; exit 1; }
  SRC=(--checkpoint "$CK")
else
  case "${MODE:?set MODE=frozen or solo-<robot> (or CK=<checkpoint>)}" in
    frozen) SRC=(--frozen-pair --pair "${PAIR:-mixed}") ;;
    solo-*) SRC=(--solo "${MODE#solo-}" --pair "${PAIR:-mixed}") ;;
    *) echo "MODE must be frozen or solo-<robot>"; exit 1 ;;
  esac
fi
nvidia-smi --query-gpu=name,memory.total --format=csv
python scripts/showcase_coop2.py --name "$NAME" "${SRC[@]}" --masses "${MASSES:-40,60,80}" ${ARGS:-}
