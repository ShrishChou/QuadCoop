"""Train Stage 1b (harder push-to-pose, ten shapes), usually warm-started from Stage 1.

    QUADCOOP_WALKER_CKPT=<walker.pt> python scripts/warmstart_push.py \\
        --task QuadCoop-PushHard-AnymalC --init <stage1 push model_N.pt>
    QUADCOOP_WALKER_CKPT=<walker.pt> python train_push_hard.py QuadCoop-PushHard-AnymalC \\
        --env.scene.num-envs 4096 --agent.resume True \\
        --agent.load-run 0000_warmstart --agent.load-checkpoint model_0.pt
"""

import quadcoop  # noqa: F401
import quadcoop.stage1  # noqa: F401
import quadcoop.stage1b  # noqa: F401
from mjlab.scripts.train import main

if __name__ == "__main__":
    main()