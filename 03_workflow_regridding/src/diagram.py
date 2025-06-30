import datetime as dt
from pathlib import Path

import finam as fm
import finam_graph as fm_gr
import finam_netcdf as fm_nc
import finam_regrid as fm_rg
import finam_vtk as fm_vtk

base = Path(__file__).parent.parent

# 30 days mean
step = dt.timedelta(days=30)

# IO specification
pre = fm_vtk.DataArray("pre", units="mm d-1")
args = fm_vtk.read_aux_file(base / "data" / "pre.json")
reader = fm_vtk.PVDReader(base / "data" / "pre.pvd", outputs=[pre], **args)
writer = fm_nc.NetCdfTimedWriter(
    base / "results" / "pre1.nc", step=step, inputs=["pre"]
)

# Adapters
grid = fm.UniformGrid((6, 5), (1.0, 1.0), axes_reversed=True)
regrid = fm_rg.Regrid(out_grid=grid, regrid_method=fm_rg.RegridMethod.CONSERVE)
mean = fm.adapters.AvgOverTime(step=0.0)

# Composition
comp = fm.Composition([reader, writer])
comp.initialize()

# Connections
reader["pre"] >> regrid >> mean >> writer["pre"]

sizes = fm_gr.GraphSizes(margin=0)
diagram = fm_gr.GraphDiagram(sizes=sizes, max_label_length=13)
labels = {
    reader: "VTK reader",
    writer: "NetCDF writer",
    regrid: "regridder",
    mean: "mean",
}
positions = {
    reader: (0, 1),
    writer: (1, 0),
    regrid: (1, 1),
    mean: (0, 0),
}
diagram.draw(
    comp,
    labels=labels,
    positions=positions,
    figsize=(4, 2.5),
    save_path=base / "results" / "regrid_graph.pdf",
)
# run for 60 * 30 days
# comp.run(end_time=dt.datetime(1993, 12, 6))
