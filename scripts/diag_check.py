"""Standalone check of quadcoop.coop2.diag (no simulator): synthetic episodes whose answer is known,
one per situation the diagnosis must tell apart. Prints PASS / FAIL per check; exit 1 on a failure."""
import math
import sys
from pathlib import Path

import torch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from quadcoop.coop2.diag import ExecDiag  # noqa: E402

DT, T = 0.02, 5.0
N = 10
names = ["push_hard", "push_soft", "wait", "hold", "walk", "moving", "misaligned", "drift", "edge", "go_break"]
fails = []


def check(name, ok, detail=""):
    print(f"{'PASS' if ok else 'FAIL'}  {name}  {detail}")
    if not ok:
        fails.append(name)


d = ExecDiag(N, "cpu", DT)
thr_d, thr_h = 0.25, math.radians(30.0)
steps = int(T / DT)
pe = torch.full((N,), 2.0)
for i in range(steps):
    t = i * DT
    cmd = torch.full((N, 2), 2, dtype=torch.long)
    on = torch.ones(N, 2, dtype=torch.bool)
    eng = torch.ones(N, 2, dtype=torch.bool)
    cdist = torch.full((N, 2), 0.10)
    herr = torch.zeros(N, 2)
    touch = torch.ones(N, 2, dtype=torch.bool)
    pdir = torch.tensor([1.0, 0.0]).expand(N, 2, 2).clone()
    force = 200.0 * pdir
    bs = torch.zeros(N, 2)
    v = torch.zeros(N, 2)
    w = torch.zeros(N)
    vw = torch.tensor([0.1, 0.0]).expand(N, 2).clone()
    go = torch.ones(N, dtype=torch.bool)
    # 1 push_soft: told to push, not touching
    touch[1] = False; force[1] = 0.0  # noqa: E702
    # 2 wait: robot 0 holds on its contact, robot 1 walks (off its contact)
    cmd[2] = torch.tensor([1, 0]); on[2, 1] = False; eng[2, 1] = False; touch[2] = False; force[2] = 0.0  # noqa: E702
    # 3 hold: both on, both hold, light contact
    cmd[3] = 1; force[3] = 5.0 * pdir[3]  # noqa: E702
    # 4 walk: both walking, far
    cmd[4] = 0; on[4] = False; eng[4] = False; touch[4] = False; force[4] = 0.0; cdist[4] = 2.0  # noqa: E702
    # 5 moving: pushing hard, object moves along the wanted motion at 0.1 m/s
    v[5] = torch.tensor([0.1, 0.0])
    # 6 misaligned: pressing at 60 deg to the push direction
    force[6] = 200.0 * torch.tensor([math.cos(math.radians(60)), math.sin(math.radians(60))])
    # 7 drift: robot 0 engaged but 0.30 m from its contact (beyond 0.25)
    on[7, 0] = False; cdist[7, 0] = 0.30; touch[7, 0] = False; force[7, 0] = 0.0  # noqa: E702
    # 8 edge: on, at 0.22 m (beyond 0.8 x 0.25)
    cdist[8] = 0.22
    # 9 go break: team pushing for 1 s, then not
    go[9] = t < 1.0
    pe = pe - torch.where(torch.arange(N) == 5, torch.full((N,), 0.1 * DT), torch.zeros(N))
    d.observe(cmd=cmd, on=on, engaged=eng, cdist=cdist, herr=herr, thr_dist=thr_d, thr_head=thr_h, touch=touch,
              force=force, push_dir=pdir, base_speed=bs, v_obj=v, w_obj=w, v_want=vw, pe=pe.clone(),
              at_goal=torch.zeros(N, dtype=torch.bool), live=torch.ones(N, dtype=torch.bool),
              present=torch.ones(N, 2, dtype=torch.bool), go=go, flips=torch.zeros(N))
rows = [d.row(j) for j in range(N)]
close = lambda a, b, tol=0.05: a != "" and abs(float(a) - b) <= tol  # noqa: E731
# standstills (5 s still, counted from the 3 s mark including those 3 s: about 5 s)
for j, c in enumerate(["push_hard", "push_soft", "wait", "hold", "walk"]):
    r = rows[j]
    others = sum(r[f"dg_st_{x}"] for x in ["push_hard", "push_soft", "wait", "hold", "walk"] if x != c)
    check(f"standstill filed as {c}", r["dg_still_n"] == 1 and close(r[f"dg_st_{c}"], 5.0, 0.05) and others == 0,
          f"n {r['dg_still_n']} {c} {r[f'dg_st_{c}']} s, others {others}")
check("push_hard standstill force = 200 N", close(rows[0]["dg_still_force"], 200, 1), f"{rows[0]['dg_still_force']}")
r = rows[5]
check("moving object: no standstill, moving 100%, aligned, progress 0.1 m/s",
      r["dg_still_n"] == 0 and close(r["dg_obj_moving"], 1.0) and close(r["dg_obj_align"], 1.0, 0.01) and close(r["dg_progress"], 0.1, 0.005),
      f"{ {k: r[k] for k in ('dg_still_n', 'dg_obj_moving', 'dg_obj_align', 'dg_progress', 'dg_obj_speed')} }")
check("pressing at 60 deg: misaligned, alignment 0.5", close(rows[6]["dg_misaligned"], 1.0) and close(rows[6]["dg_push_align"], 0.5, 0.01),
      f"{rows[6]['dg_misaligned']} {rows[6]['dg_push_align']}")
check("aligned pushing: alignment 1, not misaligned", close(rows[0]["dg_push_align"], 1.0, 0.01) and close(rows[0]["dg_misaligned"], 0.0))
check("drift by distance: half the engaged time drifted (robot 0 of 2), all by distance",
      close(rows[7]["dg_drift"], 0.5) and close(rows[7]["dg_drift_dist"], 1.0) and close(rows[7]["dg_drift_head"], 0.0),
      f"{rows[7]['dg_drift']} {rows[7]['dg_drift_dist']} {rows[7]['dg_drift_head']}")
check("near the zone edge: 100% of on-time", close(rows[8]["dg_edge"], 1.0) and close(rows[0]["dg_edge"], 0.0))
check("team-push latch broken once", rows[9]["dg_go_breaks"] == 1 and rows[0]["dg_go_breaks"] == 0)
check("command shares: wait env = half hold, half walk", close(rows[2]["dg_hold"], 0.5) and close(rows[2]["dg_walk"], 0.5))
check("push sub-shares: hard env 100% pressing, soft env 100% not touching",
      close(rows[0]["dg_push_press"], 1.0) and close(rows[1]["dg_push_notouch"], 1.0))
check("both pressing (env 0) vs none (env 1)", close(rows[0]["dg_both_press"], 1.0) and close(rows[1]["dg_none_press"], 1.0))
print("DIAG CHECK", "PASS" if not fails else f"FAIL {fails}")
sys.exit(1 if fails else 0)
