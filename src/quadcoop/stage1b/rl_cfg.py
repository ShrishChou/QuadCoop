"""PPO for Stage 1b: same network as Stage 1 (so it can be warm-started), gentler LR."""

from __future__ import annotations

from quadcoop.stage1.rl_cfg import push_ppo_cfg


def hard_ppo_cfg(robot_name: str):
    cfg = push_ppo_cfg(robot_name)
    cfg.experiment_name = f"pushhard_{robot_name}"
    cfg.algorithm.learning_rate = 3.0e-4
    cfg.algorithm.entropy_coef = 0.004
    cfg.max_iterations = 8_000
    return cfg