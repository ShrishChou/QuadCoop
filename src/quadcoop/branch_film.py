"""Side-by-side films of matched branches (scripts/chain4_branch.py --film): the same task from the same simulator state
at the decision time, left = one arm (e.g. k3, the trio stays), right = another (e.g. k4, robot 4 joins), with what the
planner did drawn and captioned, so a failure can be shown and explained, not only counted.

Recording is cheap and covers every env of the filmed arms (qpos, goal markers, robot / object / goal positions, each
robot's assigned contact and push direction, and a caption vector). After a mass, `render` picks the informative tasks
(robot 4 disrupted a success, rescued a failure, both failed, both succeeded; spread over objects) and writes one MP4
per task plus a JSON of both arms' episode rows and an index (index.csv / index.md).

Drawn per robot (colour = identity: R1 cyan, R2 yellow, R3 magenta, R4 orange):
  ball above the robot       which robot it is (only robots in the team)
  post on the object         its assigned contact (faint: not pushing there yet)
  arrow at the post's top    the push direction the planner assigned
Caption per panel: time, distance and heading still to go, each robot's state (PUSH and its measured contact force
when above 20 N, at its contact without force, walking to its contact, FELL), robots touching each other, contact changes, when robots 3 / 4 joined (and robot 4's withdrawal).
"""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

import numpy as np
import torch

COLS = ((0.0, 0.95, 0.95), (1.0, 0.85, 0.0), (1.0, 0.15, 0.9), (1.0, 0.45, 0.05))
NAMES = ("R1 cyan", "R2 yellow", "R3 magenta", "R4 orange")
LABEL = {"k2": "2 robots (pair only)", "k3b": "3 robots (robot 3 called at t2)", "k3": "3 robots (stay at three)",
         "k4": "4 robots (robot 4 called at t2)", "k3null": "3 robots (null copy)", "k2null": "2 robots (null copy)"}
# caption vector layout (per env and frame)
C_D, C_E, C_TOUCH, C_SW, C_NH, C_WD = range(6)
C_R = 6  # then per robot q: present, pushing, force, fell, has contact  (5 x 4)


