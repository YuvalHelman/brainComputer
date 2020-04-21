#!/bin/bash

net=containersNetwork
vol=sharedVolume

sudo docker volume create --name ${vol}
sudo docker network create ${net}

# Build base image
sudo docker build -t brainbase . &&

# Run needed external containers
sudo docker run -d --name mongodb -p 27017:27017 --net ${net} mongo
sudo docker run -d --name rab -p 5672:5672 --net ${net} rabbitmq

# Build App's images
sudo docker build -f brainComputer/server/Dockerfile -t brain/server .

sudo docker build -f brainComputer/parsers/Dockerfile -t brain/pose --build-arg PARSER_NAME=pose .
sudo docker build -f brainComputer/parsers/Dockerfile -t brain/color_image --build-arg PARSER_NAME=color_image .
sudo docker build -f brainComputer/parsers/Dockerfile -t brain/depth_image --build-arg PARSER_NAME=depth_image .
sudo docker build -f brainComputer/parsers/Dockerfile -t brain/feelings --build-arg PARSER_NAME=feelings .

sudo docker build -f brainComputer/saver/Dockerfile -t brain/saver .

sudo docker build -f brainComputer/api/Dockerfile -t brain/api .

sudo docker build -f brainComputer/gui/Dockerfile -t brain/gui .

sleep 1m

# Run app's containers
sudo docker run -d --name server -p 0.0.0.0:8000:8000/tcp -v ${vol}:/tmp/brainComputer/data --net ${net} brain/server

sudo docker run -d --name pose_parser --net ${net} brain/pose
sudo docker run -d --name feelings_parser --net ${net} brain/feelings
sudo docker run -d --name color_image_parser -v ${vol}:/tmp/brainComputer/data --net ${net} brain/color_image
sudo docker run -d --name depth_image_parser -v ${vol}:/tmp/brainComputer/data --net ${net} brain/depth_image

sudo docker run -d --name saver --net ${net} brain/saver

sudo docker run -d --name api -p 5000:5000/tcp -v ${vol}:/tmp/brainComputer/data --net ${net} brain/api

sudo docker run -d --name gui -p 8080:8080/tcp -v ${vol}:/tmp/brainComputer/data --net ${net} brain/gui
