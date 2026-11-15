# Three teams: ANYmal + ANYmal, Spot + Spot, ANYmal + Spot

Status (2026-11-14): queued overnight (`slurm/submit_three_teams.sh`). Uses the current Spot (no arm, QuadCoop's
`rai-falcon` walker). The Spot-arm version follows when its port exists (`docs/spot_arm.md`).

**Question.** How does a mixed team compare with the two same-robot teams, under IPPO and MAPPO, on the same tasks?
ANYmal is the stronger single pusher (51% alone on the ten objects, Spot 40%).

**Recipe, identical for every team and algorithm:**
1. From the two single-robot push policies: r7 reward, KL anchor 0.05, 3000 iterations (as `ippo_aa_kl_s0`).
2. Ten-object restart: level 4 held, 20–80 kg, 1000 more iterations (as `ippo_aa_kl_ten_s0`).
3. The 480 seed-7100 ten-object tasks, evaluated twice.

| team | IPPO | MAPPO |
|---|---|---|
| ANYmal + ANYmal | exists (`ippo_aa_kl_ten_s0`) | step 2 job 29136593; evals 29136594, 29136595 |
| ANYmal + Spot | step 1 job 29136577, step 2 29136578; evals 29136579, 29136580 | 29136581, 29136582; evals 29136583, 29136584 |
| Spot + Spot | 29136585, 29136586; evals 29136587, 29136588 | 29136589, 29136590; evals 29136591, 29136592 |

Baselines on the same tasks, two runs each: mixed frozen pair (29136596, 29136599), Spot frozen pair (29136597,
29136600), Spot alone (29136598, 29136601). ANYmal's baselines are in the presentation set.

Step 1 runs on `mit_preemptable` (about 5 h each; a requeued job resumes from its checkpoints). One seed per cell.

**Not included:** the contact planner for Spot teams. Its executor was trained for two ANYmals over about 15,000
iterations in several stages; a Spot or mixed executor is a separate multi-day chain.

**Reading rules.** A rerun flips about 15% of outcomes, so compare two-run means per task with intervals. Report by
mass: the mixed team's interesting cells are 60–80 kg, where one Spot is weakest.
