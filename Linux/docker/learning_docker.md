# Learning Docker

## Commands

### Image

```shell
docker image ls # == docker images
docker image pull ros:humble # == docker pull
docker image rm # == docker rmi
docker image rm -f # Delete image even there is a container related to the image
docker image build -t <new_image_name> <Dockerfile_folder>

# 保存、压缩镜像
# 注：在 Ubuntu 上，zstd 需要另外安装。通常 xz 比 zstd 压缩率高，但速度慢
docker save my_image:latest | xz -T16 -6 -v > my_image.tar.xz # 使用 xz。-T16：使用 16 个线程；-9：压缩等级（0-9，9 最高）；-v 显示进度
docker save my_image:latest | zstd -T16 -10 -v > my_image.tar.zst # 使用 zstd。-T16：使用 16 个线程；-10：压缩等级（1-19, 19 最高）；-v 显示进度

# 保存、压缩并传输镜像
docker save my_image:latest | xz -T16 -9 -v | ssh user@target_host 'cat > my_image.tar.xz'  # 使用 xz

# 保存、压缩、传输并加载镜像
docker save my_image:latest | xz -T16 -v | ssh user@target_host 'xz -d | docker load'  # 使用 xz
docker save my_image:latest | zstd -T0 --adapt -v | ssh user@target_host 'zstd -d | docker load' # 使用 zstd. --adapt: Dynamically adapt compression level to I/O conditions.

# 加载镜像
xz -d -c my_image.tar.xz | docker load # 使用 xz
zstd -d -c my_image.tar.zst | docker load # 使用 zstd
```

### Container

#### docker container run

`docker container run` == `docker run`

```shell
docker run [switches] <image>
# Recommended example:
docker run -it --user ros --network=host --ipc=host -v $PWD/source:/my_source_code my_image
```

| switches                              | description                                                                        |
| ------------------------------------- | ---------------------------------------------------------------------------------- |
| -it                                   | -i: interactive -t: TTY                                                            |
| --rm                                  | Remove container after it stopped.                                                 |
| --name <container_name>               | Give the new container a name.                                                     |
| -v <path_on_host>:<path_in_container> | Mount path_on_host to path_in_container. Note: these path should be absolute path. |
| --user`<user>`                        | Run as a user.`<user>` can be user name or uid which is in docker environment.     |
| --network=host                        | 容器与宿主机共享相同的网络接口和 IP 地址                                           |
| --ipc=host                            | 容器使用宿主机的 IPC（Inter-Process Communication，进程间通信）命名空间            |

#### Other commands

```shell
docker container start -i <container> # Start a stopped container

docker container exec <container> <COMMAND> # == docker exec -it <container>. Run another command in the same container.
docker exec -it <container> bash # Run another bash shell in the same container

docker container ls -a # == docker ps -a
docker container stop
docker container rm # == docker rm
docker container prune # Remove all stopped container

docker commit <container> image:tag # 将容器转换成镜像
```

## Example docker files

See subfolders

## 清理

```shell
docker system df # 查看磁盘占用
docker container prune # 删除所有停止运行的容器
docker buildx prune #  clear the build cache. 在 build cache 出错导致 build 失败时，这条命令很有用
docker image prune # remove unused images
docker volume prune # removes all anonymous volumes not used by any containers
docker network prune # remove unused networks
docker system prune #  remove all unused containers, images, networks, and build cache
```

## GUI and GPU

### 使容器内可以运行 GUI 程序

该方法适用于所有显卡，步骤如下：

1. docker run 时，添加下面的参数：

    ```shell
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw
    --env DISPLAY
    ```

    例如：

    ```shell
    docker run -it \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw --env DISPLAY \
        <IMAGE_NAME>
    ```

3. 有时需要在主机上执行以下命令（每次开机只需要执行一次）

    ```shell
    xhost +local:docker # 允许 docker 内的程序访问主机中的 X 服务器，从而能在主机中显示
    # or
    xhost + # Allow all users to display
    ```

5. 测试验证

    1. 在 docker 中安装一些简单的 GUI 程序：

        ```shell
        sudo apt install x11-apps
        ```
    2. 在 docker 中运行下面的一些 GUI 程序，如果出现窗口，则成功了
        - xclock
        - xeyes

### 开启 N 卡加速

上面的操作只是能显示图形界面，但没有 GPU 硬件加速。这会导致一些 3D 界面可能很卡，并且不能用显卡跑网络

该方法只适用于 N 卡，步骤如下：

1. 安装 Nvidia Container Toolkit：
    1. 打开链接：https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html
    2. 按照网页中的指引，在主机中安装 nvidia-container-toolkit
    3. 执行网页中 Configuring Docker 的部分，注意不需要执行 Rootless mode

