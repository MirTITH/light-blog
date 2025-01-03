#!/bin/bash

set -e

script_path=$(readlink -f "$0")        # 脚本文件的绝对路径
script_dir=$(dirname "$script_path")   # 脚本文件的目录

print_usage() {
    echo "Usage: $0 Dockerfile_FOLDER [IMAGE_NAME]"
}

Dockerfile_FOLDER=$1
if [ -z "$Dockerfile_FOLDER" ]; then
    echo "Dockerfile_FOLDER not specified"
    print_usage
    exit 1
fi
BUILD_DIR=$script_dir/$Dockerfile_FOLDER

IMAGE_NAME=$2
if [ -z "$IMAGE_NAME" ]; then
    IMAGE_NAME=$Dockerfile_FOLDER
    echo "IMAGE_NAME not specified, use default: $IMAGE_NAME"
    print_usage
    read -p "Press enter to continue"
fi
echo "IMAGE_NAME: $IMAGE_NAME"

DOCKER_ARGS=(
    build -t $IMAGE_NAME $BUILD_DIR
    # --build-arg "http_proxy=http://localhost:7890"
    # --build-arg "https_proxy=http://localhost:7890"
    # --build-arg "all_proxy=socks5://localhost:7890"
    # --network host
)

cp -r $script_dir/mirrors $BUILD_DIR

docker "${DOCKER_ARGS[@]}"

rm -rf $BUILD_DIR/mirrors