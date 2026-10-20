"""The frozen Stage 0 walker, rebuilt from an rsl_rl checkpoint (model_<iter>.pt).

The checkpoint's ``actor_state_dict`` holds the observation normalizer and the MLP:

    obs_normalizer._mean / _std     (1, 48)
    mlp.0 / mlp.2 / mlp.4 / mlp.6   Linear layers, ELU between them

We rebuild exactly that and output the deterministic (mean) action. No gradients:
Stage 1 trains only the high-level policy on top of it.
"""

from __future__ import annotations

import re
from pathlib import Path

import torch

_EPS = 1e-2  # rsl_rl EmpiricalNormalization: (x - mean) / (std + eps)


class FrozenWalker(torch.nn.Module):
    def __init__(self, checkpoint: str | Path, device: str):
        super().__init__()
        ck = torch.load(str(checkpoint), map_location=device, weights_only=False)
        sd = ck["actor_state_dict"] if "actor_state_dict" in ck else ck["model_state_dict"]
        self.register_buffer("mean", sd["obs_normalizer._mean"].to(device))
        self.register_buffer("std", sd["obs_normalizer._std"].to(device))
        idx = sorted({int(m.group(1)) for k in sd if (m := re.match(r"mlp\.(\d+)\.weight", k))})
        layers = []
        for i in idx:
            w, b = sd[f"mlp.{i}.weight"], sd[f"mlp.{i}.bias"]
            lin = torch.nn.Linear(w.shape[1], w.shape[0], device=device)
            lin.weight.data.copy_(w)
            lin.bias.data.copy_(b)
            layers.append(lin)
        self.layers = torch.nn.ModuleList(layers)
        self.obs_dim = int(self.layers[0].in_features)
        self.act_dim = int(self.layers[-1].out_features)
        self.iteration = int(ck.get("iter", -1))
        self.requires_grad_(False)
        self.eval()

    @torch.no_grad()
    def forward(self, obs: torch.Tensor) -> torch.Tensor:
        x = (obs - self.mean) / (self.std + _EPS)
        for lin in self.layers[:-1]:
            x = torch.nn.functional.elu(lin(x))
        return self.layers[-1](x)