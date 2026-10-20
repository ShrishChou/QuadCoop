"""Watch / record Stage 1b. QUADCOOP_PUSH_LEVEL (0-5) and QUADCOOP_PUSH_OBJECT (e.g. arch).

    QUADCOOP_WALKER_CKPT=<walker.pt> QUADCOOP_PUSH_LEVEL=4 QUADCOOP_PUSH_OBJECT=arch \\
        python play_push_hard.py QuadCoop-PushHard-AnymalC --checkpoint-file <model.pt> --video True
"""

import quadcoop  # noqa: F401
import quadcoop.stage1  # noqa: F401
import quadcoop.stage1b  # noqa: F401
from mjlab.scripts.play import main

if __name__ == "__main__":
    main()