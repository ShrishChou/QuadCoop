"""Evaluate a Stage 0 walker over objects x masses, record videos, log to W&B.

    python scripts/eval_walker.py --task QuadCoop-Walker-AnymalC --checkpoint <model_N.pt>
    python scripts/eval_walker.py ... --wandb            # needs `wandb login` once
    MUJOCO_GL=egl python scripts/eval_walker.py ... --video   # videos need EGL on a GPU node

Runs, with 64 envs each by default:
  A  track     vx = 0.5 m/s, no disturbance
  B  resist    vx = 0.5 m/s against a constant 25% body-weight bumper force
  C  push      0.4 m/s into each object at each mass, in each push direction

Writes eval.json next to the checkpoint and (with --video) MP4s to eval_videos/.
Scores are the same quantities the validation gate uses (fall rate, speed kept,
object displacement), so a table of them is directly comparable across checkpoints.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import torch  # noqa: E402
import validate_walker as vw  # noqa: E402

import quadcoop  # noqa: E402,F401  (registers tasks)

from quadcoop.robots.objects import OBJECT_NAMES as OBJECTS  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--task", required=True)
    ap.add_argument("--checkpoint", required=True)
    ap.add_argument("--masses", default="5,15,30")
    ap.add_argument("--bearings", default="0,90,180",
                    help="push directions in deg, robot frame (0 fwd, 90 left, 180 back)")
    ap.add_argument("--num-envs", type=int, default=64)
    ap.add_argument("--seconds", type=float, default=10.0)
    ap.add_argument("--force-frac", type=float, default=0.25)
    ap.add_argument("--video", action="store_true")
    ap.add_argument("--wandb", action="store_true")
    ap.add_argument("--wandb-project", default="quadcoop")
    ap.add_argument("--seed", type=int, default=0)
    ap.add_argument("--device", default=None)
    ap.add_argument("--out-dir", default=None, help="default: eval_<ckpt> next to the checkpoint")
    args = ap.parse_args()

    device = args.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    ckpt = Path(args.checkpoint)
    out_dir = Path(args.out_dir) if args.out_dir else ckpt.parent / f"eval_{ckpt.stem}"
    out_dir.mkdir(parents=True, exist_ok=True)
    video_dir = str(out_dir / "videos") if args.video else None

    def ns(**kw):
        return SimpleNamespace(
            checkpoint=str(ckpt), num_envs=args.num_envs, seconds=args.seconds,
            force_frac=args.force_frac, obj_mass=15.0, object="obj_cube", seed=args.seed,
            video_dir=video_dir, **kw)

    rows: dict[str, dict] = {}
    rows["A_track"] = vw.run_test(args.task, "A", ns(video_name="A_track"), device)
    rows["B_resist"] = vw.run_test(args.task, "B", ns(video_name="B_resist"), device)
    for obj in OBJECTS:
        for m in (float(x) for x in args.masses.split(",")):
            for bdeg in (float(x) for x in args.bearings.split(",")):
                key = f"C_{obj}_{m:g}kg_{bdeg:g}deg"
                a = ns(video_name=key)
                a.object, a.obj_mass, a.push_bearing = obj, m, bdeg
                rows[key] = vw.run_test(args.task, "C", a, device)

    (out_dir / "eval.json").write_text(json.dumps(rows, indent=2))
    print(f"\nwrote {out_dir/'eval.json'}")

    if args.wandb:
        import wandb

        run = wandb.init(project=args.wandb_project, job_type="eval",
                         name=f"eval-{args.task}-{ckpt.parent.name}-{ckpt.stem}",
                         config={"task": args.task, "checkpoint": str(ckpt), **vars(args)})
        table = wandb.Table(columns=["condition", "fall_rate", "vx_kept", "object_disp_median_m"])
        for k, r in rows.items():
            table.add_data(k, r["fall_rate"], r["vx_kept"], r.get("box_disp_median"))
            run.summary[f"{k}/fall_rate"] = r["fall_rate"]
            if "box_disp_median" in r:
                run.summary[f"{k}/object_disp_median"] = r["box_disp_median"]
        run.log({"eval_table": table})
        if video_dir:
            for mp4 in sorted(Path(video_dir).glob("*.mp4")):
                run.log({f"video/{mp4.stem}": wandb.Video(str(mp4))})
        run.finish()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())