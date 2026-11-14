#!/bin/bash
# Next-wave preflight (docs/next_wave.md), no training: one GPU, four steps in order, each must pass.
#   1-2  actor transfer: PARENT's actors into IPPO and into MAPPO (fresh critics); both compared with the
#        source on the same saved observations (collected once, under the source policy), before any update
#   3    task bank: drawn once with the arms' env (seed, env count, flags), replay-checked on every slot
#   4    the same bank replay-checked under MAPPO's env build (the arms must see identical slot physics)
#
#   PARENT=logs/marl2/ippo_aa_kl_s0/model_3000.pt sbatch --dependency=afterany:<eval job> slurm/next_wave_checks.sbatch
# Optional: TAG (default from PARENT), BANK (default logs/next_wave/bank_ten_s0_k16.pt, parent-independent: it
# depends only on the env, seed and flags; reused, replay-checked again, if it exists).
#SBATCH -J qc-nwcheck
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
PARENT=${PARENT:?set PARENT=<trainer checkpoint>}
TAG=${TAG:-$(basename "$(dirname "$PARENT")")_$(basename "$PARENT" .pt)}
OUT=logs/next_wave
BANK=${BANK:-$OUT/bank_ten_s0_k16.pt}
mkdir -p "$OUT"
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
# the arms' settings (the ten-object restart's, actors from PARENT, critics fresh and trained alone first)
ARM="--pair anymal --partner-map --reward r7 --kl-ref 0.05 --max-actor-lr 1e-4 --fixed-difficulty --fixed-level 4 \
  --train-mass 20,80 --train-shapes $shapes --init-actors $PARENT --critic-warmup-resume 100 --seed 0 --video-interval 0"
OBS=$OUT/obs_${TAG}.pt
for algo in ippo mappo; do
  echo "== transfer check: $PARENT -> $algo"
  python train_coop2.py --algo "$algo" --run-name "chk_transfer_${algo}_${TAG}" --num-envs 512 $ARM --transfer-check "$OBS"
done
if [[ -f "$BANK" ]]; then
  echo "== bank exists: $BANK (replay check under ippo)"
  python train_coop2.py --algo ippo --run-name "chk_bank_ippo_${TAG}" --num-envs 4096 $ARM --task-bank-file "$BANK" --bank-check
else
  echo "== bank make + replay check: $BANK"
  python train_coop2.py --algo ippo --run-name "chk_bank_ippo_${TAG}" --num-envs 4096 $ARM --task-bank-file "$BANK" --bank-make
fi
echo "== bank replay check under mappo"
python train_coop2.py --algo mappo --run-name "chk_bank_mappo_${TAG}" --num-envs 4096 $ARM --task-bank-file "$BANK" --bank-check
echo "== all next-wave checks passed ($TAG)"
