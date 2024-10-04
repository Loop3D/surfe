#!/bin/bash

# Update package list and install prerequisites
sudo apt-get update
sudo apt-get install -y build-essential cmake git libeigen3-dev pybind11-dev

echo "Installation of pybind11, Eigen, and CMake is complete."

