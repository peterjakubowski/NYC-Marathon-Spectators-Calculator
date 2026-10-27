from datetime import datetime, timedelta


def calculate_pace(
        duration: tuple[int, int, int],
        distance: float
) -> tuple[float, float]:
    """
    Calculate a runner's pace given the duration of time running and distance run.
    :param duration:
    :param distance:
    :return: The runner's pace in minutes and in seconds.
    """
    estimated_finish_time = timedelta(
        seconds=(duration[0] * 60 * 60) + (duration[1] * 60) + duration[2]
    )
    seconds_per_mile = estimated_finish_time.seconds / distance
    minutes_per_mile = (seconds_per_mile // 60) + (seconds_per_mile % 60) / 60

    return minutes_per_mile, seconds_per_mile


def get_time_at_marker(
        start_time: datetime,
        mile_marker: float,
        duration: tuple[int, int, int],
        distance: float
) -> datetime:
    """
    Returns the time at a given mile marker based on a runner's pace at a checkpoint.
    :param start_time: Time that the runner started the race (wave).
    :param mile_marker: Mile marker that the spectator is nearest.
    :param duration: Duration of time (hours, minutes) from the race start to checkpoint.
    :param distance: Distance from the race start to checkpoint.
    :return: The predicted time the runner will pass the spectator at the given mile marker point.
    """

    minutes_per_mile, _ = calculate_pace(duration, distance)
    minutes_to_marker = minutes_per_mile * mile_marker
    time_at_marker = start_time + timedelta(minutes=minutes_to_marker)

    return time_at_marker
