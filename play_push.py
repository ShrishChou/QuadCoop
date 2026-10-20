"""Watch / record the pushing policy. The goal is the green area on the floor.

    QUADCOOP_WALKER_CKPT=<walker model_N.pt> QUADCOOP_PUSH_LEVEL=2 \\
        python play_push.py QuadCoop-Push-AnymalC --checkpoint-file <push model_N.pt> \\
        --viewer viser --num-envs 4          # or --video True on a cluster node

Without --checkpoint-file it runs the high-level policy untrained (to check the scene).
"""

import quadcoop  # noqa: F401
import quadcoop.stage1  # noqa: F401
from mjlab.scripts.play import main

if __name__ == "__main__":
    main()