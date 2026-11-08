"""Importing this package registers the Stage 0 walker tasks with mjlab.

    QuadCoop-Walker-AnymalC
    QuadCoop-Walker-Spot
    QuadCoop-Walker-AnymalC-Compliant   walker v2 (mdp/compliance.py): force sensing, compliant
                                        velocity target, small commands; logs under
                                        logs/rsl_rl/walker_anymal_c_compliant/
"""

from mjlab.tasks.registry import register_mjlab_task
from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner

from quadcoop.rl_cfg import walker_ppo_cfg
from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.walker_env_cfg import make_walker_env_cfg

TASKS = {
    "QuadCoop-Walker-AnymalC": ANYMAL_C,
    "QuadCoop-Walker-Spot": SPOT,
}

for _task_id, _robot in TASKS.items():
    register_mjlab_task(
        task_id=_task_id,
        env_cfg=make_walker_env_cfg(_robot),
        play_env_cfg=make_walker_env_cfg(_robot, play=True),
        rl_cfg=walker_ppo_cfg(_robot.name),
        runner_cls=VelocityOnPolicyRunner,
    )

register_mjlab_task(
    task_id="QuadCoop-Walker-AnymalC-Compliant",
    env_cfg=make_walker_env_cfg(ANYMAL_C, compliant=True),
    play_env_cfg=make_walker_env_cfg(ANYMAL_C, play=True, compliant=True),
    rl_cfg=walker_ppo_cfg(f"{ANYMAL_C.name}_compliant"),
    runner_cls=VelocityOnPolicyRunner,
)
