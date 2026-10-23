"""Check Stage 2's inputs before training: shapes, profile images, rates, sampler, ablations.

    MUJOCO_GL=egl QUADCOOP_WALKER_CKPT=<walker.pt> python scripts/check_push2.py --robot anymal_c

For variants a and b it builds a small env, puts every shape (trained and held out) in
front of the robot at a random heading, and checks:

  1. geometry: each object's simulated geom sizes equal the randomized part sizes
  2. top profile: negative (inside) at a solid shape's centre; for the arch, positive in
     the doorway and negative at the pillars; the bar (1 m up) is not in the slice
  3. front profile: the arch is open under its bar and solid at bar height
  4. robot-frame map (b): the object appears where it is relative to the robot, and turns
     when the object turns; rebuilt every map_every policy steps (10 Hz)
  5. heading ablation: heading_zero changes the policy's heading inputs (b: not the map);
     heading_zero_map also redraws b's map with the object unrotated
  6. sampler: in training, held-out shapes are never chosen
  7. observation shapes and value ranges

It writes check_push2_<variant>.png: for each shape a top-down render of the simulated
object next to the images the policy receives. Look at it: the profiles must match the
renders (sizes, gaps, orientation).
"""

from __future__ import annotations

import argparse
import math
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
os.environ.setdefault("QUADCOOP_SHAPES", "v2")

import torch  # noqa: E402

RESULTS: list[tuple[str, bool, str]] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    RESULTS.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}  {detail}", flush=True)


