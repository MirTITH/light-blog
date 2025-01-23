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
# 压缩为 tar.xz，压缩等级选择范围：0-9, 默认为 6
tar -I 'xz -T0 -v -9' -cf output.tar.xz file1 folder1

# 压缩为 tar.zst，压缩等级选择范围：1-19, Default: 3
tar -I 'zstd -T0 -v -10' -cf output.tar.zst file1 folder1
```

### 压缩的同时通过 SSH 传输

```shell
# 使用 zstd 压缩
tar -I 'zstd -T16 -19 -v' -cf - my_folder | ssh user@host "cat > Documents/my_folder.tar.zst"

# 使用 xz 压缩
tar -I 'xz -T16 -9 -v' -cf - my_folder | ssh user@host "cat > Documents/my_folder.tar.xz"
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
