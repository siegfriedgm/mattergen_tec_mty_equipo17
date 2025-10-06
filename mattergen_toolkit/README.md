# MatterGen Toolkit — Generación Au+C (metálico) y utilidades

Este paquete contiene **comandos y scripts** para:
1) Ejecutar MatterGen en macOS con Apple Silicon evitando errores MPS.
2) Generar muchas muestras **metálicas** y **filtrar** solo las que contienen **Au y C**.
3) (Opcional) Acelerar el muestreo con un sampler ligero (200 pasos).
4) (Opcional) Construir una heteroestructura **grafeno sobre SiC(111)**.

## 0) Variables de entorno

**A — MPS con fallback a CPU**
```bash
export WANDB_DISABLED=true
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTORCH_ENABLE_MPS_FALLBACK=1
```

**B — CPU puro**
```bash
export WANDB_DISABLED=true
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export PYTORCH_MPS_DISABLE=1
```

## 1) Generar Au+C metálico

**Normal (1000 pasos):**
```bash
bash scripts/generate_auc.sh results_AuC 20
```

**Rápido (200 pasos):**
```bash
bash scripts/generate_auc_fast.sh results_AuC_fast 20
```

## 2) Filtrar por composición (Au y C)

```bash
python scripts/filter_auc.py results_AuC/generated_crystals_cif.zip results_AuC/filtered_AuC_only.zip
```

## 3) Visualización (opcional)
```bash
pip install py3Dmol ase
python scripts/view_cif_py3dmol.py results_AuC/filtered_AuC_only.zip
```

## 4) (Extra) Grafeno sobre SiC(111)
```bash
pip install ase numpy
python scripts/build_graphene_on_sic.py
```
