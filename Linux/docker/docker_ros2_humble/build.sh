#!/bin/bash

set -e

IMAGE_NAME=$1

if [ -z "$IMAGE_NAME" ]; then
    echo "Usage: $0 <image-name>"
    exit 1
fi

# Build image with proxy set
# --network host makes localhost to be successfully resolved to host
docker build -t $IMAGE_NAME . \
    --build-arg "http_proxy=http://localhost:1081" \
    --build-arg "https_proxy=http://localhost:1081" \
    --network host