FROM nvcr.io/nvidia/isaac-sim:4.1.0

# Do not change these args because they are created by the base image
ARG USERNAME=ubuntu
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Install sudo
RUN apt-get update \
    && apt-get install -y sudo \
    && rm -rf /var/lib/apt/lists/* \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN chown -R $USERNAME:$USERNAME /isaac-sim
USER ubuntu

COPY --chown=$USERNAME:$USERNAME scripts/runapp_ros_humble.sh /isaac-sim/