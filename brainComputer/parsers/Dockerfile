FROM brainbase

ARG PARSER_NAME
ENV PARSER_ENV_NAME=${PARSER_NAME}

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN echo ${PARSER_NAME}

ENTRYPOINT python3 -m brainComputer.parsers run-parser ${PARSER_ENV_NAME} 'rabbitmq://rab.containersnetwork:5672/'
