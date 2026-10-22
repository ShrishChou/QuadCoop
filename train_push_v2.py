"""Train Stage 1c (single-robot pushing, fixed fall rule / masses / geometry).

    QUADCOOP_SHAPES=v2 QUADCOOP_WALKER_CKPT=<walker.pt> python train_push_v2.py \\
        QuadCoop-PushHard2-AnymalC --env.scene.num-envs 4096 --agent.resume True \\
        --agent.load-run 0000_warmstart --agent.load-checkpoint model_0.pt

slurm/train_push_v2.sbatch does the warm start (a copy of the newest Stage 1b
checkpoint) and the resume chain.
"""

import os

os.environ.setdefault("QUADCOOP_SHAPES", "v2")

import quadcoop  # noqa: E402, F401
import quadcoop.stage1  # noqa: E402, F401
import quadcoop.stage1b  # noqa: E402, F401
import quadcoop.stage1c  # noqa: E402, F401
from mjlab.scripts.train import main  # noqa: E402

if __name__ == "__main__":
    main()
