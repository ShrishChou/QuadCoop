#!/bin/bash
# Stages 3-4: ANYmal C + Spot push one Stage 2 object together (train_coop2.py).
# Models from evals/models.yaml. A job continues its run if it has checkpoints (so a requeued or
# resubmitted job picks up where it stopped) and stops at ITERS total.
#
#   ALGO=mappo SEED=0 sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   ALGO=ippo  SEED=0 sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   slurm/submit_coop2_first.sh       # both, plus the baseline evaluations and the final evaluations
#   Stage 4 (push from assigned contacts, two ANYmal C, success tolerance curriculum):
#   ALGO=mappo SEED=0 RUN_NAME=s4_aa_s0 EXTRA="--pair anymal --partner-map --reward r7 --contacts --kl-ref 0.05 \
#     --kl-ramp 1000 --need-frac 0.5 --critic-warmup 500 --max-actor-lr 1e-4" \
#     sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Stage 4b (contacts re-chosen every 3-6 s, 30% random starts), continuing a Stage 4 run: copy its last
#   checkpoint into logs/marl2/s4b_aa_s0/ first, then
#   ALGO=mappo SEED=0 RUN_NAME=s4b_aa_s0 ITERS=6000 EXTRA="--pair anymal --partner-map --reward r7 --contacts \
#     --reselect-s 3,6 --random-start 0.3 --need-frac 0.5 --max-actor-lr 1e-4" \
#     sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Stage 4c (no deadlines, no ending for being off contact: pulled to the contact, cost per second off it;
#   train_coop2.py's default --off-contact soft), continuing Stage 4b: copy its model_6000.pt into
#   logs/marl2/s4c_aa_s0/ first, then
#   ALGO=mappo SEED=0 RUN_NAME=s4c_aa_s0 ITERS=9000 EXTRA="--pair anymal --partner-map --reward r7 --contacts \
#     --reselect-s 3,6 --random-start 0.3 --need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 100" \
#     sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Stage 4d (guided reaching: route inputs, route-length pull, bump cost, scripted object motion), from Stage 4b's
#   model (its networks are expanded for the 6 new inputs; a requeued job continues from its own checkpoints):
#   ALGO=mappo SEED=0 RUN_NAME=s4d_aa_s0 ITERS=9000 EXTRA="--pair anymal --partner-map --reward r7 --contacts --guide \
#     --disturb-frac 0.2 --reselect-s 3,6 --random-start 0.3 --need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 100 \
#     --init-from logs/marl2/s4b_aa_s0/model_6000.pt" sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Stage 4e (a push direction per robot recomputed every step, the wrench contact rule, pose_progress /
#   motion_credit / walk_cost rewards, partner-aware route), from Stage 4d's model (4 more inputs per robot):
#   ALGO=mappo SEED=0 RUN_NAME=s4e_aa_s0 ITERS=12000 EXTRA="--pair anymal --partner-map --reward r7 --contacts --guide \
#     --push-cmd --contact-mix wrench:2,spread:1,random:1 --reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 \
#     --disturb-frac 0.2 --reselect-s 3,6 --random-start 0.5 --need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 300 \
#     --init-from logs/marl2/s4d_aa_s0/model_9000.pt" sbatch -p mit_preemptable --requeue -t 2-00:00:00 slurm/train_coop2.sbatch
#   Phase 2 executor v2 (a phase command walk / hold / push and the team-ready flag, 4 more inputs per robot; motion
#   credit only when told to push, hold_cost while told to hold; commands from the expert planner and the barrier,
#   random holds on 30% of arrivals), from Stage 4e's model. ITERS is the iteration to stop at (4e ends at 12000):
#   first a 200-iteration trial (throughput, every reward term moving), then the full run (8000 more):
#   ALGO=mappo SEED=0 RUN_NAME=ex2_trial ITERS=12200 EXTRA="--pair anymal --partner-map --reward r7 --contacts --guide \
#     --push-cmd --exec-v2 --hold-rand 0.3 --contact-mix wrench:1,spread:1,random:1,expert:2 --reselect-min-dist 0 \
#     --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 --reselect-s 3,6 --random-start 0.5 --need-frac 0.5 \
#     --max-actor-lr 1e-4 --critic-warmup-resume 300 --init-from logs/marl2/s4e_aa_s0/model_12000.pt" \
#     sbatch -p mit_preemptable --requeue -t 0-04:00:00 slurm/train_coop2.sbatch
#   ALGO=mappo SEED=0 RUN_NAME=ex2_aa_s0 ITERS=20000 EXTRA="<the same>" sbatch -p mit_preemptable --requeue \
#     -t 2-00:00:00 slurm/train_coop2.sbatch
#   Hovering test, both from Stage 4e's model, 1500 more iterations each (about 4-5 h; mit_normal_gpu, 6 h):
#   A: Stage 4e's reward without bump_cost, motion credit only while pressing 30 N or more;
#   B: minimal reward (progress x2, success, failure, falls, contact approach, contact work):
#   S4E="--pair anymal --partner-map --contacts --guide --push-cmd --contact-mix wrench:2,spread:1,random:1 \
#     --reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 --reselect-s 3,6 --random-start 0.5 \
#     --need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 300 --init-from logs/marl2/s4e_aa_s0/model_12000.pt"
#   ALGO=mappo SEED=0 RUN_NAME=hvA_aa_s0 ITERS=13500 EXTRA="$S4E --reward r7 --bump-cost 0 --credit-press 30" \
#     sbatch -p mit_normal_gpu -t 06:00:00 slurm/train_coop2.sbatch
#   ALGO=mappo SEED=0 RUN_NAME=hvB_aa_s0 ITERS=13500 EXTRA="$S4E --reward rmin" \
#     sbatch -p mit_normal_gpu -t 06:00:00 slurm/train_coop2.sbatch
#   turn_debug: the minimal-reward run (hvB) with turn practice - 30% of episodes are a turn in place (goal within
#   0.3 m, heading off 15-90 deg either way); same settings otherwise, 1500 more iterations from hvB's kept model.
#   wandb: turn-in-place success = Metrics turn_success / turn_task. Evaluate with contact_test.py --tasks turn.
#   ALGO=mappo SEED=0 RUN_NAME=turn_debug ITERS=15000 EXTRA="--pair anymal --partner-map --contacts --guide --push-cmd \
#     --contact-mix wrench:2,spread:1,random:1 --reselect-min-dist 0 --drift-dist 0.25 --drift-heading 30 --disturb-frac 0.2 \
#     --reselect-s 3,6 --random-start 0.5 --need-frac 0.5 --max-actor-lr 1e-4 --critic-warmup-resume 300 --reward rmin \
#     --turn-frac 0.3 --init-from logs/keep/marl2/hvB_aa_s0/model_13500.pt" sbatch -p mit_normal_gpu -t 06:00:00 slurm/train_coop2.sbatch
# Optional: VARIANT (b|ctrl), ITERS (3000), NUM_ENVS (4096), LOGGER (wandb|tensorboard), RUN_NAME,
# EXTRA (more train_coop2.py args).
#SBATCH -J qc-coop2
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
ALGO=${ALGO:?set ALGO=mappo or ippo}
SEED=${SEED:-0}
VARIANT=${VARIANT:-b}
SUFFIX=""
if [[ "$VARIANT" == ctrl ]]; then SUFFIX=_ctrl; fi
RUN=${RUN_NAME:-${ALGO}${SUFFIX}_s${SEED}}
echo "run $RUN: $ALGO, variant $VARIANT, seed $SEED, to ${ITERS:-3000} iterations"
nvidia-smi --query-gpu=name,memory.total --format=csv
python train_coop2.py --algo "$ALGO" --variant "$VARIANT" --seed "$SEED" --run-name "$RUN" --resume \
    --num-envs "${NUM_ENVS:-4096}" --max-iterations "${ITERS:-3000}" --logger "${LOGGER:-wandb}" ${EXTRA:-}
