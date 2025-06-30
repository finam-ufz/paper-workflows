"""
LAI component for the Bi-directional_toy-model
"""

from datetime import datetime, timedelta

import finam as fm
import numpy as np


class LAI(fm.TimeComponent):
    """
    Component for the calculation of LAI

    Args:
        start (datetime.datetime): Start date
        step (datetime.timedelta): time step
        init_lai (int, optional): initial value of LAI. Defaults to 3.
        factor_lai_sm (float, optional): Constant to account for the relationship
                            between lai and sm. Defaults to 0.5.

    Raises:
        ValueError: if start is not of type datetime
        ValueError: if step is not of type timedelta
    """

    def __init__(self, start, step, init_lai=3, factor_lai_sm=0.005):
        super().__init__()

        if not isinstance(start, datetime):
            raise ValueError("Start must be of type datetime")
        if not isinstance(step, timedelta):
            raise ValueError("Step must be of type timedelta")

        self.time = start
        self.step = step
        self.previous_lai = init_lai
        self.factor = factor_lai_sm

    @property
    def next_time(self):
        """Next pull time."""
        return self.time + self.step

    def _initialize(self):
        self.inputs.add(
            name="sm", time=self.time, grid=fm.NoGrid(), units="dimensionless"
        )

        # output Info will be generated during connection
        self.outputs.add(
            name="lai", time=self.time, grid=fm.NoGrid(), units="dimensionless"
        )

        self.create_connector()

    def _connect(self, start_time):
        push_data = {}
        if self.connector.all_data_pulled and self.connector.data_required["lai"]:
            push_data["lai"] = self.previous_lai

        self.try_connect(start_time=start_time, push_data=push_data)

    def _update(self):
        # capturing previous sm value
        previous_sm = self.inputs["sm"].pull_data(self.time)

        # Increment model time-step
        self.time = self.next_time

        # Run the model step here & calculate lai
        lai = lai_calculator(
            previous_lai=self.previous_lai,
            sm=fm.data.get_magnitude(previous_sm),
            factor_lai_sm=self.factor,
        )

        self.previous_lai = lai
        # Push model state to outputs
        self.outputs["lai"].push_data(lai, self.time)


def lai_calculator(previous_lai, sm, factor_lai_sm):
    xp = [0.0, 0.6, 1]
    fp = [0, 5, 3]
    return factor_lai_sm * previous_lai + (1 - factor_lai_sm) * np.interp(sm, xp, fp)
