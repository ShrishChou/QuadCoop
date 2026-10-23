"""Stage 2: shape-aware goal guidance (single robot).

    QuadCoop-Push2a-{AnymalC,Spot}     + object-frame top and front profiles
    QuadCoop-Push2b-{AnymalC,Spot}     + robot-frame top map (10 Hz) and object-frame front profile
    QuadCoop-Push2ctrl-{AnymalC,Spot}  same task, Stage 1b's 42 inputs only (the control)

Experiments: logs/rsl_rl/push2{a,b,ctrl}_<robot>. Train with train_push2.py; warm start
from Stage 1b/1c with scripts/warmstart_push2.py (slurm/train_push2.sbatch does both).
"""

from mjlab.tasks.registry import register_mjlab_task

from quadcoop.robots.anymal_c import ROBOT as ANYMAL_C
from quadcoop.robots.spot import ROBOT as SPOT
from quadcoop.stage2.env_cfg import VARIANTS, make_push2_env_cfg
from quadcoop.stage2.rl_cfg import push2_ppo_cfg
from quadcoop.stage2.runner import Push2Runner

TASKS = {}
for _variant in VARIANTS:
    for _suffix, _robot in (("AnymalC", ANYMAL_C), ("Spot", SPOT)):
        _task = f"QuadCoop-Push2{_variant}-{_suffix}"
        TASKS[_task] = (_robot, _variant)
        register_mjlab_task(
            task_id=_task,
            env_cfg=make_push2_env_cfg(_robot, _variant),
            play_env_cfg=make_push2_env_cfg(_robot, _variant, play=True),
            rl_cfg=push2_ppo_cfg(_robot.name, _variant),
            runner_cls=Push2Runner,  # logs image-path usage (Loss/img_weight_ratio_*, Loss/cnn_change_*)
        )
