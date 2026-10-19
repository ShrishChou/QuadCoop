#!/bin/bash
# One-time setup on Engaging. Run from the repo root on a LOGIN node (needs internet):
#
#   bash slurm/setup_engaging.sh
#
# Creates .venv/ with Python 3.12, installs mjlab (pinned) + this package, and
# fetches the robot models. Takes ~10-15 min, mostly downloading PyTorch.
set -euo pipefail
cd "$(dirname "$0")/.."

# uv manages Python itself, so no conda/module is needed.
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
  export PATH="$HOME/.local/bin:$PATH"
fi

# Keep uv's download cache off the home quota if you have pool storage, e.g.
#   export UV_CACHE_DIR=/orcd/pool/$USER/uv-cache
uv venv --python 3.12 .venv
# shellcheck disable=SC1091
source .venv/bin/activate

# Install a CUDA 12.8 PyTorch build first. PyPI's default Linux wheel now targets
# CUDA 13, which needs a newer NVIDIA driver than many clusters run. If the smoke
# test reports "driver is too old", rerun with TORCH_CUDA=cu126.
uv pip install torch --index-url "https://download.pytorch.org/whl/${TORCH_CUDA:-cu128}"
# --no-sources: ignore mjlab's own uv index overrides (NVIDIA index for warp-lang); PyPI has it.
uv pip install --no-sources -e .

python scripts/fetch_assets.py
python -c "import mjlab, mujoco, warp, torch; print('mjlab ok | mujoco', mujoco.__version__, '| warp', warp.__version__, '| torch', torch.__version__)"

mkdir -p logs/slurm
echo
echo "Setup done. Next: sbatch slurm/smoke.sbatch   (GPU check, ~5 min)"
