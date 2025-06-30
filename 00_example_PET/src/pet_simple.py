import datetime as dt
import sys
from pathlib import Path

import finam as fm
import finam_netcdf as fm_nc

base = Path(__file__).parent.parent
sys.path.append(str(base / "src"))

from component import PET

# config
start_time = dt.datetime(1990, 1, 1)
end_time = dt.datetime(1991, 1, 1)
day = dt.timedelta(days=1)
# components
pet = PET(start_time=start_time, step=day)
reader = fm_nc.NetCdfReader(base / "data/temp.nc")
writer = fm_nc.NetCdfTimedWriter(base / "results/pet.nc", inputs=["PET"], step=day)
# composition
composition = fm.Composition([pet, reader, writer])
# data flow
reader.outputs["tmin"] >> pet.inputs["tmin"]
reader.outputs["tmax"] >> pet.inputs["tmax"]
reader.outputs["lat"] >> pet.inputs["lat"]
pet.outputs["PET"] >> writer.inputs["PET"]
# execution
composition.run(end_time=end_time)
