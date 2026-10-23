"""Train Stage 2 (shape-aware goal guidance).

    QUADCOOP_SHAPES=v2 QUADCOOP_WALKER_CKPT=<walker.pt> python train_push2.py QuadCoop-Push2a-AnymalC \\
        --env.scene.num-envs 4096 --agent.resume True --agent.load-run 0000_warmstart

slurm/train_push2.sbatch does the warm start and the resume.
"""

import os

os.environ.setdefault("QUADCOOP_SHAPES", "v2")

import quadcoop  # noqa: E402, F401
import quadcoop.stage1  # noqa: E402, F401
import quadcoop.stage1b  # noqa: E402, F401
import quadcoop.stage2  # noqa: E402, F401
from mjlab.scripts.train import main  # noqa: E402

if __name__ == "__main__":
    main()
