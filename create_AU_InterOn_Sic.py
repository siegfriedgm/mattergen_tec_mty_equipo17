#!/usr/bin/env python3

"""
v4: Graphene / Au intercalated / SiC(111)
- Slab SiC(111) via pymatgen
- Fixed matching: 5x5 graphene over 4x4 SiC(111) (≈0.5-1% mismatch)
- Au monolayer intercalated (registry top/fcc/hcp)
- Dimensionality check (Larsen)
- CIF + CSV summary
"""

import math
import numpy as np
import pandas as pd
from pathlib import Path

from ase.atoms import Atoms
from ase.io import write
from ase.build import make_supercell
from ase.geometry import cell_to_cellpar

from pymatgen.core import Lattice, Structure
from pymatgen.core.surface import SlabGenerator
from pymatgen.io.ase import AseAtomsAdaptor
from pymatgen.analysis.dimensionality import get_dimensionality_larsen

# ---------- User parameters ----------
OUT_DIR = Path("au_graphene_sic_v4_out")
OUT_DIR.mkdir(exist_ok=True)

# SiC slab
SIC_A = 4.3596
SIC_LAYERS = 6
VACUUM = 20.0

# Graphene
GRAPHENE_A = 2.46

# Fixed matching supercells (validated)
SIC_MULT = (4, 4)
G_MULT = (5, 5)

# Intercalation distances (initial)
SEP_AU_SIC = 2.8
SEP_G_AU = 3.3

# Registry lateral for Au
AU_REGISTRY = "fcc"  # "top" | "fcc" | "hcp"
# -----------------------------------


def build_sic_111():
    lat = Lattice.cubic(SIC_A)
    bulk = Structure(
        lattice=lat,
        species=["Si", "C"],
        coords=[[0,0,0],[0.25,0.25,0.25]],
    )
    min_slab = max(8.0, SIC_LAYERS * 2.0)
    sg = SlabGenerator(
        initial_structure=bulk,
        miller_index=(1,1,1),
        min_slab_size=min_slab,
        min_vacuum_size=VACUUM,
        center_slab=True,
        in_unit_planes=True,
        primitive=True,
    )
    slab = sg.get_slab()
    sic_atoms = AseAtomsAdaptor.get_atoms(slab)

    cell = sic_atoms.cell.copy()
    cell[2,2] = VACUUM
    sic_atoms.set_cell(cell)
    return sic_atoms


def build_graphene():
    positions = [(0.0,0.0,0.0),(1/3,2/3,0.0)]
    cell = [[GRAPHENE_A,0,0],
            [GRAPHENE_A/2,GRAPHENE_A*math.sqrt(3)/2,0],
            [0,0,VACUUM]]
    g = Atoms("C2",
              scaled_positions=positions,
              cell=cell,
              pbc=[True,True,True])
    g.positions[:,2] += VACUUM/2
    return g


def shift_registry(au: Atoms, mode=AU_REGISTRY):
    shifts = {"top": (0,0),"fcc": (1/3,1/3),"hcp": (2/3,2/3)}
    dx,dy = shifts.get(mode,(0,0))
    au.wrap()
    s = au.get_scaled_positions()
    s[:,0] = (s[:,0] + dx) % 1.0
    s[:,1] = (s[:,1] + dy) % 1.0
    au.set_scaled_positions(s)
    return au


def is_2d(at: Atoms):
    try:
        dim = get_dimensionality_larsen(AseAtomsAdaptor.get_structure(at), bonds="crystal")
        return dim == 2
    except:
        return False


def main():
    sic = build_sic_111()
    sic_sc = make_supercell(sic, [[SIC_MULT[0],0,0],[0,SIC_MULT[1],0],[0,0,1]])

    g = build_graphene()
    g_sc = make_supercell(g, [[G_MULT[0],0,0],[0,G_MULT[1],0],[0,0,1]])

    cell = sic_sc.cell.copy()
    cell[2,2] = VACUUM
    sic_sc.set_cell(cell)
    g_sc.set_cell(cell, scale_atoms=True)

    au = Atoms("Au2",
                scaled_positions=[(0,0,0),(1/3,2/3,0)],
                cell=[cell[0],cell[1],[0,0,VACUUM]],
                pbc=[True,True,True])

    au = shift_registry(au)

    sic_sc.positions[:,2] = 2 + sic_sc.positions[:,2] - np.min(sic_sc.positions[:,2])
    au.positions[:,2] = np.max(sic_sc.positions[:,2]) + SEP_AU_SIC
    g_sc.positions[:,2] = np.max(au.positions[:,2]) + SEP_G_AU

    stack = sic_sc + au + g_sc
    stack.set_cell(cell)
    stack.wrap()

    sa,sb,*_ = cell_to_cellpar(sic_sc.cell)
    ga,gb,*_ = cell_to_cellpar(g_sc.cell)
    mis_a = abs(ga-sa)/sa
    mis_b = abs(gb-sb)/sb
    mismatch = max(mis_a,mis_b)*100

    dim2d = is_2d(stack)

    cif = f"Au_G_SiC111_v4_mis{mismatch:.2f}pct_{AU_REGISTRY}.cif"
    write(OUT_DIR/cif, stack)

    pd.DataFrame([{
        "file": cif,
        "mismatch_pct": round(mismatch,3),
        "sep_Au_SiC": SEP_AU_SIC,
        "sep_G_Au": SEP_G_AU,
        "registry": AU_REGISTRY,
        "dimensionality_is_2D": bool(dim2d)
    }]).to_csv(OUT_DIR/"summary.csv", index=False)

    print("Generado CIF:")
    print(" ", OUT_DIR/cif)
    print(f"  mismatch ≈ {mismatch:.2f}%")
    print(f"  2D: {dim2d}")


if __name__ == "__main__":
    main()