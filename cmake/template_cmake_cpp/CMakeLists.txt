cmake_minimum_required(VERSION 3.12)

project(cpp_project VERSION 0.1.0) # 项目名称和版本

# 编译器相关参数
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall") # 添加 c++ 编译器参数
set(CMAKE_C_STANDARD 11) #使用c11标准
set(CMAKE_CXX_STANDARD 11) #使用c++11标准

# 项目版本管理
configure_file(version.h.in version.h) # 根据 version.h.in 生成 version.h
include_directories(${PROJECT_BINARY_DIR}) # 包含 version.h 所在目录

include_directories(include) # 在 include 文件夹搜索头文件

# 搜索所有的 .c .cpp 文件，并将列表赋给 src_list（需要最低3.12版本）
file(GLOB src_list CONFIGURE_DEPENDS "src/*.c" "src/*.cpp")
add_executable(${PROJECT_NAME} ${src_list})

#设置可执行文件输出目录
# set(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR})

# 单元测试
# include(CTest)
# enable_testing()

# 项目打包
# set(CPACK_PROJECT_NAME ${PROJECT_NAME})
# set(CPACK_PROJECT_VERSION ${PROJECT_VERSION})
# include(CPack)
