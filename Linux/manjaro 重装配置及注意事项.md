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
Server = https://mirrors.osa.moe/manjaro/stable/$repo/$arch
Server = https://mirrors.ustc.edu.cn/manjaro/stable/$repo/$arch
```

2. 更新系统

```
sudo pacman -Syu
```

### 调整挂载

#### 添加 @data 子卷
```shell
sudo su
mkdir /mnt/root
mount /dev/nvmeXnXpX /mnt/root/ # 将 nvmeXnXpX 修改为系统所在分区
cd /mnt/root/
btrfs subvolume create @data
chown xy:xy \@data
su xy
cd \@home/xy/
mv Documents Downloads Music Pictures Public Templates Videos /mnt/root/\@data/
```

仿照下面内容修改 /etc/fstab:

> 注意：ntfs3 仅在 Linux Kernel 5.15 及之后版本支持，在之前的版本需要改为 ntfs

```
# /etc/fstab: static file system information.
#
# Use 'blkid' to print the universally unique identifier for a device; this may
# be used with UUID= as a more robust way to name devices that works even if
# disks are added and removed. See fstab(5).
#
# <file system>             <mount point>  <type>  <options>  <dump>  <pass>
UUID=ECF3-4233                              /boot/efi            vfat    umask=0077                               0 2 
UUID=54f87a00-f2f8-43cf-ba1f-fc907d8af239   /                    btrfs   subvol=/@,discard=async,ssd              0 0 
UUID=54f87a00-f2f8-43cf-ba1f-fc907d8af239   /home                btrfs   subvol=/@home,discard=async,ssd          0 0 
UUID=54f87a00-f2f8-43cf-ba1f-fc907d8af239   /mnt/data            btrfs   subvol=/@data,discard=async,ssd          0 0 
UUID=54f87a00-f2f8-43cf-ba1f-fc907d8af239   /var/cache           btrfs   subvol=/@cache,discard=async,ssd         0 0 
UUID=54f87a00-f2f8-43cf-ba1f-fc907d8af239   /var/log             btrfs   subvol=/@log,discard=async,ssd           0 0 
UUID=50ef37f3-c793-4358-a857-3c943b5aac37   swap                 swap    noatime                                  0 0 
tmpfs                                       /tmp                 tmpfs   noatime,mode=1777                        0 0 

/mnt/data/Documents                         /home/xy/Documents   none    bind                                     0 0 
/mnt/data/Downloads                         /home/xy/Downloads   none    bind                                     0 0 
/mnt/data/Music                             /home/xy/Music       none    bind                                     0 0 
/mnt/data/Pictures                          /home/xy/Pictures    none    bind                                     0 0 
/mnt/data/Public                            /home/xy/Public      none    bind                                     0 0 
/mnt/data/Templates                         /home/xy/Templates   none    bind                                     0 0 
/mnt/data/Videos                            /home/xy/Videos      none    bind                                     0 0 
UUID=7484A7EC84A7AF54                       /mnt/win_d           ntfs3   windows_names,uid=1000,gid=1000,nofail   0 0 
```

### 安装 AUR 助手等
```bash
# 编译各种包需要的依赖
sudo pacman -S base-devel

# AUR 助手
sudo pacman -S yay

# clash-verge-rev-bin
yay -S clash-verge-rev-bin

# v2raya（没有 clash 好用）
yay -S v2raya-bin

# v2raya 自启动
sudo systemctl disable v2ray --now
sudo systemctl start v2raya.service
sudo systemctl enable v2raya.service

# 另一个 AUR 助手（没有梯子装不上）
yay -S paru-bin

# edge 建议先将系统语言切换成英文，这样默认bing才是国际版的
paru -S microsoft-edge-stable-bin
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
sudo pacman -Rns firefox

# 如果说会破坏依赖，可以尝试如下命令，删除软件包和所有依赖这个软件包的程序
sudo pacman -Rsc firefox
```

### Zsh
#### Oh My Zsh
```bash
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

#### Theme: powerlevel10k
1. Clone the repository:
```bash
git clone --depth=1 https://gitee.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

2. Set ZSH_THEME="powerlevel10k/powerlevel10k" in ~/.zshrc.

#### 插件
> https://zhuanlan.zhihu.com/p/61447507

```
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
```

Edit ~/.zshrc:

```
plugins=(
    git
    z
    zsh-autosuggestions
    zsh-syntax-highlighting
)
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
paru -S arm-none-eabi-gcc arm-none-eabi-gdb arm-none-eabi-newlib
```

### git
```shell
git config --global user.email "1023515576@qq.com"
git config --global user.name "Yang XIE"
git config --global core.quotepath false
```

### 其他软件
- gdb
- cmake ninja make
- linuxqq
- qqmusic
- netease-cloud-music
- noto-fonts-cjk
- ttf-lxgw-wenkai
- dotnet-runtime-6.0
- tldr

> 另见 [linux 软件安装.md](linux%20软件安装.md)

### ssh
```shell
sudo pacman -S openssh
sudo systemctl enable sshd.service
sudo systemctl start sshd.service
```

### Piper 鼠标管理软件
paru -S piper

### 禁用鼠标键盘唤醒
[ubuntu 重装配置.md](ubuntu%20重装配置.md##%20禁用鼠标键盘唤醒)

### reboot-to-manjaro.sh
```bash
mkdir ~/.local/bin
cp ./reboot-to-manjaro.sh ~/.local/bin/
```

## xyrc

```shell
cp xyrc ~/.local/
```

然后在 .zshrc 和 .bashrc 中添加 `source $HOME/.local/xyrc`

## 注意事项

### 安装软件时密钥出错
Signature from "User <email@gmail.com>" is unknown trust, installation failed

<https://wiki.archlinuxcn.org/wiki/Pacman#Signature_from_%22User_%3Cemail@gmail.com%3E%22_is_unknown_trust,_installation_failed>

### 关闭 TTY Tab 报警声
`setterm --blength 0`

### swap 文件

> btrfs 不太支持 swap 文件，如果是 btrfs 建议使用 swap 分区

```bash
sudo fallocate -l 8G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
sudo bash -c "echo /swapfile none swap defaults 0 0 >> /etc/fstab"
```