"""Place the box in the robot's path (or park it out of reach)."""

from __future__ import annotations

from typing import TYPE_CHECKING

import torch
from mjlab.envs.mdp.events import resolve_env_ids
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.utils.lab_api.math import quat_apply, quat_from_euler_xyz, yaw_quat

if TYPE_CHECKING:
    from mjlab.entity import Entity
    from mjlab.envs import ManagerBasedRlEnv

_ROBOT = SceneEntityCfg("robot")
_BOX = SceneEntityCfg("box")


def place_box_in_path(
    env: ManagerBasedRlEnv,
    env_ids: torch.Tensor | None,
    p_in_path: float,
    robot_half_length: float,
    box_half_size: tuple[float, float, float],
    gap_range: tuple[float, float] = (0.1, 1.0),
    lateral_range: tuple[float, float] = (-0.25, 0.25),
    yaw_jitter: float = 0.3,
    park_distance: float = 30.0,
    command_name: str = "twist",
    robot_cfg: SceneEntityCfg = _ROBOT,
    box_cfg: SceneEntityCfg = _BOX,
) -> None:
    """With prob ``p_in_path`` put the box ahead along the commanded direction.

    "Ahead" is the commanded planar velocity direction when the robot is told to
    move, otherwise its heading. The near face lands ``gap_range`` metres beyond
    the robot's front, offset sideways by ``lateral_range``. Envs that don't get
    the box have it parked ``park_distance`` away. Each env is its own MuJoCo
    world, so a parked box never interacts with anything.

    Used both at reset and as an interval event, so a robot meets several boxes
    per episode. At reset the command is the previous episode's (the command
    manager resets after reset events); that only perturbs the direction.
    """
    env_ids = resolve_env_ids(env, env_ids)
    n = len(env_ids)
    if n == 0:
        return
    dev = env.device
    robot: Entity = env.scene[robot_cfg.name]
    box: Entity = env.scene[box_cfg.name]

    # Read the root pose from qpos, not root_link_pos_w: that one comes from
    # forward kinematics, which is stale inside a reset event (reset_base has
    # just written qpos, but no forward pass has run yet).
    q_adr = robot.indexing.free_joint_q_adr
    qpos = robot.data.data.qpos[env_ids]
    root_pos = qpos[:, q_adr[0:3]]
    q_yaw = yaw_quat(qpos[:, q_adr[3:7]])

    twist = env.command_manager.get_command(command_name)[env_ids]
    vxy = twist[:, :2]
    moving = torch.linalg.norm(vxy, dim=-1) > 0.1
    angle = torch.where(moving, torch.atan2(vxy[:, 1], vxy[:, 0]), torch.zeros(n, device=dev))

    dist = (
        robot_half_length
        + box_half_size[0]
        + torch.empty(n, device=dev).uniform_(*gap_range)
    )
    lat = torch.empty(n, device=dev).uniform_(*lateral_range)
    offset_yaw = torch.stack(
        [
            dist * torch.cos(angle) - lat * torch.sin(angle),
            dist * torch.sin(angle) + lat * torch.cos(angle),
            torch.zeros(n, device=dev),
        ],
        dim=-1,
    )
    pos = root_pos + quat_apply(q_yaw, offset_yaw)
    pos[:, 2] = box_half_size[2] + 0.005

    in_path = torch.rand(n, device=dev) < p_in_path
    parked = root_pos + torch.tensor([park_distance, 0.0, 0.0], device=dev)
    parked[:, 2] = box_half_size[2] + 0.005
    pos = torch.where(in_path.unsqueeze(-1), pos, parked)

    # Face the robot, with some yaw so it doesn't always meet a flat face.
    robot_yaw = 2.0 * torch.atan2(q_yaw[:, 3], q_yaw[:, 0])
    box_yaw = robot_yaw + angle + torch.empty(n, device=dev).uniform_(-yaw_jitter, yaw_jitter)
    zeros = torch.zeros(n, device=dev)
    quat = quat_from_euler_xyz(zeros, zeros, box_yaw)

    state = torch.zeros(n, 13, device=dev)
    state[:, 0:3] = pos
    state[:, 3:7] = quat
    box.write_root_state_to_sim(state, env_ids)

