#!/bin/bash
# Late-help branching (scripts/branch_help.py, docs/late_help.md). KIND:
#   check   1 -> 2 clone fidelity (twins stay solo after the copy), 2 objects, 40 kg
#   check3  2 -> 3 clone fidelity in the trio env (the pair pushes, robot 3 parked), 2 objects, 80 kg
#   run     FROM (1 | 2) robots in the probe -> +1; SEED (7100 = test; 1001.. = training); PROBES (space list, s);
#           12 objects x 4 positions x REPS; 20-80 kg (FROM 1) or 20-120 kg (FROM 2)
# 1 -> 2: solo parent s2b-anymal-term80 -> IPPO pair ippo_aa_kl_ten_s0 it 4000
# 2 -> 3: that IPPO pair -> the trio trained from it, trio_ippo_s0 it 5500
#SBATCH -J qc-latehelp
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH --requeue
#SBATCH --exclude=node4207
#SBATCH -G l40s:1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH -o logs/slurm/%x-%j.out
set -uo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
PAIR=logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt
TRIO=logs/marl2/trio_ippo_s0/model_5500.pt
T3="--pair anymal3 --from-team 2 --probe-checkpoint $PAIR --checkpoint $TRIO"
case "${KIND:?}" in
  check)  python scripts/branch_help.py --name lh-check --objects cube,beam --masses 40 --reps 1 --probe-s 5 --check ;;
  check3) python scripts/branch_help.py --name lh23-check $T3 --objects cube,beam --masses 80 --reps 1 --probe-s 5 --check ;;
  run)
    FROM=${FROM:-1}; SEED=${SEED:-7100}
    if [[ $FROM == 2 ]]; then X="$T3"; M=${MASSES:-20,40,60,80,100,120}; else X="--checkpoint $PAIR"; M=${MASSES:-20,40,60,80}; fi
    for p in ${PROBES:-8}; do
      name=lh$FROM$((FROM + 1))-p$p-s$SEED
      [[ -s logs/evals/$name/branches.csv ]] && { echo "skip $name"; continue; }
      python scripts/branch_help.py --name $name $X --masses $M --probe-s $p --reps ${REPS:-5} --seed $SEED || echo "!! $name failed"
    done ;;
esac
