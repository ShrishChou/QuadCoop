#!/bin/bash
# Register the newest checkpoint of a training run and evaluate it (used by
# slurm/chain_push2_scratch.sh for the milestone and final evaluations).
#
#   EXP=logs/rsl_rl/push2b_spot RUN=fs ID=s2b-spot-fs WALKER_ID=walker-spot-rai-falcon \
#   TASK=QuadCoop-Push2b-Spot SUITES="h80" sbatch slurm/eval_checkpoint.sbatch
#
# The method id is ID-it<iteration> (e.g. s2b-spot-fs-it9999), or exactly ID with FINAL=1.
# SUITES: eval_method.py suites run one after another (default h80). SHOWCASE=<name> also films
# eval_videos/<name>/. NOTE: text for the registry. Stats land in evals/<id>/eval/<suite>/.
#SBATCH -J qc-evalck
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
unset QUADCOOP_WALKER_CKPT QUADCOOP_WALKER_CKPT_ANYMAL_C QUADCOOP_WALKER_CKPT_SPOT QUADCOOP_PUSH_FORCE
: "${EXP:?}" "${RUN:?}" "${ID:?}" "${WALKER_ID:?}" "${TASK:?}"
CK=$(python scripts/methods.py latest --run-dir "$EXP" --run-name "$RUN")
IT=$(basename "$CK" | sed -E 's/model_([0-9]+)\.pt/\1/')
if [[ "${FINAL:-0}" == "1" ]]; then MID=$ID; else MID=$ID-it$IT; fi
echo "evaluating $CK as $MID (suites: ${SUITES:-h80}${SHOWCASE:+, showcase $SHOWCASE})"
python scripts/methods.py register --id "$MID" --stage stage2 --task "$TASK" --checkpoint "$CK" \
  --walker "$WALKER_ID" --env QUADCOOP_SHAPES=v2 --note "${NOTE:-$RUN} (iteration $IT)" --force
for S in ${SUITES:-h80}; do
  python scripts/eval_method.py --id "$MID" --suite "$S" || echo "suite $S returned $?"
done
if [[ -n "${SHOWCASE:-}" ]]; then
  python scripts/showcase.py --id "$MID" --name "$SHOWCASE" || echo "showcase returned $?"
fi
python scripts/report.py > /dev/null && echo "updated evals/README.md"
