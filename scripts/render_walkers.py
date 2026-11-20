"""Presentation renders of the Stage 0 walkers (presentation_export/01_walkers).

    python scripts/render_walkers.py --task QuadCoop-Walker-AnymalC --checkpoint logs/evals/walker-anymal-v1/model.pt \
        --name anymal --out logs/evals/pres-walkers

Two kinds of clip, all 1920x1080, 8x multisampling, H.264 CRF 16 (preset slow), no debug markers:

fleet   the training environment (training config: command resampling, pushes, object episodes, resets) with
        --num-envs robots on their grid, every robot drawn in one frame (each env's moving geoms added to one
        scene, as mjlab's viewer draws its neighbours, but all of them):
          <name>_fleet_corner.mp4    fixed camera above the grid's top-right corner, looking across the whole grid
          <name>_fleet_flyover.mp4   a lower camera gliding over the grid in a slow S, so every row passes close by
single  one robot, the evaluation conditions of scripts/eval_walker.py (validate_walker.make_cfg), a free camera
        that follows the robot (and the object it pushes) from a fixed three-quarter angle:
          <name>_walk_forward.mp4          0.5 m/s straight ahead
          <name>_resist_push.mp4           0.5 m/s against a constant 25% body-weight push
          <name>_push_cube_30kg.mp4        0.4 m/s into a 30 kg cube, straight ahead
          <name>_push_cube_30kg_side.mp4   0.4 m/s into a 30 kg cube, sideways (90 deg)
The policy is the walker's own (deterministic actor output). Models are rebuilt with the walker's env vars
(scripts/methods.py env --id <id>, which the job sets).
"""
from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import numpy as np  # noqa: E402
import torch  # noqa: E402

import quadcoop  # noqa: E402,F401  (registers tasks)

W, H = 1920, 1080


def writer(path: Path, fps: float):
    import imageio_ffmpeg

    path.parent.mkdir(parents=True, exist_ok=True)
    wr = imageio_ffmpeg.write_frames(str(path), (W, H), fps=fps, ffmpeg_log_level="error", quality=None,
                                     macro_block_size=8, output_params=["-crf", "16", "-preset", "slow"])
    wr.send(None)
    return wr


def make_renderer(m, max_geom: int):
    import mujoco

    m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), W)
    m.vis.global_.offheight = max(int(m.vis.global_.offheight), H)
    m.vis.quality.offsamples = 8
    m.vis.quality.shadowsize = 8192
    m.vis.global_.fovy = 45.0
    return mujoco.Renderer(m, height=H, width=W, max_geom=max_geom)


def env_and_policy(task: str, cfg, checkpoint: str, device: str):
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.rl import RslRlVecEnvWrapper

    import validate_walker as vw

    base = ManagerBasedRlEnv(cfg=cfg, device=device)
    env = RslRlVecEnvWrapper(base)
    policy = vw.load_policy(env, task, checkpoint, device)
    return base, env, policy


@torch.no_grad()
def fleet(a, device: str) -> None:
    import mujoco
    from mjlab.tasks.registry import load_env_cfg

    cfg = load_env_cfg(a.task, play=False)  # the training environment
    cfg.scene.num_envs = a.num_envs
    base, env, policy = env_and_policy(a.task, cfg, a.checkpoint, device)
    m = base.sim.mj_model
    d = mujoco.MjData(m)
    r = make_renderer(m, max_geom=200 * a.num_envs + 2000)
    opt, pert = mujoco.MjvOption(), mujoco.MjvPerturb()
    origins = base.scene.env_origins.cpu().numpy()
    lo, hi = origins[:, :2].min(0), origins[:, :2].max(0)
    c = 0.5 * (lo + hi)
    span = float(max(hi - lo)) + 4.0
    print(f"[fleet] {a.name}: {a.num_envs} envs, grid {lo.round(1)} .. {hi.round(1)} (span {span:.1f} m)", flush=True)

    corner = mujoco.MjvCamera()
    corner.type = mujoco.mjtCamera.mjCAMERA_FREE
    # above the top-right corner (+x, +y), looking back across the grid toward the far corner
    corner.lookat[:] = [c[0] - 0.05 * span, c[1] - 0.05 * span, 0.0]
    corner.azimuth, corner.elevation, corner.distance = 225.0, -24.0, 0.95 * span
    fly = mujoco.MjvCamera()
    fly.type = mujoco.mjtCamera.mjCAMERA_FREE
    fly.azimuth, fly.elevation, fly.distance = 90.0, -32.0, 11.0

    steps = int(a.seconds / base.step_dt)
    stride = 2
    fps = 1.0 / (stride * base.step_dt)
    out = Path(a.out)
    w_corner = writer(out / f"{a.name}_fleet_corner.mp4", fps)
    w_fly = writer(out / f"{a.name}_fleet_flyover.mp4", fps)
    obs = env.get_observations()
    n_frames = steps // stride
    margin = 0.12 * (hi[1] - lo[1])

    def draw(cam) -> bytes:
        q = base.sim.data.qpos.cpu().numpy()
        mp = base.sim.data.mocap_pos.cpu().numpy() if m.nmocap else None
        mq = base.sim.data.mocap_quat.cpu().numpy() if m.nmocap else None
        for i in range(base.num_envs):
            d.qpos[:] = q[i]
            if m.nmocap:
                d.mocap_pos[:], d.mocap_quat[:] = mp[i], mq[i]
            mujoco.mj_forward(m, d)
            if i == 0:
                r.update_scene(d, camera=cam)
            else:
                mujoco.mjv_addGeoms(m, d, opt, pert, mujoco.mjtCatBit.mjCAT_DYNAMIC.value, r.scene)
        return r.render().tobytes()

    for f in range(n_frames):
        for _ in range(stride):
            obs, _, _, _ = env.step(policy(obs))
        u = f / max(n_frames - 1, 1)
        # slow S over the grid: across the rows from the near edge to the far edge, sweeping side to side
        fly.lookat[:] = [c[0] + 0.38 * (hi[0] - lo[0]) * math.sin(2.0 * math.pi * 1.5 * u),
                         lo[1] + margin + (hi[1] - lo[1] - 2 * margin) * u, 0.3]
        w_corner.send(draw(corner))
        w_fly.send(draw(fly))
        if f % 100 == 0:
            print(f"[fleet] {a.name}: frame {f}/{n_frames}", flush=True)
    w_corner.close()
    w_fly.close()
    base.close()


