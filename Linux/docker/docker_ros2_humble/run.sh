#!/bin/bash

USER_NAME=ros

IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
    echo "Usage: $0 <image-name>"
    exit 1
fi

docker run -it --user $USER_NAME --network=host --ipc=host \
    -v $PWD/Documents:/home/$USER_NAME/Documents \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    --env DISPLAY \
    --gpus all \
    --env NVIDIA_DRIVER_CAPABILITIES=all \
    $IMAGE_NAME
