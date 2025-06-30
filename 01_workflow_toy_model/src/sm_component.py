"""
soil moisture component for the Bi-directional_toy-model
"""

from datetime import datetime, timedelta

import finam as fm
import numpy as np


class SM(fm.TimeComponent):
    """
    Component for the calculation of soil moisture (sm)

    Args:
        start (datetime.datetime): Start date
        step (datetime.timedelta): time step
        antecedent_sm (float, optional): antecedent soil moisture. Defaults to 0.3.
        C (float, optional): Constant to account for the soil type and
                            vegetation characteristics. Defaults to 0.002.

    Raises:
        ValueError: if start is not of type datetime
        ValueError: if step is not of type timedelta
    """

    def __init__(
        self, start, step, antecedent_sm=0.3, pre_factor=0.002, lai_factor=0.004
    ):
        super().__init__()

        if not isinstance(start, datetime):
            raise ValueError("Start must be of type datetime")
        if not isinstance(step, timedelta):
            raise ValueError("Step must be of type timedelta")

        self.time = start
        self.step = step
        self.previous_sm = antecedent_sm
        self.pre_factor = pre_factor
        self.lai_factor = lai_factor

    @property
    def next_time(self):
        """Next pull time."""
        return self.time + self.step

    def _initialize(self):
        self.inputs.add(name="pre", time=self.time, grid=fm.NoGrid(), units="mm/day")
        self.inputs.add(
            name="lai", time=self.time, grid=fm.NoGrid(), units="dimensionless"
        )

        # output Info will be generated during connection
        self.outputs.add(
            name="sm", time=self.time, grid=fm.NoGrid(), units="dimensionless"
        )

        self.create_connector(pull_data=self.inputs.names)

    def _connect(self, start_time):
        push_data = {}
        if self.connector.all_data_pulled and self.connector.data_required["sm"]:
            in_data = self.connector.in_data
            init_sm = self.previous_sm
            sm_calculator(
                pre=fm.data.get_magnitude(in_data["pre"]),
                lai=fm.data.get_magnitude(in_data["lai"]),
                previous_sm=self.previous_sm,
                pre_factor=self.pre_factor,
                lai_factor=self.lai_factor,
            )
            push_data["sm"] = init_sm

        self.try_connect(start_time=start_time, push_data=push_data)

    def _update(self):
        # Increment model time
        self.time = self.next_time

        # Retrieve inputs
        pre = self.inputs["pre"].pull_data(self.time)
        lai = self.inputs["lai"].pull_data(self.time)

        # Run the model step here & calculate sm
        sm = sm_calculator(
            pre=fm.data.get_magnitude(pre),
            lai=fm.data.get_magnitude(lai),
            previous_sm=self.previous_sm,
            pre_factor=self.pre_factor,
            lai_factor=self.lai_factor,
        )

        self.previous_sm = sm
        # Push model state to outputs
        self.outputs["sm"].push_data(sm, self.time)


def sm_calculator(pre, lai, previous_sm, pre_factor, lai_factor):
    return np.clip(previous_sm + (pre_factor * pre) - (lai_factor * lai), 0, 1)
