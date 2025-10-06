#!/usr/bin/env bash
set -euo pipefail
OUTDIR="${1:-results_AuC_fast}"
NUM="${2:-20}"
SAMPLER="${3:-sampling_conf/fast_pc.yaml}"
mattergen-generate "$OUTDIR/"   --pretrained-name dft_band_gap   --batch_size=1   --num_batches="$NUM"   --sampling_config_path "$SAMPLER"   --properties_to_condition_on='{"dft_band_gap":{"target":0.0,"tolerance":0.1}}'
