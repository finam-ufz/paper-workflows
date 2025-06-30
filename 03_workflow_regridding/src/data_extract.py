import datetime as dt
from pathlib import Path

import finam as fm
import finam_netcdf as fm_nc
import finam_regrid as fm_rg
import finam_vtk as fm_vtk


def val_select(grid):
    return grid[0][151]


base = Path(__file__).parent.parent

# 30 days mean
day = dt.timedelta(days=1)
step = 30 * day

# IO specification
pre = fm_vtk.DataArray("pre", units="mm d-1")
args = fm_vtk.read_aux_file(base / "data" / "pre.json")
reader = fm_vtk.PVDReader(base / "data" / "pre.pvd", outputs=[pre], **args)

writer1 = fm.components.CsvWriter(
    base / "results" / "in_ts.csv",
    inputs=["pre"],
    start=dt.datetime(1989, 1, 2),
    step=day,
)
writer2 = fm.components.CsvWriter(
    base / "results" / "out_ts.csv",
    inputs=["pre"],
    start=dt.datetime(1989, 1, 2),
    step=step,
)

# Adapters
value1 = fm.adapters.GridToValue(val_select)
value2 = fm.adapters.GridToValue(val_select)
mean = fm.adapters.AvgOverTime(step=0.0)

# Composition
comp = fm.Composition([reader, writer1, writer2])
comp.initialize()

# Connections
reader["pre"] >> value1 >> writer1["pre"]
reader["pre"] >> value2 >> mean >> writer2["pre"]

# run for 60 * 30 days
comp.run(end_time=dt.datetime(1994, 1, 6))
