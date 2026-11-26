#!/usr/bin/env bash
# Submit every talk render group (scripts/talk/render_talk.sbatch), then compose with
#   nice -n 19 .venv/bin/python scripts/talk/compose_talk.py
set -euo pipefail
cd "$(dirname "$0")/../.."
for g in ${GROUPS_:-A1 A2 A3 A4 A5 A6 B1 B2 B3 B5}; do
  echo "$g $(GROUP=$g sbatch --parsable -J qc-talk-$g scripts/talk/render_talk.sbatch)"
done
