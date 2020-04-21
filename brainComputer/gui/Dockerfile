FROM brainbase

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ENTRYPOINT python3 -m brainComputer.gui run-server  -h '0.0.0.0' -p '8080' --database mongodb://mongodb.containersnetwork:27017
