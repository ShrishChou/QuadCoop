"""Spot-arm pushing walker: RAI's released whole-body walker fine-tuned with ANYmal walker v1's push curriculum.

Why (docs/spot_arm.md, step 2): RAI's walker tracks velocity but gives way under load. No constant command moved a
40 kg box 0.2 m, so every Spot-arm pusher above 20 kg failed. ANYmal's walker (v1) was trained to push through
objects; this task gives RAI's network the same training.

Recipe = walker v1 (walker_env_cfg.make_walker_env_cfg, unchanged): push episodes with objects put on the line of
travel, free-walk episodes, the object push-progress reward, the mass curriculum gated on falls and tracking.
Differences, all needed to keep RAI's network as it is:

* Actor input = RAI's 84 numbers in RAI's order (spot_arm.RaiWalker): body-frame linear and angular velocity,
  projected gravity, the 25-number command (base velocity from the twist command, arm targets, leg overrides 0,
  torso 0 / 0 / 0.52), 19 joint positions minus RAI's offsets and 19 joint velocities (Isaac order), the previous 12
  leg actions. No observation normalization (RAI's network takes raw inputs).
* Action = RAI's 12 leg outputs (Isaac order) -> leg targets = action x 0.2 + RAI's leg offsets; arm joints follow
  the arm command below. Same network shape (84 -> 512 -> 256 -> 128 -> 12, ELU), started from RAI's weights.
* Arm command: the pusher moves the arm, so the walker practises with it moving. Per env, every 2-6 s a new arm goal:
  stowed (40%), RAI's "out" pose (20%), or a random pose (40%) in the range the capability test used (shoulder yaw
  +-0.4, shoulder pitch -2.6..-0.3, elbow 0.5..2.9, wrist pitch -1.5..0.8); targets move at most 1.5 rad/s (the pair
  env's arm rate limit). The arm targets are part of the command the walker sees, as in RAI's interface.
* Foot sites are the model's own site_<leg> (at the foot sphere centre); the pose reward covers the leg joints only.
* Critic: the actor's inputs plus the stock foot terms (air time, contact, contact forces, foot height), normalized.

Training (spot_arm_walker_runner): the actor's first QUADCOOP_CRITIC_WARMUP iterations (default 100) are frozen so
the fresh critic learns RAI's behaviour before the policy moves; the learning rate is held at its start value during
that time. Std starts at 0.25 (action units; 0.05 rad).

Defaults differing from v1 (each an env var as in walker_env_cfg): warm-up QUADCOOP_WARMUP_ITERS 100 (v1 1000: it
learned to walk first), object ramp QUADCOOP_OBJ_RAMP 500 (v1 1500), masses QUADCOOP_OBJ_MASS "5,40" (v1 "5,30").

Use in the pair env: QUADCOOP_SPOT_ARM_WALKER=<model_N.pt> makes spot_arm.RaiWalker load this actor.
"""
from __future__ import annotations

import dataclasses
import os
from dataclasses import dataclass

import torch
from mjlab.envs import ManagerBasedRlEnv
from mjlab.envs import mdp as envs_mdp
from mjlab.envs.mdp.actions import JointPositionActionCfg
from mjlab.managers.action_manager import ActionTerm, ActionTermCfg
from mjlab.managers.observation_manager import ObservationGroupCfg, ObservationTermCfg
from mjlab.managers.scene_entity_config import SceneEntityCfg
from mjlab.tasks.velocity import mdp
from mjlab.utils.noise import UniformNoiseCfg as Unoise

from quadcoop.robots import spot_arm as sa

FOOT_SITES = ("site_front_left", "site_front_right", "site_rear_left", "site_rear_right")
ARM_RAND_LO = (-0.4, -2.6, 0.5, 0.0, -1.5, 0.0, 0.0)
ARM_RAND_HI = (0.4, -0.3, 2.9, 0.0, 0.8, 0.0, 0.0)
ARM_OUT_7 = tuple(sa.ARM_OUT)
ARM_STOW_7 = tuple(sa.ARM_STOWED)


def _setdefault_env(name: str, value: str) -> None:
    os.environ.setdefault(name, value)


