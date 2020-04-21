FROM brainbase

ARG PARSER_NAME
ENV PARSER_ENV_NAME=${PARSER_NAME}

RUN echo ${PARSER_NAME}

CMD python -m brainComputer.parsers run-parser ${PARSER_ENV_NAME} 'rabbitmq://rab.containersNetwork:5672/'
