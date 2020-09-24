import os
import yaml

from .date_parser import parser
import logging

events_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../events.yml")

events = []
with open(events_file) as f:
    data = yaml.load(f, Loader=yaml.FullLoader)
    for v in data['events'].values():
        date, time, message = v.values()
        events.append((parser.parse(date, time), message))

logging.info('Loaded events successfully from file {}.'.format(events_file))
