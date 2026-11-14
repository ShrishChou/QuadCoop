#!/usr/bin/env bash
# Start-placement comparison of existing checkpoints (docs/placement_eval.md): the 480 seed-7100 benchmark tasks in
# three start formations (standard, flank, goal_behind), each also with the robots' start places exchanged, so
# 2880 episodes per checkpoint. No training. Then: scripts/placement_compare.py.
#
#   AFTER=<job id> bash slurm/submit_placement_eval.sh     # optional: wait for that job to succeed (smoke test)
# Runs arm A (IPPO), arm B (MAPPO) and the parent (iteration 4000, after A ends): at most two GPUs at once.
set -euo pipefail
cd "$(dirname "$0")/.."
shapes=cube,long,sphere,cylinder,arch,dumbbell,t_shape,l_shape,u_channel,plus
ARGS="--objects $shapes --seed 7100 --videos 0 --formations standard,flank,goal_behind --swap"
dep=()
[[ -n "${AFTER:-}" ]] && dep=(--dependency="afterok:${AFTER}")
sub() {  # name checkpoint [extra sbatch args]
  [[ -s "$2" ]] || { echo "missing $2" >&2; exit 1; }
  NAME="$1" CK="$2" SOLO= MASSES=20,40,60,80 REPS=3 ARGS="$ARGS" sbatch --parsable "${@:3}" slurm/eval_coop2.sbatch
}
a=$(sub place-nwA-ippo-it5000 logs/marl2/nwA_ippo_uniform_s0/model_5000.pt "${dep[@]}")
b=$(sub place-nwB-mappo-it5000 logs/marl2/nwB_mappo_uniform_s0/model_5000.pt "${dep[@]}")
p=$(sub place-ten-ippo-it4000 logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt --dependency="afterany:${a}")
echo "IPPO arm A: $a   MAPPO arm B: $b   parent it4000: $p (after $a)"
