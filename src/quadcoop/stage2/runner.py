"""Training runner for Stage 2: logs whether the image path is actually being learned.

Added to the PPO losses every iteration (W&B "Loss/..."):

    img_weight_ratio_actor / _critic   |first-layer weights on the image features| /
                                       |first-layer weights on the 42 (45) numbers|.
                                       Starts at 0 (warm start); rising = the network is
                                       giving the images weight.
    cnn_change_actor / _critic         |CNN weights - their initial values| / |initial|:
                                       the encoders are receiving gradients and changing.

For the control (no images) nothing is added.

Checkpoints also store the curriculum state (level, success EMA, per-shape success) under
infos["push2_curriculum"], and loading a checkpoint restores it, so a resumed or requeued run
continues at the level it reached instead of restarting at the configured start level.
Checkpoints written before this (no such entry) load as before.
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

    def _goal(self):
        return self.env.unwrapped.command_manager.get_term("goal")

    def save(self, path: str, infos=None) -> None:
        try:
            g = self._goal()
            cur = {"level": int(g.level), "ema_success": float(g.ema_success),
                   "shape_success": [float(x) for x in g.shape_success.tolist()]}
            infos = {**(infos or {}), "push2_curriculum": cur}
        except Exception:  # noqa: BLE001  (never block saving)
            pass
        super().save(path, infos)

    def load(self, path: str, load_cfg: dict | None = None, strict: bool = True,
             map_location: str | None = None) -> dict:
        infos = super().load(path, load_cfg=load_cfg, strict=strict, map_location=map_location)
        cur = (infos or {}).get("push2_curriculum")
        if cur:
            g = self._goal()
            g.level = min(int(cur["level"]), len(g.cfg.levels) - 1)
            g.ema_success = float(cur["ema_success"])
            ss = torch.tensor(cur["shape_success"], device=g.shape_success.device, dtype=g.shape_success.dtype)
            if ss.shape == g.shape_success.shape:
                g.shape_success[:] = ss
            # the iteration counter is restored with common_step_counter: let the level dwell restart
            g.last_change_iter = self.env.unwrapped.common_step_counter / 24
            print(f"[push2] curriculum restored from checkpoint: level {g.level}, success EMA {g.ema_success:.2f}")
        return infos

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
