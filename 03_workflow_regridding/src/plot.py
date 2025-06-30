from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

base = Path(__file__).parent.parent

# Read the CSV file
file_path = "path/to/your/csvfile.csv"
df1 = pd.read_csv(base / "results" / "in_ts.csv", sep=";", parse_dates=["time"])
df2 = pd.read_csv(base / "results" / "out_ts.csv", sep=";", parse_dates=["time"])

# Plotting
fig, ax = plt.subplots()
ax.step(df1["time"], df1["pre"], alpha=0.7, where="pre", label="daily")
ax.step(df2["time"], df2["pre"], color="k", where="pre", label="30 day mean")

# Major locators for every year
ax.xaxis.set_major_locator(mdates.YearLocator())
ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

# Minor locator for every month
ax.xaxis.set_minor_locator(mdates.MonthLocator())
ax.xaxis.set_minor_formatter(mdates.DateFormatter(""))

# Rotating date labels for better readability
plt.gcf().autofmt_xdate()

# Adding labels and title
plt.xlabel("Date")
plt.ylabel("Precipitation (mm/day)")
plt.title("Precipitation time series for a single cell")
plt.legend()

# Display the plot
plt.tight_layout()
plt.savefig(base / "results" / "time_series.pdf")
plt.show()
