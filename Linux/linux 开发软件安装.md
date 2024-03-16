# 开发软件

## Miniconda

These four commands quickly and quietly install the latest 64-bit version of the installer and then clean up after themselves. To install a different version or architecture of Miniconda for Linux, change the name of the `.sh` installer in the `wget` command.

```bash
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
rm -rf ~/miniconda3/miniconda.sh
```

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:

```bash
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

取消默认进入 base

```shell
conda config --set auto_activate_base false
```

## Conda CUDA

```sh
# 安装
conda install cuda -c nvidia

# 卸载
conda remove cuda
```

## ROS

校内源：https://mirrors-help.osa.moe/ros/

官网：http://wiki.ros.org/noetic/Installation/Ubuntu

## ROS 2

### Humble for 22.04

```shell
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

# 添加源（以下二选一）：
# 官方源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# HITsz 内网源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.osa.moe/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop ros-dev-tools
# 完成！

# Gazebo 11
sudo apt install ros-humble-gazebo-ros-pkgs

# 测试：
# 开一个终端：
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
# 再开一个终端：
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

### 解决zsh下ros2命令无法补全的问题

在 `/opt/ros/humble/setup.zsh` 中最后加上

```sh
# argcomplete for ros2 & colcon
eval "$(register-python-argcomplete3 ros2)"
eval "$(register-python-argcomplete3 colcon)"
```

> https://blog.csdn.net/lhz_king/article/details/132456374

## Qt Creator

官网下载安装包

如果要换源：

```
./qt-unified-linux-x64-4.5.1-online.run --mirror https://ipv4.mirrors.ustc.edu.cn/qtproject
```

## .Net 6

```shell
# 注意 20.04 改成对应的 ubuntu 发行版本
# ubuntu 22.04 可以直接执行最后一步 apt install
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt update
sudo apt install dotnet-runtime-6.0
```
