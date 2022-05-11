# Module for utility helper methods
from datetime import *

TIME_FORMAT = '%I:%M %p'


def add_time(init_time, time_delta):
    """
    Adds a time_delta to a time object.

    :param datetime.time init_time: the starting time
    :param datetime.time_delta time_delta: the time_delta
    :return: the sum
    :rtype: datetime.time
    """
    # O(1)
    # Must convert to datetime first
    init_dt = time_to_datetime(init_time)
    sum_dt = init_dt + time_delta
    return sum_dt.time()


def time_to_datetime(t):
    """
    Converts a time object to a datetime object.

    :param datetime.time t: the time object
    :return: the datetime object
    :rtype: datetime.datetime
    """
    # Time complexity O(1)
    return datetime.combine(date.today(), t)


def time_str(t, fmt):
    """
    Formats a time object as a string.

    :param datetime.time t: the time object
    :param string fmt: the format
    :return: the formatted time object
    :rtype: string
    """
    # Time complexity O(1)
    return time_to_datetime(t).strftime(fmt)


def str_to_time(s, fmt):
    """
    Parses a string into a time object

    :param string s: the string to parse
    :param string fmt: the format
    :return: the parsed time object
    :rtype: datetime.time
    """
    # Time complexity O(1)
    return datetime.strptime(s, fmt).time()


def time_diff(t1, t2):
    """
    Calculates the difference of two datetime.time objects

    :param datetime.time t1: the minuend
    :param datetime.time t2: the subtrahend
    :return: the difference
    :rtype: datetime.time_delta
    """
    # Time complexity O(1)
    dt1 = time_to_datetime(t1)
    dt2 = time_to_datetime(t2)
    return dt1 - dt2
