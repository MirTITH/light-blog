#!/bin/bash

# docker run --name isaac-sim --entrypoint bash -it --runtime=nvidia --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
#     -e "PRIVACY_CONSENT=Y" \
#     -v ~/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
#     -v ~/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
#     -v ~/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
#     -v ~/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
#     -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
#     -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
#     -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
#     -v ~/docker/isaac-sim/documents:/root/Documents:rw \
#     nvcr.io/nvidia/isaac-sim:4.1.0

xhost +
docker run --name isaac-sim --entrypoint bash -it --gpus all -e "ACCEPT_EULA=Y" --rm --network=host \
  -e "PRIVACY_CONSENT=Y" \
  -v $HOME/.Xauthority:/root/.Xauthority \
  -e DISPLAY \
  -v ~/docker/isaac-sim/cache/kit:/isaac-sim/kit/cache:rw \
  -v ~/docker/isaac-sim/cache/ov:/root/.cache/ov:rw \
  -v ~/docker/isaac-sim/cache/pip:/root/.cache/pip:rw \
  -v ~/docker/isaac-sim/cache/glcache:/root/.cache/nvidia/GLCache:rw \
  -v ~/docker/isaac-sim/cache/computecache:/root/.nv/ComputeCache:rw \
  -v ~/docker/isaac-sim/logs:/root/.nvidia-omniverse/logs:rw \
  -v ~/docker/isaac-sim/data:/root/.local/share/ov/data:rw \
  -v ~/docker/isaac-sim/documents:/root/Documents:rw \
  nvcr.io/nvidia/isaac-sim:4.1.0 \
  ./runapp.sh