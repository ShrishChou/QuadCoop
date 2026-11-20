#!/bin/bash
# Videos of the final ten-object ANYmal pairs (IPPO ippo_aa_kl_ten_s0/model_4000, MAPPO nwB_mappo_uniform_s0/
# model_5000, the checkpoints behind presentation folder 05) on the twelve benchmark objects (beam and asym held
# out in training) x the four scenarios x 40 / 80 kg, rep 0, seed 7100: 96 clips per algorithm.
# Videos: logs/evals/pairvid-{ippo,mappo}/pair/ (and the eval's own success table).
#   sbatch slurm/pair_videos.sbatch
#SBATCH -J qc-pairvid
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 04:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
OBJ=cube,long,sphere,cylinder,arch,dumbbell,t_shape,beam,l_shape,asym,u_channel,plus
V="--objects $OBJ --masses 40,80 --reps 1 --seed 7100 --videos 1 --video-tasks all/40,80/all/0"
python scripts/eval_coop2.py --name pairvid-ippo --checkpoint logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt $V || echo "!! ippo failed"
python scripts/eval_coop2.py --name pairvid-mappo --checkpoint logs/marl2/nwB_mappo_uniform_s0/model_5000.pt $V || echo "!! mappo failed"
