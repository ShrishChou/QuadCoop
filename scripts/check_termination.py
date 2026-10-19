"""Falls must be detected: a clean spawn is not terminated, lying/crawling on the body is.

    python scripts/check_termination.py --task QuadCoop-Walker-AnymalC
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

import torch  # noqa: E402

import quadcoop  # noqa: E402,F401

ok = True


def check(c: bool, msg: str) -> None:
    global ok
    ok &= bool(c)
    print(("  ok   " if c else "  FAIL ") + msg)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--task", required=True)
    ap.add_argument("--device", default=None)
    a = ap.parse_args()
    device = a.device or ("cuda:0" if torch.cuda.is_available() else "cpu")
    from mjlab.envs import ManagerBasedRlEnv
    from mjlab.tasks.registry import load_env_cfg

    cfg = load_env_cfg(a.task)
    cfg.scene.num_envs = 4
    cfg.events.pop("push_robot", None)
    cfg.events.pop("object_interval", None)
    cfg.events["object_reset"].params.update(p_override=0.0)
    cfg.commands.pop("push_force", None)
    cfg.observations["critic"].terms.pop("push_force", None)
    env = ManagerBasedRlEnv(cfg=cfg, device=device)
    env.reset()
    print(f"[{a.task}] termination terms: {env.termination_manager.active_terms}")
    zero = torch.zeros(env.action_space.shape, device=device)
    any_done = False
    # Zero action is not a stable stand (the PD gains are soft and the policy supplies
    # the offsets), so only check the first steps after spawn: no false positives from
    # the feet or from the spawn pose.
    for _ in range(5):
        _, _, term, _, _ = env.step(zero)
        any_done |= bool(term.any())
    check(not any_done, "no termination in the first 5 steps after spawn (feet don't count)")

    # Drop the robot onto its belly: body and thighs on the ground, legs splayed.
    robot = env.scene["robot"]
    ids = torch.arange(4, device=device)
    state = robot.data.default_root_state.clone()
    state[:, 2] = 0.12
    robot.write_root_state_to_sim(state, ids)
    hit = torch.zeros(4, dtype=torch.bool, device=device)
    for _ in range(40):
        _, _, term, _, _ = env.step(zero)
        hit |= term
    check(bool(hit.all()), f"lying on the body is terminated in {int(hit.sum())}/4 envs")
    print("PASSED" if ok else "FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())