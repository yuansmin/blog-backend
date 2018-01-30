# -*- coding: utf-8 -*-
"""
__author__ = 'fancy'
__mtime__ = '2018/1/30'
"""

def check_param_completion(params, needs):
    missing = []
    for i in needs:
        if i not in params:
            missing.append(i)

    return missing