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

### 解决zsh下ros2命令无法补全的问题

在 `/opt/ros/humble/setup.zsh` 中最后加上

```sh
# argcomplete for ros2 & colcon
eval "$(register-python-argcomplete3 ros2)"
eval "$(register-python-argcomplete3 colcon)"
```

> https://blog.csdn.net/lhz_king/article/details/132456374
