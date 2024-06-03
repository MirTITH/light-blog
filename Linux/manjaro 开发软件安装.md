# manjaro 开发软件安装

### docker

```shell
# 安装
paru -S docker docker-buildx

# 启动和开机自启
sudo systemctl start docker.service
sudo systemctl enable docker.service

# 检查
sudo docker version
sudo docker info

# 使得运行 docker 命令不需要 root 权限，重启生效
sudo usermod -aG docker $USER
reboot
```

接下来安装 NVIDIA Container Toolkit 使得 docker 能够使用 NVIDIA GPU

> https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html

```shell
# 安装
sudo pacman -S nvidia-container-toolkit

# 配置
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker
```

docker 运行 GUI 程序

```shell
# 安装 xorg-xhost
sudo pacman -S  xorg-xhost

# 下面的命令重启电脑后需要再次执行
xhost +local:docker

# 在 docker 中测试
sudo apt update
sudo apt install x11-apps
xclock
```

