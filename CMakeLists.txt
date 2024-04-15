# CMake config
cmake_minimum_required(VERSION 3.22)

project(p2 LANGUAGES CXX)

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release)
endif()

# C++ Config
set(CMAKE_CXX_STANDARD 23)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# compiler config
add_definitions(-std=c++23)
add_compile_options(-Wall -Wextra -pedantic -pedantic-errors -fPIC)

if (CMAKE_COMPILER_IS_GNUCXX AND CMAKE_CXX_COMPILER_VERSION LESS 11.0)
    message (
        FATAL_ERROR
        "GCC-11.0 or above is required"
    )
endif()


# compile libs
add_subdirectory(src)