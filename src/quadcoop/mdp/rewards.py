"""Reward for moving the object the way the robot was told to go."""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from mjlab.utils.lab_api.math import quat_apply, yaw_quat

if TYPE_CHECKING:
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.sensor import ContactSensor


def object_push_progress(
    env: ManagerBasedRlEnv,
    command_name: str,
    object_names: tuple[str, ...],
    sensor_names: tuple[str, ...],
) -> torch.Tensor:
    """While touching an object: its speed along the commanded direction / commanded speed.

    0 when not touching anything, so it never pays for standing still or for walking
    around an object; it pays for keeping contact and moving the object on the line
    the robot was told to follow. Clipped to [0, 1.5].
    """
    robot = env.scene["robot"]
    cmd = env.command_manager.get_command(command_name)  # body frame (vx, vy, wz)
    speed = torch.linalg.norm(cmd[:, :2], dim=-1)
    cmd_w = quat_apply(yaw_quat(robot.data.root_link_quat_w),
                       torch.cat([cmd[:, :2], torch.zeros_like(cmd[:, :1])], dim=-1))[:, :2]
    u = cmd_w / speed.clamp(min=1e-3).unsqueeze(-1)
    total = torch.zeros(env.num_envs, device=env.device)
    for obj, sname in zip(object_names, sensor_names, strict=True):
        sensor: ContactSensor = env.scene[sname]
        assert sensor.data.found is not None
        touching = torch.any(sensor.data.found > 0, dim=-1).float()
        v = env.scene[obj].data.root_link_lin_vel_w[:, :2]
        along = (v * u).sum(-1) / speed.clamp(min=0.1)
        total += touching * along.clamp(0.0, 1.5)
    return torch.where(speed > 0.1, total, torch.zeros_like(total))