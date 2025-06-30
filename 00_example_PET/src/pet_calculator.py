"""
Setup to calculate PET (PET) according to
George H. Hargreaves and Zohrab A. Samani (1985).
Check README.md file in '01_Hargreaves-Samani' folder for references and more information.
"""

import datetime as dt
import sys
from pathlib import Path

base = Path(__file__).parent.parent
sys.path.append(str(base / "src"))

import component
import finam as fm
import finam_netcdf as fm_nc
import finam_plot as fm_plt

# config
start_time = dt.datetime(1990, 1, 1)
end_time = dt.datetime(1991, 1, 1)
day = dt.timedelta(days=1)

# PET component
pet_calculator = component.PET(start_time=start_time, step=day)
# netcdf reader and writer
temp_reader = fm_nc.NetCdfReader(base / "data/temp.nc")
pet_writer = fm_nc.NetCdfTimedWriter(base / "results/pet.nc", inputs=["PET"], step=day)
# live viewer
pet_viewer = fm_plt.ColorMeshPlot(vmin=0.0, vmax=6.0, update_interval=10)

composition = fm.Composition([temp_reader, pet_calculator, pet_writer, pet_viewer])

# Model coupling
temp_reader.outputs["tmin"] >> pet_calculator.inputs["tmin"]
temp_reader.outputs["tmax"] >> pet_calculator.inputs["tmax"]
temp_reader.outputs["lat"] >> pet_calculator.inputs["lat"]
pet_calculator.outputs["PET"] >> pet_writer.inputs["PET"]
pet_calculator.outputs["PET"] >> pet_viewer.inputs["Grid"]

composition.run(end_time=end_time)
