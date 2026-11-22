"""Which two robots the two-robot task uses: QUADCOOP_PAIR, read once at import.

    mixed   (default) ANYmal C + Spot     slots "anymal", "spot"
    anymal  two ANYmal C                  slots "anymal1", "anymal2"
    spot    two Spot                      slots "spot1", "spot2"
    spot_arm  two Spot with the arm, on RAI's frozen walker (quadcoop/robots/spot_arm.py; docs/spot_arm_pair.md)
                                          slots "spotarm1", "spotarm2"
    anymal_arm  ANYmal C + Spot with the arm (RAI walker)   slots "anymal", "spotarm"
    anymal3 three ANYmal C (team of three)  slots "anymal1", "anymal2", "anymal3"
    anymal4 four ANYmal C (team of four)    slots "anymal1" .. "anymal4" (planner pair + two helpers, play only)

Teams of more than two: each robot's "partner" inputs (the 9 numbers and the partner map channel) describe its
nearest teammate (PARTNER[a] == NEAREST) and the map channel draws every teammate; robot-robot contact and crowding
terms cover every pair. With two robots everything is as before.

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
    "spot_arm": (("spotarm1", "spot_arm"), ("spotarm2", "spot_arm")),
    "anymal_arm": (("anymal", "anymal_c"), ("spotarm", "spot_arm")),
    "anymal3": (("anymal1", "anymal_c"), ("anymal2", "anymal_c"), ("anymal3", "anymal_c")),
    "anymal4": (("anymal1", "anymal_c"), ("anymal2", "anymal_c"), ("anymal3", "anymal_c"), ("anymal4", "anymal_c")),
}
ARM_PAIRS = tuple(p for p, sl in PAIRS.items() if any(t == "spot_arm" for _, t in sl))  # pairs with a Spot-arm slot
ROLE = {"anymal_c": "anymal", "spot": "spot", "spot_arm": "spot_arm"}  # evals/models.yaml role suffix of each robot type


def slots(pair: str | None = None) -> tuple[tuple[str, str], ...]:
    """((slot, robot type), (slot, robot type)) for `pair` (default: QUADCOOP_PAIR or mixed)."""
    pair = pair or os.environ.get("QUADCOOP_PAIR", "mixed")
    if pair not in PAIRS:
        raise ValueError(f"QUADCOOP_PAIR={pair!r}: choose from {sorted(PAIRS)}")
    return PAIRS[pair]


PAIR = os.environ.get("QUADCOOP_PAIR", "mixed")
AGENTS = tuple(s for s, _ in slots(PAIR))
ROBOT_TYPE = dict(slots(PAIR))
NEAREST = "nearest"  # PARTNER value in teams of more than two: the nearest teammate, chosen per env and step
OTHERS = {a: tuple(b for b in AGENTS if b != a) for a in AGENTS}
PARTNER = {AGENTS[0]: AGENTS[1], AGENTS[1]: AGENTS[0]} if len(AGENTS) == 2 else {a: NEAREST for a in AGENTS}
if len(AGENTS) >= 3 and os.environ.get("QUADCOOP_HELPER") == "1":  # planner + helper(s) (scripts/helper_test.py):
    PARTNER = {AGENTS[0]: AGENTS[1], AGENTS[1]: AGENTS[0]} | {a: NEAREST for a in AGENTS[2:]}  # the pair sees each other
PAIRS_OF = tuple((AGENTS[i], AGENTS[j]) for i in range(len(AGENTS)) for j in range(i + 1, len(AGENTS)))