@torch.no_grad()
def single(a, device: str) -> None:
    import mujoco

    import validate_walker as vw

    clips = [("walk_forward", "A", {}), ("resist_push", "B", {}),
             ("push_cube_30kg", "C", {"object": "obj_cube", "obj_mass": 30.0, "push_bearing": 0.0}),
             ("push_cube_30kg_side", "C", {"object": "obj_cube", "obj_mass": 30.0, "push_bearing": 90.0})]
    for clip, test, extra in clips:
        args = SimpleNamespace(checkpoint=a.checkpoint, num_envs=1, seconds=a.single_seconds, force_frac=0.25,
                               obj_mass=15.0, object="obj_cube", seed=0, push_bearing=0.0)
        for k, v in extra.items():
            setattr(args, k, v)
        torch.manual_seed(0)
        cfg = vw.make_cfg(a.task, test, args)
        base, env, policy = env_and_policy(a.task, cfg, a.checkpoint, device)
        m = base.sim.mj_model
        d = mujoco.MjData(m)
        r = make_renderer(m, max_geom=4000)
        cam = mujoco.MjvCamera()
        cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        robot = base.scene["robot"]
        obj = base.scene[args.object] if test == "C" else None
        q = robot.data.root_link_quat_w[0].cpu().numpy()
        yaw0 = math.degrees(math.atan2(2 * (q[0] * q[3] + q[1] * q[2]), 1 - 2 * (q[2] ** 2 + q[3] ** 2)))
        # front three-quarter view from the robot's right; the pushing clips look a little more from the side
        cam.azimuth = yaw0 + (150.0 if test != "C" else 120.0 + args.push_bearing)
        cam.elevation, cam.distance = -22.0, 3.8 if test != "C" else 4.4
        stride = 2
        fps = 1.0 / (stride * base.step_dt)
        wr = writer(Path(a.out) / f"{a.name}_{clip}.mp4", fps)
        obs = env.get_observations()
        look = None
        for f in range(int(a.single_seconds / base.step_dt) // stride):
            for _ in range(stride):
                obs, _, _, _ = env.step(policy(obs))
            p = robot.data.root_link_pos_w[0, :2].cpu().numpy()
            if obj is not None:
                p = 0.5 * (p + obj.data.root_link_pos_w[0, :2].cpu().numpy())
            look = p if look is None else 0.85 * look + 0.15 * p
            cam.lookat[:] = [look[0], look[1], 0.35]
            d.qpos[:] = base.sim.data.qpos[0].cpu().numpy()
            if m.nmocap:
                d.mocap_pos[:] = base.sim.data.mocap_pos[0].cpu().numpy()
                d.mocap_quat[:] = base.sim.data.mocap_quat[0].cpu().numpy()
            mujoco.mj_forward(m, d)
            r.update_scene(d, camera=cam)
            wr.send(r.render().tobytes())
        wr.close()
        print(f"[single] {a.name}: {clip} done", flush=True)
        base.close()
        del env, base, policy


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--name", required=True, help="file prefix, e.g. anymal or spot")
    ap.add_argument("--out", required=True)
    ap.add_argument("--mode", choices=("fleet", "single", "all"), default="all")
    ap.add_argument("--num-envs", type=int, default=256)
    ap.add_argument("--seconds", type=float, default=40.0, help="fleet clips")
    ap.add_argument("--single-seconds", type=float, default=12.0)
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    if a.mode in ("fleet", "all"):
        fleet(a, device)
    if a.mode in ("single", "all"):
        single(a, device)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
