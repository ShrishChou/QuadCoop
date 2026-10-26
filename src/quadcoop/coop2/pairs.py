"""Which two robots the two-robot task uses: QUADCOOP_PAIR, read once at import.

    mixed   (default) ANYmal C + Spot     slots "anymal", "spot"
    anymal  two ANYmal C                  slots "anymal1", "anymal2"
    spot    two Spot                      slots "spot1", "spot2"

A slot name is the robot's scene entity name and the suffix of its per-robot reward terms
(push_credit_anymal2, ...). The slot's robot type picks its walker and its Stage 2 policy
(evals/models.yaml roles walker_<role>, push2<variant>_<role>, role = ROLE[type]), its size and
its fall rule. With two robots of one type both start from the same walker and Stage 2 policy.

No package imports here: train_coop2.py loads this file before the environment variables that
the robot modules read at import are set.
"""

from __future__ import annotations

import os

PAIRS = {
    "mixed": (("anymal", "anymal_c"), ("spot", "spot")),
    "anymal": (("anymal1", "anymal_c"), ("anymal2", "anymal_c")),
    "spot": (("spot1", "spot"), ("spot2", "spot")),
}
ROLE = {"anymal_c": "anymal", "spot": "spot"}  # evals/models.yaml role suffix of each robot type


def slots(pair: str | None = None) -> tuple[tuple[str, str], ...]:
    """((slot, robot type), (slot, robot type)) for `pair` (default: QUADCOOP_PAIR or mixed)."""
    pair = pair or os.environ.get("QUADCOOP_PAIR", "mixed")
    if pair not in PAIRS:
        raise ValueError(f"QUADCOOP_PAIR={pair!r}: choose from {sorted(PAIRS)}")
    return PAIRS[pair]


PAIR = os.environ.get("QUADCOOP_PAIR", "mixed")
AGENTS = tuple(s for s, _ in slots(PAIR))
ROBOT_TYPE = dict(slots(PAIR))
PARTNER = {AGENTS[0]: AGENTS[1], AGENTS[1]: AGENTS[0]}