class RaiLegAction(ActionTerm):
    """12 RAI leg outputs (Isaac order) -> 19 joint targets (legs from the policy, arm from the arm schedule)."""

    cfg: RaiLegActionCfg

    def __init__(self, cfg: RaiLegActionCfg, env: ManagerBasedRlEnv):
        super().__init__(cfg, env)
        self.robot = env.scene[cfg.entity_name]
        assert tuple(self.robot.joint_names) == sa.JOINTS, self.robot.joint_names
        self._joint = JointPositionActionCfg(entity_name=cfg.entity_name, actuator_names=(".*",), scale=1.0,
                                             use_default_offset=False).build(env)
        C = sa._constants()
        n, dev = self.num_envs, self.device
        self.i2m = torch.tensor(C["ISAAC_TO_MUJOCO_INDICES_12"], device=dev)
        self.m2i = torch.tensor(C["MUJOCO_TO_ISAAC_INDICES_19"], device=dev)
        self.joff = torch.tensor(C["LOCOMOTION_DEFAULT_JOINTS_OFFSET"], device=dev, dtype=torch.float32)
        self.loff = torch.tensor(C["LOCOMOTION_DEFAULT_LEGS_OFFSET"], device=dev, dtype=torch.float32)
        self._raw = torch.zeros(n, 12, device=dev)
        self.stow = torch.tensor(ARM_STOW_7, device=dev)
        self.out = torch.tensor(ARM_OUT_7, device=dev)
        self.rlo = torch.tensor(ARM_RAND_LO, device=dev)
        self.rhi = torch.tensor(ARM_RAND_HI, device=dev)
        self.arm_goal = self.stow.repeat(n, 1)
        self.arm_target = self.stow.repeat(n, 1)
        self.arm_timer = torch.zeros(n, device=dev)
        self.torso_default = torch.tensor([0.0, 0.0, sa.STAND_HEIGHT_CMD], device=dev)
        self.torso = self.torso_default.repeat(n, 1)  # commanded roll, pitch, height (posture variant: sampled)

    @property
    def action_dim(self) -> int:
        return 12

    @property
    def raw_action(self) -> torch.Tensor:
        return self._raw

    def _new_goals(self, ids: torch.Tensor) -> None:
        m = ids.numel()
        if m == 0:
            return
        u = torch.rand(m, device=self.device)
        rnd = self.rlo + torch.rand(m, 7, device=self.device) * (self.rhi - self.rlo)
        goal = torch.where((u < self.cfg.p_stowed).unsqueeze(-1), self.stow.expand(m, 7),
                           torch.where((u < self.cfg.p_stowed + self.cfg.p_out).unsqueeze(-1), self.out.expand(m, 7), rnd))
        self.arm_goal[ids] = goal
        if self.cfg.torso_sample:  # posture variant: a new torso command with each arm goal (default 40%)
            keep = torch.rand(m, device=self.device) < self.cfg.p_torso_default
            h = self.cfg.torso_height[0] + torch.rand(m, device=self.device) * (self.cfg.torso_height[1] - self.cfg.torso_height[0])
            pt = (2 * torch.rand(m, device=self.device) - 1) * self.cfg.torso_pitch
            t = torch.stack([torch.zeros_like(h), pt, h], -1)
            self.torso[ids] = torch.where(keep.unsqueeze(-1), self.torso_default.expand(m, 3), t)
        lo, hi = self.cfg.hold_s
        self.arm_timer[ids] = lo + torch.rand(m, device=self.device) * (hi - lo)

    def command25(self) -> torch.Tensor:
        twist = self._env.command_manager.get_term(self.cfg.twist_name)
        return sa.RaiWalker.command(twist.command[:, :3], self.arm_target, self.torso)

    def process_actions(self, actions: torch.Tensor) -> None:
        self._raw[:] = actions
        dt = self._env.step_dt
        if self.cfg.move_arm:
            self.arm_timer -= dt
            self._new_goals(torch.nonzero(self.arm_timer <= 0.0).squeeze(-1))
        step = self.cfg.arm_rate * dt
        self.arm_target += torch.clamp(self.arm_goal - self.arm_target, -step, step)
        legs = actions[:, self.i2m] * 0.2 + self.loff[self.i2m]
        self._joint.process_actions(torch.cat([legs, self.arm_target], -1))

    def apply_actions(self) -> None:
        self._joint.apply_actions()

    def reset(self, env_ids: torch.Tensor | slice | None = None) -> None:
        self._joint.reset(env_ids)
        ids = torch.arange(self.num_envs, device=self.device) if env_ids is None or isinstance(env_ids, slice) \
            else torch.as_tensor(env_ids, device=self.device)
        self._raw[ids] = 0.0
        self.arm_goal[ids] = self.stow
        self.arm_target[ids] = self.stow
        self.torso[ids] = self.torso_default
        # first arm goal after a short stowed start (the robot is dropped at reset)
        self.arm_timer[ids] = 0.5 + torch.rand(ids.numel(), device=self.device) * 1.5


