#!/bin/bash
# Walker acceptance test (scripts/walker_test.py): free walking incl. small commands and kicks,
# pressing an immovable cube (force vs commanded speed), pushing 20/40/80 kg cubes. Any number of
# walkers on identical cases. Stats -> evals/<NAME>/ (summary.md, summary.json, cases.csv).
#
#   V2=$(ls -t logs/rsl_rl/walker_anymal_c_compliant/*/model_*.pt | head -1)
#   WALKERS="v1=logs/evals/walker-anymal-v1/model.pt,v2=$V2" sbatch slurm/walker_test.sbatch
#
# Walker v2.1 against v2, with videos of the cases v2 failed (eval_videos/<NAME>/<walker>/, git-ignored):
#   E=logs/rsl_rl/walker_anymal_c_compliant
#   V2=$(ls $(ls -d $E/*_compliant | tail -1)/model_*.pt | sort -V | tail -1)
#   V21=$(ls $(ls -d $E/*_v21 | tail -1)/model_*.pt | sort -V | tail -1)
#   WALKERS="v2=$V2,v21=$V21" NAME=wt-v21 ARGS="--videos fwd,side,yaw,wall,objects" sbatch slurm/walker_test.sbatch
#SBATCH -J qc-wtest
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 02:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
nvidia-smi --query-gpu=name,memory.total --format=csv
python scripts/walker_test.py --walkers "${WALKERS:?set WALKERS=label=checkpoint,...}" --name "${NAME:-wt-test}" ${ARGS:-}
