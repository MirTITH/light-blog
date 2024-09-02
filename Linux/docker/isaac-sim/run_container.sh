#!/bin/bash

set -e

echo "Setting variables..."
command="$@"
if [[ -z "$@" ]]; then
    command="bash"
fi
# Set to desired Nucleus
omni_server="http://omniverse-content-production.s3-us-west-2.amazonaws.com/Assets/Isaac/4.1"
if ! [[ -z "${OMNI_SERVER}" ]]; then
	omni_server="${OMNI_SERVER}"
fi
# Set to desired Nucleus username
omni_user="admin"
if ! [[ -z "${OMNI_USER}" ]]; then
	omni_user="${OMNI_USER}"
fi
# Set to desired Nucleus password
omni_password="admin"
if ! [[ -z "${OMNI_PASS}" ]]; then
	omni_password="${OMNI_PASS}"
fi
# Set to "Y" to accept EULA
accept_eula="Y"
if ! [[ -z "${ACCEPT_EULA}" ]]; then
	accept_eula="${ACCEPT_EULA}"
fi
# Set to "Y" to opt-in
privacy_consent="Y"
if ! [[ -z "${PRIVACY_CONSENT}" ]]; then
	privacy_consent="${PRIVACY_CONSENT}"
fi
# Set to an email or unique user name
privacy_userid="${omni_user}"
if ! [[ -z "${PRIVACY_USERID}" ]]; then
	privacy_userid="${PRIVACY_USERID}"
fi

# echo "Logging in to nvcr.io..."
# docker login nvcr.io

# echo "Pulling docker image..."
# docker pull nvcr.io/nvidia/isaac-sim:4.1.0

echo "Running Isaac Sim container with X11 forwarding..."
xhost +local:docker

# Create directories by current user
mkdir -p ~/docker/isaac-sim/kit/cache
mkdir -p ~/docker/isaac-sim/home

docker run -it --name isaac-sim --entrypoint bash --runtime=nvidia --gpus all -e "ACCEPT_EULA=${accept_eula}" --rm --network=host \
	-v $HOME/.Xauthority:/home/ubuntu/.Xauthority -e DISPLAY \
	-e "OMNI_USER=${omni_user}" -e "OMNI_PASS=${omni_password}" \
	-e "OMNI_SERVER=${omni_server}" \
    -e "PRIVACY_CONSENT=${privacy_consent}" -e "PRIVACY_USERID=${privacy_userid}" \
    -v ~/docker/isaac-sim/kit/cache:/isaac-sim/kit/cache:rw \
	-v ~/docker/isaac-sim/home:/home/ubuntu:rw \
	my-isaac-sim \
	-c "${command}"

echo "Isaac Sim container run completed!"
