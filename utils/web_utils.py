import math
import os
from collections import OrderedDict
from datetime import datetime

import pytz
import yaml
from pytz import timezone


class WebUtils:

    discover_filter_options = {}
    discover_filters = {}

    @classmethod
    def format_count(cls, raw_count):
        if raw_count > 999:
            # convert int to 2.4k format
            thousands = math.floor(raw_count / 1000)
            hundreds = math.floor((raw_count - (thousands * 1000)) / 100)
            return str(int(thousands)) + "." + str(int(hundreds)) + "k"
        elif raw_count is None:
            return "0"
        else:
            return str(raw_count)

    @classmethod
    def root_path(cls):
        utils_folder = os.path.dirname(__file__)
        root_folder = os.path.dirname(utils_folder)
        return root_folder

    @classmethod
    def load_discover_filter_options(cls):
        def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
            class OrderedLoader(Loader):
                pass

            def construct_mapping(loader, node):
                loader.flatten_mapping(node)
                return object_pairs_hook(loader.construct_pairs(node))
            OrderedLoader.add_constructor(
                yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                construct_mapping)
            return yaml.load(stream, OrderedLoader)

        # Read display values YAML
        filter_options_yaml_path = os.path.join(cls.root_path(), 'resources/discover_filter_options.yaml')
        filter_options_yaml = open(filter_options_yaml_path, 'r')
        filter_options_raw = ordered_load(filter_options_yaml, yaml.SafeLoader)

        # Parse values
        filter_ops = {}
        types = filter_options_raw.keys()
        for filter_type in types:
            filter_ops[filter_type] = OrderedDict(filter_options_raw[filter_type].items())

        # Store display values
        cls.discover_filter_options = filter_ops

    @classmethod
    def get_filter_options(cls, value_type):
        if len(cls.discover_filter_options) == 0:
            cls.load_discover_filter_options()
        return cls.discover_filter_options.get(value_type, {})

    @classmethod
    def get_filter_option_display_value(cls, value_type, name):
        if len(cls.discover_filter_options) == 0:
            cls.load_discover_filter_options()
        return cls.discover_filter_options.get(value_type, {}).get(name)

    @classmethod
    def load_discover_filters(cls):
        # Read display values YAML
        filters_yaml_path = os.path.join(cls.root_path(), 'resources/discover_filters.yaml')
        filters_yaml = open(filters_yaml_path, 'r')
        filters_raw = yaml.load(filters_yaml)

        # Parse filter config objs
        filter_vals = {}
        types = filters_raw.keys()
        for filter_type in types:
            filter_vals[filter_type] = dict(filters_raw[filter_type].items())

        # Store display values
        cls.discover_filters = filter_vals

    @classmethod
    def get_discover_filter(cls, name):
        if len(cls.discover_filters) == 0:
            cls.load_discover_filters()
        return cls.discover_filters.get(name, {})

    @classmethod
    def get_date_from_string(cls, date_string):
        # sample date string: 2016-01-05T19:04:53.066123
        return datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S.%f')

    @classmethod
    def format_friendly_date(cls, date_string):
        d = cls.get_date_from_string(date_string)
        return d.strftime('%b %d, %Y')

    @classmethod
    def format_friendly_time(cls, date_string):
        local_timezone = timezone('US/Pacific')
        d = cls.get_date_from_string(date_string)
        d = pytz.utc.localize(d, is_dst=None).astimezone(local_timezone)
        return d.strftime('%I:%M%p PST')

    @classmethod
    def get_feet_from_inches(cls, inches):
        inches = int(inches)
        feet = int(inches / 12)
        extra_inches = inches % 12
        feet_and_inches = str(feet) + "\'"
        if extra_inches > 0:
            feet_and_inches += " " + str(extra_inches) + "\""
        return feet_and_inches

    @classmethod
    def get_cm_from_inches(cls, inches):
        inches = float(inches)
        cm = inches * 2.54
        return int(cm)

    @classmethod
    def get_kg_from_lbs(cls, lbs):
        lbs = int(lbs)
        kg = lbs * 0.453592
        return int(kg)

    @classmethod
    def get_uk_cup_size(cls, cup):
        cup_mapping = OrderedDict([
           ("AA", "A"),
           ("A", "B"),
           ("B", "C"),
           ("C", "D"),
           ("D", "DD"),
           ("DD", "E"),
           ("DDD", "E+")])
        return cup_mapping[cup]


