"""PPO for Stage 2. Same MLP as Stage 1b (256-128-64); variants "a" and "b" put a small
convolutional encoder in front of it for each profile image (rsl_rl's CNNModel):

    top   (1 x 32 x 32) -> conv 5x5/2 (16) -> conv 3x3/2 (32) -> conv 3x3/2 (16) -> 4 x 4 x 16 = 256
    front (1 x 16 x 32) -> same layers                                          -> 2 x 4 x 16 = 128
    MLP input = [42 normalized numbers (critic: 45), 256, 128]

The first 42 (45) MLP inputs are Stage 1b's, in the same order, so a Stage 1b policy is
copied in with the image inputs at zero weight (scripts/warmstart_push2.py).
"""

from __future__ import annotations

from quadcoop.stage1b.rl_cfg import hard_ppo_cfg

CNN = {"output_channels": (16, 32, 16), "kernel_size": (5, 3, 3), "stride": 2, "padding": "zeros",
       "activation": "elu"}


def push2_ppo_cfg(robot_name: str, variant: str):
    cfg = hard_ppo_cfg(robot_name)
    cfg.experiment_name = f"push2{variant}_{robot_name}"
    cfg.max_iterations = 6_000
    cfg.algorithm.entropy_coef = 0.005
    if variant != "ctrl":
        for model in (cfg.actor, cfg.critic):
            model.class_name = "CNNModel"
            model.cnn_cfg = dict(CNN)
        cfg.obs_groups = {"actor": ("actor", "profile_top", "profile_front"),
                          "critic": ("critic", "profile_top", "profile_front")}
    return cfg
