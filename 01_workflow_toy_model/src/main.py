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
sm_constant_lai = sm_component.SM(
    start=start_date,
    step=time_step,
    antecedent_sm=0.5,
    pre_factor=0.002,
    lai_factor=0.002,
)
lai_bi = lai_component.LAI(
    start=start_date, step=time_step, init_lai=2.5, factor_lai_sm=0.995
)
constant_lai = fm.components.CallbackGenerator(
    callbacks={
        "lai": (
            lambda t: 2.5 * fm.UNITS.Unit("dimensionless"),
            fm.Info(time=None, grid=fm.NoGrid(), units="dimensionless"),
        )
    },
    start=start_date,
    step=time_step,
)
output_var = fm.components.CsvWriter(
    path=base / "results" / "output.csv",
    time_column="time",
    inputs=["pre", "sm_bi", "lai_bi", "sm_constant_lai", "constant_lai"],
    start=dt.datetime(1989, 1, 1),
    step=dt.timedelta(days=1),
    separator=",",
)
plot = fmp.TimeSeriesPlot(
    {
        # "pre": "mm/day", # commented for better sm and lai plot visualization
        "sm_bi": "dimensionless",
        "lai_bi": "dimensionless",
        "sm_constant_lai": "dimensionless",
        "constant_lai": "dimensionless",
    },
    colors=["black", "green", "blue", "red"],
    title="Bi-directional VS one way toy model",
)

composition = fm.Composition(
    components=[
        input_pre,
        sm_bi,
        lai_bi,
        sm_constant_lai,
        constant_lai,
        output_var,
        # plot,
    ]
)

# Bi-directional model coupling
input_pre["pre"] >> sm_bi.inputs["pre"]
lai_bi.outputs["lai"] >> sm_bi.inputs["lai"]
sm_bi.outputs["sm"] >> fm.adapters.DelayFixed(time_step) >> lai_bi.inputs["sm"]

# One way model copling
input_pre["pre"] >> sm_constant_lai.inputs["pre"]
constant_lai.outputs["lai"] >> sm_constant_lai.inputs["lai"]

# Saving info as CSV file
input_pre["pre"] >> output_var.inputs["pre"]
sm_bi.outputs["sm"] >> output_var.inputs["sm_bi"]
lai_bi.outputs["lai"] >> output_var.inputs["lai_bi"]
sm_constant_lai.outputs["sm"] >> output_var.inputs["sm_constant_lai"]
constant_lai.outputs["lai"] >> output_var.inputs["constant_lai"]

# Ploting
# input_pre["pre"] >> plot["pre"] # commented for better sm and lai plot visualization
# sm_bi.outputs["sm"] >> plot["sm_bi"]
# lai_bi.outputs["lai"] >> plot["lai_bi"]
# sm_constant_lai.outputs["sm"] >> plot["sm_constant_lai"]
# constant_lai.outputs["lai"] >> plot["constant_lai"]

# Model composition diagram
diagram = GraphDiagram()
diagram.draw(composition, save_path=base / "results" / "graph.svg")

composition.run(end_time=datetime(1993, 12, 31))

plt.show()
