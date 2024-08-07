#!/bin/bash

USER_NAME=ros

IMAGE_NAME=$1
CONTAINER_NAME=$2

if [ -z $IMAGE_NAME ]; then
    IMAGE_NAME=my-ros-humble
fi

if [ -z $CONTAINER_NAME ]; then
    CONTAINER_NAME=my-ros-humble
fi

script_path=$(readlink -f "$0")        # 脚本文件的绝对路径
script_dir=$(dirname "$script_path")   # 脚本文件的目录
workspace_dir=$(dirname "$script_dir") # 工作空间的目录，即 script_dir 的父目录

echo "IMAGE_NAME: $IMAGE_NAME"
echo "CONTAINER_NAME: $CONTAINER_NAME"

docker run -d --name $CONTAINER_NAME --user $USER_NAME \
    --network=host --ipc=host \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw --env DISPLAY \
    --gpus all --env NVIDIA_DRIVER_CAPABILITIES=all \
    -v $HOME/.ssh:/home/$USER_NAME/.ssh \
    -v $HOME/Documents:/home/$USER_NAME/Documents \
    -v $HOME/Downloads:/home/$USER_NAME/Downloads \
    -v $script_dir/.bash_aliases:/home/$USER_NAME/.bash_aliases \
    -v $script_dir/.zshrc:/home/$USER_NAME/.zshrc \
    -v $script_dir/common_rc:/home/$USER_NAME/.local/common_rc \
    $IMAGE_NAME
