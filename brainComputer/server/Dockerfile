FROM brainbase

EXPOSE 8000

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENTRYPOINT python3 -m brainComputer.server run-server --data_path '/tmp/brainComputer/data/' -h '0.0.0.0' -p '8000' rabbitmq://rab.containersnetwork:5672/
