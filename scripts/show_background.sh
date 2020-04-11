#!/bin/bash

netstat -tulpn | grep '5000\|8000\|8080'
sleep 1
sudo docker ps -a

