FROM osrf/ros:humble-desktop-full

# Create a non-root user
ARG USERNAME=ros
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
  && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
  && mkdir /home/$USERNAME/.config && chown $USER_UID:$USER_GID /home/$USERNAME/.config


# Remove docker-clean to enable auto-completion for apt
RUN rm /etc/apt/apt.conf.d/docker-clean

# Change Ubuntu source list
COPY mirror_osa.list /etc/apt/sources.list

# Change ROS 2 source list
# RUN rm /etc/apt/sources.list.d/ros2-latest.list
# RUN apt install curl gnupg2 && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.osa.moe/ros2/ubuntu jammy main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null
# RUN echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu jammy main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Set up sudo
RUN apt-get update \
  && apt-get install -y sudo \
  && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME\
  && chmod 0440 /etc/sudoers.d/$USERNAME \
  && rm -rf /var/lib/apt/lists/*

# Copy the entrypoint and bashrc scripts so we have 
# our container's environment set up correctly
COPY entrypoint.sh /entrypoint.sh
COPY bashrc /home/${USERNAME}/.bashrc

# Example of installing programs
RUN apt-get update \
  && apt-get install -y \
  nano \
  vim \
  bash-completion \
  net-tools

# Set up entrypoint and default command
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
CMD ["bash"]
