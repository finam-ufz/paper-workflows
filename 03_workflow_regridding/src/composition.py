import datetime as dt

import finam as fm
import finam_netcdf as fm_nc
import finam_regrid as fm_rg
import finam_vtk as fm_vtk

base = Path(__file__).parent.parent

# IO specification
args_i = fm_vtk.read_aux_file(base / "data" / "pre.json")
pre_i = fm_vtk.DataArray("pre", units="mm d-1")
reader = fm_vtk.PVDReader(base / "data" / "pre.pvd", outputs=[pre_i], **args_i)

step = dt.timedelta(days=30)
grid = fm.UniformGrid((6, 5), (1, 1), axes_reversed=True)
pre_o = fm_nc.Variable("pre", grid=grid)
writer = fm_nc.NetCdfTimedWriter(base / "results" / "pre.nc", inputs=[pre_o], step=step)

# Adapters
method = fm_rg.RegridMethod.CONSERVE
regrid = fm_rg.Regrid(regrid_method=method)
mean = fm.adapters.AvgOverTime(step=0)

# Composition
comp = fm.Composition([reader, writer])
comp.initialize()

# Connections
reader["pre"] >> regrid >> mean >> writer["pre"]

# run for 61 * 30 days
comp.run(end_time=dt.datetime(1994, 1, 6))
