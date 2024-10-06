cmake_minimum_required(VERSION 3.15...3.27)
 
PROJECT(surfe)
#SET(BUILD_SHARED_LIBS_ON)
SET(CMAKE_CXX_STANDARD 11 )
SET(CMAKE_INSTALL_RPATH "${CMAKE_INSTALL_PREFIX}")

find_package(OpenMP)
if (OPENMP_FOUND)
    set (CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set (CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)
# Get Eigen dependency
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})
#include_directories(${PROJECT_SOURCE_DIR}/eigen-git-mirror/Eigen)#add_subdirectory(eigen-git-mirror)
set(CMAKE_INSTALL_RPATH "$ORIGIN")
# Setup RPATH for finding shared libraries at runtime
set(CMAKE_INSTALL_RPATH "$ORIGIN")

# Setup math_lib
FILE(GLOB MATH_LIB_HEADERS "math_lib/*.h")
FILE(GLOB MATH_LIB_SOURCES "math_lib/*.cpp")

add_library(math_lib SHARED ${MATH_LIB_HEADERS} ${MATH_LIB_SOURCES})
target_include_directories(math_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/math_lib)

# Setup surfe_lib
FILE(GLOB SURFE_LIB_HEADERS "surfe_lib/*.h")
FILE(GLOB SURFE_LIB_SOURCES "surfe_lib/*.cpp")

add_library(surfe_lib SHARED ${SURFE_LIB_HEADERS} ${SURFE_LIB_SOURCES})
target_include_directories(surfe_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/surfe_lib
                                            ${CMAKE_CURRENT_SOURCE_DIR}/math_lib)
target_link_libraries(surfe_lib math_lib)

# Setup Python bindings
pybind11_add_module(_surfepy surfepy/pybindings.cpp)
target_link_libraries(_surfepy PRIVATE surfe_lib math_lib)

# Install targets
install(TARGETS _surfepy surfe_lib math_lib DESTINATION ${CMAKE_INSTALL_PREFIX}/surfepy)



