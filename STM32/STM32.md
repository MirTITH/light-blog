# STM32 

## 相关软件安装

### CubeMX

在官网下载安装

创建快捷方式（提前看一眼CubeMX.desktop中的位置是否正确）

```bash
sudo cp CubeMX.desktop /usr/share/applications 
```

### arm-none-eabi-gcc

注意，apt install 的名称 gcc 在前面

```bash
sudo apt install gcc-arm-none-eabi

arm-none-eabi-gcc -v
```

