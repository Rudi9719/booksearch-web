#!/usr/bin/env python

import datetime


def parse_date_string(date_string):

    date = None

    try:
        date = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
    except:
        pass

    return date
