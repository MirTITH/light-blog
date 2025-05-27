# manjaro 重装配置及注意事项

## 重装配置

### 更新系统

1. 换源

- 方法一：自动配置
    ```shell
    sudo pacman-mirrors -c China
    ```

- 方法二：图形界面手动选择
  
    ```shell
    sudo pacman-mirrors -i -c China
    ```
    
- 方法三：编辑配置文件，可以使用官方源里没有的镜像

    编辑文件 `/etc/pacman.d/mirrorlist`

    ```
    ## Country : China
    Server = https://mirrors.osa.moe/manjaro/stable/$repo/$arch
    
    ## Country : China
    Server = https://mirrors.ustc.edu.cn/manjaro/stable/$repo/$arch
    
    ## Country : China
    Server = https://mirrors.sjtug.sjtu.edu.cn/manjaro/stable/$repo/$arch
    ```
    
    之后将 `/etc/pacman.d/mirrorlist` 设为只读，防止被自动更改：
    
    ```shell
    # 添加只读属性
    sudo chattr +a /etc/pacman.d/mirrorlist
    
    # 如果想再次修改，需要先删除只读属性
    sudo chattr -a /etc/pacman.d/mirrorlist
    
    # 检查属性
    lsattr /etc/pacman.d/mirrorlist
    ```


2. 更新系统

    ```shell
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
编译各种包需要的依赖
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

# edge 建议先将系统语言切换成英文，这样默认 bing 才是国际版的
paru -S microsoft-edge-stable-bin

# Chrome
paru -S google-chrome
```

```bash
编辑配置
kate /etc/pacman.conf /etc/makepkg.conf /etc/paru.conf
```

并进行如下修改：

| 文件         | 修改                                   |
| ------------ | -------------------------------------- |
| pacman.conf  | 取消注释：`#Color`                     |
| makepkg.conf | MAKEFLAGS = "-j2" -> MAKEFLAGS = "-j8" |
| paru.conf    | 取消注释：`#BottomUp` `#SudoLoop`      |


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
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k
```

2. Set ZSH_THEME = "powerlevel10k/powerlevel10k" in ~/.zshrc.

#### 插件
> https://zhuanlan.zhihu.com/p/61447507

```
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/conda-incubator/conda-zsh-completion ${ZSH_CUSTOM:=~/.oh-my-zsh/custom}/plugins/conda-zsh-completion
```

Edit ~/.zshrc:

```
plugins=(
    git
    z
    zsh-autosuggestions
    zsh-syntax-highlighting
    conda-zsh-completion
)
```


### 安装 fcitx5 中文输入法
```bash
paru -S manjaro-asian-input-support-fcitx5 fcitx5-chinese-addons fcitx5-pinyin-zhwiki fcitx5-pinyin-moegirl
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
- linuxqq-nt-bwrap
    - slirp4netns: 固定 MAC 地址时需要
    - socat: 固定 MAC 地址时需要
    - 沙盒目录挂载配置文件：将文件 `config_files/qq-bwrap-flags.conf` 复制到 `~/.config/`

- wechat-universal-bwrap
    - 沙盒目录挂载配置文件：将文件夹 `config_files/wechat-universal/` 复制到 `~/.config/`

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
```shell
paru -S wakeup-triggers
sudo systemctl start wakeup-triggers.service
sudo systemctl enable wakeup-triggers.service
```

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

## 开启休眠功能

KDE桌面环境的manjaro在安装时，如果选择“自动分区，带有休眠功能“，则应该已经自动配置好了。

如果是手动分区安装的，则似乎不会自动配置好。

### 开启步骤

1. 确保已经创建并启用 swap 分区

   > 建议使用 swap 分区，而不是 swap 文件

2. 配置 initramfs：

   编辑 /etc/mkinitcpio.conf，在 `HOOKS=` 中添加 `resume`. 

   > 注意： the `resume` hook must go *after* the `udev` hook.

   例如，对于我的 manjaro：

   ```
   HOOKS=(base udev autodetect kms modconf block keyboard keymap consolefont plymouth filesystems resume)
   ```

   或（来自 ArchWiki）：

   ```
   HOOKS=(base udev autodetect microcode modconf kms keyboard keymap consolefont block filesystems resume fsck)
   ```

3. Regenerate the initramfs for these changes to take effect: 

   ```shell
   sudo mkinitcpio -P
   ```

4. 测试：

   对于比较新的 UEFI 固件的电脑，到此为止应该配置完毕了，可以休眠测试一下。

   如果休眠失败，则重启后再休眠测试一下。

   如果还失败，则进行以下步骤：

   1. 找到 SWAP 分区的 UUID（不是 PARTUUID）：

      ```shell
      sudo blkid | grep swap
      ```

   2. 编辑 /etc/default/grub，向 `GRUB_CMDLINE_LINUX_DEFAULT` 添加 resume=xxx，例如：

      ```
      GRUB_CMDLINE_LINUX_DEFAULT="quiet splash resume=UUID=xxxx-xxxx-xxxx"
      ```

      其中 resume 格式可以如下（建议使用UUID）：

      - `resume=UUID=4209c845-f495-4c43-8a03-5363dd433153`
      - `resume="PARTLABEL=Swap partition"`
      - `resume=/dev/archVolumeGroup/archLogicalVolume`

   3. 重启

   4. 再次测试

### 休眠方法

KDE 应该在开始菜单里有休眠按钮

命令行方法：

```shell
sudo systemctl hibernate
```

## manjaro 注意事项

### 安装软件时密钥出错
Signature from "User <email@gmail.com>" is unknown trust, installation failed

<https://wiki.archlinuxcn.org/wiki/Pacman#Signature_from_%22User_%3Cemail@gmail.com%3E%22_is_unknown_trust,_installation_failed>

```shell
sudo pacman -Sy archlinux-keyring manjaro-keyring
```

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