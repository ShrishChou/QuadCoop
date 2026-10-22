"""Stage 1c: the single-robot pushing task again, with the fixes from the Stage 1b eval.

    QuadCoop-PushHard2-AnymalC
    QuadCoop-PushHard2-Spot

Same observations, actions and network as Stage 1b, so a Stage 1b checkpoint is the
starting point as it is (no conversion). Run with QUADCOOP_SHAPES=v2.
"""

from mjlab.rl import MjlabOnPolicyRunner
from mjlab.tasks.registry import register_mjlab_task

from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.stage1c.env_cfg import make_v2_env_cfg
from quadcoop.stage1c.rl_cfg import v2_ppo_cfg

V2_TASKS = {
    "QuadCoop-PushHard2-AnymalC": ANYMAL_C,
    "QuadCoop-PushHard2-Spot": SPOT,
}

for _task_id, _robot in V2_TASKS.items():
    register_mjlab_task(
        task_id=_task_id,
        env_cfg=make_v2_env_cfg(_robot),
        play_env_cfg=make_v2_env_cfg(_robot, play=True),
        rl_cfg=v2_ppo_cfg(_robot.name),
        runner_cls=MjlabOnPolicyRunner,
    )
