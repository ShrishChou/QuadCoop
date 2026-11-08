#!/bin/bash
# Train walker v2.1 (task QuadCoop-Walker-AnymalC-Compliant-v21, src/quadcoop/walker_env_cfg.py) on one L40S:
# the same network as walker v2, resumed from v2's final checkpoint, with what v2's test and training curves
# showed missing (no new reward terms):
#   - the smooth force field on and felt (ramp-hold-ramp loads up to 0.5 x weight, in the force input and
#     the compliant target), so every force level is practised, not only rigid impacts
#   - the mass curriculum unstuck (v2 sat at 35-40 kg: training falls 0.15-0.2 against a 0.10 gate)
#   - a slower force filter and at most 0.1 m/s back-off (v2 tapped: impact spikes said "retreat")
#   - pure turns on the spot, slow speeds log-uniform 0.02-0.3 m/s, 40% free walk, tighter turn tracking
#
#   sbatch slurm/train_walker_v21.sbatch                 # resume from v2's newest checkpoint, ITERS (3000) more
#   RESUME=1 sbatch slurm/train_walker_v21.sbatch        # continue the newest v2.1 run (after the 6 h limit)
#
# Checkpoints every 100 iterations in logs/rsl_rl/walker_anymal_c_compliant/<date>_v21/ (numbering continues from
# v2's, e.g. model_3100.pt ... model_6000.pt). Training videos in that folder's videos/train/.
# Optional: V2_RUN (v2 run folder name; default the newest *_compliant), V2_CKPT (default its newest model_*.pt),
# ITERS, NUM_ENVS (4096), SEED (0), LOGGER (wandb|tensorboard), VIDEO (1|0), and any QUADCOOP_* knob from
# src/quadcoop/walker_env_cfg.py (e.g. QUADCOOP_PUSH_MAX_FRAC=0.6, QUADCOOP_CURR_FALL=0.3).
#SBATCH -J qc-walker21
#SBATCH -p mit_normal_gpu
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "${SLURM_SUBMIT_DIR:-$PWD}"
[[ -f .venv/bin/activate ]] && source .venv/bin/activate
export MUJOCO_GL=egl
export PYTHONPATH="$PWD/src:${PYTHONPATH:-}"
command -v nvidia-smi >/dev/null && nvidia-smi --query-gpu=name,memory.total --format=csv

TASK=QuadCoop-Walker-AnymalC-Compliant-v21
EXP=logs/rsl_rl/walker_anymal_c_compliant
newest_ckpt() { ls "$1"/model_*.pt 2>/dev/null | sort -V | tail -1 | xargs -r basename; }

ARGS=(--env.scene.num-envs "${NUM_ENVS:-4096}"
      --agent.seed "${SEED:-0}"
      --agent.max-iterations "${ITERS:-3000}"
      --agent.run-name v21
      --agent.logger "${LOGGER:-wandb}")
[[ -n "${EXTRA_ARGS:-}" ]] && ARGS+=(${EXTRA_ARGS})
if [[ "${VIDEO:-1}" == "1" ]]; then
  ARGS+=(--video True --video-length 300 --video-interval "${VIDEO_INTERVAL:-5000}")
fi
if [[ "${RESUME:-0}" == "1" ]]; then
  RUN=""
  for d in $(ls -d "$EXP"/*_v21 2>/dev/null | sort -r); do  # newest v2.1 run that has a checkpoint
    if [[ -n "$(newest_ckpt "$d")" ]]; then RUN=$(basename "$d"); break; fi
  done
  [[ -n "$RUN" ]] || { echo "no v2.1 run with checkpoints in $EXP to continue"; exit 1; }
else
  RUN=${V2_RUN:-$(ls -d "$EXP"/*_compliant 2>/dev/null | sort | tail -1 | xargs -r basename)}
  [[ -n "$RUN" && -d "$EXP/$RUN" ]] || { echo "no v2 run (*_compliant) in $EXP; set V2_RUN"; exit 1; }
fi
CKPT=${V2_CKPT:-$(newest_ckpt "$EXP/$RUN")}
[[ "${RESUME:-0}" == "1" ]] && CKPT=$(newest_ckpt "$EXP/$RUN")
[[ -n "$CKPT" && -f "$EXP/$RUN/$CKPT" ]] || { echo "no checkpoint in $EXP/$RUN"; exit 1; }
echo "starting from $EXP/$RUN/$CKPT"
ARGS+=(--agent.resume True --agent.load-run "^${RUN}\$" --agent.load-checkpoint "^${CKPT}\$")
echo "task=$TASK args=${ARGS[*]}"
python train.py "$TASK" "${ARGS[@]}"
