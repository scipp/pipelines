# ~~~
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
# ~~~
cmake_minimum_required(VERSION 3.16)
project(pipelines-test)
if(NOT DEFINED CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif(NOT DEFINED CMAKE_CXX_STANDARD)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

include(GTest)

set(TARGET_NAME "pipelines-test")
add_executable(${TARGET_NAME} EXCLUDE_FROM_ALL test.cpp)
include_directories(SYSTEM ${GTEST_INCLUDE_DIR})
target_link_libraries(${TARGET_NAME} LINK_PRIVATE gtest_main ${GTEST_LIBRARIES})
