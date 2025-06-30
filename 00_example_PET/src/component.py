"""
Component for the calculation of Potential PET (PET)
according to George H. Hargreaves and Zohrab A. Samani (1985).
Check README.md file in '01_Hargreaves-Samani' folder for references and more information.
"""

from datetime import datetime, timedelta

import finam as fm
import numpy as np


class PET(fm.TimeComponent):
    """
    Component for the calculation of Potential (PET).

    Parameters
    ----------
    start_time : datetime.datetime
        start time
    step : datetime.timedelta
        time step
    ket : float, optional
        Hargreaves-Samani parameter, by default 0.0023

    Raises
    ------
    ValueError
        if start is not of type datetime
    ValueError
        if step is not of type timedelta
    """

    def __init__(self, start_time, step, ket=0.0023):
        super().__init__()

        if not isinstance(start_time, datetime):
            raise ValueError("Start time must be of type datetime")
        if not isinstance(step, timedelta):
            raise ValueError("Step must be of type timedelta")

        self.time = start_time
        self.step = step
        self.ket = ket

    def _next_time(self):
        """Next pull time."""
        return self.time + self.step

    def _initialize(self):
        self.inputs.add(name="tmin", time=self.time, grid=None, units="degC")
        self.inputs.add(name="tmax", time=self.time, grid=None, units="degC")
        self.inputs.add(name="lat", time=None, static=True, grid=None, units="radians")
        # output Info will be generated during connection
        self.outputs.add(name="PET")
        self.create_connector(
            pull_data=self.inputs.names,
            out_info_rules={
                "PET": [
                    fm.tools.FromInput("tmin", ["grid", "time"]),
                    fm.tools.FromValue("units", "mm/day"),
                ]
            },
        )

    def _connect(self, start_time):
        push_data = {}
        if self.connector.all_data_pulled and self.connector.data_required["PET"]:
            push_data["PET"] = self._calc_pet(self.connector.in_data)
        self.try_connect(start_time=start_time, push_data=push_data)

    def _calc_pet(self, data):
        return pet_calculator(
            t_min=fm.data.get_magnitude(data["tmin"]),
            t_max=fm.data.get_magnitude(data["tmax"]),
            lat=fm.data.get_magnitude(data["lat"]),
            time=self.time,
            ket=self.ket,
        )

    def _update(self):
        # Increment model time
        self.time = self.next_time
        # Retrieve inputs
        data = {i: self[i].pull_data(self.time) for i in self.inputs}
        # calculate PET for the current time step
        pet = self._calc_pet(data)
        # Push model state to outputs
        self.outputs["PET"].push_data(pet, self.time)


def pet_calculator(t_min, t_max, lat, time, ket=0.0023, t_avg=None):
    """
    Calculation of Potential Evapotranspiration (PET)
    according to George H. Hargreaves and Zohrab A. Samani (1985).

    Parameters
    ----------
    t_min : numpy.ndarray
        minimum temperature data set in °C.
    t_max : numpy.ndarray
        maximum temperature data set in °C.
    time : datetime.datatime
        Timestamp for the data.
    lat : numpy.ndarray
        latitude for the data set in radians.
    ket : float, optional
        Calibration coefficient to account for units.
        Default is 0.0023.
    t_avg : numpy.ndarray, optional
        average temperature data set in °C.
        Default is None.

    Returns
    -------
    numpy.ndarray
        Potential Evapotranspiration (PET) data.
    """
    t_dif = t_max - t_min

    if t_avg is None:
        t_avg = t_min + t_dif / 2

    e_rad = e_rad_calculator(time, lat)

    return ket * (t_avg + 17.8) * t_dif**0.5 * e_rad


def e_rad_calculator(time, lat):
    """
    Calculation of Extraterrestrial radiation
    according to John A. Duffie (Deceased) and William A. Beckman (2013).

    Parameters
    ----------
    time : datetime.datatime
        Timestamp for the data.
    lat : numpy.ndarray
        latitude for the data set in radians.

    Returns
    -------
    numpy.ndarray
        Extraterrestrial radiation data in mm/day.
    """

    # converting current time to Day-of-year(doy)
    doy = time.timetuple().tm_yday

    # relative distance between sun and earth
    dist = 1 + 0.033 * (np.cos(((2 * np.pi * doy) / 365)))

    # solar declination
    dec = np.radians(23.45 * np.sin(360 / 365 * (doy + 284) * np.pi / 180))

    # sunset hour angle
    ang = np.arccos(np.maximum(-1, np.minimum(1, -np.tan(lat) * np.tan(dec))))

    # extraterrestrial radiation (mm/day)
    e_rad = ang * np.sin(lat) * np.sin(dec) + np.cos(lat) * np.cos(dec) * np.sin(ang)

    return 15.3351 * dist * e_rad
