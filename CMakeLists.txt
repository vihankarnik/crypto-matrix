cmake_minimum_required(VERSION 3.14)
project(blockchain_backend)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Find Python and pybind11
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)
find_package(pybind11 REQUIRED)

# Find OpenSSL
find_package(OpenSSL REQUIRED)

# Add pybind11 module (ensure you use the correct paths for your source files)
pybind11_add_module(blockchain
    ../backend/bindings.cpp
    #../backend/blockchain_core.cpp
)

# Link OpenSSL libraries to your target
target_link_libraries(blockchain PRIVATE OpenSSL::SSL OpenSSL::Crypto)

# Include backend folder for headers (if needed)
include_directories(${CMAKE_SOURCE_DIR}/../backend)
