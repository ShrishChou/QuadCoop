"""Train a walker. Same CLI as mjlab's `train`, with our tasks registered.

    python train.py QuadCoop-Walker-AnymalC --env.scene.num-envs 4096
    python train.py QuadCoop-Walker-Spot    --env.scene.num-envs 4096

Resume an interrupted run (e.g. after the 6 h limit on mit_normal_gpu):

    python train.py QuadCoop-Walker-AnymalC --env.scene.num-envs 4096 \\
        --agent.resume True --agent.load-run <run-dir-name>

Logs and checkpoints land in logs/rsl_rl/walker_<robot>/<date>_<run-name>/.
"""

import quadcoop  # noqa: F401  (registers QuadCoop-* tasks)
from mjlab.scripts.train import main

if __name__ == "__main__":
    main()
