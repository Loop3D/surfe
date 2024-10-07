cmake_minimum_required(VERSION 3.15...3.27)

project(surfe)

# Get Eigen dependency
set(CMAKE_MODULE_PATH ${PROJECT_SOURCE_DIR}/cmake)
include(FetchContent)

FetchContent_Declare(
  Eigen
  GIT_REPOSITORY https://github.com/eigenteam/eigen-git-mirror
  GIT_TAG 3.3.7
  GIT_SHALLOW TRUE
  GIT_PROGRESS TRUE
)
FetchContent_MakeAvailable(Eigen)

# Set C++ standard
set(CMAKE_CXX_STANDARD 11)

# Setup OpenMP (if available)
find_package(OpenMP)
if (OPENMP_FOUND)
    set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
endif()

# Setup pybind11
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(pybind11 CONFIG REQUIRED)

# Setup RPATH for finding shared libraries at runtime
set(CMAKE_INSTALL_RPATH "$ORIGIN")

# Setup math_lib
file(GLOB MATH_LIB_HEADERS "math_lib/*.h")
file(GLOB MATH_LIB_SOURCES "math_lib/*.cpp")
add_library(math_lib SHARED ${MATH_LIB_HEADERS} ${MATH_LIB_SOURCES})
target_include_directories(math_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/math_lib)
target_include_directories(math_lib PRIVATE ${eigen_SOURCE_DIR})  # Include Eigen in math_lib

# Setup surfe_lib
file(GLOB SURFE_LIB_HEADERS "surfe_lib/*.h")
file(GLOB SURFE_LIB_SOURCES "surfe_lib/*.cpp")
add_library(surfe_lib SHARED ${SURFE_LIB_HEADERS} ${SURFE_LIB_SOURCES})
target_include_directories(surfe_lib PUBLIC ${CMAKE_CURRENT_SOURCE_DIR}/surfe_lib
                                             ${CMAKE_CURRENT_SOURCE_DIR}/math_lib)
target_include_directories(surfe_lib PRIVATE ${eigen_SOURCE_DIR})  # Include Eigen in surfe_lib
target_link_libraries(surfe_lib math_lib)

# Setup Python bindings
pybind11_add_module(_surfepy surfepy/pybindings.cpp)
target_link_libraries(_surfepy PRIVATE surfe_lib math_lib)
target_include_directories(_surfepy PRIVATE ${eigen_SOURCE_DIR})  # Include Eigen in Python bindings

# Install targets
install(TARGETS _surfepy surfe_lib math_lib DESTINATION ${CMAKE_INSTALL_PREFIX}/surfepy)
