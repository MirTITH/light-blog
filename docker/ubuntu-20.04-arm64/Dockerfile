FROM nvcr.io/nvidia/l4t-base:35.4.1

ARG DOCKER_FILE_FOLDER

# Create a non-root user
ARG USERNAME=docker_user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

# Update ca-certificates to avoid "Certificate verification failed" error
RUN apt-get update && apt-get install -y ca-certificates

# Change Ubuntu source list
COPY mirrors/ubuntu_20.04_osa_ports.list /etc/apt/sources.list
# COPY mirrors/ubuntu_20.04_tuna_ports.list /etc/apt/sources.list

# Remove docker-clean to enable auto-completion for apt
RUN rm /etc/apt/apt.conf.d/docker-clean

# 设置时区环境变量
ENV TZ=Asia/Shanghai

# 安装 tzdata 并设置时区
RUN apt-get update && apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/$TZ /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

# Create the user
RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -s /bin/bash --uid $USER_UID --gid $USER_GID -m $USERNAME \
    && apt-get update && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

# Switch to non-root user
USER $USERNAME
WORKDIR /home/$USERNAME

# Install some dependencies packages
RUN sudo apt-get update && sudo apt-get upgrade -y \
    && sudo apt-get install -y \
    git vim bash-completion gdb curl \
    iputils-ping zsh python3 python3-pip 
    

# Add user to video group to allow access to webcam
RUN sudo usermod --append --groups video $USERNAME

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

ENTRYPOINT []
CMD ["/bin/zsh"]