import os
import pandas as pd


class Procedure:
    TIME_COLUMN = "time (ms)"
    VELOCITY_COLUMN = "velocity"

    def __init__(self, procedure_folder: str):
        procedure_file_path = os.path.join(procedure_folder, "procedure.csv")

        with open(procedure_file_path, "r") as file:
            self._procedure_name = file.readline().strip().split(": ")[-1]
            self._pressurization_time = float(file.readline().strip().split(": ")[-1])
            self._depressurization_time = float(file.readline().strip().split(": ")[-1])

        self._procedure_profile = pd.read_csv(procedure_file_path, delimiter=";", skiprows=4)
        self._procedure_profile.columns = [self.TIME_COLUMN, self.VELOCITY_COLUMN]

    @property
    def procedure_name(self) -> str:
        return self._procedure_name

    @property
    def pressurization_time(self) -> int:
        return self._pressurization_time

    @property
    def depressurization_time(self) -> int:
        return self._depressurization_time

    @property
    def procedure_profile(self) -> pd.DataFrame:
        return self._procedure_profile

    @property
    def time(self) -> pd.DataFrame:
        return self._procedure_profile[self.TIME_COLUMN]

    @property
    def velocity(self) -> pd.DataFrame:
        return self._procedure_profile[self.VELOCITY_COLUMN]
