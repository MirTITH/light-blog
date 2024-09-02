#!/bin/bash

USER_NAME=docker_user

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

check_and_create_file() {
    local file_path="$1"

    if [ ! -f "$file_path" ]; then
        touch "$file_path"
        echo "File '$file_path' does not exist, created."
    fi
}

check_and_create_directory() {
    local dir_path="$1"

    if [ ! -d "$dir_path" ]; then
        mkdir -p "$dir_path"
        echo "Directory '$dir_path' does not exist, created."
    fi
}

check_and_create_file $HOME/.gitconfig
check_and_create_directory $HOME/.ssh

docker run -d --name $CONTAINER_NAME --user $USER_NAME \
    --network=host --ipc=host \
    --privileged \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw --env DISPLAY \
    --runtime=nvidia --gpus all --env NVIDIA_DRIVER_CAPABILITIES=all \
    -v $XDG_RUNTIME_DIR/pulse:/tmp/pulse -e PULSE_SERVER=unix:/tmp/pulse/native -v $HOME/.config/pulse/cookie:/home/$USER_NAME/.config/pulse/cookie \
    -v $HOME/.ssh:/home/$USER_NAME/.ssh \
    -v $HOME/.gitconfig:/home/$USER_NAME/.gitconfig \
    -v $HOME/Documents:/home/$USER_NAME/Documents \
    -v $HOME/Downloads:/home/$USER_NAME/Downloads \
    -v $script_dir/.bash_aliases:/home/$USER_NAME/.bash_aliases \
    -v $script_dir/.zshrc:/home/$USER_NAME/.zshrc \
    -v $script_dir/common_rc:/home/$USER_NAME/.local/common_rc \
    $IMAGE_NAME sleep infinity
