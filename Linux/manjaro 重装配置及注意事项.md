# manjaro 重装配置及注意事项

## 重装配置

### 更新系统

1. 换源

- 方法一（自动配置）
    ```shell
    sudo pacman-mirrors -c China
    ```

- 方法二（图形界面手动选择）
    ```
    sudo pacman-mirrors -i -c China
    ```

- 方法三（编辑配置文件，可以使用官方源里没有的镜像）
    > 编辑文件 /etc/pacman.d/mirrorlist
    ```
    ##
    ## Manjaro Linux custom mirrorlist
    ## Generated on 2023-02-22 11:31
    ##
    ## Please use 'pacman-mirrors -id' To reset custom mirrorlist
    ## Please use 'pacman-mirrors -c all' To reset custom mirrorlist
    ## To remove custom config run  'pacman-mirrors -c all'
    ##

    ## Country : China
    Server = http://10.249.12.85/manjaro/stable/$repo/$arch
    Server = https://mirrors.ustc.edu.cn/manjaro/stable/$repo/$arch

    ```


2. 更新系统
    ```
    sudo pacman -Syu
    ```


### 安装 AUR 助手等
```bash
# AUR 助手
sudo pacman -Ss yay

# v2raya，没有梯子寸步难行
yay -S v2raya-bin

sudo systemctl disable v2ray --now
sudo systemctl start v2raya.service
sudo systemctl enable v2raya.service

# 浏览器（没有梯子安装慢）
yay -S microsoft-edge-stable-bin

# 另一个 AUR 助手（没有梯子装不上）
yay -S paru-bin
```

```bash
# 编辑配置
kate /etc/pacman.conf /etc/makepkg.conf /etc/paru.conf
```

并进行如下修改：

| 文件         | 修改                               |
| ------------ | ---------------------------------- |
| pacman.conf  | 取消注释：`#Color`                 |
| makepkg.conf | MAKEFLAGS="-j2" -> MAKEFLAGS="-j8" |
| paru.conf    | 取消注释：`#BottomUp` `#SudoLoop`  |


### 删除 firefox
```bash
sudo pacman -Rs firefox

# 如果说会破坏依赖，可以尝试如下命令，删除软件包和所有依赖这个软件包的程序
sudo pacman -Rsc firefox
```

### 安装 fcitx5 中文输入法
1. 安装输入法
```bash
paru -S manjaro-asian-input-support-fcitx5 fcitx5-chinese-addons fcitx5-pinyin-zhwiki fcitx5-pinyin-moegirl
```
2. 解决 Qt6 程序无法使用输入法的问题

    > 可以尝试直接将编译好的文件复制到相应目录（记得修改为你的Qt安装路径）
    ```
    cp ./libfcitx5platforminputcontextplugin.so ~/Qt/6.4.2/gcc_64/plugins/platforminputcontexts
    cp ./libfcitx5platforminputcontextplugin.so ~/Qt/Tools/QtCreator/lib/Qt/plugins/platforminputcontexts
    ```

    如果以上操作无效：

    1. 克隆仓库
        ```
        git clone git@github.com:fcitx/fcitx5-qt.git
        或：
        git clone https://github.com/fcitx/fcitx5-qt.git
        ```
    2. 修改CMakeLists.txt
        ```
        option(ENABLE_QT4 "Enable Qt 4" On)
        option(ENABLE_QT5 "Enable Qt 5" On)
        option(ENABLE_QT6 "Enable Qt 6" On)
        ```
    3. 编译安装
        ```
        cd fcitx5-qt
        mkdir build && cd build
        cmake ..
        make -j8
        sudo make install
        ```
    4. 复制文件（记得修改为你的Qt安装路径）
    ```
    # qt6 程序
    cp ./qt6/platforminputcontext/libfcitx5platforminputcontextplugin.so ~/Qt/6.4.2/gcc_64/plugins/platforminputcontexts
    # qt creator
    cp ./qt6/platforminputcontext/libfcitx5platforminputcontextplugin.so ~/Qt/Tools/QtCreator/lib/Qt/plugins/platforminputcontexts
    ```

### 修改 grub
```bash
kate /etc/default/grub
```

### 安装 arm-none-eabi 套件
```bash
paru arm none eabi
# 然后选择安装需要的 arm-none-eabi-gcc arm-none-eabi-gdb arm-none-eabi-newlib
```

### docker
```
paru -S docker
sudo systemctl start docker.service
sudo systemctl enable docker.service
sudo docker version
sudo docker info
sudo usermod -aG docker $USER
reboot
```

### 其他软件
- gdb
- cmake ninja
- linuxqq
- qqmusic
- netease-cloud-music
- noto cjk
- dotnet-runtime-6.0

> 另见 [linux 软件安装.md](linux%20软件安装.md)

### 禁用鼠标键盘唤醒
[ubuntu 重装配置.md](ubuntu%20重装配置.md##%20禁用鼠标键盘唤醒)

### reboot-to-manjaro.sh
```bash
mkdir ~/.local/bin
cp ./reboot-to-manjaro.sh ~/.local/bin/
```


## 注意事项

### 安装软件时密钥出错
Signature from "User <email@gmail.com>" is unknown trust, installation failed

<https://wiki.archlinuxcn.org/wiki/Pacman#Signature_from_%22User_%3Cemail@gmail.com%3E%22_is_unknown_trust,_installation_failed>

### 关闭 TTY Tab 报警声
`setterm -blength 0`

### swap 文件

> btrfs 不太支持 swap 文件，如果是 btrfs 建议使用 swap 分区

```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo bash -c "echo /swapfile none swap defaults 0 0 >> /etc/fstab"
```
