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
conda config --set auto_activate false
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

# 添加源（以下几个源选择一个）：
# 官方源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# HITsz 内网源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.osa.moe/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# 中科大源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.ustc.edu.cn/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
# 清华源
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] https://mirrors.tuna.tsinghua.edu.cn/ros2/ubuntu jammy main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop ros-dev-tools
# 完成！

# Gazebo 11（可选）
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

### 解决 EasyInstallDeprecationWarning

如果没有报 warning，可以跳过这一步。

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

## Docker

### For Ubuntu

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

5. 安装 Nvidia Container Toolkit：
   1. 打开链接：https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
   2. 按照网页中的指引，在主机中安装 nvidia-container-toolkit
   3. 执行网页中 Configuring Docker 的部分，注意不需要执行 Rootless mode

### For manjaro

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

如果更新显卡驱动后 docker 容器启动异常，报错类似于：
```
Error response from daemon: failed to create task for container: failed to create shim task: OCI runtime create failed: runc create failed: unable to start container process: error during container init: failed to fulfil mount request: open /usr/lib/libEGL_nvidia.so.590.48.01: no such file or directory
```

可重新安装 nvidia-container-toolkit，或执行：

```bash
sudo nvidia-ctk cdi generate --output="/etc/cdi/nvidia.yaml"
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

## texlive

```shell
paru -S texlive-meta texlive-langcjk texlive-langchinese biber
```

## Matlab
### For Arch

1. **安装mpm (Matlab package manager)**
   
   ```shell
   paru -S matlab-mpm
   ```
   
2. **使用mpm安装Matlab**
   
   ```shell
   mpm install --release=<release> --destination=~/matlab MATLAB <other products>
   ```
   若希望为设备上所有用户安装，则将目录修改为公共目录，例如:
   ```shell
   sudo mpm install --release R2025b --products \
                  Simulink \
                  Stateflow \
                  Simulink_Control_Design \
                  Simulink_Compiler \
                  Simulink_Real-Time \
                  DSP_System_Toolbox \
                  Simscape \
                  Simscape_Electrical \
                  Simscape_Fluids \
                  Simscape_Multibody \
                  Fixed-Point_Designer \
                  --matlabroot /opt/MATLAB/R2025b/
   ```
   
3. **激活Matlab**

   如果 `--release <= R2022b`
   ```shell
   ~/matlab/bin/activate_matlab.sh
   ```
   如果 `--release >= R2023a`
   ```shell
   ~/matlab/bin/glnxa64/MathWorksProductAuthorizer.sh
   ```
   注意，当为所有用户安装时，应相应修改路径。可能需要sudo以提供权限，否则可能出现权限冲突的错误提示：Unable to install license. Please try again later.
   ```shell
   sudo /opt/MATLAB/R2025b/bin/glnxa64/MathWorksProductAuthorizer.sh
   ```

4. **修复链接库**
   如果 `--release >= R2023a`，在运行`MathWorksProductAuthorizer.sh`时极大概率报`segfault`，是由于某个版本的`gnutls`更新导致的，运行以下命令使得matlab激活脚本使用老版的`gnutls`：
   ```shell
   wget https://archive.archlinux.org/packages/g/gnutls/gnutls-3.8.9-1-x86_64.pkg.tar.zst
   mkdir -p matlab/gnutls
   tar -xf gnutls-3.8.9-1-x86_64.pkg.tar.zst -C matlab/gnutls
   mkdir -p ~/matlab/bin/glnxa64/gnutls
   cp -a ~/matlab/gnutls/usr/lib/libgnutls* ~/matlab/bin/glnxa64/gnutls/
   cd /home/user/matlab/bin/glnxa64/
   ln -s gnutls/* ./
   ```
   为所有用户安装的命令相应修改为
   ```shell
   wget https://archive.archlinux.org/packages/g/gnutls/gnutls-3.8.9-1-x86_64.pkg.tar.zst
   mkdir -p matlab/gnutls
   tar -xf gnutls-3.8.9-1-x86_64.pkg.tar.zst -C matlab/gnutls
   sudo mkdir -p /opt/MATLAB/R2025b/bin/glnxa64/gnutls
   sudo cp -a matlab/gnutls/usr/lib/libgnutls.* /opt/MATLAB/R2025b/bin/glnxa64/gnutls/
   sudo ln -s gnutls/* ./
   ```
   之后应该可以回到上一步成功进行Matlab的激活。
   ```shell
   sudo ./MathWorksProductAuthorizer.sh
   ```

5. **权限问题**
   直接运行会出现安全提示：You are currently running MATLAB as root。在 Linux 中，长期以 root 身份运行图形界面程序会有安全风险，且以后产生的代码文件权限也会变成 root，导致普通用户无法编辑。最后可以把MATLAB目录的所有权交还给普通用户
   首先创建软连接：
   ```shell
   sudo ln -s /opt/MATLAB/R2025b/bin/matlab /usr/local/bin/matlab
   ```

6. **（可选）修复中文输入法**

   由于 Arch 总是滚动更新到最新的 GCC 和 Qt，而 MATLAB 捆绑的库相对滞后，导致了 ABI 不兼容。通过强制使用系统 C++ 标准库可以暂时修复输入法。
   <u>***注意**：如果下次 MATLAB 小版本更新（如 R2025b Update 1），这些操作可能需要重新执行，因为更新程序可能会还原这些库文件。</u>

   （1）进入 MATLAB 安装目录下的系统库路径，重命名其自带的库文件，迫使系统调用 `/usr/lib/libstdc++.so.6`。

   ```bash
   cd /opt/MATLAB/R2025b/sys/os/glnxa64/
   sudo mv libstdc++.so.6 libstdc++.so.6.bak
   ```

   （2）将 MATLAB 自带的 Qt5 相关动态库移出搜索路径，强制使用与系统插件版本一致（或兼容）的 Qt 库。

   ```bash
   cd /opt/MATLAB/R2025b/bin/glnxa64/
   sudo mkdir qt_backup
   sudo mv libQt5* qt_backup/
   ```

   （3）在MATLAB插件目录下建立系统插件软连接，注入 fcitx5 输入法插件

   ```bash
   sudo mkdir -p /opt/MATLAB/R2025b/bin/glnxa64/platforminputcontexts
   sudo ln -sf /usr/lib/qt/plugins/platforminputcontexts/libfcitx5platforminputcontextplugin.so /opt/MATLAB/R2025b/bin/glnxa64/platforminputcontexts/
   ```

   （4）在启动脚本中加入环境配置

   ```bash
   export QT_IM_MODULE=fcitx
   export XMODIFIERS=@im=fcitx
   ```

   

## Vivado

1. 安装依赖库
```shell
paru -S ncurses5-compat-libs  libxcrypt-compat  libpng12  lib32-libpng12  gtk3  inetutils  xorg-xlsclients  cpio
```

2. 在Vivado官网下载安装脚本并运行
```shell
chmod +x FPGA_*.bin
./ FPGA_*.bin
```
