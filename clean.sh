#!/bin/sh
sudo docker stop $(sudo docker ps -a -q)
sudo docker rm $(sudo docker ps -a -q)
sudo docker system prune -a
sudo docker volume prune
