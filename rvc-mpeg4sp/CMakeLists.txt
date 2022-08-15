cmake_minimum_required(VERSION 3.3)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)


set(XCF_CONFIG "configuration_0.xcf")
set(FPGA_NAME "xcu200-fsgd2104-2-e")
set(PLATFORM "xilinx_u200_xdma_201830_2")
set(TARGET "hw_emu")

set(CAL_SOURCE_PATH
  ${CMAKE_SOURCE_DIR}
  ${CMAKE_SOURCE_DIR}/../system
)

set(GEN_DIR ${CMAKE_CURRENT_BINARY_DIR}/generated)

# -- Heterogeneous HLS target
streamblocks(
  RVC_HLS
  PLATFORM vivado-hls
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${GEN_DIR}/hetero
  SOURCE_PATH ${CAL_SOURCE_PATH}
  XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${XCF_CONFIG}
  PARTITIONING
)

# -- Heterogeneous MULTICORE target
streamblocks(
  RVC_MULTICORE
  PLATFORM multicore
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${GEN_DIR}/hetero
  SOURCE_PATH ${CAL_SOURCE_PATH}
  XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${XCF_CONFIG}
  PARTITIONING
)

add_custom_command(
  OUTPUT ${GEN_DIR}/hetero/build
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GEN_DIR}/hetero/build
)


# Combined target for code-generation
add_custom_target(
  RVC_GEN
  DEPENDS RVC_HLS RVC_MULTICORE ${GEN_DIR}/hetero/build
)



add_custom_target(
  RVC_BUILD_DIR
  DEPENDS ${GEN_DIR}/hetero/build
)
# Target for building the xclbin
add_custom_command(
  OUTPUT ${GEN_DIR}/hetero/bin/xclbin/Top_RVC_Decoder_kernel.${TARGET}.xclbin
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GEN_DIR}/hetero/build
  COMMAND ${CMAKE_COMMAND}
    -DHLS_CLOCK_PERIOD=4
    -DUSE_SDACCEL=0
    -DUSE_VITIS=1
    -DTARGET=${TARGET}
    -DFPGA_NAME=${FPGA_NAME}
    -DPLATFORM=${PLATFORM}
    -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
    .. > cmake.xclbin.config.log
  COMMAND ${CMAKE_COMMAND} --build .  --target Top_RVC_Decoder_kernel_xclbin -- -j
  DEPENDS RVC_GEN ${GEN_DIR}/hetero/build
  WORKING_DIRECTORY ${GEN_DIR}/hetero/build
  COMMENT "Building FPGA binary"

)

add_custom_target(
  RVC_xclbin
  DEPENDS ${GEN_DIR}/hetero/bin/xclbin/Top_RVC_Decoder_kernel.${TARGET}.xclbin
)

add_custom_command(
  OUTPUT ${GEN_DIR}/hetero/bin/Top_RVC_Decoder_kernel
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit ${GEN_DIR}/hetero/bin/foreman_qcif_30.bit
  COMMAND ${CMAKE_COMMAND} --build . --target Top_RVC_Decoder
  DEPENDS ${GEN_DIR}/hetero/bin/xclbin/Top_RVC_Decoder_kernel.${TARGET}.xclbin
  WORKING_DIRECTORY ${GEN_DIR}/hetero/build
  COMMENT "Building software binary"
)

add_custom_target(
  RVC ALL
  DEPENDS ${GEN_DIR}/hetero/bin/Top_RVC_Decoder_kernel
)


# -- hardware profile target
streamblocks_systemc(
  RVC_HW_PROFILE
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${GEN_DIR}/profiling/hw
  SOURCE_PATH ${CAL_SOURCE_PATH}
  XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/configuration_0.xcf
)


add_custom_command(
  OUTPUT ${GEN_DIR}/profiling/hw/build ${GEN_DIR}/profiling/hw/bin ${GEN_DIR}/profiling/hw/bin/foreman_qcif_30.bit
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GEN_DIR}/profiling/hw/build
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GEN_DIR}/profiling/hw/bin
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit ${GEN_DIR}/profiling/hw/bin/foreman_qcif_30.bit
)

add_custom_target(
  _hw_profile_files
  DEPENDS ${GEN_DIR}/profiling/hw/build ${GEN_DIR}/profiling/hw/bin
)

add_dependencies(
  RVC_HW_PROFILE _hw_profile_files
)

add_custom_command(
  OUTPUT ${GEN_DIR}/profiling/hw/bin/Top_RVC_Decoder
  COMMAND ${CMAKE_COMMAND} .. -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  COMMAND ${CMAKE_COMMAND} --build . --target Top_RVC_Decoder -- -j
  DEPENDS RVC_HW_PROFILE
  WORKING_DIRECTORY ${GEN_DIR}/profiling/hw/build
)

add_custom_target(
  RVC_HW_PROFILE_BINARY
  DEPENDS ${GEN_DIR}/profiling/hw/bin/Top_RVC_Decoder
)
# -- software profile target

streamblocks(
  RVC_SW_PROFILE
  PLATFORM multicore
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${GEN_DIR}/profiling/sw
  SOURCE_PATH ${CAL_SOURCE_PATH}
)


add_custom_command(
  OUTPUT ${GEN_DIR}/profiling/sw/build ${GEN_DIR}/profiling/sw/bin ${GEN_DIR}/profiling/sw/bin/foreman_qcif_30.bit
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GEN_DIR}/profiling/sw/build
  COMMAND ${CMAKE_COMMAND} -E make_directory ${GEN_DIR}/profiling/sw/bin
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit ${GEN_DIR}/profiling/sw/bin/foreman_qcif_30.bit
)

add_custom_target(
  _sw_profile_files
  DEPENDS ${GEN_DIR}/profiling/sw/build ${GEN_DIR}/profiling/sw/bin
)

add_dependencies(
  RVC_SW_PROFILE _sw_profile_files
)


add_custom_command(
  OUTPUT ${GEN_DIR}/profiling/sw/bin/Top_RVC_Decoder
  COMMAND ${CMAKE_COMMAND} .. -DCMAKE_BUILD_TYPE=${CMAKE_BUILD_TYPE}
  COMMAND ${CMAKE_COMMAND} --build . --target Top_RVC_Decoder -- -j
  DEPENDS RVC_SW_PROFILE
  WORKING_DIRECTORY ${GEN_DIR}/profiling/sw/build
)

add_custom_target(
  RVC_SW_PROFILE_BINARY
  DEPENDS ${GEN_DIR}/profiling/sw/bin/Top_RVC_Decoder
)




