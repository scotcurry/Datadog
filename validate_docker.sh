#!/bin/zsh

if docker ps | grep CONTAINER; then
  echo "Docker is Running"
else
  echo "Docker is not Running"
  open -a Docker
  while ! pgrep -f "com.docker.build"; do
    echo "Working"
    sleep 10.0
  done
fi