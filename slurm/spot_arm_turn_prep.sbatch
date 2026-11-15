#!/bin/bash
# Spot-arm turn in place, preparation (docs/spot_arm_pair.md): scripted demonstrations, then trainer checks (2
# iterations, 256 envs) for MAPPO stowed / hand_rate / hand_rate + demonstrations, then the evaluator on the
# cloned checkpoint. ~40 min.
#SBATCH -J qc-saprep
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 4
#SBATCH --mem=64G
#SBATCH -t 01:30:00
#SBATCH --exclude=node4207
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
source slurm/spot_arm_turn.env
[[ -s $DEMOS ]] || python scripts/spot_arm/collect_demos.py --out $DEMOS
for v in stowed:stowed hand:hand_rate bc:hand_rate; do
  nm=${v%%:*}; arm=${v##*:}; extra=""; [[ $nm == bc ]] && extra="$BC"
  echo "== check: mappo $nm"
  rm -rf "logs/marl2/sa_turnwire_${nm}_check"
  python train_coop2.py --algo mappo --seed 0 --run-name sa_turnwire_${nm} --check --num-envs 256 --arm $arm $TURN $extra
done
# the cloned policy before any PPO update (model_0 = after cloning) on the held-out tasks
python scripts/spot_arm/turn_inplace.py --checkpoint logs/marl2/sa_turnwire_bc_check/model_0.pt --reps 4 \
  --out evals/spot_arm/turnwire_bc_model0
