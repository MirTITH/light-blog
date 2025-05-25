#!/bin/bash

set -e

script_path=$(readlink -f "$0")        # 脚本文件的绝对路径
script_dir=$(dirname "$script_path")   # 脚本文件的目录

print_usage() {
    echo "Usage: $0 DOCKERFILE_FOLDER IMAGE_NAME"
    echo "Example: $0 ros-humble my-ros-humble"
}

# Docker file folder
DOCKERFILE_FOLDER=$1
if [ -z "$DOCKERFILE_FOLDER" ]; then
    echo "DOCKERFILE_FOLDER not specified"
    print_usage
    exit 1
fi
DOCKERFILE_PATH=$script_dir/$DOCKERFILE_FOLDER/Dockerfile

# Image name
IMAGE_NAME=$2
if [ -z "$IMAGE_NAME" ]; then
    echo "IMAGE_NAME not specified"
    print_usage
    exit 1
fi
echo "IMAGE_NAME: $IMAGE_NAME"

# Build the image
DOCKER_ARGS=(
    build -f $DOCKERFILE_PATH -t $IMAGE_NAME $script_dir
    --build-arg DOCKER_FILE_FOLDER=$DOCKERFILE_FOLDER
    # --build-arg "http_proxy=http://localhost:7890"
    # --build-arg "https_proxy=http://localhost:7890"
    # --build-arg "all_proxy=socks5://localhost:7890"
    # --network host
)

# echo "The following command will be run:"
# echo "docker ${DOCKER_ARGS[@]}"
# read -p "Press Enter to continue..."

docker ${DOCKER_ARGS[@]}
