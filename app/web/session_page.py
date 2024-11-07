import streamlit as st
from data_processing.session import Session
import os
import pandas as pd
import altair as alt


class SessionPage():
    def __init__(self, session: Session):
        self.session = session

        page_title = self.session.session_name.capitalize().replace("_", " ")
        self.page = st.Page(self._page, title=page_title, url_path=page_title)

    def _page(self):
        cases_names = [f"Case {i}" for i in range(self.session.number_of_cases)]
        session_elements = ["Session data"] + cases_names
        st.sidebar.radio(
            "Session elements", session_elements, key="session_elements"
        )
        st.sidebar.s

        if st.session_state.session_elements == "Session data":
            self._session_data()
        else:
            self._case_data(st.session_state.session_elements)

    def _session_data(self):
        st.title("Session: " + self.session.session_name)
        col1, col2 = st.columns(2)
        col1.metric("Total number of grasps", self.session.total_number_of_grasps)
        col2.metric("Cases in session", self.session.number_of_cases)

        # Convert datetime to minutes starting from minute 0
        self.session.session_data['minutes'] = (self.session.session_data['datetime'] - self.session.session_data['datetime'].min()).dt.total_seconds() / 60
        st.line_chart(self.session.session_data, x="datetime", y="acc_z", x_label="Time [minutes]", y_label="Acceleration [g]")

    def _case_data(self, case_names):
        case = self.session._cases[int(case_names.split(" ")[1])]
        col1, col2 = st.columns(2)
        col1.markdown(f"Case folder: **{case.case_folder.split(os.sep)[-1]}**")
        c1, c2 = col1.columns(2)
        c1.metric("Methode", case.case_procedure_name)
        c2.metric("Number of correct attempts", case.number_of_attempts)

        c1, c2 = col1.columns(2)
        c1.metric("Max force [grams]", case.case_data["load_cell"].max().round(2))
        c2.metric("Zero-G duration [s]", case.zero_g_duration)
        self.procedure_stplot(case._procedure, col2)

        col1, col2 = st.columns(2)
        data_zero_g = case.case_data[case.case_data["acc_z"] < 0.08]
        col1.line_chart(data_zero_g, x="time", y="acc_z")
        col2.line_chart(data_zero_g, x="time", y="load_cell")

        st.line_chart(data_zero_g, x="time", y=["pressure_tank", "pressure_macki"], x_label="Time [ms]", y_label="Pressure [bar]")

        video_files = case.video_files
        columns = st.columns(len(video_files))
        if video_files:
            for col1, video_file in zip(columns, video_files):
                col1.video(video_file)

    def procedure_stplot(self, procedure, col):
        # Prepare the main data for the line chart
        velocity = pd.DataFrame({
            'Time': procedure.time,
            'Velocity': procedure.velocity,
            'label': ['Velocity'] * len(procedure.time)
        })

        if procedure.pressurization_time:
            # Prepare the data for the vertical line
            pressurization_time = pd.DataFrame({
                'x': [procedure.pressurization_time],
                'y': [0],
                'label': ['Pressurization']}
            )

            depressurization_time = pd.DataFrame({
                'x': [procedure.depressurization_time],
                'y': [0],
                'label': ['Depressurization']}
            )

        # Base line chart
        line_chart = alt.Chart(velocity).mark_line().encode(
            x='Time',
            y='Velocity',
            color=alt.Color('label:N', legend=alt.Legend(title="Legend")),
            tooltip=['Time', 'Velocity']
        )

        if procedure.pressurization_time:
            # Vertical line
            pressurization_line = alt.Chart(pressurization_time).mark_rule(size=3).encode(
                x='x',
                color=alt.Color('label:N', legend=alt.Legend(title="Legend")),
                tooltip=['label']
            )

            depressurization_line = alt.Chart(depressurization_time).mark_rule(size=3).encode(
                x='x',
                color=alt.Color('label:N', legend=alt.Legend(title="Legend")),
                tooltip=['label']
            )

        # Combine the line chart and vertical line chart
        if procedure.pressurization_time:
            chart = (line_chart + pressurization_line + depressurization_line).properties(
                width=600,
                height=400,
                title="Procedure profile"
            )
        else:
            chart = (line_chart).properties(
                width=600,
                height=400,
                title="Case profile"
            )
        col.altair_chart(chart, use_container_width=True)

        

        