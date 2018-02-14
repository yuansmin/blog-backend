# -*- coding: utf-8 -*-
import time

def format_time(time):
    """

    :param datetime.datetime:
    :return: "2018-02-23 10:10:00"
    """
    return time.strftime('%Y-%m-%d %H:%M:%S')

def is_before_now(time_str):
    """

    :param time_str: str "%Y-%m-%d %H:%M:%S"
    :return: bool
    """
    result = False
    now = time.time()
    the_time = time.mktime(time.strptime(time_str, '%Y-%m-%d %H:%M:%S'))
    if the_time < now:
        result = True

    return result