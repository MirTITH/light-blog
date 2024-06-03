FROM osrf/ros:noetic-desktop-full

# Add vscode user with same UID and GID as your host system
# (copied from https://code.visualstudio.com/remote/advancedcontainers/add-nonroot-user#_creating-a-nonroot-user)
ARG USERNAME=vscode
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Remove docker-clean to enable auto-completion for apt
RUN rm /etc/apt/apt.conf.d/docker-clean

# Change Ubuntu source list
COPY mirror_osa_20.04.list /etc/apt/sources.list
# RUN echo deb [ signed-by=/usr/share/keyrings/ros1-latest-archive-keyring.gpg ] https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu focal main | tee /etc/apt/sources.list.d/ros1-latest.list
RUN echo deb [ signed-by=/usr/share/keyrings/ros1-latest-archive-keyring.gpg ] https://mirrors.osa.moe/ros/ubuntu focal main | tee /etc/apt/sources.list.d/ros1-latest.list

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch from root to user
USER $USERNAME

COPY bashrc /home/$USERNAME/.bashrc
COPY bash_aliases /home/$USERNAME/.bash_aliases

# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME

# Update all packages
RUN sudo apt-get update && sudo apt-get upgrade -y && sudo apt-get install -y \
    git net-tools vim mesa-utils bash-completion vim nano

# Rosdep update
# RUN rosdep update

