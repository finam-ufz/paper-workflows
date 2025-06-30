import tempfile
# import finam_graph
from datetime import datetime, timedelta

import finam as fm
from bodium_module import bodium
from finam_ogs6.ogs6_model import CouplingInfo, OGS6Model

project_file = "BodiumOGS/OGS/simulation_modell/AdvectionDiffusionSorptionDecay.prj"
ogs_input_coupling_info = [
    CouplingInfo(
        mesh_name="Top1And2",
        variable_name="concentration",
        data_location="CELLS",
        unit="",
    ),
]
ogs_output_coupling_info = []

output_dir = tempfile.mkdtemp()
ogs_start_time = datetime(2000, 1, 1)

ogs_model = OGS6Model(
    ogs_start_time,
    step=timedelta(days=1),
    project_file=project_file,
    output_dir=output_dir,
    input_coupling_info=ogs_input_coupling_info,
    output_coupling_info=ogs_output_coupling_info,
)

start_time = datetime(2000, 1, 1)
bodium_model = bodium.Bodium(start_time, step=timedelta(days=1))

# create a composition of ogs model and Bodium generator
composition = fm.Composition([ogs_model, bodium_model])

# couple Bodium outputs to OGS6 inputs
(
    bodium_model.outputs["Nout"]
    >> fm.adapters.RegridLinear()
    >> ogs_model.inputs[ogs_input_coupling_info[0].mesh_name]
)

# diagram = finam_graph.GraphDiagram()
# diagram.draw(composition, save_path="graph.svg")

composition.run(end_time=datetime(2001, 12, 31))
