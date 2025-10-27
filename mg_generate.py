#!/usr/bin/env python3
"""
mg_generate.py
---------------------------------
"""

import argparse
import os
import shlex
import subprocess
import sys
from pathlib import Path
import datetime as _dt

def run(cmd: str):
    print(f"\n$ {cmd}")
    proc = subprocess.run(cmd, shell=True)
    if proc.returncode != 0:
        sys.exit(proc.returncode)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--elements", type=str, required=True,
                    help='Lista de elementos entre comillas, ej. "Au C Si"')
    ap.add_argument("--n", "--num-structures", dest="n", type=int, default=20,
                    help="Número de estructuras a generar (default: 20)")
    ap.add_argument("--out", "--output", dest="out", type=str, default="results_mg",
                    help="Carpeta de salida (default: results_mg)")
    ap.add_argument("--config", type=str, default="sampling_conf/default.yaml",
                    help="Ruta al archivo de configuración YAML de sampling")
    ap.add_argument("--ckpt", "--checkpoint", dest="ckpt", type=str,
                    default="checkpoints/mattergen_base/checkpoints/last.ckpt",
                    help="Ruta al checkpoint (.ckpt) del modelo")
    ap.add_argument("--device", type=str, default="cuda",
                    choices=["cuda","cpu"], help="Dispositivo (cuda o cpu)")
    ap.add_argument("--seed", type=int, default=42, help="Semilla aleatoria")
    args = ap.parse_args()

    repo_root = Path.cwd()
    cfg = repo_root / args.config
    ckpt = repo_root / args.ckpt
    out = repo_root / args.out
    out.mkdir(parents=True, exist_ok=True)

    # Mensajes de sanidad
    print("== MatterGen runner ==")
    print("Fecha:", _dt.datetime.now().isoformat(timespec="seconds"))
    print("Python:", sys.executable)
    print("Working dir:", repo_root.resolve())
    print("Config:", cfg)
    print("Checkpoint:", ckpt)
    print("Salida:", out)

    # Verificación de archivos requeridos
    missing = []
    if not cfg.is_file():
        missing.append(str(cfg))
    if not ckpt.is_file():
        missing.append(str(ckpt))
    if missing:
        print("\n[ERROR] No se encontraron estos archivos requeridos:")
        for m in missing:
            print(" -", m)
        sys.exit(2)

    # Verifica instalación del paquete 'mattergen' y PyTorch
    try:
        import mattergen  # type: ignore
        import torch  # type: ignore
        print(f"mattergen OK ({getattr(mattergen,'__version__','?')}); torch {torch.__version__}")
        if args.device == "cuda":
            if not torch.cuda.is_available():
                print("[ADVERTENCIA] CUDA no disponible. Forzando a CPU.")
                args.device = "cpu"
    except Exception as e:
        print("[ERROR] No se pudo importar 'mattergen' y/o 'torch'.")
        print("Detalle:", e)
        print("  pip install --index-url https://download.pytorch.org/whl/cu121 torch torchvision torchaudio")
        print("  pip install mattergen==1.0.3")
        sys.exit(3)

    # Construye comando CLI de mattergen del paquete
    cmd = [
        sys.executable, "-m", "mattergen.scripts.generate",
        "--checkpoint", str(ckpt),
        "--config", str(cfg),
        "--num-structures", str(args.n),
        "--elements", args.elements,
        "--device", args.device,
        "--output", str(out),
        "--seed", str(args.seed),
    ]

    run(" ".join(shlex.quote(c) for c in cmd))

    print("\nCIF/EXTXYZ:", out)

if __name__ == "__main__":
    main()
