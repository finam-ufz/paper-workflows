"""
Bi-directional toy model using LAI and soil moisture (sm)
"""

import datetime as dt
import sys
from datetime import datetime, timedelta
from pathlib import Path

import finam as fm
import finam_plot as fmp
import matplotlib.pyplot as plt
from finam_graph import GraphDiagram

base = Path(__file__).parent.parent
sys.path.append(str(base / "src"))

import lai_component
import sm_component

start_date = datetime(1989, 1, 1)
time_step = timedelta(days=1)


# pre = pre.sel(xc=3973369.0, yc=2951847.0)
input_pre = fm.components.CsvReader(
    path=base / "data" / "pre.csv",
    time_column="time",
    outputs={"pre": "mm/day"},
    date_format=None,
    separator=",",
)
sm_bi = sm_component.SM(
    start=start_date,
    step=time_step,
    antecedent_sm=0.5,
    pre_factor=0.002,
    lai_factor=0.002,
)
lai_bi = lai_component.LAI(
    start=start_date, step=time_step, init_lai=2.5, factor_lai_sm=0.995
)
output_var = fm.components.CsvWriter(
    path=base / "results" / "output_bi.csv",
    time_column="time",
    inputs=["sm_bi", "lai_bi"],
    start=dt.datetime(1989, 1, 1),
    step=dt.timedelta(days=1),
    separator=",",
)

composition = fm.Composition(
    components=[
        input_pre,
        sm_bi,
        lai_bi,
        output_var,
    ]
)

# Bi-directional model coupling
input_pre["pre"] >> sm_bi.inputs["pre"]
lai_bi.outputs["lai"] >> sm_bi.inputs["lai"]
sm_bi.outputs["sm"] >> fm.adapters.DelayFixed(time_step) >> lai_bi.inputs["sm"]

# Saving info as CSV file
sm_bi.outputs["sm"] >> output_var.inputs["sm_bi"]
lai_bi.outputs["lai"] >> output_var.inputs["lai_bi"]


# Model composition diagram
diagram = GraphDiagram()
diagram.draw(composition, save_path=base / "results" / "graph_bi.svg")

composition.run(end_time=datetime(1993, 12, 31))

plt.show()
