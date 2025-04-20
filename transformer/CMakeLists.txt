cmake_minimum_required(VERSION 3.10)
project(transformer)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find required packages
find_package(CURL REQUIRED)

# Add source files
set(TRANSFORMER_SOURCES
    src/transformer.cpp
)

# Add benchmark sources
set(BENCHMARK_SOURCES
    benchmark/benchmark.cpp
    benchmark/utils.cpp
    benchmark/run_benchmarks.cpp
)

# Create transformer library
add_library(transformer STATIC ${TRANSFORMER_SOURCES})
target_include_directories(transformer 
    PUBLIC 
    ${CMAKE_CURRENT_SOURCE_DIR}/include
)

# Create benchmark executable
add_executable(run_benchmarks ${BENCHMARK_SOURCES})
target_link_libraries(run_benchmarks 
    PRIVATE 
    transformer
    CURL::libcurl
)
target_include_directories(run_benchmarks 
    PRIVATE 
    ${CMAKE_CURRENT_SOURCE_DIR}/include
    ${CMAKE_CURRENT_SOURCE_DIR}/benchmark
)

# Enable optimization
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O2") 