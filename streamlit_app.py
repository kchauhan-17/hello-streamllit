import streamlit as st
import pandas as pd
import altair as alt
from streamlit_autorefresh import st_autorefresh

from function.anedya import anedya_config
from function.anedya import fetchHumidityData
from function.anedya import fetchTemperatureData

# Set the page configuration as the first Streamlit command
st.set_page_config(page_title="SMART HOME", layout="wide")

# nodeId = "20deeee8-f8ae-11ee-9dd8-c3aa61afe2fb"  # get it from anedya dashboard -> project -> node
nodeId = "4229885e-3456-11ef-9ecc-a1461caa74a3"  # get it from anedya dashboard -> project -> node
apiKey = "829d921000ee5204aa1cdb4fe4d2002fe7bbbe2c157983dad9bd7658f40d7229"  # aneyda project apikey

# Uncomment to show count
# count = st_autorefresh(interval=30000, limit=None, key="auto-refresh-handler")
st_autorefresh(interval=30000, limit=None, key="auto-refresh-handler")

# --------------- HELPER FUNCTIONS -----------------------
def V_SPACE(lines):
    for _ in range(lines):
        st.write("&nbsp;")

humidityData = pd.DataFrame()
temperatureData = pd.DataFrame()

def main():
    global humidityData, temperatureData
    anedya_config(NODE_ID=nodeId, API_KEY=apiKey)

    # Initialize the log in state if does not exist
    if "LoggedIn" not in st.session_state:
        st.session_state.LoggedIn = False

    if "CurrentHumidity" not in st.session_state:
        st.session_state.CurrentHumidity = 0

    if "CurrentTemperature" not in st.session_state:
        st.session_state.CurrentTemperature = 0

    if st.session_state.LoggedIn is False:
        drawLogin()
    else:
        humidityData = fetchHumidityData()
        temperatureData = fetchTemperatureData()

        drawDashboard()

def drawLogin():
    cols = st.columns([1, 0.8, 1], gap='small')
    with cols[0]:
        pass
    with cols[1]:
        st.markdown("<h1 style='color:navy;'>SMART HOME DATA MONITORING</h1>", unsafe_allow_html=True)
        username_inp = st.text_input("Username")
        password_inp = st.text_input("Password", type="password")
        submit_button = st.button(label="Submit")

        if submit_button:
            if username_inp == "admin" and password_inp == "admin":
                st.session_state.LoggedIn = True
                st.rerun()
            else:
                st.error("Invalid Credential!")
    with cols[2]:
        pass

def drawDashboard():
    headercols = st.columns([1, 0.1, 0.1], gap="small")
    with headercols[0]:
        st.markdown("<h1 style='color:navy;'>SMART HOME DATA MONITORING</h1>", unsafe_allow_html=True)
    with headercols[1]:
         st.button("Refresh")

    with headercols[2]:
        logout = st.button("Logout")

    if logout:
        st.session_state.LoggedIn = False
        st.rerun()

    st.markdown("<p style='color:navy;'>This dashboard provides temperature and humidity data for the Smart Home Data Monitoring project!</p>", unsafe_allow_html=True)

    st.subheader(body="Current Status", anchor=False)
    cols = st.columns(2, gap="medium")
    with cols[0]:
        st.metric(label="Humidity", value=str(st.session_state.CurrentHumidity) + " %")
    with cols[1]:
        st.metric(label="Temperature", value=str(st.session_state.CurrentTemperature) + "  °C")
    # with cols[2]:
    #    st.metric(label="Refresh Count", value=count)

    charts = st.columns(2, gap="small")
    with charts[0]:
        st.subheader(body="Humidity", anchor=False)
        if humidityData.empty:
            st.write("No Data !!")
        else:
            humidity_chart_an = alt.Chart(data=humidityData).mark_area(
                line={'color': '#1fa22f'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#1fa22f', offset=1),
                           alt.GradientStop(color='rgba(255,255,255,0)', offset=0)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0,
                ),
                interpolate='monotone',
                cursor='crosshair'
            ).encode(
                x=alt.X(
                    shorthand="Datetime:T",
                    axis=alt.Axis(format="%Y-%m-%d %H:%M:%S", title="Datetime", tickCount=10, grid=True, tickMinStep=5),
                ),  # T indicates temporal (time-based) data
                y=alt.Y(
                    "aggregate:Q",
                    scale=alt.Scale(domain=[20, 65]),
                    axis=alt.Axis(title="Humidity (%)", grid=True, tickCount=10),
                ),  # Q indicates quantitative data
                tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                         alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
            ).properties(height=400).interactive()

            # Display the Altair chart using Streamlit
            st.altair_chart(humidity_chart_an, use_container_width=True)

    with charts[1]:
        st.subheader(body="Temperature", anchor=False)
        if temperatureData.empty:
            st.write("No Data !!")
        else:
            temperature_chart_an = alt.Chart(data=temperatureData).mark_area(
                line={'color': '#1fa22f'},
                color=alt.Gradient(
                    gradient='linear',
                    stops=[alt.GradientStop(color='#1fa22f', offset=1),
                           alt.GradientStop(color='rgba(255,255,255,0)', offset=0)],
                    x1=1,
                    x2=1,
                    y1=1,
                    y2=0,
                ),
                interpolate='monotone',
                cursor='crosshair'
            ).encode(
                x=alt.X(
                    shorthand="Datetime:T",
                    axis=alt.Axis(format="%Y-%m-%d %H:%M:%S", title="Datetime", tickCount=10, grid=True, tickMinStep=5),
                ),  # T indicates temporal (time-based) data
                y=alt.Y(
                    "aggregate:Q",
                    # scale=alt.Scale(domain=[0, 100]),
                    scale=alt.Scale(zero=False, domain=[10, 50]),
                    axis=alt.Axis(title="Temperature (°C)", grid=True, tickCount=10),
                ),  # Q indicates quantitative data
                tooltip=[alt.Tooltip('Datetime:T', format="%Y-%m-%d %H:%M:%S", title="Time",),
                         alt.Tooltip('aggregate:Q', format="0.2f", title="Value")],
            ).properties(height=400).interactive()

            st.altair_chart(temperature_chart_an, use_container_width=True)

if __name__ == "__main__":
    main()
