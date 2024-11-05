import streamlit as st
import pandas as pd
import os
import glob
from data_processing.session import Session
# import matplotlib.pyplot as plt
import altair as alt
import numpy as np
import cv2

data_folder = "data"
folders = glob.glob(data_folder + "/*")
print(folders)
sessions = [Session(f) for f in folders]


session = sessions[0]

def test():
    st.write("Hello")
    st.write("World")


def session_page(session):
    st.title("Session Data")
    st.metric("Session folder", os.path.basename(session.session_data_folder))
    col1, col2 = st.columns(2)
    col1.metric("Total number of grasps", session.total_number_of_grasps)
    col2.metric("Cases in session", session.number_of_cases)
    st.line_chart(session.session_data, x="time", y="acc_z")
    zero_g_cases = [case for case in session._cases if case.zero_g_duration is not None]
    tabs = st.tabs([f"Case {i}" for i in range(len(zero_g_cases))])
    for case, tab in zip(zero_g_cases, tabs):
        with tab:
            col1, col2 = st.columns(2)
            col1.markdown(f"Case folder: **{case.case_folder.split(os.sep)[-1]}**")
            c1, c2 = col1.columns(2)
            c1.metric("Methode", case.case_procedure_name)
            c2.metric("Number of correct attempts", case.number_of_attempts)

            c1, c2 = col1.columns(2)
            c1.metric("Max force [grams]", case.case_data["load_cell"].max().round(2))
            c2.metric("Zero-G duration [s]", case.zero_g_duration)
            procedure_stplot(case._procedure, col2)

            col1, col2 = st.columns(2)
            data_zero_g = case.case_data[case.case_data["acc_z"] < 0.08]
            col1.line_chart(data_zero_g, x="time", y="acc_z")
            col2.line_chart(data_zero_g, x="time", y="load_cell")


            # cam1 = st.columns((1))
            # video_1 = cam1[0].empty()

            # video_path = session._cases[i]._video_files[0]
            # cap1 = cv2.VideoCapture(video_path)
            # while cap1.isOpened():
            #     ret, frame1 = cap1.read()

            #     frame1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB)
            #     video_1.image(frame1, channels="RGB")

            # cap1.release()
            # cv2.destroyAllWindows()
            # st.video(video_path, format="application/mp4")

def procedure_plot(procedure):
    fig, ax = plt.subplots()
    x = procedure.procedure_time
    y = procedure.procedure_velocity
    ax.plot(x, y, label='Velocity profile')

    ax.axvline(x=procedure.pressurization_time, color='lime', linestyle='--', label='Pressurization')
    ax.axvline(x=procedure.depressurization_time, color='violet', linestyle='--', label='Depressurization')
    ax.legend()
    ax.set_xlabel('X')
    ax.set_ylabel('Y')

    st.pyplot(fig)

def procedure_stplot(procedure, col):
    # Prepare the main data for the line chart
    velocity = pd.DataFrame({
        'Time': procedure.time,
        'Velocity': procedure.velocity,
        'label': ['Velocity'] * len(procedure.time)
    })

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
    chart = (line_chart + pressurization_line + depressurization_line).properties(
        width=600,
        height=400,
        title="Case profile"
    )
    col.altair_chart(chart, use_container_width=True)


def main():
    st.set_page_config(layout="wide")
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Session Data", "Test Page"])

    if page == "Session Data":
        session_page(session)
    elif page == "Test Page":
        test()

if __name__ == "__main__":
    main()
# st.sidebar.write("Hello")
# st.sidebar.page_link(page)

# df = pd.read_csv("my_data.csv", delimiter=";")
# st.line_chart(df)

# set danych z calego lotu -> sesja
# dane z jednej paraboli -> case
# pojedynczy chwyt -> attempt