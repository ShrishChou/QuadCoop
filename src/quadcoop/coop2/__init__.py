"""Stages 3-4: ANYmal C + Spot push one Stage 2 object together (IPPO / MAPPO).

    env:      quadcoop.coop2.env_cfg.make_coop2_env_cfg   (Stage 2 task, two robots)
    task:     quadcoop.coop2.mdp
    trainer:  quadcoop.coop2.marl                         (train_coop2.py)

Each robot's actor starts as its Stage 2b policy (evals/models.yaml: push2b_anymal, push2b_spot)
with the partner inputs at zero weight, on its own frozen walker (walker_anymal, walker_spot).
The older Stage 1b-based two-robot code (quadcoop.coop, train_coop.py) is kept unchanged.
"""
