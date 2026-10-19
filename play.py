"""Watch a trained walker (box always placed in front). Needs a display or Viser.

    python play.py QuadCoop-Walker-AnymalC \\
        --checkpoint-file logs/rsl_rl/walker_anymal_c/<run>/model_5999.pt \\
        --viewer viser --num-envs 4

On Engaging, use Viser and forward its port over SSH (see README), or record a
video instead with --video True.
"""

import quadcoop  # noqa: F401  (registers QuadCoop-* tasks)
from mjlab.scripts.play import main

if __name__ == "__main__":
    main()
