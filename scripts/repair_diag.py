"""Execution-repair mechanism checks (evals/e1-repair-acceptance.md): why a command-level repair did or did not
change heavy-object transport. Reads the 10 Hz traces (contact_test.py --trace 2).

  python scripts/repair_diag.py A=logs/evals/e1s-A-expert/pair R=logs/evals/e1s-R-expert/pair RT=... [--masses=80]

Per arm and mass:
  (a) command      while both robots press (force along the push >= 30 N each): mean forward command and share at
                   the walker's vx limit (0.8 m/s)
  (b) force        mean force along the push direction (and magnitude) per robot, same samples
  (c) motion       object speed, same samples; yaw agreement: share of samples where the wanted yaw rate is >= 5 deg/s
                   and the object turns the wanted way, and mean measured / wanted yaw rate on those samples
  (d) retention    contact exits (on -> off, same contact id) per pressing robot-second, share of exits by distance
                   (> drift radius) vs heading, falls per 100 exits
Interpretation: (a) not at the limit = the command repair was ineffective; (a) at the limit without more (b) / (c) =
force allocation or contact geometry; neither alone implicates the planner.
"""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import exec_report as X  # noqa: E402

VX_LIM = 0.79
YAW_MIN = 5.0  # deg/s


def arm_mass(d, mass):
    s = dict(vx=[], lim=[], fa=[], fm=[], v=[], agree=[], ratio=[], press_s=0.0, exits=0, dist_exits=0, falls=0, ep=0)
    for obj, sc, m, outcome, rows in X.traces(d):
        if float(m) != mass:
            continue
        s["ep"] += 1
        ags = X.agents(rows[0].keys())
        g = lambda k: np.array([float(r[k]) for r in rows])  # noqa: E731
        live = g("live") > 0.5
        F = np.stack([g(f"force_along_cmd_{a}") for a in ags], 1)
        P = (F >= X.PRESS) & live[:, None]
        both = P.all(1)
        for i, a in enumerate(ags):
            vx = g(f"wcmd_vx_{a}")[both]
            s["vx"] += list(vx)
            s["lim"] += list(vx >= VX_LIM)
            s["fa"] += list(F[both, i])
            s["fm"] += list(g(f"force_{a}")[both])
            on = g(f"on_{a}") > 0.5
            cd = g(f"contact_dist_{a}")
            ci = g(f"cidx_{a}") if f"cidx_{a}" in rows[0] else np.zeros(len(rows))
            ex = np.where(on[:-1] & ~on[1:] & (ci[1:] == ci[:-1]))[0]
            s["exits"] += len(ex)
            s["dist_exits"] += int((cd[ex + 1] >= 0.25).sum())
            s["falls"] += int(g(f"fell_{a}").max() > 0.5)
        s["press_s"] += P.sum() * 0.1
        s["v"] += list(g("obj_speed")[both])
        wy, yr = g("want_yaw_rate_deg"), np.rad2deg(g("obj_yaw_rate"))
        tw = live & (np.abs(wy) >= YAW_MIN)
        s["agree"] += list((np.sign(yr[tw]) == np.sign(wy[tw])))
        s["ratio"] += list(yr[tw] / wy[tw])
    return s


def main():
    arms, masses = {}, [80.0]
    for x in sys.argv[1:]:
        if x.startswith("--masses="):
            masses = [float(v) for v in x.split("=", 1)[1].split(",")]
        else:
            k, v = x.split("=", 1)
            arms[k] = Path(v)
    mean = lambda v: float(np.mean(v)) if len(v) else float("nan")  # noqa: E731
    print("| arm | mass | (a) cmd vx / at limit | (b) force along / magnitude N | (c) obj speed m/s | (c) yaw right way / "
          "measured:wanted | (d) exits per press-s | (d) distance exits | (d) falls per 100 exits |")
    print("|---" * 9 + "|")
    for m in masses:
        for k, d in arms.items():
            s = arm_mass(d, m)
            print(f"| {k} | {m:g} kg | {mean(s['vx']):.2f} / {mean(s['lim']):.2f} | {mean(s['fa']):.0f} / {mean(s['fm']):.0f} | "
                  f"{mean(s['v']):.3f} | {mean(s['agree']):.2f} / {np.median(s['ratio']) if s['ratio'] else float('nan'):.2f} | "
                  f"{s['exits'] / max(s['press_s'], 1e-9):.2f} | {s['dist_exits'] / max(s['exits'], 1):.2f} | "
                  f"{100 * s['falls'] / max(s['exits'], 1):.2f} |")


if __name__ == "__main__":
    main()
