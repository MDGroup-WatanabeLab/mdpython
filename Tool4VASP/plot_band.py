from pymatgen.io.vasp.outputs import Vasprun
from pymatgen.electronic_structure.plotter import BSPlotter
import matplotlib.pyplot as plt

vaspout = Vasprun("vasprun.xml")
bandstr = vaspout.get_band_structure(line_mode=True)
band = BSPlotter(bandstr).get_plot(ylim=[-20,20])

band.plot()

plt.savefig("band.png")

plt.show()