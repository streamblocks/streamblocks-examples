cmake_minimum_required(VERSION 3.10)

project(bandwidth_test)

add_subdirectory(plink)
set(EXECUTABLE_OUTPUT_PATH ${CMAKE_SOURCE_DIR})
add_executable(bandwidth bandwidth.cpp)
target_include_directories(bandwidth PUBLIC plink/include)
target_link_libraries(bandwidth art-plink)
target_compile_definitions(bandwidth PUBLIC -DOCL_VERBOSE=0)

set_target_properties(bandwidth PROPERTIES CXX_STANDARD 14)