@dataclass(kw_only=True)
class RaiLegActionCfg(ActionTermCfg):
    twist_name: str = "twist"
    move_arm: bool = True
    p_stowed: float = 0.4
    p_out: float = 0.2
    hold_s: tuple[float, float] = (2.0, 6.0)
    arm_rate: float = 1.5
    # posture variant (push_ft_s2): torso commands sampled with each arm goal, and followed (torso_track reward)
    torso_sample: bool = False
    p_torso_default: float = 0.4
    torso_height: tuple[float, float] = (0.40, 0.55)
    torso_pitch: float = 0.2

    def build(self, env: ManagerBasedRlEnv) -> RaiLegAction:
        return RaiLegAction(self, env)


# -- RAI's observation, term by term (so each part can carry its own noise) -------------------------------------------
def _term(env) -> RaiLegAction:
    return env.action_manager.get_term("joint_pos")


def rai_lin_vel(env) -> torch.Tensor:
    return env.scene["robot"].data.root_link_lin_vel_b


def rai_ang_vel(env) -> torch.Tensor:
    return env.scene["robot"].data.root_link_ang_vel_b


def rai_gravity(env) -> torch.Tensor:
    return env.scene["robot"].data.projected_gravity_b


def rai_command(env) -> torch.Tensor:
    return _term(env).command25()


def rai_joint_pos(env) -> torch.Tensor:
    t = _term(env)
    return env.scene["robot"].data.joint_pos[:, t.m2i] - t.joff


def rai_joint_vel(env) -> torch.Tensor:
    t = _term(env)
    return env.scene["robot"].data.joint_vel[:, t.m2i]


def rai_prev_action(env) -> torch.Tensor:
    return _term(env).raw_action


def _rai_terms(noise: bool) -> dict:
    nz = (lambda lo: Unoise(n_min=-lo, n_max=lo)) if noise else (lambda lo: None)
    return {
        "rai_lin_vel": ObservationTermCfg(func=rai_lin_vel, noise=nz(0.1)),
        "rai_ang_vel": ObservationTermCfg(func=rai_ang_vel, noise=nz(0.1)),
        "rai_gravity": ObservationTermCfg(func=rai_gravity, noise=nz(0.03)),
        "rai_command": ObservationTermCfg(func=rai_command),
        "rai_joint_pos": ObservationTermCfg(func=rai_joint_pos, noise=nz(0.01)),
        "rai_joint_vel": ObservationTermCfg(func=rai_joint_vel, noise=nz(0.5)),
        "rai_prev_action": ObservationTermCfg(func=rai_prev_action),
    }


def torso_track(env, height_std: float = 0.05, tilt_std: float = 0.1) -> torch.Tensor:
    """1 with the base at the commanded height and roll / pitch, as ReLIC's tracking terms (projected gravity
    against the commanded attitude's: (sin pitch, -sin roll cos pitch, ..) for roll 0 is (sin pitch, 0))."""
    t = _term(env)
    d = env.scene["robot"].data
    h_err = (d.root_link_pos_w[:, 2] - t.torso[:, 2]) / height_std
    goal = torch.stack([torch.sin(t.torso[:, 1]), torch.zeros_like(t.torso[:, 1])], -1)
    g_err = torch.linalg.norm(d.projected_gravity_b[:, :2] - goal, dim=-1) / tilt_std
    return torch.exp(-(h_err.square() + g_err.square()))


