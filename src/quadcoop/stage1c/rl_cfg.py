"""PPO for Stage 1c: Stage 1b's settings, its own experiment folder."""

from __future__ import annotations

from quadcoop.stage1b.rl_cfg import hard_ppo_cfg


def v2_ppo_cfg(robot_name: str):
    cfg = hard_ppo_cfg(robot_name)
    cfg.experiment_name = f"pushhard2_{robot_name}"
    cfg.max_iterations = 4_000
    return cfg
