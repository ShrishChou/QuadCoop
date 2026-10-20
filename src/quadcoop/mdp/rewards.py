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


def velocity_progress(env: ManagerBasedRlEnv, command_name: str) -> torch.Tensor:
    """Fraction of the commanded speed actually achieved along the commanded direction.

    Linear, so standing still earns 0 and full speed earns 1 (clipped at 1: going faster
    than told is not rewarded). The stock exp(-err^2/0.25) tracking term pays a robot
    that stands still against a 0.2-0.4 m/s command 50-85% of full reward, which made
    "brace and stand" a near-optimal answer to the push force.
    """
    robot = env.scene["robot"]
    cmd = env.command_manager.get_command(command_name)[:, :2]
    speed = torch.linalg.norm(cmd, dim=-1)
    v_b = robot.data.root_link_lin_vel_b[:, :2]
    frac = (v_b * cmd).sum(-1) / speed.clamp(min=1e-3).square()
    return torch.where(speed > 0.1, frac.clamp(0.0, 1.0), torch.zeros_like(frac))


def base_smoothness(env: ManagerBasedRlEnv, std_vz: float = 0.1, std_wxy: float = 0.5) -> torch.Tensor:
    """1 when the base (most of the robot's mass, so a proxy for the COM) moves smoothly.

    Falls off with vertical bobbing (m/s) and roll/pitch rate (rad/s):
        exp(-(v_z / std_vz)^2 - |w_xy|^2 / std_wxy^2)
    Yaw rate and forward/sideways speed are not penalized: those are commanded.
    """
    robot = env.scene["robot"]
    vz = robot.data.root_link_lin_vel_b[:, 2]
    wxy = robot.data.root_link_ang_vel_b[:, :2]
    return torch.exp(-(vz / std_vz).square() - wxy.square().sum(-1) / std_wxy**2)


def base_height(env: ManagerBasedRlEnv, target: float, std: float = 0.07) -> torch.Tensor:
    """1 at the nominal walking height, falling off as the body sags (or pops up)."""
    z = env.scene["robot"].data.root_link_pos_w[:, 2]  # flat ground at z = 0
    return torch.exp(-((z - target) / std).square())