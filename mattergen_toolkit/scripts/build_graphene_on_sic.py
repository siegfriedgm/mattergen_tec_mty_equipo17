import numpy as np
from ase.build import bulk, surface, graphene
from ase.io import write

a_sic = 4.3596
nlayers = 10
vacuum = 15.0
z_gap  = 3.30
m_sic = 4
m_gr  = 5

sic_bulk = bulk('SiC', crystalstructure='zincblende', a=a_sic)
slab = surface(sic_bulk, (1, 1, 1), nlayers)
slab.center(vacuum=vacuum, axis=2)
slab = slab.repeat((m_sic, m_sic, 1))

a_graphene = 2.46
gr = graphene(a=a_graphene).repeat((m_gr, m_gr, 1))

A = slab.get_cell()[:2, :2]
B = gr.get_cell()[:2, :2]
import numpy as np
scale_mat = A @ np.linalg.inv(B)
cell = gr.get_cell()
cell[:2, :2] = scale_mat @ B
gr.set_cell(cell, scale_atoms=True)

z_top = slab.positions[:, 2].max()
gr.translate([0, 0, z_top + z_gap - gr.positions[:, 2].min()])

hetero = slab + gr
hetero.set_pbc([True, True, False])

write('graphene_on_SiC.cif', hetero)
write('graphene_on_SiC.xyz', hetero)
write('POSCAR_graphene_on_SiC', hetero, format='vasp')

print("Listo: graphene_on_SiC.cif / .xyz / POSCAR_graphene_on_SiC")
