"""Videos of the two-robot task: a camera that follows both robots, the object and the goal.

PairVideo films env 0 of a training run (as trained, stochastic actions) for ``length`` steps
into videos/iter_<N>.mp4. render_episode() turns recorded states of any env into an MP4 (the
evaluation records states while it runs and films chosen episodes afterwards). Rendering
failures (no EGL) switch videos off with a warning instead of stopping the run.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from quadcoop.coop2.mdp import AGENTS


class Camera:
    W, H = 640, 480

    def __init__(self, env, width: int | None = None, height: int | None = None):
        import mujoco

        from quadcoop.stage2.mdp import fix_render_frames

        self.W, self.H = width or self.W, height or self.H
        self.env = env
        fix_render_frames(env)
        m = env.sim.mj_model
        m.vis.global_.offwidth = max(int(m.vis.global_.offwidth), self.W)
        m.vis.global_.offheight = max(int(m.vis.global_.offheight), self.H)
        self.m, self.d = m, mujoco.MjData(m)
        self.r = mujoco.Renderer(m, height=self.H, width=self.W)
        self.cam = mujoco.MjvCamera()
        self.cam.type = mujoco.mjtCamera.mjCAMERA_FREE
        self.look = None
        self.synced = None

    def sync(self, j: int) -> None:
        """Copy env j's randomized model fields (object sizes, masses) to the render model."""
        if self.synced == j:
            return
        try:
            from mjlab.viewer.model_sync import VIEWER_MODEL_FIELDS, sync_model_fields

            fields = self.env.sim.expanded_fields & VIEWER_MODEL_FIELDS
            sync_model_fields(self.m, self.env.sim.model, fields, j)
        except Exception:  # noqa: BLE001  (older mjlab: draw nominal sizes)
            pass
        self.synced = j

    def frame(self, qpos: np.ndarray, mocap_pos: np.ndarray | None, mocap_quat: np.ndarray | None,
              pts: np.ndarray) -> bytes:
        import mujoco

        self.d.qpos[:] = qpos
        if self.m.nmocap and mocap_pos is not None:
            self.d.mocap_pos[:] = mocap_pos
            self.d.mocap_quat[:] = mocap_quat
        mujoco.mj_forward(self.m, self.d)
        c = pts.mean(0)
        dist = max(4.0, min(14.0, 1.1 * float(np.max(np.linalg.norm(pts[:, None] - pts[None], axis=-1))) + 3.0))
        self.look = (c, dist) if self.look is None else (0.9 * self.look[0] + 0.1 * c, 0.95 * self.look[1] + 0.05 * dist)
        self.cam.lookat[:] = [self.look[0][0], self.look[0][1], 0.3]
        self.cam.distance, self.cam.azimuth, self.cam.elevation = self.look[1], 90.0, -40.0
        self.r.update_scene(self.d, camera=self.cam)
        return self.r.render().tobytes()


def key_points(env, j: int) -> np.ndarray:
    g = env.command_manager.get_term("goal")
    return np.stack([env.scene[a].data.root_link_pos_w[j, :2].cpu().numpy() for a in AGENTS]
                    + [g.box_pos()[j, :2].cpu().numpy(), g.goal_xy[j].cpu().numpy()])


class PairVideo:
    def __init__(self, env, folder: Path, length: int):
        self.env, self.folder, self.length = env, Path(folder), length
        self.active, self.ok = False, True
        self.started_at = 0
        self.cam = None

    def start(self, it: int) -> None:
        if not self.ok:
            return
        try:
            if self.cam is None:
                self.cam = Camera(self.env)
        except Exception as e:  # noqa: BLE001
            print(f"[marl2] training videos off: cannot render ({e}); set MUJOCO_GL=egl on a GPU node")
            self.ok = False
            return
        import imageio_ffmpeg

        self.folder.mkdir(parents=True, exist_ok=True)
        self.path = self.folder / f"iter_{it}.mp4"
        self.wr = imageio_ffmpeg.write_frames(str(self.path), (self.cam.W, self.cam.H), fps=1.0 / self.env.step_dt,
                                              quality=6, ffmpeg_log_level="error")
        self.wr.send(None)
        self.active, self.n_frames, self.started_at = True, 0, it
        self.cam.look = None
        self.cam.synced = None

    def step(self) -> Path | None:
        if not self.active:
            return None
        sd = self.env.sim.data
        self.cam.sync(0)
        mp = sd.mocap_pos[0].cpu().numpy() if self.cam.m.nmocap else None
        mq = sd.mocap_quat[0].cpu().numpy() if self.cam.m.nmocap else None
        self.wr.send(self.cam.frame(sd.qpos[0].cpu().numpy(), mp, mq, key_points(self.env, 0)))
        self.n_frames += 1
        if self.n_frames < self.length:
            return None
        self.wr.close()
        self.active = False
        return self.path


def render_episode(cam: Camera, j: int, qpos: np.ndarray, mocap_pos: np.ndarray | None, mocap_quat: np.ndarray | None,
                   pts: np.ndarray, path: Path, fps: float, caption=None) -> Path:
    """qpos (F, nq), mocap (F, nmocap, 3/4), pts (F, 4, 2) for env j -> MP4 at `path`.
    caption(f) -> optional text burned into frame f (needs Pillow)."""
    import imageio_ffmpeg

    path.parent.mkdir(parents=True, exist_ok=True)
    cam.sync(j)
    cam.look = None
    wr = imageio_ffmpeg.write_frames(str(path), (cam.W, cam.H), fps=fps, quality=6, ffmpeg_log_level="error")
    wr.send(None)
    font = None
    for f in range(len(qpos)):
        raw = cam.frame(qpos[f], None if mocap_pos is None else mocap_pos[f],
                        None if mocap_quat is None else mocap_quat[f], pts[f])
        if caption is not None:
            try:
                from PIL import Image, ImageDraw

                im = Image.frombytes("RGB", (cam.W, cam.H), raw)
                dr = ImageDraw.Draw(im)
                dr.rectangle([0, 0, cam.W, 22], fill=(0, 0, 0))
                dr.text((6, 5), caption(f), fill=(255, 255, 255), font=font)
                raw = im.tobytes()
            except Exception:  # noqa: BLE001
                caption = None
        wr.send(raw)
    wr.close()
    return path
