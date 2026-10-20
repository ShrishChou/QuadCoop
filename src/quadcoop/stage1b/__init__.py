"""Stage 1b tasks: harder push-to-pose with ten shapes.

    QuadCoop-PushHard-AnymalC
    QuadCoop-PushHard-Spot
"""

from mjlab.rl import MjlabOnPolicyRunner
from mjlab.tasks.registry import register_mjlab_task

from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.stage1b.env_cfg import make_hard_env_cfg
from quadcoop.stage1b.rl_cfg import hard_ppo_cfg

HARD_TASKS = {
    "QuadCoop-PushHard-AnymalC": ANYMAL_C,
    "QuadCoop-PushHard-Spot": SPOT,
}

for _task_id, _robot in HARD_TASKS.items():
    register_mjlab_task(
        task_id=_task_id,
        env_cfg=make_hard_env_cfg(_robot),
        play_env_cfg=make_hard_env_cfg(_robot, play=True),
        rl_cfg=hard_ppo_cfg(_robot.name),
        runner_cls=MjlabOnPolicyRunner,
    )