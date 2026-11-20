#!/bin/sh
# P4 smoke runs (SPEC-003 section 9). Wall-clock start/end of each block are logged for the runtime projection.
set -e
cd "$(dirname "$0")/../.."
PY=${PY:-python}
for b in m3 m4; do
  echo "[smoke] block $b start $(date -u +%FT%T.%3NZ)"
  $PY 07_src/scripts/run_experiment.py --design main-$b-smoke --out results/main_smoke/$b --workers 2
  echo "[smoke] block $b end $(date -u +%FT%T.%3NZ)"
done
