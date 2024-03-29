#!/bin/bash

#see https://roboticseabass.com/2021/04/21/docker-and-ros/ for details

xhost + 

docker run -it --net=host --gpus all \
    --env="LANG=C.UTF-8" \
    --env="NVIDIA_DRIVER_CAPABILITIES=all" \
    --env="DISPLAY" \
    --env="QT_X11_NO_MITSHM=1" \
    --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
    --name="nvidia_ros_noetic_container" \
    -v $HOME:$HOME \
    nvidia_ros_noetic \
    zsh
