FROM brainbase

EXPOSE 8000

CMD python -m brainComputer.server run-server --data_path '/tmp/brainComputer/data/' -h '0.0.0.0' -p '8000' rabbitmq://rab.containersNetwork:5672/