class BranchFilm:
    def __init__(self, base, g, robots, cases, pairs, stride: int, out_dir: Path, film_max: int, size=(960, 720),
                 t_from: float = 16.0):
        self.base, self.g, self.robots, self.cases = base, g, robots, cases
        self.pairs = pairs  # [(left_arm, right_arm), ...]
        arms = {x for p in pairs for x in p}
        self.ids = [j for j, c in enumerate(cases) if c[0] in arms]
        self.col = {j: i for i, j in enumerate(self.ids)}
        self.fid = torch.tensor(self.ids, dtype=torch.long, device=base.device)
        self.stride, self.out, self.film_max = stride, Path(out_dir), film_max
        self.W, self.H = size
        self.t_from = t_from
        self.nmocap = base.sim.mj_model.nmocap
        self.q, self.mp, self.mq, self.pts, self.mk, self.cap, self.t = [], [], [], [], [], [], []

    # -- recording -----------------------------------------------------------------------------------------------
    def record(self, t: float, S: dict, present: list, pressing: list, forces: list, touching: torch.Tensor) -> None:
        g, f = self.g, self.fid
        sd = self.base.sim.data
        self.t.append(t)
        self.q.append(sd.qpos[f].cpu().numpy().astype(np.float32))
        if self.nmocap:
            self.mp.append(sd.mocap_pos[f].cpu().numpy().astype(np.float32))
            self.mq.append(sd.mocap_quat[f].cpu().numpy().astype(np.float32))
        bp = g.box_pos()[:, :2]
        self.pts.append(torch.stack([r.data.root_link_pos_w[:, :2] for r in self.robots] + [bp, g.goal_xy], 1)[f]
                        .cpu().numpy().astype(np.float32))
        yaw = g.contact_frame_yaw()
        cs, sn = torch.cos(yaw), torch.sin(yaw)

        def rot(v):
            return torch.stack([cs * v[:, 0] - sn * v[:, 1], sn * v[:, 0] + cs * v[:, 1]], -1)

        mk, has = [], []
        for k in range(2):
            pw, _ = g.contact_world(k)
            mk.append(torch.cat([pw, g.push_dir_world(k)], -1))
            has.append(torch.ones_like(bp[:, 0], dtype=torch.bool))
        for j in range(2):
            mk.append(torch.cat([bp + rot(S[f"h_p{j}"]), -rot(S[f"h_n{j}"])], -1))
            has.append(S[f"h_has{j}"] & (S[f"h_idx{j}"] >= 0))
        self.mk.append(torch.stack(mk, 1)[f].cpu().numpy().astype(np.float32))
        d, e = g.errors()
        e = torch.where(g.symmetry() > 0, e, torch.zeros_like(e))
        sw = g.c_switches + S["sw2"] + S["sw3"]
        cap = [d, torch.rad2deg(e), (touching > 0).float(), sw, S["nh"].float(), S["wd"].float()]
        for q in range(4):
            cap += [present[q].float(), (pressing[q] & present[q]).float(), forces[q], S[f"fell{q}"].float(), has[q].float()]
        self.cap.append(torch.stack(cap, -1)[f].cpu().numpy().astype(np.float32))

    # -- choosing ------------------------------------------------------------------------------------------------
    def choose(self, rows: list, left: str, right: str) -> list:
        """(task index, category) for up to film_max tasks: disruptions, rescues, both failed, both succeeded."""
        L = {r["task"]: r for r in rows if r["arm"] == left}
        R = {r["task"]: r for r in rows if r["arm"] == right}
        cat = {"disrupted": [], "rescued": [], "both failed": [], "both succeeded": []}
        for k, rl in L.items():
            rr = R.get(k)
            if rr is None or int(rl["ended_t2"]):
                continue
            sl, sr = int(rl["success"]), int(rr["success"])
            c = ("disrupted" if sl and not sr else "rescued" if sr and not sl else
                 "both succeeded" if sl else "both failed")
            cat[c].append(k)
        quota = {"disrupted": 0.4, "rescued": 0.2, "both failed": 0.25, "both succeeded": 0.15}
        want = {c: max(1, int(round(q * self.film_max))) if cat[c] else 0 for c, q in quota.items()}
        out = []
        for c, ks in cat.items():
            by_obj = {}
            for k in sorted(ks, key=lambda k: (L[k]["object"], L[k]["scenario"], L[k]["rep"])):
                by_obj.setdefault(L[k]["object"], []).append(k)
            pick, lists = [], list(by_obj.values())
            while len(pick) < want[c] and any(lists):  # round-robin over objects
                for lst in lists:
                    if lst and len(pick) < want[c]:
                        pick.append(lst.pop(0))
            out += [(k, c) for k in pick]
        return out[: self.film_max]

    # -- rendering -----------------------------------------------------------------------------------------------
    def render(self, rows: list, mass: float, t_decide: float, horizon: float) -> list:
        """Write the chosen side-by-side films for this mass; returns their index rows."""
        if not self.q:
            return []
        import mujoco
        from PIL import Image, ImageDraw, ImageFont

        from quadcoop.coop2.video import Camera

        Q, P, MK, CP = (np.stack(x, 1) for x in (self.q, self.pts, self.mk, self.cap))  # (envs, F, ...)
        MP = np.stack(self.mp, 1) if self.mp else None
        MQ = np.stack(self.mq, 1) if self.mq else None
        T = np.array(self.t)
        cam = Camera(self.base, self.W, self.H)
        try:
            font = ImageFont.load_default(size=max(13, int(13 * self.H / 480)))
        except Exception:  # noqa: BLE001
            font = ImageFont.load_default()
        fs = getattr(font, "size", 13)
        lh = fs + 3
        index = []
        task_env = {(c[0], c[4]): j for j, c in enumerate(self.cases)}
        fps = 1.0 / (T[1] - T[0]) if len(T) > 1 else 10.0
        for left, right in self.pairs:
            for k, category in self.choose([r for r in rows if r["mass"] == mass], left, right):
                jl, jr = task_env[(left, k)], task_env[(right, k)]
                rl = next(r for r in rows if r["mass"] == mass and r["arm"] == left and r["task"] == k)
                rr = next(r for r in rows if r["mass"] == mass and r["arm"] == right and r["task"] == k)
                ends = []
                for r_ in (rl, rr):
                    tf = [float(r_[c]) for c in r_ if c.startswith("t_fall_") and r_[c] != ""]
                    ends.append(float(r_["t_success"]) if r_["t_success"] != "" else min(tf + [horizon]))
                t_end = min(horizon, max(ends) + 2.0)
                frames = np.nonzero((T >= self.t_from - 1e-6) & (T <= t_end + 1e-6))[0]
                if len(frames) == 0:
                    continue
                o, s_name, rep = rl["object"], rl["scenario"], rl["rep"]
                stem = f"{o}_{mass:g}kg_{s_name}_r{rep}__{left}-{rl['outcome']}__{right}-{rr['outcome']}"
                vdir = self.out / f"{left}_vs_{right}"
                vdir.mkdir(parents=True, exist_ok=True)
                path = vdir / f"{stem}.mp4"
                import imageio_ffmpeg

                wr = imageio_ffmpeg.write_frames(str(path), (2 * self.W, self.H), fps=fps, ffmpeg_log_level="error",
                                                 quality=None, macro_block_size=8,
                                                 output_params=["-crf", "16", "-preset", "medium", "-pix_fmt", "yuv420p"])
                wr.send(None)
                cam.synced = None
                cam.sync(jl)
                look = None
                head = (f"{o} {mass:g} kg, {s_name}, rep {rep} | {category.upper()} | left {LABEL.get(left, left)} -> "
                        f"{_out(rl)} | right {LABEL.get(right, right)} -> {_out(rr)}")
                legend = ("ball above robot = identity (" + ", ".join(NAMES) + "); post = its assigned contact (faint: "
                          "not pushing yet); arrow = assigned push direction")
                for fr in frames:
                    sel = []
                    for j in (jl, jr):
                        c = self.col[j]
                        pres = [CP[c, fr, C_R + 5 * q] > 0.5 for q in range(4)]
                        sel += [P[c, fr, q] for q in range(4) if pres[q]] + [P[c, fr, 4], P[c, fr, 5]]
                    pts = np.stack(sel)
                    ctr = pts.mean(0)
                    dist = max(4.0, min(14.0, 1.1 * float(np.max(np.linalg.norm(pts[:, None] - pts[None], axis=-1))) + 3.0))
                    look = (ctr, dist) if look is None else (0.9 * look[0] + 0.1 * ctr, 0.95 * look[1] + 0.05 * dist)
                    panels = []
                    for side, (j, arm, r_) in enumerate(((jl, left, rl), (jr, right, rr))):
                        c = self.col[j]
                        cam.d.qpos[:] = Q[c, fr]
                        if MP is not None:
                            cam.d.mocap_pos[:] = MP[c, fr]
                            cam.d.mocap_quat[:] = MQ[c, fr]
                        mujoco.mj_forward(cam.m, cam.d)
                        cam.cam.lookat[:] = [look[0][0], look[0][1], 0.3]
                        cam.cam.azimuth, cam.cam.elevation, cam.cam.distance = 90.0, -40.0, look[1]
                        cam.r.update_scene(cam.d, camera=cam.cam)
                        cam._draw(self._marks(c, fr, P, MK, CP))
                        im = Image.frombytes("RGB", (self.W, self.H), cam.r.render().tobytes())
                        dr = ImageDraw.Draw(im)
                        lines = self._caption(c, fr, T[fr], arm, r_, t_decide)
                        top = 2 * lh + 2
                        dr.rectangle([0, top, self.W, top + 6 + lh * len(lines)], fill=(0, 0, 0))
                        for li, txt in enumerate(lines):
                            dr.text((6, top + 4 + lh * li), txt, fill=(255, 255, 255), font=font)
                        panels.append(np.asarray(im))
                    frame = Image.fromarray(np.concatenate(panels, 1))
                    dr = ImageDraw.Draw(frame)
                    dr.rectangle([0, 0, 2 * self.W, 2 * lh + 2], fill=(25, 25, 60))
                    dr.text((6, 2), head, fill=(255, 255, 255), font=font)
                    dr.text((6, 2 + lh), legend, fill=(200, 200, 200), font=font)
                    dr.line([(self.W, 2 * lh + 2), (self.W, self.H)], fill=(255, 255, 255), width=2)
                    wr.send(frame.tobytes())
                wr.close()
                keep = ["arm", "outcome", "success", "t_success", "final_pos_err", "t_add3", "t_add4", "arrive3", "arrive4",
                        "robots_touch_frac", "switches1", "switches2", "switches3", "switches4", "helper4_s",
                        "f2_d", "f2_e_deg", "f2_n_free", "f2_free_best", "f2_strength", "f2_need_more"]
                keep += [c for c in rl if c.startswith(("fell_", "t_fall_", "press_frac"))]
                info = {"object": o, "mass": mass, "scenario": s_name, "rep": rep, "category": category, "file": path.name,
                        left: {c: rl.get(c, "") for c in keep}, right: {c: rr.get(c, "") for c in keep}}
                path.with_suffix(".json").write_text(json.dumps(info, indent=1))
                index.append({"pair": f"{left}_vs_{right}", "file": f"{left}_vs_{right}/{path.name}", "object": o,
                              "mass": mass, "scenario": s_name, "rep": rep, "category": category,
                              f"left": f"{left}: {_out(rl)}", "right": f"{right}: {_out(rr)}",
                              "touch_left": rl["robots_touch_frac"], "touch_right": rr["robots_touch_frac"],
                              "arrive4_right": rr.get("arrive4", ""), "n_free_t2": rl.get("f2_n_free", "")})
                print(f"  [film] {path.relative_to(self.out.parent)}", flush=True)
        self._write_index(index)
        self.q, self.mp, self.mq, self.pts, self.mk, self.cap, self.t = [], [], [], [], [], [], []
        return index

    def _marks(self, c, fr, P, MK, CP):
        out = []
        for q in range(4):
            if CP[c, fr, C_R + 5 * q] < 0.5:  # not in the team
                continue
            col = COLS[q]
            rx, ry = P[c, fr, q]
            out.append(("sphere", (rx, ry, 1.45), 0.11, (*col, 1.0)))
            if CP[c, fr, C_R + 5 * q + 4] < 0.5:  # no assigned contact
                continue
            px, py, dx, dy = MK[c, fr, q]
            alpha = 1.0 if CP[c, fr, C_R + 5 * q + 1] > 0.5 else 0.35
            out.append(("arrow", (px, py, 0.25), (px, py, 1.05), 0.012, (*col, alpha)))
            out.append(("sphere", (px, py, 1.05), 0.07, (*col, alpha)))
            out.append(("arrow", (px - 0.6 * dx, py - 0.6 * dy, 1.05), (px - 0.1 * dx, py - 0.1 * dy, 1.05), 0.035,
                        (*col, alpha)))
        return out

    def _caption(self, c, fr, t, arm, r_, t_decide):
        x = self.cap[fr][c]
        st = []
        for q in range(4):
            pres, push, fn, fell, has = x[C_R + 5 * q: C_R + 5 * q + 5]
            if pres < 0.5:
                st.append(f"R{q + 1} -")
            elif fell > 0.5:
                st.append(f"R{q + 1} FELL")
            elif fn > 20.0:
                st.append(f"R{q + 1} PUSH {fn:.0f} N")
            elif push > 0.5:
                st.append(f"R{q + 1} at contact, no force")
            elif has > 0.5:
                st.append(f"R{q + 1} walking to contact")
            else:
                st.append(f"R{q + 1} idle")
        ev = []
        if r_.get("t_add3", "") != "":
            ev.append(f"R3 called {float(r_['t_add3']):.0f} s")
        if r_.get("t_add4", "") != "":
            ev.append(f"R4 called {float(r_['t_add4']):.0f} s")
        if r_.get("t_withdraw", "") != "" and t >= float(r_["t_withdraw"]):
            ev.append(f"R4 withdrew {float(r_['t_withdraw']):.0f} s")
        phase = "before the decision (both sides identical)" if t < t_decide - 1e-6 else "after the decision"
        return [f"{LABEL.get(arm, arm)} | t {t:4.1f} s, {phase}",
                f"to goal {x[C_D]:.2f} m, heading {x[C_E]:+.0f} deg | contact changes {x[C_SW]:.0f}"
                + (" | ROBOTS TOUCHING" if x[C_TOUCH] > 0.5 else ""),
                "  ".join(st),
                ", ".join(ev) + f" | final: {_out(r_)}"]

    def _write_index(self, index: list) -> None:
        if not index:
            return
        p = self.out / "index.csv"
        old = list(csv.DictReader(open(p))) if p.exists() else []
        allr = old + [{k: str(v) for k, v in r.items()} for r in index]
        keys = list(dict.fromkeys(k for r in allr for k in r))
        with open(p, "w", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=keys)
            w.writeheader()
            w.writerows(allr)
        L = ["# Matched-branch films", "", "Same task, same simulator state at the decision; left and right differ only "
             "in the arm. Categories: disrupted (left succeeded, right failed), rescued (the reverse), both failed, both "
             "succeeded. Each clip has a JSON with both arms' episode rows.", "",
             "| clip | mass | category | left | right | robots touching (left / right) |", "|---|---|---|---|---|---|"]
        for r in allr:
            L.append(f"| [{Path(r['file']).name}]({r['file']}) | {r['mass']} | {r['category']} | {r['left']} | "
                     f"{r['right']} | {r['touch_left']} / {r['touch_right']} |")
        (self.out / "index.md").write_text("\n".join(L) + "\n")


def _out(r: dict) -> str:
    if int(r["success"]):
        return f"success at {float(r['t_success']):.1f} s"
    o = r["outcome"]
    if o.startswith("fell_"):
        who = o[5:].replace("anymal", "R")
        tf = [float(r[c]) for c in r if c.startswith("t_fall_") and r[c] != ""]
        return f"FELL ({who}) at {min(tf):.1f} s" if tf else f"FELL ({who})"
    return f"timeout, {float(r['final_pos_err']):.2f} m short" if o == "horizon" else o
