# fcitx5 安装 

## 卸载fcitx

```shell
sudo apt purge *fcitx*
```

## 安装 fcitx5
### ubuntu 22.04
```shell
sudo apt update
sudo apt install fcitx5 'fcitx5-frontend*' fcitx5-chinese-addons fcitx5-material-color fcitx5-module-cloudpinyin kde-config-fcitx5
```

### ubuntu 20.04
```shell
sudo apt update
sudo apt install fcitx5 'fcitx5-frontend*' fcitx5-chinese-addons
```

## 配置 fcitx5
### kubuntu 22.04

 方法1：自行用图形化界面配置

方法2：使用我喜欢的配置

```shell
# 备份
mv ~/.config/fcitx5 ~/.config/fcitx5.bak
mv ~/.local/share/fcitx5 ~/.local/share/fcitx5.bak

# 配置
cp -r fcitx5_config_file/config/fcitx5 ~/.config/
cp -r fcitx5_config_file/share/fcitx5 ~/.local/share/
```

## 安装词典

中文维基

https://github.com/felixonmars/fcitx5-pinyin-zhwiki

萌娘百科

https://github.com/outloudvi/mw2fcitx/releases


Copy into ~/.local/share/fcitx5/pinyin/dictionaries/ (create the folder if it does not exist)

```
mkdir -p ~/.local/share/fcitx5/pinyin/dictionaries/
```

## 安装皮肤
### fcitx5-breeze
1.  下载 https://github.com/scratch-er/fcitx5-breeze/releases
2.  执行 `install.sh`


### Simple-white 和 Simple-dark
> https://www.cnblogs.com/maicss/p/15056420.html

```bash
mkdir -p ~/.local/share/fcitx5/themes/
cp -r fcitx5-simple-themes/* ~/.local/share/fcitx5/themes
gedit ~/.config/fcitx5/conf/classicui.conf
# 修改为 Simple-white 或 Simple-dark
```

## 启用fcitx5
kubuntu 22.04 重启即可

如果重启不行：
```bash
im-config
```

然后选择fcitx5 
