import os
import pandas as pd
import glob
from data_processing.procedure import Procedure


class Case:
    ZERO_G_THRESHOLD = 0.08

    def __init__(self, case_folder: str):
        self._case_folder = case_folder
        self._case_data_file = os.path.join(case_folder, "data.csv")
        self._case_data = pd.read_csv(self._case_data_file, delimiter=";")
        self._case_data["datetime"] = pd.to_datetime(
            self._case_data["datetime"], format="%Y-%m-%d_%H-%M-%S.%f"
        )

        self._video_files = glob.glob(case_folder + "/*.mp4")

        self._case_procedure_name = self._case_folder[50:]

        self._procedure = Procedure(self._case_folder)

        self._case_data_zero_g = self._case_data[self._case_data["acc_z"] < self.ZERO_G_THRESHOLD]

        self._number_of_attempts = self._case_data_zero_g["procedure_time"].diff().lt(0).sum()
        self._number_of_attempts -= 1  # If the last attempt is not completed, it is not counted

    @property
    def case_folder(self) -> str:
        return self._case_folder

    @property
    def case_data_file(self) -> str:
        return self._case_data_file

    @property
    def case_data(self) -> pd.DataFrame:
        return self._case_data

    @property
    def case_data_zero_g(self) -> pd.DataFrame:
        return self._case_data_zero_g

    @property
    def zero_g_duration(self) -> float:
        if self._case_data_zero_g.empty:
            return None
        return (
            (self._case_data_zero_g["time"].max() - self._case_data_zero_g["time"].min()) / 1000).round(2)

    @property
    def case_procedure_name(self) -> str:
        return self._case_procedure_name

    @property
    def number_of_attempts(self):
        return self._number_of_attempts