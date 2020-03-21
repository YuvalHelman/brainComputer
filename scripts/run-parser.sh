#!/bin/bash

PARSER_NAME=$1

.env/bin/python -m brainComputer.parsers run-parser ${PARSER_NAME} 'rabbitmq://127.0.0.1:5672/'
