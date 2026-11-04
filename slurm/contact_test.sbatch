#!/bin/bash
# Scripted contacts (scripts/contact_test.py): hand-assigned contact rules on the pair-evaluation tasks.
# Stats -> evals/<PREFIX>-<rule>/eval/pair/ (one folder per rule), videos -> logs/evals/<PREFIX>-<rule>/pair/videos/.
#
#   sbatch slurm/contact_test.sbatch                                   # two ANYmal C, rules centre/adjacent/spread
#   PAIR=mixed sbatch slurm/contact_test.sbatch                        # ANYmal C + Spot
#   PREFIX=contact-aa-re4 ARGS="--reassign-s 4" sbatch slurm/contact_test.sbatch
#   ARGS="--executor policy" sbatch slurm/contact_test.sbatch                     # hand-off test -> handoff-aa-<rule>
#   PREFIX=handoff-aa-free ARGS="--executor policy --return-dist 0" sbatch slurm/contact_test.sbatch   # never pulled back
#   PREFIX=s4-aa-s0-it3000 ARGS="--executor stage4 --checkpoint logs/marl2/s4_aa_s0/model_3000.pt" RULES=spread,adjacent,random \
#     sbatch slurm/contact_test.sbatch                        # Stage 4 policy from assigned contacts
#   Stage 4d (guided reaching) - the same eval, then reaching from behind the object, with the object shoved:
#   PREFIX=s4d-aa-s0 ARGS="--executor stage4 --checkpoint logs/marl2/s4d_aa_s0/model_9000.pt" RULES=spread,adjacent,random \
#     sbatch slurm/contact_test.sbatch
#   PREFIX=s4d-aa-s0-reach ARGS="--executor stage4 --checkpoint logs/marl2/s4d_aa_s0/model_9000.pt --start behind \
#     --disturb-frac 0.5 --videos 0" RULES=spread sbatch slurm/contact_test.sbatch      # and the same with s4b's model_6000
#   Videos to look at (every object x scenario, rep 0, at 40 and 60 kg; contacts, push direction and waypoints
#   drawn in; browse eval_videos/<PREFIX>-<rule>/index.html, failures first):
#   PREFIX=vid-s4d RULES=spread MASSES=40,60 REPS=1 ARGS="--executor stage4 --checkpoint logs/marl2/s4d_aa_s0/model_9000.pt \
#     --video-masses 40,60 --video-scenarios all --video-objects all --video-dir eval_videos" sbatch slurm/contact_test.sbatch
#   Stage 4e: Step 0 (the 4d model with the wrench rule, contacts re-chosen down to the goal), then the 4e model:
#   PREFIX=step0-s4d ARGS="--executor stage4 --checkpoint logs/marl2/s4d_aa_s0/model_9000.pt --reselect-min-dist 0" \
#     RULES=wrench,spread sbatch slurm/contact_test.sbatch
#   PREFIX=s4e-aa-s0 ARGS="--executor stage4 --checkpoint logs/marl2/s4e_aa_s0/model_12000.pt" \
#     RULES=wrench,spread,adjacent,random sbatch slurm/contact_test.sbatch
#   Stage 5 payoff sweep (every usable contact pair; then python scripts/contact_game.py --sweep evals/game-s4b-allpairs):
#   for m in 40 70; do MASSES=$m RULES=allpairs PREFIX=game-s4b \
#     ARGS="--executor stage4 --checkpoint logs/marl2/s4b_aa_s0/model_6000.pt --videos 0" sbatch slurm/contact_test.sbatch; done
#   larger sweep (12 placements per ordered pair; jobs split by object, all merge into one result):
#   for m in 40 70; do for objs in arch,dumbbell beam,t_shape u_channel,l_shape,plus; do MASSES=$m RULES=allpairs REPS=12 \
#     PREFIX=game12-s4b ARGS="--executor stage4 --checkpoint logs/marl2/s4b_aa_s0/model_6000.pt --videos 0 --objects $objs" \
#     sbatch slurm/contact_test.sbatch; done; done
# Masses can be split over jobs with the same PREFIX: each job merges its masses into the same results, and
# results are saved after every mass (a job that hits the time limit keeps the masses it finished), e.g.
#   for m in 40 60 80; do MASSES=$m PREFIX=handoff-aa-free ARGS="--executor policy --return-dist 0" sbatch slurm/contact_test.sbatch; done
# Optional: PAIR (anymal), PREFIX (contact-<aa|mx|ss>), RULES (centre,adjacent,spread), MASSES (20,40,60,80),
# REPS (3), ARGS (more contact_test.py args).
#SBATCH -J qc-contact
#SBATCH -p mit_normal_gpu,mit_preemptable
#SBATCH -G 1
#SBATCH -c 8
#SBATCH --mem=64G
#SBATCH -t 06:00:00
#SBATCH --requeue
#SBATCH -o logs/slurm/%x-%j.out
set -euo pipefail
cd "$SLURM_SUBMIT_DIR"
source .venv/bin/activate
export MUJOCO_GL=egl
EXTRA=()
if [[ -n "${PREFIX:-}" ]]; then EXTRA+=(--prefix "$PREFIX"); fi
python scripts/contact_test.py --pair "${PAIR:-anymal}" --rules "${RULES:-centre,adjacent,spread}" \
  --masses "${MASSES:-20,40,60,80}" --reps "${REPS:-3}" "${EXTRA[@]}" ${ARGS:-}
