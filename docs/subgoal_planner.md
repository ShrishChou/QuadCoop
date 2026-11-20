# Regret-minimizing planners

Two experiments that put a no-regret learner above the learned pushing behaviour.

## Step 1: the contact game (one-shot)

Each robot picks one of the object's contacts; both get the team outcome. `scripts/contact_game.py` builds the payoff
matrix per task (object x position x mass) from the payoff sweep `evals/game-hvB-allpairs` (the contact executor
hvB, iteration 13500, from every usable ordered contact pair; 40 and 80 kg; 3139 episodes) and compares:

* team optimum (best pair), pure Nash equilibria (including the worst: a miscoordination trap), the hand-made rules;
* two independent learners, one per robot, playing the game repeatedly with noisy payoffs: regret matching, RM+,
  Hedge (full information) and Exp3 (bandit feedback). In self-play their average joint play approaches a coarse
  correlated equilibrium; in a common-payoff game that equilibrium can still be a bad one, so the measure is how
  close they get to the optimum and how often they end on it.

`--split-reps` chooses on even placements and scores on odd ones (no selection bias from the noisy maximum).

    python scripts/contact_game.py --sweep evals/game-hvB-allpairs --split-reps --out evals/game-hvB-game

## Step 2: the subgoal planner (during the episode)

`src/quadcoop/coop2/subgoal.py`, run through `scripts/eval_coop2.py --subgoal`. The MAPPO pair
(`nwB_mappo_uniform_s0/model_5000`) is unchanged; the planner replaces the goal the pair *sees* with a moving
subgoal from a menu of six arms (direct = the true goal, straight, translate-first, rotate-first, arc left, arc
right; 1.5 m look-ahead, recomputed every step). Success is always scored on the true goal.

Every 2 s each episode picks an arm; the epoch pays its progress on the true goal in [0, 1] (0.75 = 0.25 m/s or
10 deg/s, a fall 0, success 1). The learner is Exp3 per context (distance bin x heading bin x stalled last epoch x
heavy), updated once per epoch from the importance-weighted mean payoff of that context's parallel episodes. The
"stalled" context is the stuck signal: an arm that keeps not paying in it loses weight and the pair is shown a
different move.

Training is regret minimization on training placements (seeds 1001-1003, the benchmark's objects and masses),
each pass continuing the previous state. Then on the benchmark (seed 7100, the 480 tasks of the 66% MAPPO result):

| run | what |
|---|---|
| `sg-fixed-<arm>-dev7100` | each arm alone; `direct` must reproduce the pair's 66%; the best one is the best fixed arm in hindsight |
| `sg-frozen-dev7100` | the trained planner, no exploration, no learning |
| `sg-online-dev7100` | the trained planner still learning (Exp3 as a no-regret learner on the test itself) |

    bash slurm/submit_subgoal.sh        # check -> train (3 passes) -> test; fixed arms in parallel

Per episode `episodes.csv` adds `sg_frac_<arm>` (share of time per arm), `sg_switches` and `sg_mean_payoff`;
`subgoal_planner.md` has per context the plays, mean payoff per arm, and the final and average strategies.

Checked on a toy (an object that moves and turns at arm-dependent rates; direct, translate and rotate alone never
finish): fixed straight / arcs 100 %, the others 0 %; Exp3 100 % from the first pass, rotate preferred near the goal
with a large heading error.
