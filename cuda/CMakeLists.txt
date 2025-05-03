cmake_minimum_required(VERSION 3.8 FATAL_ERROR)
project(vector_add CUDA)

# Set CUDA specific flags
set(CMAKE_CUDA_STANDARD 14)
set(CMAKE_CUDA_STANDARD_REQUIRED ON)

# Add executable
add_executable(vector_add vector_add.cu)

# Set CUDA specific properties
set_target_properties(vector_add PROPERTIES
    CUDA_SEPARABLE_COMPILATION ON) 