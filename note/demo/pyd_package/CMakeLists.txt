cmake_minimum_required(VERSION 3.20)
project(c_fib C)

#ADD_DEFINITIONS(-DMS_WINDOWS)
include_directories("C:/Users/guanglin.liang/Downloads/Python-3.6.15/Python-3.6.15/Include")
include_directories("C:/Users/guanglin.liang/Downloads/Python-3.6.15/Python-3.6.15/PC")
link_directories("D:/tools/tools/python366-32with-pdb/libs")
link_libraries("python36_d.lib")

set(CMAKE_SHARED_MODULE_SUFFIX_CXX ".pyd")
set(CMAKE_SHARED_LIBRARY_SUFFIX_CXX ".pyd")
set(CMAKE_SHARED_MODULE_SUFFIX_C ".pyd")
set(CMAKE_SHARED_LIBRARY_SUFFIX_C ".pyd")

set(CMAKE_C_STANDARD 11)

add_library(c_fib SHARED my_module/c_fib.c)
