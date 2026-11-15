#!/bin/bash
# Spot-arm pair wiring test (docs/spot_arm_pair.md): the trainer builds and updates for IPPO / MAPPO x arms stowed /
# learned (2 iterations each), then the arm test and video with the reloaded MAPPO learned-arm checkpoint. ~20 min.
#SBATCH -J qc-sawire
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
source slurm/spot_arm_pilot.env
for algo in mappo ippo; do
  for arm in learned stowed; do
    echo "== check: $algo, arm $arm"
    rm -rf "logs/marl2/sa_wire_${algo}_${arm}_check"
    python train_coop2.py --algo $algo --seed 0 --run-name sa_wire_${algo}_${arm} --check --num-envs 256 \
        --arm $arm $PILOT
    ls logs/marl2/sa_wire_${algo}_${arm}_check/
  done
done
CK=$(ls -v logs/marl2/sa_wire_mappo_learned_check/model_*.pt | tail -1)
python scripts/spot_arm/pair_wiring.py --checkpoint "$CK"
