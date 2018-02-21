# -*- coding: utf-8 -*-
import os
import errno
import time


IMGS = ['jpg', 'jpeg', 'png']


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


def check_imgs(image):
    """

    :param image: request.Files file werkzeug.datastructures.FileStorage
    :return: bool
    """
    result = False
    if image.content_type.split('/')[1] in IMGS:
        result = True
    return result


def ensure_dir(dirname):
    # for race condition, if the directory is created between the
    # os.path.exists and the os.makedirs calls,
    # the os.makedirs will fail with an OSError
    while True:
        try:
            if not os.path.exists(dirname):
                os.makedirs(dirname)
            break
        except OSError, e:
            if e.errno == errno.EEXIST:
                pass
            raise e
