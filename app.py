import streamlit as st

from src.markers import markers_kilometers, markers_miles
from src.utils import calculate_pace, get_time_at_marker
from src.waves import start_waves

# ===============================
# ============ Intro ============
# ===============================

st.title("NYC Marathon Spectator's Calculator")

st.markdown("A calculator for NYC Marathon spectators. "
            "Estimate when your runner will pass you on the course based on their latest official timing splits."
            )

st.subheader("Instructions")

st.markdown("1) **Select the runner's start wave** to set their start time.\n"
            "2) **Enter the mile marker** where you are standing.\n"
            "3) **Open the official [NYRR App](https://www.nyrr.org/get-involved/nyrr-app)** to find "
            "your runner’s most recent split time.\n"
            "4) **Input the split** to calculate their estimated local time of arrival at your location."
            )

st.divider()


# =================================
# ============ Sidebar ============
# =================================

with st.sidebar:
    # Start time (wave start times)
    start_time_options = [wave[0] for wave in start_waves]
    start_wave = st.selectbox(
        label="Start Wave",
        key="start_wave",
        options=start_time_options,
        index=5,
        help="The wave the runner started the race in.",
        bind="query-params",
    )
    # Mile marker spectator is standing nearest
    mile_marker = st.number_input(
        label="Spectator at Mile Marker",
        key="mile_marker",
        min_value=0.0,
        max_value=26.2,
        value=8.0,
        step=0.05,
        help="The mile marker the spectator is closest to.",
        bind="query-params"

    )
    # Splits section
    st.divider()
    st.subheader("Split", help="The runner's split time at a given marker on the course.")
    col1, col2 = st.columns(2)
    with col1:
        # Split distance
        split_distance = st.selectbox(
            label="Distance",
            key="split_distance",
            options=markers_miles if st.session_state.get("split_unit", "miles") == "miles" else markers_kilometers,
            index=0,
            bind="query-params",
        )
    with col2:
        # Split marker units, miles or kilometers
        split_unit = st.selectbox(
            label="Unit",
            key="split_unit",
            options=["miles", "kilometers"],
            index=0,
            bind="query-params",
        )

    col1, col2, col3 = st.columns(3)
    with col1:
        # Split duration hours
        split_hours = st.number_input(
            label="Hours",
            key="split_hours",
            min_value=0,
            max_value=11,
            value=0,
            step=1,
            bind="query-params"
        )
    with col2:
        # Split duration minutes
        split_minutes = st.number_input(
            label="Minutes",
            key="split_minutes",
            min_value=0,
            max_value=59,
            value=24,
            step=1,
            bind="query-params"
        )
    with col3:
        # Split duration seconds
        split_seconds = st.number_input(
            label="Seconds",
            key="split_seconds",
            min_value=0,
            max_value=59,
            value=0,
            step=1,
            bind="query-params"
        )

# =================================
# ============ Metrics ============
# =================================

col1, col2 = st.columns(2)
with col1:
    start_time = start_waves[start_time_options.index(st.session_state.get('start_wave'))][1]
    st.metric(
        label="Runner Start Time",
        value=start_time.strftime("%-I:%M:%S %p"),
        border=True,
    )

with col2:
    # Estimate the time the runner will be at a marker
    time_at_marker = get_time_at_marker(
        start_time=start_time,
        mile_marker=mile_marker,
        duration=(split_hours, split_minutes, split_seconds),
        distance=split_distance if split_unit == "miles" else split_distance * 0.621371
    )
    st.metric(
        label=f"Estimated Time at {mile_marker} Mile Marker",
        value=time_at_marker.strftime("%-I:%M:%S %p"),
        border=True
    )

pace_minutes, pace_seconds = calculate_pace(
    duration=(split_hours, split_minutes, split_seconds),
    distance=split_distance if split_unit == "miles" else split_distance * 0.621371
)

st.markdown(f"A runner starting in **{start_wave} ({start_time.strftime("%-I:%M:%S %p")})** "
            f"who crosses the **{split_distance} {split_unit.strip('s')}** marker in "
            f"**{split_hours} hours {split_minutes} minutes and {split_seconds} seconds** "
            f"({int(pace_minutes // 1):01d}:{int(pace_seconds) % 60:02d}/mi pace) is estimated to "
            f"reach the **{mile_marker} mile** point at **{time_at_marker.strftime("%-I:%M:%S %p")}.** "
            )