def place(env, g, ids, shapes, rel_xy, rel_yaw):
    """Put shapes[ids] at rel_xy (robot frame) with heading rel_yaw; park the rest."""
    from mjlab.utils.lab_api.math import quat_from_euler_xyz

    from quadcoop.stage1.mdp import yaw_of
    robot = env.scene["robot"]
    q_adr = robot.indexing.free_joint_q_adr
    qpos = robot.data.data.qpos[ids]
    root, ryaw = qpos[:, q_adr[0:3]], yaw_of(qpos[:, q_adr[3:7]])
    cs, sn = torch.cos(ryaw), torch.sin(ryaw)
    xy = root[:, :2] + torch.stack([cs * rel_xy[:, 0] - sn * rel_xy[:, 1], sn * rel_xy[:, 0] + cs * rel_xy[:, 1]], -1)
    head = ryaw + rel_yaw
    g.shape[ids] = shapes
    z = torch.zeros(len(ids), device=env.device)
    for k, o in enumerate(g.objs):
        st = torch.zeros(len(ids), 13, device=env.device)
        st[:, :2] = torch.where((shapes == k).unsqueeze(-1), xy, root[:, :2] + torch.tensor([40.0 + 4 * k, 0.0], device=env.device))
        st[:, 2] = g.rest_env[ids, k] + 0.005
        st[:, 3:7] = quat_from_euler_xyz(z, z, head)
        o.write_root_state_to_sim(st, ids)
    g.goal_xy[ids] = xy + 3.0
    env.sim.forward()
    g.refresh_profiles(ids)
    return xy, head


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--robot", default="anymal_c", choices=("anymal_c", "spot"))
    ap.add_argument("--variants", default="a,b")
    ap.add_argument("--device", default=None)
    ap.add_argument("--out", default=".")
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    sys.path.insert(0, str(ROOT))
    if not os.environ.get("QUADCOOP_WALKER_CKPT"):
        from train_coop import newest_run_ckpt
        os.environ["QUADCOOP_WALKER_CKPT"] = str(newest_run_ckpt(ROOT / "logs/rsl_rl" / f"walker_{a.robot}"))

    import quadcoop  # noqa: F401
    import quadcoop.stage1  # noqa: F401
    import quadcoop.stage1b  # noqa: F401
    import quadcoop.stage2  # noqa: F401
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.tasks.registry import load_env_cfg

    from quadcoop.stage2 import profiles as pf
    from quadcoop.stage2.shapes import KIND_NONE, SHAPE_NAMES2, TRAIN_NAMES, geom_size_pos

    suffix = "AnymalC" if a.robot == "anymal_c" else "Spot"
    S = len(SHAPE_NAMES2)
    for variant in a.variants.split(","):
        print(f"\n===== variant {variant} =====")
        cfg = load_env_cfg(f"QuadCoop-Push2{variant}-{suffix}")
        cfg.scene.num_envs = 2 * S
        cfg.curriculum = {}
        env = ManagerBasedRlEnv(cfg=cfg, device=device)
        obs, _ = env.reset()
        g = env.command_manager.get_term("goal")
        n, dev = env.num_envs, env.device

        # 7. observation shapes / ranges
        shp = {k: tuple(v.shape) for k, v in obs.items()}
        top_hw = (pf.ROBOT_TOP if variant == "b" else pf.OBJ_TOP)["hw"]
        check("observation shapes", shp["actor"] == (n, 42) and shp["critic"] == (n, 45)
              and shp["profile_top"] == (n, 1, *top_hw) and shp["profile_front"] == (n, 1, *pf.FRONT["hw"]), str(shp))

        # 6. sampler never picks held-out shapes in training
        counts = torch.zeros(S, dtype=torch.long)
        for _ in range(20):
            env.command_manager.reset(torch.arange(n, device=dev))
            counts += torch.bincount(g.shape.cpu(), minlength=S)
        held = [i for i, nm in enumerate(SHAPE_NAMES2) if nm not in TRAIN_NAMES]
        check("sampler: held-out shapes never chosen in training", int(counts[held].sum()) == 0,
              ", ".join(f"{SHAPE_NAMES2[i]}={int(c)}" for i, c in enumerate(counts)))

        # place every shape twice: once straight, once turned
        ids = torch.arange(n, device=dev)
        shapes = torch.arange(n, device=dev) % S
        rel_xy = torch.tensor([[2.0, 0.0]], device=dev).repeat(n, 1)
        rel_yaw = torch.where(ids < S, torch.zeros(n, device=dev), torch.full((n,), math.radians(35), device=dev))
        place(env, g, ids, shapes, rel_xy, rel_yaw)

        # 1. geometry in the sim matches the part sizes
        worst = 0.0
        for k, o in enumerate(g.objs):
            kinds = g.kinds[k]
            npart = int((kinds != KIND_NONE).sum())
            size, pos = geom_size_pos(g.parts[:, k], kinds.unsqueeze(0))
            gid = o.indexing.geom_ids[:npart].long()
            worst = max(worst, float((env.sim.model.geom_size[:, gid] - size[:, :npart]).abs().max()),
                        float((env.sim.model.geom_pos[:, gid] - pos[:, :npart]).abs().max()))
        sizes = g.parts[:, SHAPE_NAMES2.index("arch"), 2, 4] * 2
        check("geometry: sim geoms equal the randomized parts", worst < 1e-5,
              f"max diff {worst:.1e}; arch pillar widths across envs {sizes.min():.2f}-{sizes.max():.2f} m")

        top, front = g.profile_top.clone(), g.profile_front.clone()
        arch = SHAPE_NAMES2.index("arch")
        j = int(arch)  # straight arch
        if variant == "a":
            h, w = pf.OBJ_TOP["hw"]
            centre = float(top[j, 0, h // 2, w // 2])
            py = float(g.parts[j, arch, 2, 1])  # pillar centre y
            col = int(round((pf.OBJ_TOP["y"][1] - py) / (pf.OBJ_TOP["y"][1] - pf.OBJ_TOP["y"][0]) * (w - 1)))
            pillar = float(top[j, 0, h // 2, col])
            check("top profile: arch doorway open, pillars solid", centre > 0 and pillar < 0,
                  f"centre {centre * pf.SCALE:+.2f} m, pillar {pillar * pf.SCALE:+.2f} m")
            cube = SHAPE_NAMES2.index("cube")
            check("top profile: solid at a cube's centre", float(top[cube, 0, h // 2, w // 2]) < 0)
        else:
            # object 2 m ahead: the map pixel at (x=2, y=0) is inside a solid shape
            h, w = pf.ROBOT_TOP["hw"]
            row = int(round((pf.ROBOT_TOP["x"][1] - 2.0) / (pf.ROBOT_TOP["x"][1] - pf.ROBOT_TOP["x"][0]) * (h - 1)))
            cube = SHAPE_NAMES2.index("cube")
            check("robot-frame map: cube 2 m ahead shows at the right pixel",
                  float(top[cube, 0, row, w // 2]) < 0 and float(top[cube, 0, h - 1, w // 2]) > 0)
            tsh = SHAPE_NAMES2.index("t_shape")
            check("robot-frame map turns with the object", float((top[tsh] - top[tsh + S]).abs().max()) > 0.2)
            # 4. rate
            before = g.map_updates
            for _ in range(2 * g.map_every):
                env.step(torch.zeros(n, 3, device=dev))
            check("robot-frame map rebuilt every map_every steps", g.map_updates - before == 2,
                  f"map_every={g.map_every} ({1 / (g.map_every * env.step_dt):.0f} Hz at {1 / env.step_dt:.0f} Hz control)")
            place(env, g, ids, shapes, rel_xy, rel_yaw)
            top = g.profile_top.clone()

        # 3. front profile: arch open under the bar, solid at bar height
        fh, fw = pf.FRONT["hw"]
        z_open, z_bar = 0.4, 1.08
        r_open = int(round((pf.FRONT["z"][1] - z_open) / (pf.FRONT["z"][1] - pf.FRONT["z"][0]) * (fh - 1)))
        r_bar = int(round((pf.FRONT["z"][1] - z_bar) / (pf.FRONT["z"][1] - pf.FRONT["z"][0]) * (fh - 1)))
        check("front profile: arch open under its bar, solid at bar height",
              float(front[j, 0, r_open, fw // 2]) > 0 and float(front[j, 0, r_bar, fw // 2]) < 0)

        # 5. heading ablation
        tsh = SHAPE_NAMES2.index("t_shape") + S  # the turned T
        box_before = env.observation_manager.compute_group("critic")[tsh, 9:13].clone()
        g.heading_zero = True
        g.refresh_profiles(ids)
        box_after = env.observation_manager.compute_group("critic")[tsh, 9:13].clone()
        changed = float((box_before - box_after).abs().max()) > 1e-3
        detail = f"heading inputs {box_before[2:4].tolist()} -> {box_after[2:4].tolist()}"
        if variant == "b":
            same_map = float((g.profile_top[tsh] - top[tsh]).abs().max()) < 1e-5
            g.heading_zero_map = True
            g.refresh_profiles(ids)
            changed = changed and same_map and float((g.profile_top[tsh] - top[tsh]).abs().max()) > 0.2
            detail += "; map unchanged by heading_zero, changed by heading_zero_map"
        check("heading ablation changes what the policy is told", changed, detail)
        g.heading_zero = g.heading_zero_map = False
        g.refresh_profiles(ids)

        render_sheet(env, g, variant, Path(a.out) / f"check_push2_{variant}.png")
        env.close()

    bad = [r for r in RESULTS if not r[1]]
    print(f"\n{len(RESULTS) - len(bad)}/{len(RESULTS)} checks passed")
    return 1 if bad else 0


def render_sheet(env, g, variant, path: Path) -> None:
    """Per shape: top-down render of the simulated scene | top profile | front profile."""
    try:
        import mujoco
        import numpy as np
        from PIL import Image, ImageDraw
        from mjlab.viewer.model_sync import VIEWER_MODEL_FIELDS, sync_model_fields
    except Exception as e:  # noqa: BLE001
        print(f"(no render: {e})")
        return
    from quadcoop.stage2 import profiles as pf
    from quadcoop.stage2.shapes import SHAPE_NAMES2

    m = env.sim.mj_model
    m.vis.global_.offwidth, m.vis.global_.offheight = max(m.vis.global_.offwidth, 256), max(m.vis.global_.offheight, 256)
    try:
        r = mujoco.Renderer(m, 256, 256)
    except Exception as e:  # noqa: BLE001
        print(f"(no render: {e}; set MUJOCO_GL=egl)")
        return
    d = mujoco.MjData(m)
    fields = env.sim.expanded_fields & VIEWER_MODEL_FIELDS
    cam = mujoco.MjvCamera()
    cam.type = mujoco.mjtCamera.mjCAMERA_FREE
    S = len(SHAPE_NAMES2)

    def cmap(img, size):
        v = img.cpu().numpy()[0]
        x = np.clip((v + 0.6) / 2.6, 0, 1)
        rgb = np.stack([x, x * 0.9, 1 - x], -1)
        rgb[v < 0] = [0.85, 0.15, 0.1]  # inside the object: red
        return Image.fromarray((rgb * 255).astype(np.uint8)).resize(size, Image.NEAREST)

    rows = []
    for j in range(2 * S):
        sync_model_fields(m, env.sim.model, fields, j)
        d.qpos[:] = env.sim.data.qpos[j].cpu().numpy()
        d.mocap_pos[:] = env.sim.data.mocap_pos[j].cpu().numpy()
        d.mocap_quat[:] = env.sim.data.mocap_quat[j].cpu().numpy()
        mujoco.mj_forward(m, d)
        robot_xy = env.scene["robot"].data.root_link_pos_w[j, :2].cpu().numpy()
        obj_xy = g.box_pos()[j, :2].cpu().numpy()
        from quadcoop.stage1.mdp import yaw_of
        ryaw = float(yaw_of(env.scene["robot"].data.root_link_quat_w[j:j + 1])[0])
        if variant == "a":  # view centred on the object, its x axis up
            cam.lookat[:] = [obj_xy[0], obj_xy[1], 0.3]
            cam.azimuth = math.degrees(float(g.heading()[j]))
        else:  # view centred 1 m ahead of the robot, robot forward up
            ahead = robot_xy + np.array([math.cos(ryaw), math.sin(ryaw)])
            cam.lookat[:] = [ahead[0], ahead[1], 0.3]
            cam.azimuth = math.degrees(ryaw)
        cam.elevation, cam.distance = -89.0, 5.5
        r.update_scene(d, camera=cam)
        im = Image.fromarray(r.render())
        row = Image.new("RGB", (256 * 3, 280), (25, 25, 25))
        row.paste(im, (0, 24))
        row.paste(cmap(g.profile_top[j], (256, 256)), (256, 24))
        row.paste(cmap(g.profile_front[j], (256, 128)), (512, 24 + 64))
        dr = ImageDraw.Draw(row)
        k = int(g.shape[j])
        dr.text((4, 4), f"{SHAPE_NAMES2[k]} {'(turned 35 deg)' if j >= S else ''}  env {j}", fill=(255, 255, 255))
        dr.text((260, 4), "top profile (" + ("object frame)" if variant == "a" else "robot frame, 4x4 m)"),
                fill=(255, 255, 255))
        dr.text((516, 4), "front profile (object frame)", fill=(255, 255, 255))
        rows.append(row)
    sheet = Image.new("RGB", (256 * 3 * 2, 280 * S), (0, 0, 0))
    for i, row in enumerate(rows):
        sheet.paste(row, ((i // S) * 768, (i % S) * 280))
    sheet.save(path)
    print(f"wrote {path}  (left: straight, right: turned 35 deg; red = inside the object)")
    r.close()
    _ = pf


if __name__ == "__main__":
    raise SystemExit(main())
