#!/bin/bash

set -e

script_path=$(readlink -f "$0")        # 脚本文件的绝对路径
script_dir=$(dirname "$script_path")   # 脚本文件的目录

IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
    IMAGE_NAME=my-ros-humble
fi

echo "IMAGE_NAME: $IMAGE_NAME"

DOCKER_ARGS=(
    build -t $IMAGE_NAME $script_dir
    # --build-arg "http_proxy=http://localhost:7890"
    # --build-arg "https_proxy=http://localhost:7890"
    # --build-arg "all_proxy=socks5://localhost:7890"
    # --network host
)

docker "${DOCKER_ARGS[@]}"