def make_spot_arm_walker_env_cfg(play: bool = False, posture: bool = False):
    from quadcoop.walker_env_cfg import make_walker_env_cfg

    _setdefault_env("QUADCOOP_WARMUP_ITERS", "100")
    _setdefault_env("QUADCOOP_OBJ_RAMP", "500")
    _setdefault_env("QUADCOOP_OBJ_MASS", "5,40")
    robot = dataclasses.replace(sa.ROBOT, foot_sites=FOOT_SITES)
    cfg = make_walker_env_cfg(robot, play=play)

    cfg.actions = {"joint_pos": RaiLegActionCfg(entity_name="robot")}
    cfg.observations["actor"] = ObservationGroupCfg(terms=_rai_terms(noise=True), concatenate_terms=True,
                                                    enable_corruption=not play)
    critic = _rai_terms(noise=False)
    for name in ("foot_height", "foot_air_time", "foot_contact", "foot_contact_forces"):
        critic[name] = cfg.observations["critic"].terms[name]
    cfg.observations["critic"] = ObservationGroupCfg(terms=critic, concatenate_terms=True, enable_corruption=False)

    # stock terms that read the IMU / angular-momentum sensors of mjlab's own robots (this model has none)
    for name in ("body_ang_vel", "angular_momentum"):
        cfg.rewards.pop(name, None)
    legs = SceneEntityCfg("robot", joint_names=sa.LEG_JOINTS)
    cfg.rewards["pose"].params["asset_cfg"] = legs
    # feet: around RAI's 0.7 (the pair env's value), not v1's 0.6-1.2, so the push it learns is the one it gets
    cfg.events["foot_friction"].params["ranges"] = (0.6, 0.9)
    if posture:  # push_ft_s2: torso commands sampled and followed; the fixed 0.5 m height reward goes
        from mjlab.managers.reward_manager import RewardTermCfg
        cfg.actions["joint_pos"].torso_sample = True
        cfg.rewards.pop("base_height", None)
        cfg.rewards["torso_track"] = RewardTermCfg(func=torso_track, weight=2.0)
    return cfg


def spot_arm_walker_ppo_cfg():
    from quadcoop.rl_cfg import walker_ppo_cfg
    c = walker_ppo_cfg("spot_arm")
    c.actor.obs_normalization = False  # RAI's network takes raw inputs
    c.actor.distribution_cfg = {**c.actor.distribution_cfg, "init_std": 0.25}
    c.algorithm.learning_rate = 1.0e-4
    c.algorithm.desired_kl = 0.005
    c.algorithm.entropy_coef = 0.002
    c.max_iterations = 3000
    return c


# -- runner: start from RAI's weights; freeze the actor while the critic warms up ----------------------------------
def rai_actor_weights() -> dict[str, torch.Tensor]:
    import onnx
    from onnx import numpy_helper
    m = onnx.load(str(sa.JUDO / "judo/models/policies/spot_locomotion.onnx"))
    w = {t.name: torch.tensor(numpy_helper.to_array(t).copy()) for t in m.graph.initializer}
    return {f"mlp.{i}.{p}": w[f"actor.{i}.{p}"] for i in (0, 2, 4, 6) for p in ("weight", "bias")}


def make_runner_cls():
    from mjlab.tasks.velocity.rl import VelocityOnPolicyRunner

    class SpotArmWalkerRunner(VelocityOnPolicyRunner):
        def __init__(self, env, train_cfg, log_dir=None, device="cpu"):
            super().__init__(env, train_cfg, log_dir, device)
            actor = self.alg.actor
            missing = actor.load_state_dict(rai_actor_weights(), strict=False)
            assert not [k for k in missing.missing_keys if k.startswith("mlp.")], missing
            print("[spot_arm_walker] actor initialised from RAI's spot_locomotion.onnx", flush=True)
            self._warm = int(os.environ.get("QUADCOOP_CRITIC_WARMUP", "100"))
            self._n_upd = 0
            base_lr = self.alg.learning_rate
            update = self.alg.update

            def update_with_warmup(*args, **kwargs):
                frozen = self.current_learning_iteration < self._warm
                for p in self.alg.actor.parameters():
                    p.requires_grad_(not frozen)
                out = update(*args, **kwargs)
                if frozen:  # no adaptive-lr growth while the actor's KL is zero
                    self.alg.learning_rate = base_lr
                    for g in self.alg.optimizer.param_groups:
                        g["lr"] = base_lr
                for p in self.alg.actor.parameters():
                    p.requires_grad_(True)
                return out

            self.alg.update = update_with_warmup

    return SpotArmWalkerRunner
