#!/usr/bin/env bash
set -euo pipefail
OUTDIR="${1:-results_AuC}"
NUM="${2:-20}"
mattergen-generate "$OUTDIR/"   --pretrained-name dft_band_gap   --batch_size=1   --num_batches="$NUM"   --properties_to_condition_on='{"dft_band_gap":{"target":0.0,"tolerance":0.1}}'
