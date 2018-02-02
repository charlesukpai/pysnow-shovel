#!/usr/bin/env bash

function usage {
    echo "usage: $0 <payload>"
    echo
    echo "Example:"
    echo "./wrapper.sh '{\"field1\": \"value1\", \"field2\": \"value2\"}'"
    exit 1
}

[ -z "$1" ] && usage

SHOVEL_HOME=$(dirname $0)

PYTHON_BIN=/usr/bin/python

API_PATH=/table/incident
CONFIG_FILE=config.json
LOG_FILE=shovel.log

# Get payload from stdin
cd ${SHOVEL_HOME} && ${PYTHON_BIN} shovel.py --api_path ${API_PATH} --config ${CONFIG_FILE} --log_file ${LOG_FILE} --payload "${1}"
