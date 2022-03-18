# cmake 的 c++ 项目模板

> by TITH

## 文件（夹）说明

### .vscode

可以不拷贝，实际上也建议不拷贝

用于使 vscode 可以直接按 F5 调试

但安装 cmake tools 之后建议使用该插件的对应功能



### version.h.in

用于版本控制

cmake 会基于此文件生成 version.h 以在c++代码中包含



### include

头文件放在这里



### src

.cpp .c 文件放在这里



## 构建流程

在 CMakeLists.txt 所在目录执行：

```bash
mkdir build
cd build
cmake ..
make
```

## 清理流程

在 CMakeLists.txt 所在目录执行：

```
rm -rf build
```