2. docker run 时，添加下面的参数：
    ```shell
    --runtime=nvidia
    --gpus all                           # 向容器中添加所有显卡
    --env NVIDIA_DRIVER_CAPABILITIES=all # 开启 N 卡驱动的所有功能。（不加该项可以跑 CUDA，但没有 OpenGL 加速）
    ```
    
    例如：
    
    ```shell
    docker run -it \
        -v /tmp/.X11-unix:/tmp/.X11-unix:rw --env DISPLAY \
        --runtime=nvidia --gpus all --env NVIDIA_DRIVER_CAPABILITIES=all \
        <IMAGE_NAME>
    ```

### 测试

#### 测试 nvidia-smi

在docker中运行 nvidia-smi，看是否正常输出

#### 测试 OpenGL

```shell
sudo apt install mesa-utils
glxinfo | grep "OpenGL version"
```

检查输出，如果类似 `OpenGL version string: 4.6.0 NVIDIA 550.107.02`，则有 NVIDIA GPU 加速

如果类似 `OpenGL version string: 4.5 (Compatibility Profile) Mesa 24.0.9-0ubuntu0.1`，则没有 GPU 加速

For AMD GPUs use the following cmd:

```shell
glxinfo | grep '^direct rendering:'
```

If you got `direct rendering: Yes` then you have 3D acceleration


#### 测试 Vulkan

```shell
sudo apt install vulkan-tools
vulkaninfo --summary
```

检查输出的 `Devices:` 部分，如果正确显示 GPU 型号，并且 deviceType=PHYSICAL_DEVICE_TYPE_DISCRETE_GPU，则有 GPU 加速，例如：

```
Devices:
========
GPU0:
        apiVersion         = 1.3.277
        driverVersion      = 550.107.2.0
        vendorID           = 0x10de
        deviceID           = 0x1f15
        deviceType         = PHYSICAL_DEVICE_TYPE_DISCRETE_GPU
        deviceName         = NVIDIA GeForce RTX 2060
        driverID           = DRIVER_ID_NVIDIA_PROPRIETARY
        driverName         = NVIDIA
        driverInfo         = 550.107.02
        conformanceVersion = 1.3.7.2
        deviceUUID         = 5078994e-b73e-29d5-6fee-afcf9a1fa407
        driverUUID         = 12adfef6-a92a-528b-8610-45df7fa0a5b8
```

如果输出如下，则没有 GPU 加速：

```
Devices:
========
GPU0:
        apiVersion         = 1.3.274
        driverVersion      = 0.0.1
        vendorID           = 0x10005
        deviceID           = 0x0000
        deviceType         = PHYSICAL_DEVICE_TYPE_CPU
        deviceName         = llvmpipe (LLVM 17.0.6, 256 bits)
        driverID           = DRIVER_ID_MESA_LLVMPIPE
        driverName         = llvmpipe
        driverInfo         = Mesa 24.0.9-0ubuntu0.1 (LLVM 17.0.6)
        conformanceVersion = 1.3.1.1
        deviceUUID         = 6d657361-3234-2e30-2e39-2d3075627500
        driverUUID         = 6c6c766d-7069-7065-5555-494400000000
```

## Sound

使得 docker 中的程序能发出声音

1. 确保主机上的 PulseAudio 已启动：

   ```shell
   # 在主机中执行
   pactl info
   ```

   如果你看到输出包含 PulseAudio 的信息，那么它已经正常运行。

2. 启动 Docker 镜像时共享音频设备

   ```shell
   docker run -it \
       --name=my_audio_container \
       --device /dev/snd \
       -v $XDG_RUNTIME_DIR/pulse:/tmp/pulse \
       -e PULSE_SERVER=unix:/tmp/pulse/native \
       -v ~/.config/pulse/cookie:/root/.config/pulse/cookie \
       ubuntu:22.04
   ```

3. 在 Docker 中安装必要的包

   ```shell
   apt update
   apt install pulseaudio
   ```

4. 测试

   ```shell
   paplay /usr/share/sounds/freedesktop/stereo/audio-channel-front-center.oga
   ```

# Issues

## docker build 时无法访问外网

```shell
docker build -t <IMAGE_NAME> . \
    --build-arg "http_proxy=http://localhost:7890" \
    --build-arg "https_proxy=http://localhost:7890" \
    --build-arg "all_proxy=socks5://localhost:7890" \
    --network host
```

## ros topic list 卡住

> 参考 https://github.com/ros2/ros2cli/issues/903#issuecomment-2146858338

在 `/etc/docker/daemon.json` 中添加 `"default-ulimits"` 配置：

```json
{
    "default-ulimits": {
        "nofile": {
            "Name": "nofile",
            "Hard": 1048576,
            "Soft": 1024
        }
    }
}
```

然后执行：

```shell
sudo systemctl restart docker
```
