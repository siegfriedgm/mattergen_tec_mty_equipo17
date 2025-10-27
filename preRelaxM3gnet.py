from pathlib import Path
from pymatgen.io.ase import AseAtomsAdaptor
from ase.io import read, write
from matgl.ext.ase import Relaxer
import os

# carpeta de salida
OUT = Path("pre_relaxed")
OUT.mkdir(exist_ok=True)

# archivo input CIF desde v4
cif = "au_graphene_sic_v4_out/Au_G_SiC111_v4_mis0.00pct_fcc.cif"

# cargar
atoms = read(cif)
structure = AseAtomsAdaptor.get_structure(atoms)

# Relaxer
relaxer = Relaxer()
result = relaxer.relax(structure)

final_structure = result["final_structure"]
relaxed = AseAtomsAdaptor.get_atoms(final_structure)

write(OUT/"relaxed.cif", relaxed)
write(OUT/"relaxed.xyz", relaxed)

print("✅ Pre-relax completado")
print("  →", OUT/"relaxed.cif")