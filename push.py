# -*- coding: utf-8 -*-

"""Simple command line utility to create an incident in ServiceNow by passing a delimited string"""

import sys
import logging
import pysnow
from pysnow.exceptions import NoResults
from config import INSTANCE_NAME, USER_NAME, PASSWORD, CI_MISSING_SYS_ID


__author__ = "Robert Wikman, Zetup AB"


class MissingPayload(Exception):
    pass


class MalformedPayload(Exception):
    pass


class UnexpectedResponse(Exception):
    pass


# Set up logger
logging.basicConfig(filename='snag.log',
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ERR_INVALID_PAYLOAD = "Expected format: hostname::short_description::description"

# Make sure input is valid
if len(sys.argv) < 2:
    raise MissingPayload(ERR_INVALID_PAYLOAD)

try:
    host_name, short_description, description = sys.argv[1].split('::')
except ValueError:
    logging.critical('Received invalid payload: %s, %s' % (sys.argv[1], ERR_INVALID_PAYLOAD))
    raise MalformedPayload(ERR_INVALID_PAYLOAD)

c = pysnow.Client(instance=INSTANCE_NAME, user=USER_NAME, password=PASSWORD)

# Set CMDB resource
cmdb = c.resource(api_path='/table/cmdb_ci')

ci = ci_id = company_id = None

# Attempt to resolve CI
try:
    ci = cmdb.get(query={'name': host_name}).first()
    ci_id = ci['sys_id']
except NoResults:
    logging.warning('Missing CI for host: %s' % host_name)
    try:
        ci = cmdb.get(query={'sys_id': CI_MISSING_SYS_ID}).first()
        ci_id = CI_MISSING_SYS_ID
    except NoResults:
        logging.warning('Missing CI fallback with ID: %s' % CI_MISSING_SYS_ID)

if ci_id:
    try:
        company_id = ci['company']['value']
    except KeyError:
        raise UnexpectedResponse('Unable to resolve company for CMDB CI: %s, name: %s' % (ci_id, host_name))


# Set incident resource
incident = c.resource(api_path='/table/incident')

# noinspection PyBroadException
try:
    result = incident.create({
        'description': description,
        'short_description': short_description,
        'cmdb_ci': ci_id,
        'company': company_id
    })
    logging.info('Incident created: %s' % result['number'])
except Exception as e:  # catch all and log error
    logging.critical('Error creating incident: %s' % e)
    sys.exit(1)

