# STM32 

## 相关软件安装

### CubeMX

#### 安装

在官网下载安装

#### 创建快捷方式

打开 CubeMX 安装目录，将 `STM32CubeMX/help/STM32CubeMX.ico` 转换成同名的 png 文件。（或者直接使用本目录下的图标）

修改本目录下的 CubeMX.desktop，将其中的路径修改为你的 CubeMX 安装目录

安装 desktop file:

```bash
# 注册 .ioc 文件类型
xdg-mime install --mode user cubemx-ioc.xml

# 添加快捷方式
# (CubeMX.desktop 中已经将 CubeMX 与 ioc 文件关联，执行下面这行后，程序菜单里会出现 CubeMX，并且双击 ioc 文件应该能够直接用 CubeMX 打开)
desktop-file-install --dir=$HOME/.local/share/applications/ CubeMX.desktop
```

### arm-none-eabi-gcc

注意，apt install 的名称 gcc 在前面

```bash
sudo apt install gcc-arm-none-eabi

arm-none-eabi-gcc -v
```
