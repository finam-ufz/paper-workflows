from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import pyvista as pv
from matplotlib.ticker import MaxNLocator

SMALL_SIZE = 14
MEDIUM_SIZE = 14
BIGGER_SIZE = 16

plt.rc("font", size=SMALL_SIZE)  # controls default text sizes
plt.rc("axes", titlesize=BIGGER_SIZE)  # fontsize of the axes title
plt.rc("axes", labelsize=MEDIUM_SIZE)  # fontsize of the x and y labels
plt.rc("xtick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("ytick", labelsize=SMALL_SIZE)  # fontsize of the tick labels
plt.rc("legend", fontsize=SMALL_SIZE)  # legend fontsize
plt.rc("figure", titlesize=BIGGER_SIZE)  # fontsize of the figure title

base = Path(__file__).parent.parent

# load a triangular PyVista unstructured mesh
mesh = pv.read(base / "data" / "pre1824.vtu")

# Extract the points (vertices) and faces (connectivity)
points = mesh.points
cells = mesh.cell_connectivity.reshape((-1, 3))
scalars = mesh["pre"]
triangulation = tri.Triangulation(points[:, 0], points[:, 1], cells)

# Plotting
fig, ax = plt.subplots()
tripcolor = ax.tripcolor(
    triangulation, scalars, edgecolors="k", cmap="twilight", vmin=0, vmax=25
)
ax.set_xlim(points[:, 0].min(), points[:, 0].max())
ax.set_ylim(points[:, 1].min(), points[:, 1].max())
ax.set_aspect("equal")

# Add a color bar
plt.colorbar(tripcolor, ax=ax, label="Precipitation (mm/day)", shrink=0.85)

# Add labels and title
plt.xlabel("X (km)")
plt.ylabel("Y (km)")
plt.title("daily mean (30.12.1993)")

# Force x and y ticks to be at integer values only
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# Display the plot
plt.tight_layout()
plt.savefig(base / "results" / "regrid_mesh.pdf")
plt.show()
