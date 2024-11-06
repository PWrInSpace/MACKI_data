import os
import glob
import pandas as pd
from data_processing.case import Case


class Session:
    def __init__(self, session_data_folder: str):
        self._session_name = session_data_folder.split(os.sep)[-1]
        self._session_data_folder = os.path.join(session_data_folder, "app")
        self._case_folders = [f for f in glob.glob(self._session_data_folder + "/*") if os.path.isdir(f)]
        self._session_data_file = os.path.join(self._session_data_folder, "data.csv")
        self._session_data = pd.read_csv(self._session_data_file, delimiter=";")

        self._total_number_of_grasps = self._session_data["procedure_time"].diff().lt(0).sum()

        self._cases = [Case(f) for f in self._case_folders]

    @property
    def session_data_folder(self) -> str:
        return self._session_data_folder

    @property
    def session_name(self) -> str:
        return self._session_name

    @property
    def case_folders(self) -> list[str]:
        return self._case_folders

    @property
    def session_data_file(self) -> str:
        return self._session_data_file

    @property
    def session_data(self) -> pd.DataFrame:
        return self._session_data

    @property
    def total_number_of_grasps(self):
        return self._total_number_of_grasps

    @property
    def number_of_cases(self):
        return len(self._case_folders)
