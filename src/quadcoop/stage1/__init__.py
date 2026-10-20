"""Stage 1 tasks: push a box to a goal pose with the frozen Stage 0 walker.

    QuadCoop-Push-AnymalC
    QuadCoop-Push-Spot

Importing this module registers them (``train_push.py`` / ``play_push.py`` do).
"""

from mjlab.rl import MjlabOnPolicyRunner
from mjlab.tasks.registry import register_mjlab_task

from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.stage1.push_env_cfg import make_push_env_cfg
from quadcoop.stage1.rl_cfg import push_ppo_cfg

PUSH_TASKS = {
    "QuadCoop-Push-AnymalC": ANYMAL_C,
    "QuadCoop-Push-Spot": SPOT,
}

for _task_id, _robot in PUSH_TASKS.items():
    register_mjlab_task(
        task_id=_task_id,
        env_cfg=make_push_env_cfg(_robot),
        play_env_cfg=make_push_env_cfg(_robot, play=True),
        rl_cfg=push_ppo_cfg(_robot.name),
        runner_cls=MjlabOnPolicyRunner,
    )