"""Training runner for Stage 2: logs whether the image path is actually being learned.

Added to the PPO losses every iteration (W&B "Loss/..."):

    img_weight_ratio_actor / _critic   |first-layer weights on the image features| /
                                       |first-layer weights on the 42 (45) numbers|.
                                       Starts at 0 (warm start); rising = the network is
                                       giving the images weight.
    cnn_change_actor / _critic         |CNN weights - their initial values| / |initial|:
                                       the encoders are receiving gradients and changing.

For the control (no images) nothing is added.
"""

from __future__ import annotations

import torch
from mjlab.rl import MjlabOnPolicyRunner

N_NUMERIC = {"actor": 42, "critic": 45}


class Push2Runner(MjlabOnPolicyRunner):
    def __init__(self, env, train_cfg: dict, log_dir: str | None = None, device: str = "cpu") -> None:
        super().__init__(env, train_cfg, log_dir, device)
        self._cnn0: dict[str, list[torch.Tensor]] | None = None
        update = self.alg.update

        def update_and_report():
            if self._cnn0 is None:  # reference = weights before the first update (after any checkpoint load)
                self._cnn0 = {k: [p.detach().clone() for p in self._cnn_params(getattr(self.alg, k))]
                              for k in ("actor", "critic")}
            out = update()
            try:
                out.update(self.image_usage())
            except Exception:  # noqa: BLE001  (diagnostics must never stop training)
                pass
            return out

        self.alg.update = update_and_report

    def _cnn_params(self, model) -> list[torch.Tensor]:
        cnns = getattr(model, "cnns", None)
        return [p for p in cnns.parameters()] if cnns is not None else []

    @torch.no_grad()
    def image_usage(self) -> dict[str, float]:
        out = {}
        for k in ("actor", "critic"):
            model = getattr(self.alg, k)
            ref = self._cnn0[k]
            if not ref:
                continue
            w = model.mlp[0].weight
            n = N_NUMERIC[k]
            out[f"img_weight_ratio_{k}"] = float(w[:, n:].norm() / w[:, :n].norm().clamp(min=1e-8))
            now = self._cnn_params(model)
            num = torch.sqrt(sum(((a - b) ** 2).sum() for a, b in zip(now, ref, strict=True)))
            den = torch.sqrt(sum((b ** 2).sum() for b in ref)).clamp(min=1e-8)
            out[f"cnn_change_{k}"] = float(num / den)
        return out
