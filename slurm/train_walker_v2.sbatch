#!/bin/bash
# Train the compliant walker (walker v2, task QuadCoop-Walker-AnymalC-Compliant; see
# src/quadcoop/mdp/compliance.py) on one L40S. The first submission warm-starts from the v1 walker
# (scripts/warmstart_walker.py: same network + 2 zero-weight force inputs) and trains; if the 6 h
# limit cuts it off, resubmit with RESUME=1 to continue from the newest checkpoint of the newest run.
#
#   sbatch slurm/train_walker_v2.sbatch                  # warm start + ITERS (3000) iterations
#   RESUME=1 sbatch slurm/train_walker_v2.sbatch         # continue
#
# Checkpoints every 100 iterations in logs/rsl_rl/walker_anymal_c_compliant/<date>_<RUN_NAME>/.
# Optional: ITERS, NUM_ENVS (4096), SEED (0), RUN_NAME (compliant), LOGGER (wandb|tensorboard), VIDEO (1|0),
# SOURCE (v1 checkpoint, default logs/evals/walker-anymal-v1/model.pt), MIN_STD (0.3), and any QUADCOOP_* knob
# from src/quadcoop/walker_env_cfg.py (e.g. QUADCOOP_STIFFNESS=1000).
#SBATCH -J qc-walker2
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
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
nvidia-smi --query-gpu=name,memory.total --format=csv

TASK=QuadCoop-Walker-AnymalC-Compliant
ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}"
      --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-3000}"
      --agent.run-name "${RUN_NAME:-compliant}"
      --agent.logger "${LOGGER:-wandb}")
if [[ "${VIDEO:-1}" == "1" ]]; then
  ARGS+=(--video True --video-length 300 --video-interval "${VIDEO_INTERVAL:-5000}")
fi
if [[ "${RESUME:-0}" == "1" ]]; then
  ARGS+=(--agent.resume True)   # newest run + newest model_*.pt under logs/rsl_rl/walker_anymal_c_compliant
else
  OUT=$(python scripts/warmstart_walker.py --source "${SOURCE:-logs/evals/walker-anymal-v1/model.pt}" --min-std "${MIN_STD:-0.3}")
  echo "$OUT"
  RUN_DIR=$(echo "$OUT" | sed -n 's/^RUN_DIR=//p')
  ARGS+=(--agent.resume True --agent.load-run "$RUN_DIR" --agent.load-checkpoint model_0.pt)
fi
echo "task=$TASK args=${ARGS[*]}"
python train.py "$TASK" "${ARGS[@]}"
