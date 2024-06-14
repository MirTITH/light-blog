FROM osrf/ros:humble-desktop-full

# Create a non-root user
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Change Ubuntu source list
COPY mirror_22.04_osa.list /etc/apt/sources.list

# Change ROS 2 source list
# https://mirrors.osa.moe/ros2/ubuntu
# https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu
# https://mirrors.ustc.edu.cn/ros2/ubuntu
ARG ROS2_MIRROR_URL=https://mirrors.osa.moe/ros2/ubuntu

RUN rm /etc/apt/sources.list.d/ros2-latest.list
RUN apt-get install curl gnupg2 && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] $ROS2_MIRROR_URL jammy main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Remove docker-clean to enable auto-completion for apt
RUN rm /etc/apt/apt.conf.d/docker-clean

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Install some dependencies packages
RUN sudo apt-get update \
    && sudo apt-get install -y \
    python3-colcon-common-extensions python3-colcon-mixin software-properties-common python3-pip xauth \
    git net-tools vim mesa-utils bash-completion nano psmisc

# Get rid of EasyInstallDeprecationWarning
RUN pip install setuptools==58.2.0

RUN colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml && colcon mixin update default

# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME

RUN rosdep update

COPY --chown=$USERNAME:$USERNAME entry_point.sh /entry_point.sh

# 保持容器运行
ENTRYPOINT ["/entry_point.sh"]
