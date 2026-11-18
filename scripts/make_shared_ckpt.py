"""A shared-actor starting checkpoint: both robots' actors = one slot's actor of a pair checkpoint.

    python scripts/make_shared_ckpt.py logs/marl2/ippo_aa_kl_ten_s0/model_4000.pt anymal1 logs/shared_init/AA_4000.pt

Both actor entries get SLOT's weights, observation normalizer and action noise (observation-group names in the keys
renamed per robot), its learning rate and noise cap. Everything else is the parent's (iteration, curriculum state,
critics). Used to evaluate A0 + A0 / B0 + B0 (scripts/eval_coop2.py --checkpoint) and to start --shared-actor runs
(train_coop2.py --init-actors). docs/actor_schedule.md.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

import torch


def main() -> int:
    src, slot, out = sys.argv[1], sys.argv[2], Path(sys.argv[3])
    ck = torch.load(src, map_location="cpu", weights_only=False)
    agents = list(ck["actors"])
    assert slot in agents, f"{slot}: checkpoint has {agents}"
    sd = ck["actors"][slot]
    pat = re.compile(rf"(?<=_){re.escape(slot)}(?=\.)")
    ck["actors"] = {a: {pat.sub(a, k): v.clone() for k, v in sd.items()} for a in agents}
    ck["lr"] = {a: ck["lr"][slot] for a in agents}
    ck["std_cap"] = {a: (ck.get("std_cap") or {}).get(slot) for a in agents}
    ck["actor_opt"] = {a: ck["actor_opt"][slot] for a in agents} if "actor_opt" in ck else {}
    ck["warm_from"] = {"shared_from": f"{src}:{slot}", **ck.get("warm_from", {})}
    out.parent.mkdir(parents=True, exist_ok=True)
    torch.save(ck, out)
    print(f"{out}: both actors = {slot} of {src} (iteration {ck['iter']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
