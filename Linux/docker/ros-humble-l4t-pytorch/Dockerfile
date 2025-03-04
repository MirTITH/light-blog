FROM dustynv/l4t-pytorch:r36.2.0

ARG DOCKER_FILE_FOLDER

# Create a non-root user
ARG USERNAME=docker_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Update ca-certificates to avoid "Certificate verification failed" error
# RUN apt-get update && apt-get install -y ca-certificates

# Change Ubuntu source list
# COPY mirrors/ubuntu_22.04_ustc.list /etc/apt/sources.list
# COPY mirrors/ubuntu_22.04_tuna.list /etc/apt/sources.list
COPY mirrors/ubuntu_22.04_osa_ports.list /etc/apt/sources.list

# 设置时区环境变量
ENV TZ=Asia/Shanghai

# 安装 tzdata 并设置时区
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata


# Change ROS 2 source list
# ARG ROS2_MIRROR_URL=https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu
# ARG ROS2_MIRROR_URL=https://mirrors.ustc.edu.cn/ros2/ubuntu
ARG ROS2_MIRROR_URL=https://mirrors.osa.moe/ros2/ubuntu

# RUN rm /etc/apt/sources.list.d/ros2.list
RUN apt-get update && apt-get install -y curl gnupg2 \ 
    && curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] $ROS2_MIRROR_URL jammy main" | tee /etc/apt/sources.list.d/ros2.list > /dev/null

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

# Install ROS2
RUN sudo apt-get update && sudo apt-get install -y locales \
    && sudo locale-gen en_US en_US.UTF-8 \
    && sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
ENV LANG=en_US.UTF-8
RUN sudo apt-get update && sudo apt-get install -y software-properties-common \
    && sudo add-apt-repository universe -y \
    && sudo apt-get upgrade -y \
    && sudo apt-get install -y ros-humble-desktop ros-dev-tools

# Install some dependencies packages
RUN sudo apt-get update && sudo apt-get upgrade -y \
    && sudo apt-get install -y \
    git net-tools vim bash-completion psmisc pulseaudio gdb \
    iputils-ping zsh breeze qt5ct fonts-noto-cjk \
    python3-colcon-common-extensions python3-colcon-mixin software-properties-common python3-pip

# Install Gazebo (Arm64 doesn't have this package)
# RUN sudo apt-get update && sudo apt-get install -y ros-humble-gazebo-ros-pkgs

# Get rid of EasyInstallDeprecationWarning
RUN pip install setuptools==58.2.0

RUN colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml && colcon mixin update default

# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME

RUN sudo rosdep init && rosdep update

# zsh
RUN sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)" \
    && git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k \
    && git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions \
    && git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

COPY --chown=$USERNAME:$USERNAME $DOCKER_FILE_FOLDER/.zshrc /home/$USERNAME/
COPY --chown=$USERNAME:$USERNAME $DOCKER_FILE_FOLDER/.bash_aliases /home/$USERNAME/
COPY --chown=$USERNAME:$USERNAME common_files/.p10k.zsh /home/$USERNAME/

RUN git config --global core.quotepath false

# Create some directories to avoid permission issues
# For example, when creating container with `-v /path/to/host_file:/home/$USERNAME/.config/file`,
# the `.config` directory will be created with root permission, and the user will not be able to write to it.
RUN mkdir -p /home/$USERNAME/.config
RUN mkdir -p /home/$USERNAME/.local
RUN mkdir -p /home/$USERNAME/.cache/huggingface
RUN mkdir -p /home/$USERNAME/.cache/modelscope

RUN pip3 install -U modelscope huggingface huggingface_hub

ENTRYPOINT []
CMD ["/bin/zsh"]