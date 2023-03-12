FROM nvidia/cudagl:11.1.1-base-ubuntu20.04

# Minimal setup
RUN echo deb http://10.249.12.85/ubuntu/ focal main restricted universe multiverse | tee /etc/apt/sources.list\
    && echo deb http://10.249.12.85/ubuntu/ focal-updates main restricted universe multiverse >> /etc/apt/sources.list\
    && echo deb http://10.249.12.85/ubuntu/ focal-backports main restricted universe multiverse >> /etc/apt/sources.list\
    && echo deb http://10.249.12.85/ubuntu/ focal-security main restricted universe multiverse >> /etc/apt/sources.list
RUN apt-get update && apt-get upgrade \
    && apt-get install -y locales lsb-release \
    && apt-get install -y zsh && chsh -s $(which zsh)
ARG DEBIAN_FRONTEND=noninteractive
RUN dpkg-reconfigure locales

# Install ROS Noetic
RUN sh -c '. /etc/lsb-release && echo "deb http://mirrors.ustc.edu.cn/ros/ubuntu/ `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
RUN apt-get install curl -y --no-install-recommends
RUN curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | apt-key add -
RUN apt-get update \
    && apt-get install -y --no-install-recommends ros-noetic-desktop-full
RUN apt-get install -y --no-install-recommends python3-rosdep
# RUN rosdep init \
#  && rosdep fix-permissions \
#  && rosdep update
RUN echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
