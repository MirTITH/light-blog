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

# 安装指定版本
# 版本列表请查看 https://anaconda.org/nvidia/cuda
# 例如
conda install nvidia/label/cuda-11.8.0::cuda

# 卸载
conda remove cuda
```

## ROS

校内源：https://mirrors-help.osa.moe/ros/

官网：http://wiki.ros.org/noetic/Installation/Ubuntu

在conda中安装ROS: https://robostack.github.io/GettingStarted.html

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

# colcon mixin
sudo apt install python3-colcon-common-extensions python3-colcon-mixin
colcon mixin add default https://raw.githubusercontent.com/colcon/colcon-mixin-repository/master/index.yaml
colcon mixin update default

# 测试：
# 开一个终端：
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_cpp talker
# 再开一个终端：
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

### zsh 下 ros2 命令补全

在 `~/.zshrc` 中加上：

```shell
# argcomplete for ros2 & colcon
eval "$(register-python-argcomplete3 ros2)"
eval "$(register-python-argcomplete3 colcon)"

source /opt/ros/humble/setup.zsh
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.zsh
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=/opt/ros/humble/
```

> https://blog.csdn.net/lhz_king/article/details/132456374

### bash 下 ros2 命令补全

在 `~/.bashrc` 中加上：

```shell
source /opt/ros/humble/setup.bash
source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash
source /usr/share/colcon_cd/function/colcon_cd.sh
export _colcon_cd_root=/opt/ros/humble/
```

### 解决 EasyInstallDeprecationWarning

因为 ros2 humble 安装 Python 包的方式已经被弃用了，所以报 warning. 

但目前 ros2 humble 并没有很好的替代方案，所以为了不报 warning, 只能降级安装工具 setuptools. 

```shell
# 降级到最后一个不会报 warning 的版本
pip install setuptools==58.2.0
```

> 参考链接：https://answers.ros.org/question/396439/setuptoolsdeprecationwarning-setuppy-install-is-deprecated-use-build-and-pip-and-other-standards-based-tools/

## Qt Creator

官网下载安装包

如果要换源：

```shell
./qt-unified-linux-x64-4.5.1-online.run --mirror https://ipv4.mirrors.ustc.edu.cn/qtproject
```

## .Net 6

### ubuntu 20.04

```shell
wget https://packages.microsoft.com/config/ubuntu/20.04/packages-microsoft-prod.deb -O packages-microsoft-prod.deb
sudo dpkg -i packages-microsoft-prod.deb
rm packages-microsoft-prod.deb
sudo apt update
sudo apt install dotnet-runtime-6.0
```

### ubuntu 22.04

```shell
sudo apt install dotnet-runtime-6.0
```

### Docker

1. 安装 docker

   ```shell
   curl -fsSL https://get.docker.com -o get-docker.sh
   sudo sh get-docker.sh
   ```

2. 使 docker 命令不需要 root 运行

   ```shell
   sudo groupadd docker
   sudo usermod -aG docker $USER
   ```

3. Log out and log back in so that your group membership is re-evaluated.

4. Test your docker installation

   ```shell
   docker run hello-world
   ```

## arm-none-eabi toolchain

1. 从这里下载安装包：

   https://github.com/xpack-dev-tools/arm-none-eabi-gcc-xpack/releases/

   > 注：不要从https://developer.arm.com/downloads/-/arm-gnu-toolchain-downloads/下载，这个网站下载的版本会遇到奇怪的依赖和python版本问题

2. 解压到 `~/.local/xPacks/arm-none-eabi-gcc`

   ```shell
   mkdir -p ~/.local/xPacks/arm-none-eabi-gcc
   cd ~/.local/xPacks/arm-none-eabi-gcc
   tar xvf <下载的安装包路径>
   
   # 删除写权限（更安全）
   chmod -R -w <刚刚解压得到的文件夹>
   # 例如 chmod -R -w xpack-arm-none-eabi-gcc-13.2.1-1.1
   
   # 测试
   cd <刚刚解压得到的文件夹（如 xpack-arm-none-eabi-gcc-13.2.1-1.1）>/bin
   # 例如 cd xpack-arm-none-eabi-gcc-13.2.1-1.1/bin
   ./arm-none-eabi-gcc -v
   ./arm-none-eabi-gdb -v
   ```

3. 链接到PATH中的路径（可选）

   ```shell
   ln -s <刚刚解压得到的文件夹的绝对路径>/bin/* ~/.local/bin
   # 例如 ln -s ~/.local/xPacks/arm-none-eabi-gcc/xpack-arm-none-eabi-gcc-13.2.1-1.1/bin/* ~/.local/bin
   ```
