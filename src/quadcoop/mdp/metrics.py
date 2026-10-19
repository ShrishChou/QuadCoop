"""Per-step metrics, logged as episode means (Episode_Metrics/<name> in W&B).

These answer "is the training environment doing what we think?" directly in the
logs, in physical units, instead of only through reward terms.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from mjlab.utils.lab_api.math import quat_apply_inverse

if TYPE_CHECKING:
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.sensor import ContactSensor


def object_contact(env: ManagerBasedRlEnv, sensor_names: tuple[str, ...]) -> torch.Tensor:
    """1 while any robot geom touches any object. Episode mean = fraction of time in contact."""
    touching = None
    for name in sensor_names:
        sensor: ContactSensor = env.scene[name]
        assert sensor.data.found is not None
        t = torch.any(sensor.data.found > 0, dim=-1)
        touching = t if touching is None else touching | t
    assert touching is not None
    return touching.float()


def velocity_error_xy(env: ManagerBasedRlEnv, command_name: str = "twist") -> torch.Tensor:
    """Planar velocity tracking error in m/s (body frame)."""
    robot = env.scene["robot"]
    cmd = env.command_manager.get_command(command_name)[:, :2]
    v_b = quat_apply_inverse(robot.data.root_link_quat_w, robot.data.root_link_lin_vel_w)[:, :2]
    return torch.linalg.norm(cmd - v_b, dim=-1)
