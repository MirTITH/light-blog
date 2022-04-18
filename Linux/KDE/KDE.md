# KDE 配置 

## 软件安装

### language package

```bash 
sudo apt install $(check-language-support)
```

### Nautilus

```bash
 sudo apt install nautilus nautilus-share
```

### yakuake

```bash
 sudo apt install yakuake
```

然后在设置-开机和关机-自动启动里添加启动项

### kde最大化窗口时隐藏标题栏

安装：Active Window Control（在顶栏显示按钮）

参考https://blog.csdn.net/yalin1997/article/details/122711033 在latte-dock 里设置最大化隐藏标题栏

### flameshot 截图工具

> https://github.com/flameshot-org/flameshot

安装：

```
sudo apt install flameshot
```

设置快捷键：

#### On KDE Plasma desktop

To make configuration easier, there's a [file](https://github.com/flameshot-org/flameshot/blob/master/docs/shortcuts-config/flameshot-shortcuts-kde.khotkeys) in the repository that more or less automates this process. This file will assign the following keys to the following actions by default:

| Keys                  | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| Prt Sc                | Start the Flameshot screenshot tool and take a screenshot    |
| Ctrl + Prt Sc         | Wait for 3 seconds, then start the Flameshot screenshot tool and take a screenshot |
| Shift + Prt Sc        | Take a full-screen (all monitors) screenshot and save it     |
| Ctrl + Shift + Prt Sc | Take a full-screen (all monitors) screenshot and copy it to the clipboard |

If you don't like the defaults, you can change them manually later.

Steps for using the configuration:

1. The configuration file configures shortcuts so that Flameshot automatically saves (without opening the save dialog) screenshots to `~/Pictures/Screenshots` folder. Make sure you have that folder by running the following command:

   ```bash
   mkdir -p ~/Pictures/Screenshots
   ```

   (If you don't like the default location, you can skip this step and configure your preferred directory later.)

2. Download the configuration file:

   ```bash
   cd ~/Desktop
   wget https://raw.githubusercontent.com/flameshot-org/flameshot/master/docs/shortcuts-config/flameshot-shortcuts-kde.khotkeys
   ```

3. Make sure you have the `khotkeys` installed using your package manager to enable custom shortcuts in KDE Plasma.

4. Go to *System Settings* → *Shortcuts* → *Custom Shortcuts*.

5. If there's one, you'll need to disable an entry for Spectacle, the default KDE screenshot utility, first because its shortcuts might collide with Flameshot's ones; so, just uncheck the *Spectacle* entry.

6. Click *Edit* → *Import...*, navigate to the Desktop folder (or wherever you saved the configuration file) and open the configuration file.

7. Now the Flameshot entry should appear in the list. Click *Apply* to apply the changes.

8. If you want to change the defaults, you can expand the entry, select the appropriate action and modify it as you wish; the process is pretty self-explanatory.

9. If you installed Flameshot as a Flatpak, you will need to create a symlink to the command:

   ```bash
   ln -s /var/lib/flatpak/exports/bin/org.flameshot.Flameshot ~/.local/bin/flameshot
   ```

