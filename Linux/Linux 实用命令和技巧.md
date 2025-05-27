# Linux 实用命令和技巧

## 终端连接 wifi 

1. 列出网卡设备`nmcli d`

2. Enable WiFi (if disabled): Use `nmcli r wifi on`

3. scan for wifi networks:  `sudo iwlist scan`

4. List available networks: Use `nmcli d wifi list` to see a list of SSIDs, security types, and signal strength.

5. Connect to a network: 

   ```shell
   # 二选一：
   sudo nmcli --ask device wifi connect <SSID> # 询问密码
   sudo nmcli d wifi connect <SSID> password <password> # 直接指定密码
   ```

## 压缩

```shell
# 压缩为 tar.xz
# -T16: 使用16个线程压缩，0 表示使用所有可用的 CPU 核心
# -v: 启用详细模式，显示压缩进度和详细信息
# -9: 设置压缩级别为9（范围：0-9, 默认为 6）
tar -I 'xz -T0 -v -9' -cf output.tar.xz file1 folder1

# 压缩为 tar.zst，压缩等级选择范围：1-19, Default: 3
tar -I 'zstd -T0 -v -19' -cf output.tar.zst file1 folder1
```

### 压缩的同时通过 SSH 传输

```shell
# 使用 zstd 压缩
tar -I 'zstd -T16 -19 -v' -cf - my_folder | ssh user@host "cat > Documents/my_folder.tar.zst"
# 使用 xz 压缩
tar -I 'xz -T16 -9 -v' -cf - my_folder | ssh user@host "cat > Documents/my_folder.tar.xz"

# 使用 zstd 压缩并自动解压（需要先在服务端安装 zstd）
# 从本地传到服务器
tar -I 'zstd -T0 -v --adapt' -cf - my_folder | ssh user@host "tar -I 'zstd' -xf - -C Documents/my_folder"
# 从服务器传到本地
ssh user@host "tar -I 'zstd -T0 -v --adapt' -cf - /path/to/server_folder" | tar -I 'zstd' -xf - -C ~/local

# 使用 xz 压缩并自动解压（一般ubuntu默认安装了 xz）
tar -I 'xz -T16 -v' -cf - my_folder | ssh user@host "tar -I 'xz' -xf - -C Documents/my_folder"
```

shell 函数：

```shell
push_to_server() {
    local src="${1:?用法：push_to_server 本地文件夹 用户@主机:远程路径}"
    local remote="${2:?用法：push_to_server 本地文件夹 用户@主机:远程路径}"
    local user_host="${remote%:*}"
    local dest_path="${remote#*:}"
    
    tar -I 'zstd -T0 -v' -cf - "$src" | ssh "$user_host" "tar -I 'zstd' -xf - -C \"$dest_path\""
}

pull_from_server() {
    local remote="${1:?用法：pull_from_server 用户@主机:远程路径 本地目标路径}"
    local user_host="${remote%:*}"
    local src_path="${remote#*:}"
    local dest="${2:?用法：pull_from_server 用户@主机:远程路径 本地目标路径}"
    
    # 自动提取父目录和目标目录名
    local parent_dir="${src_path%/*}"
    local dir_name="${src_path##*/}"

    # 强制进入父目录打包（天然去除父路径）
    ssh "$user_host" "tar -C \"$parent_dir\" -I 'zstd -T0 -v' -cf - \"$dir_name\"" | tar -I 'zstd' -xf - -C "$dest"
}
```

## 关闭图形界面

```shell
# 关闭图形界面
sudo systemctl isolate multi-user.target

# 开启图形界面
do systemctl isolate graphical.target
```

## manjaro 包管理器

以下命令中，paru 和 sudo pacman 应该都可以互换

paru 还可以安装 AUR 仓库中的软件

```shell
paru -Rns package_name # 删除软件，配置文件，依赖
paru -Qdt # 列出孤包
sudo pacman -U /path/to/package/package_name-version.pkg.tar.zst # 安装本地包
sudo pacman -U http://www.example.com/repo/example.pkg.tar.zst # 安装远程包（指定网址）
```

#### 查询一个包含具体文件的包名

```shell
paru -Fy # 同步文件数据库
paru -F libcrypto.so.1.1 # 查找某个文件在哪个包里（报缺失 .so 错误时很有用）
```

## tmux

启用鼠标：

方法一（临时）：

Ctrl+B, 输入：`set -g mouse`

方法二（永久）：

```shell
vim ~/.tmux.conf
# 在文件中写入
set-option -g mouse on
```

## Force GpenGL software rendering

```shell
LIBGL_ALWAYS_SOFTWARE=1 ./the_program_name

# or
QT_XCB_FORCE_SOFTWARE_OPENGL=1 ./the_program_name

# or
export LIBGL_ALWAYS_SOFTWARE=1
./the_program_name
```

## 使 Qt 程序以 x11 运行

### 在终端中

```shell
QT_QPA_PLATFORM=xcb <your_app>
```

### desktop 文件

以 yakuake 为例：
```shell
`cp /usr/share/applications/org.kde.yakuake.desktop ~/.local/share/applications/`
```

Then open `~/.local/share/applications/org.kde.yakuake.desktop` file with your favourite text editor, find the line `Exec=yakuake` and change it to `Exec=env QT_QPA_PLATFORM=xcb yakuake`. Now restart the app.

> [Workaround for yakuake in Wayland : r/kde](https://www.reddit.com/r/kde/comments/hh99xb/workaround_for_yakuake_in_wayland/)