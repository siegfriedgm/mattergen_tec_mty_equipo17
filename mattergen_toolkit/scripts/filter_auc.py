import sys, zipfile
from pymatgen.core import Structure

if len(sys.argv) < 3:
    print("Uso: python scripts/filter_auc.py <zip_entrada> <zip_salida>")
    sys.exit(1)

zip_in, zip_out = sys.argv[1], sys.argv[2]
keep = []
with zipfile.ZipFile(zip_in) as zin, zipfile.ZipFile(zip_out, "w") as zout:
    for name in zin.namelist():
        if not name.lower().endswith(".cif"):
            continue
        s = Structure.from_str(zin.read(name).decode(), fmt="cif")
        elems = {str(e) for e in s.composition.elements}
        if elems == {"Au","C"}:
            keep.append(name)
            zout.writestr(name, zin.read(name))
print("Estructuras Au+C:", keep if keep else "NINGUNA (genera más num_batches o repite corrida)")
