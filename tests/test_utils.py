from datetime import datetime

from src.utils import calculate_pace, get_time_at_marker


class TestCalculatePace:

    def test_calculate_pace(self):

        result = calculate_pace(
            duration=(0, 10, 0),
            distance=1
        )

        assert result == (10.0, 600.0)


class TestGetTimeAtMaker:

    def test_get_time_at_maker(self):

        result = get_time_at_marker(
            start_time=datetime.strptime("01 Nov 26 8 0 0", "%d %b %y %H %M %S"),
            mile_marker=1.0,
            duration=(0, 10, 0),
            distance=1.0
        )

        assert result == datetime(2026, 11, 1, 8, 10,0)
