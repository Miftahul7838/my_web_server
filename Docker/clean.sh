#!/bin/bash


sudo docker stop $(docker ps -q)
sudo docker rmi -f $(docker images -q)
