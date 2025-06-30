from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
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

ds = xr.load_dataset(base / "results" / "pre.nc")

# Create a rectangular grid
x = ds["x"].data
y = ds["y"].data
X, Y = np.meshgrid(x, y)
Z = ds["pre"].data[-1]  # last time-step

# Plotting using pcolormesh
fig, ax = plt.subplots()
c = ax.pcolormesh(
    X, Y, Z, cmap="twilight", vmin=0, vmax=25, shading="auto", edgecolors="k"
)
quad_mesh = ax.collections[0]
quad_mesh.set_linewidth(0.5)

# Add a color bar
cbar = plt.colorbar(c, ax=ax, label="Precipitation (mm/day)", shrink=0.85)

# Set color limits on the ScalarMappable object
# c.set_clim(0, 60)
ax.set_aspect("equal")

# Add labels and title
plt.xlabel("X (km)")
plt.ylabel("Y (km)")
plt.title("30 days mean (8.12.1993 - 6.1.1994)")

# Force x and y ticks to be at integer values only
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))

# Display the plot
plt.tight_layout()
plt.savefig(base / "results" / "regrid_grid.pdf")
plt.show()
