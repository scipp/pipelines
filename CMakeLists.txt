# ~~~
# SPDX-License-Identifier: BSD-3-Clause
# Copyright (c) 2021 Scipp contributors (https://github.com/scipp)
# ~~~
cmake_minimum_required(VERSION 3.16)
project(pipelines-test)
set(CMAKE_MODULE_PATH "${CMAKE_SOURCE_DIR}/cmake")

add_subdirectory(lib)

include(GNUInstallDirs)
install(DIRECTORY "src/pipelines-test/" DESTINATION "pipelines-test")
