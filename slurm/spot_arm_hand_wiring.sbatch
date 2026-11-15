#!/bin/bash
# Spot-arm hand wave preflight (docs/spot_arm_pair.md): the trainer builds and updates (2 iterations, 256 envs) for
# MAPPO x arms hand / joint / stowed with --hand-obs at +-60 deg, then scripts/spot_arm/hand_reach.py (each Spot alone
# reaches left / right / stays stowed and walks into the 20 kg long object) with the reloaded hand checkpoint. ~25 min.
#SBATCH -J qc-sahand
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 4
#SBATCH --mem=48G
#SBATCH -t 01:00:00
#SBATCH --exclude=node4207
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
source slurm/spot_arm_hand.env
for arm in hand learned stowed; do
  echo "== check: mappo, arm $arm, +-60 deg"
  rm -rf "logs/marl2/sa_handwire_${arm}_check"
  python train_coop2.py --algo mappo --seed 0 --run-name sa_handwire_${arm} --check --num-envs 256 --arm $arm $TURN60
  ls logs/marl2/sa_handwire_${arm}_check/
done
CK=$(ls -v logs/marl2/sa_handwire_hand_check/model_*.pt | tail -1)
python scripts/spot_arm/hand_reach.py --checkpoint "$CK" ${ARGS:-}
