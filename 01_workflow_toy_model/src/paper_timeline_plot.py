from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.ticker import ScalarFormatter

base = Path(__file__).parent.parent

# Read CSV file
df = pd.read_csv(
    base / "results" / "output.csv", parse_dates=["time"], index_col="time"
)

# Create a figure with two subplots (2 rows, 1 column)
fig, axs = plt.subplots(2, 1, figsize=(10, 8), gridspec_kw={"height_ratios": [1, 3]})

# Plot 1: Bar plot with everything on top
bars = axs[0].bar(df.index, df["pre"], bottom=None, color="black")
# axs[0].invert_yaxis()
axs[0].set_yticks(np.arange(max(df["pre"]), 0, -5))
axs[0].set_ylabel("Precipitation (mm/day)")

# Set Y-axis labels for the pre plot as rounded numbers with 0 decimals
axs[0].yaxis.set_major_formatter(ScalarFormatter(useOffset=False, useMathText=True))
axs[0].get_yaxis().set_major_formatter(
    plt.FuncFormatter(lambda x, loc: "{:.0f}".format(x))
)

# Hide the bottom X-axis ticks and labels for the bar plot
axs[0].set_xticks([])
axs[0].set_xticklabels([])

# Plot 2: Timeline plot for lai_bi, constant_lai, sm_bi, and sm_constant_lai
(line1,) = axs[1].plot(df.index, df["lai_bi"], label="LAI", color="C0", linestyle="--")
(line2,) = axs[1].plot(
    df.index, df["constant_lai"], label="Constant LAI", color="C1", linestyle="--"
)
axs[1].set_ylabel("LAI (m²/m²)", color="black")
axs[1].tick_params("y", colors="black")

ax2 = axs[1].twinx()
(line3,) = ax2.plot(df.index, df["sm_bi"], label="SM", color="C0")
(line4,) = ax2.plot(
    df.index, df["sm_constant_lai"], label="SM at constant LAI", color="C1"
)
ax2.set_ylabel("SM (mm/mm)", color="black")
ax2.tick_params("y", colors="black")

# Set X axis label
axs[1].set_xlabel("Time")

# Combine legends
lines = [line1, line2, line3, line4]
labels = [line.get_label() for line in lines]
axs[1].legend(lines, labels, loc="upper left")

# Adjust layout to prevent clipping of ylabel
plt.tight_layout()

# Save the combined plot in the current directory as a PNG file
plt.savefig(base / "results" / "bi_directional_toy_model_timeline.png")

# Show the combined plot
plt.show()
