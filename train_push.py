"""Train the Stage 1 pushing policy on top of a frozen Stage 0 walker.

    QUADCOOP_WALKER_CKPT=logs/rsl_rl/walker_anymal_c/<run>/model_5999.pt \\
        python train_push.py QuadCoop-Push-AnymalC --env.scene.num-envs 4096

Logs and checkpoints: logs/rsl_rl/push_<robot>/<date>_<run-name>/.
"""

import quadcoop  # noqa: F401  (walker tasks)
import quadcoop.stage1  # noqa: F401  (push tasks)
from mjlab.scripts.train import main

if __name__ == "__main__":
    main()