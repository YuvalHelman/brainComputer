FROM fnndsc/ubuntu-python3

COPY . /app
WORKDIR /app

RUN apt-get update
RUN apt-get update && apt-get install -y libxft-dev libfreetype6 libfreetype6-dev

RUN pip install -r requirements.txt

