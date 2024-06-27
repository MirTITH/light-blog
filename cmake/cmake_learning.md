# Cmake Learning

## find_package()

### 示例

```cmake
find_package(fmt 10.2.1 REQUIRED)
target_link_libraries(YOUR_TARGET fmt::fmt)
```

- fmt: 包名
- 10.2.1: 最小要求版本
- REQUIRED: 表示 CMake 必须找到软件包，否则将停止构建过程

target_link_libraries 用于链接该库

在使用编写良好的库时，只需要这两步就可以添加该库

### 查找路径 

```cmake
# These are search paths for find_package()
# They are in the order of search priority
# cmake 的搜索机制非常复杂，这些只是一部分
# 详细介绍请参考: https://cmake.org/cmake/help/latest/command/find_package.html
# 注意：${CMAKE_PREFIX_PATH} 表示 cmake 内部的变量
#      $ENV{CMAKE_PREFIX_PATH} 表示 shell 中的环境变量

# message("CMAKE_PREFIX_PATH: ${CMAKE_PREFIX_PATH}")
# message("CMAKE_FRAMEWORK_PATH: ${CMAKE_FRAMEWORK_PATH}")
# message("CMAKE_APPBUNDLE_PATH: ${CMAKE_APPBUNDLE_PATH}")

# message("CMAKE_PREFIX_PATH env: $ENV{CMAKE_PREFIX_PATH}")
# message("CMAKE_FRAMEWORK_PATH env: $ENV{CMAKE_FRAMEWORK_PATH}")
# message("CMAKE_APPBUNDLE_PATH env: $ENV{CMAKE_APPBUNDLE_PATH}")

# message("PATH env: $ENV{PATH}")

# message("CMAKE_SYSTEM_PREFIX_PATH: ${CMAKE_SYSTEM_PREFIX_PATH}")
# message("CMAKE_SYSTEM_FRAMEWORK_PATH: ${CMAKE_SYSTEM_FRAMEWORK_PATH}")
# message("CMAKE_SYSTEM_APPBUNDLE_PATH: ${CMAKE_SYSTEM_APPBUNDLE_PATH}")

# message("CMAKE_FIND_ROOT_PATH: ${CMAKE_FIND_ROOT_PATH}")
```

