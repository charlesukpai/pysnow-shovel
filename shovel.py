# -*- coding: utf-8 -*-

"""Simple command line utility for creating items in ServiceNow"""

import sys
import argparse
import logging
import json
import pysnow


__author__ = "Robert Wikman, Zetup AB"


def init_logger(log_file, debug):
    logger = logging.getLogger('pysnow-shovel')

    if debug:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    if log_file:
        handler = logging.FileHandler(log_file)
        handler.setFormatter(logging.Formatter('[%(asctime)s %(levelname)s] %(message)s'))
    else:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

    logger.addHandler(handler)
    return logger


parser = argparse.ArgumentParser(description='Shovel into ServiceNow.')

payload_group = parser.add_mutually_exclusive_group(required=True)
logging_group = parser.add_mutually_exclusive_group(required=False)

parser.add_argument('--api_path', dest='api_path', action='store', required=True,
                    help='ServiceNow API path, example: /table/incident')

payload_group.add_argument('--payload', dest='payload', action='store', required=False,
                           help='Pass JSON payload string as an argument')

payload_group.add_argument('--payload_file', dest='payload_file', action='store', required=False,
                           help='Read JSON payload from file')

parser.add_argument('--config', dest='config_file', action='store', default='config.json',
                    help='Config file, defaults to config.json')

logging_group.add_argument('--log_file', dest='log_file', action='store', required=False,
                           help='Send logs to terminal')


args = parser.parse_args()

if args.payload:
    payload = json.loads(args.payload)
else:
    payload = json.load(open(args.payload_file))

config = json.load(open(args.config_file))

log = init_logger(args.log_file, debug=False)

c = pysnow.Client(instance=config['instance_name'], user=config['user_name'], password=config['password'])

# Set incident resource
incident = c.resource(api_path=args.api_path)
incident.parameters.add_custom({'sysparm_input_display_value': True})

# noinspection PyBroadException
try:
    result = incident.create(payload=payload)
    log.debug(result)
    log.info('Record created: %s' % result['sys_id'])
except Exception as e:  # catch all and log error
    log.critical('Error creating incident: %s' % e)
    sys.exit(1)

sys.exit(0)
