#!/usr/bin/env bash
# generate_mattergen.sh
# Wrapper simple para generar estructuras con MatterGen del paquete,
# usando los checkpoints/configs del repo local.
#
# Ejemplo:
#   ./generate_mattergen.sh "Au C Si" 20 results_mg cuda
#
# Parámetros:
#   $1 -> elementos entre comillas (ej. "Au C Si")
#   $2 -> número de estructuras (default 20)
#   $3 -> carpeta de salida (default results_mg)
#   $4 -> dispositivo: cuda|cpu (default cuda)

set -euo pipefail

ELEMENTS="${1:-"Au C Si"}"
N="${2:-20}"
OUTDIR="${3:-results_mg}"
DEVICE="${4:-cuda}"

# rutas relativas al repo
CONFIG="sampling_conf/default.yaml"
CKPT="checkpoints/mattergen_base/checkpoints/last.ckpt"

echo "== generate_mattergen.sh =="
echo "Python: $(which python)"
echo "Elements: ${ELEMENTS}"
echo "Num: ${N}"
echo "Out: ${OUTDIR}"
echo "Device: ${DEVICE}"
echo "Config: ${CONFIG}"
echo "Checkpoint: ${CKPT}"

python -m mattergen.scripts.generate \
  --checkpoint "${CKPT}" \
  --config "${CONFIG}" \
  --num-structures "${N}" \
  --elements "${ELEMENTS}" \
  --device "${DEVICE}" \
  --output "${OUTDIR}" \
  --seed 42

echo "Archivos de salida en: ${OUTDIR}/"
