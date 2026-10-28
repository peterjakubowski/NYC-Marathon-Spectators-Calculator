from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

APP_FILE_PATH = Path("../app.py")


@pytest.fixture
def at():
    app_test = AppTest.from_file(APP_FILE_PATH)
    app_test.run()
    return app_test


class TestStartUp:

    def test_smoke(self, at: AppTest):
        assert not at.exception, "App should run without any exceptions."

    def test_no_error(self, at: AppTest):
        assert not at.error, "App should start without displaying an error message."

    def test_app_displays_title_element(self, at: AppTest):
        assert at.title, "App should have a title element."
        assert at.title[0].body == "NYC Marathon Spectator's Calculator"

    def test_app_display_markdown_element(self, at: AppTest):
        assert at.markdown, "App should display a markdown element."
        assert at.markdown[0].body.startswith("A calculator for NYC Marathon spectators.")

    def test_app_displays_instructions_markdown_element(self, at: AppTest):
        assert at.subheader[0].value == "Instructions"
        assert at.markdown[1].body.startswith("1) **Select the runner's start wave**")


class TestSidebarStartup:

    def test_app_displays_sidebar(self, at: AppTest):
        assert at.sidebar, "App should display the sidebar."

    def test_app_displays_sidebar_elements(self, at: AppTest):
        assert len(at.sidebar) == 6

    def test_app_displays_sidebar_start_time_element(self, at: AppTest):
        assert at.sidebar[0].label == "Start Wave"
        assert at.sidebar[0].type == "selectbox"
        assert at.sidebar[0].key == "start_wave"
        assert at.sidebar[0].value == "Wave 1"
        assert len(at.sidebar[0].options) == 10

    def test_app_displays_sidebar_mile_marker_element(self, at: AppTest):
        assert at.sidebar[1].label == "Spectator at Mile Marker"
        assert at.sidebar[1].type == "number_input"
        assert at.sidebar[1].key == "mile_marker"
        assert at.sidebar[1].value == 8.0

    def test_app_displays_sidebar_divider_element(self, at: AppTest):
        assert at.sidebar[2].type == "divider"

    def test_app_display_sidebar_subheader_split_element(self, at: AppTest):
        assert at.sidebar[3].type == "subheader"
        assert at.sidebar[3].value == "Split"

    def test_app_displays_sidebar_split_in_two_columns(self, at: AppTest):
        assert len(at.sidebar[4]) == 2
        assert at.sidebar[4].type == "flex_container"

    def test_app_displays_sidebar_split_distance_element(self, at: AppTest):
        assert at.sidebar[4][0][0].label == "Distance"
        assert at.sidebar[4][0][0].type == "selectbox"
        assert at.sidebar[4][0][0].key == "split_distance"
        assert at.sidebar[4][0][0].value == 3

    def test_app_displays_sidebar_split_unit_element(self, at: AppTest):
        assert at.sidebar[4][1][0].label == "Unit"
        assert at.sidebar[4][1][0].type == "selectbox"
        assert at.sidebar[4][1][0].key == "split_unit"
        assert at.sidebar[4][1][0].value == "miles"
        assert len(at.sidebar[4][1][0].options) == 2

    def test_app_displays_sidebar_split_in_three_columns(self, at: AppTest):
        assert len(at.sidebar[5]) == 3
        assert at.sidebar[5].type == "flex_container"

    def test_app_displays_sidebar_split_duration_hours(self, at: AppTest):
        assert at.sidebar[5][0][0].label == "Hours"
        assert at.sidebar[5][0][0].type == "number_input"
        assert at.sidebar[5][0][0].key == "split_hours"
        assert at.sidebar[5][0][0].value == 0

    def test_app_displays_sidebar_split_duration_minutes(self, at: AppTest):
        assert at.sidebar[5][1][0].label == "Minutes"
        assert at.sidebar[5][1][0].type == "number_input"
        assert at.sidebar[5][1][0].key == "split_minutes"
        assert at.sidebar[5][1][0].value == 24

    def test_app_displays_sidebar_split_duration_seconds(self, at: AppTest):
        assert at.sidebar[5][2][0].label == "Seconds"
        assert at.sidebar[5][2][0].type == "number_input"
        assert at.sidebar[5][2][0].key == "split_seconds"
        assert at.sidebar[5][2][0].value == 0


class TestMetrics:

    def test_app_displays_two_metric_elements(self, at: AppTest):
        assert len(at.metric) == 2

    def test_app_displays_runner_start_time_element(self, at: AppTest):
        assert at.metric[0].label == "Runner Start Time"

    def test_app_displays_runner_estimated_time_at_marker_element(self, at: AppTest):
        assert at.metric[1].label.startswith("Estimated Time at")

    def test_app_displays_runner_summary_markdown_element(self, at: AppTest):
        assert at.markdown[2].body.startswith("A runner starting in")


class TestElements:

    def test_changing_split_unit_changes_split_distance_options(self, at: AppTest):
        assert at.sidebar.get_by_key("split_unit").value == "miles"
        assert len(at.sidebar.get_by_key("split_distance").options) == 25
        at.sidebar.selectbox(key="split_unit").set_value("kilometers").run()
        assert len(at.sidebar.get_by_key("split_distance").options) == 8

    def test_changing_values_changes_metrics_summary_text(self, at: AppTest):
        at.sidebar.selectbox(key="start_wave").set_value("Wave 4").run()
        at.sidebar.number_input(key="mile_marker").set_value(9.0).run()
        at.sidebar.selectbox(key="split_distance").set_value(10).run()
        at.sidebar.selectbox(key="split_unit").set_value("kilometers").run()
        at.sidebar.number_input(key="split_hours").set_value(1).run()
        at.sidebar.number_input(key="split_minutes").set_value(15).run()
        at.sidebar.number_input(key="split_seconds").set_value(30).run()
        result = at.markdown[2].body
        expected = ("A runner starting in **Wave 4 (10:55:00 AM)** who crosses the **10 kilometer** marker "
                    "in **1 hours 15 minutes and 30 seconds** (12:09/mi pace) is estimated to reach the "
                    "**9.0 mile** point at **12:44:21 PM.**")
        assert result == expected
