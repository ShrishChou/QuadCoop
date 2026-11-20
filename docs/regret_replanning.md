# Regret minimization in the contact planner's re-planning

The expert planner (rule 4, `CoopPush2Command._propose_expert`) re-plans about 9 times per episode (timer 3-6 s, no
progress, weak pair, finishing, slow arrival). At each re-plan it prices every contact pair with a model-based cost
J = force-model residual + time weight x slower robot's arrival + stop weight x robots that stop pushing, and switches
to the cheapest if it beats the current pair by a margin.

`RegretCoordinator` (`src/quadcoop/coop2/coord.py`, `contact_test.py --coordinator regret`) keeps that schedule and
those triggers and replaces only the final choice: Exp3 picks one of

| option | pair |
|---|---|
| expert | the expert's own decision (margin and finishing-zone rules included) |
| keep | the current pair |
| second | the cheapest pair other than the expert's and the current |
| third | the next cheapest |

per context = object x heavy (> 50 kg) x re-plan triggered by a stall x finishing zone. The payoff of a decision is
settled at that episode's next re-plan (or its end): pose-error progress rate mapped to [0, 1] (0.5 + 0.25 x rate /
0.1 m/s, clipped), failure 0, success 1. Updates are importance-weighted per context (Exp3, gamma 0.1, eta 0.1).
Because the expert's pick is one of the options, the learner can only move away from it where the outcomes say
another ranked option does better: where the force model's ranking is wrong.

    sbatch chain: slurm/regret_replan.sbatch (check -> 3 training passes, seeds 1001-1003, 20-80 kg ->
    test on seed 7100: expert alone, frozen regret, online regret; 12 objects x 4 positions x 5 trials x 20-80 kg)

Outputs: `evals/rr-test-{base,frozen,online}-expert/` (success tables), `logs/evals/rr-state/*.pt|.md` (learner state
and per-context payoff per option). The log prints, per mass, how often each option was chosen and the share of
decisions that differ from the expert.
