cmake_minimum_required(VERSION 3.10)


# Streamblocks build command
include(${CMAKE_CURRENT_LIST_DIR}/../../../Streamblocks.cmake)


# Common options
include(${CMAKE_CURRENT_LIST_DIR}/../../../common.cmake)


set(HLS_JOBS "4" CACHE STRING "Number of parallel HLS jobs")


set(ORCC_APPS_PATH ${CMAKE_CURRENT_LIST_DIR}/../../../orc-apps)
set(ORCC_DESIGN_PATH ${CMAKE_CURRENT_LIST_DIR}/../../../orcc-designs)

set(ORCC_SOURCE_PATH 
  ${ORCC_APPS_PATH}/Research/src
  ${ORCC_APPS_PATH}/System/src
  ${ORCC_APPS_PATH}/RVC/src
  ${ORCC_DESIGN_PATH}/Research/src
)

set(XDF_SOURCE_PATH
  ${ORCC_DESIGN_PATH}/Research/src
  ${ORCC_APPS_PATH}/Research/src
  ${CMAKE_CURRENT_LIST_DIR}/../../../
)

set(CAL_SOURCE_PATH 
  ${CMAKE_SOURCE_DIR}
  ${CMAKE_CURRENT_LIST_DIR}/../../../system/art
  ${CMAKE_CURRENT_LIST_DIR}/../../utils
)

function(generate_network NAMESPACE NETWORK_NAME CONFIG_PATH CLK_IX) 


  list(GET CLOCK_LIST ${CLK_IX} CLOCK_SETTING)
  list(GET CLOCK_IDS ${CLK_IX} CLK_ID)
  set(__TARGET_PATH__ ${OUTPUT_PATH}/${CONFIG_PATH}_${CLOCK_SETTING})

  set(__TARGET__ ${CONFIG_PATH}_${CLOCK_SETTING})


  
  streamblocks(
    ${__TARGET__}_HLS
    PLATFORM vivado-hls
    QID ${NAMESPACE}.${NETWORK_NAME}
    SOURCE_PATH ${CAL_SOURCE_PATH}
    ORCC_SOURCE_PATH ${ORCC_SOURCE_PATH}
    XDF_SOURCE_PATH ${XDF_SOURCE_PATH}
    TARGET_PATH ${__TARGET_PATH__}
    XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${CONFIG_ROOT}/${CONFIG_PATH}.xcf
    QUEUE_DEPTH ${FIFO_QUEUE_DEPTH}
    PARTITIONING
  )

  streamblocks(
    ${__TARGET__}_MULTICORE
    PLATFORM multicore
    QID ${NAMESPACE}.${NETWORK_NAME}
    SOURCE_PATH ${CAL_SOURCE_PATH}
    ORCC_SOURCE_PATH ${ORCC_SOURCE_PATH}
    XDF_SOURCE_PATH ${XDF_SOURCE_PATH}
    TARGET_PATH ${__TARGET_PATH__}
    XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${CONFIG_ROOT}/${CONFIG_PATH}.xcf
    PARTITIONING
  )

  set(__TARGET_DIRS_FILES__
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin 
    xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}
  )

  add_custom_command(
    OUTPUT ${__TARGET_DIRS_FILES__}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}
    # COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/foreman_qcif_30.bit
    COMMENT "Making directories for ${__TARGET__} ${CMAKE_COMMAND} -E make_directory ${__TARGET_PATH__}/build ${__TARGET_PATH__}/bin ${__TARGET_PATH__}/bin/xclbin xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}"
    DEPENDS ${__TARGET__}_MULTICORE ${__TARGET__}_HLS
  )

  add_custom_target(
    ${__TARGET__} ALL
    DEPENDS ${__TARGET__}_HLS ${__TARGET__}_MULTICORE ${__TARGET_DIRS_FILES__}
  )
  
  # -- command to build FPGA binary
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/${NETWORK_NAME}_kernel.hw.xclbin
    COMMAND ${CMAKE_COMMAND} 
      -DHLS_CLOCK_PERIOD=${CLOCK_SETTING} 
      -DUSE_SDACCEL=${USE_SDACCEL} 
      -DUSE_VITIS=${USE_VITIS}
      -DTARGET=hw
      -DIS_MPSOC=${IS_MPSOC}
      -DFPGA_NAME=${FPGA_NAME}
      -DPLATFORM=${PLATFORM}
      -DMPSOC_CLOCK_ID=${CLK_ID}
      -DKERNEL_FREQ=${KERNEL_FREQ}
      .. > cmake.xclbin.config.log
    COMMAND make ${NETWORK_NAME}_kernel_xclbin -j${HLS_JOBS}
    DEPENDS ${__TARGET__}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
    COMMENT "Building FPGA binary for ${__TARGET__}"
  
  )
  add_custom_target(
    ${__TARGET__}_xclbin ALL
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/${NETWORK_NAME}_kernel.hw.xclbin
  )

  add_dependencies(all_xclbin ${__TARGET__}_xclbin)
endfunction()


function (generate_profiliing NAMESPACE NETWORK_NAME)
  # SystemC profiling target
  streamblocks_systemc(
    hardware_profiling
    QID                 ${NAMESPACE}.${NETWORK_NAME}
    TARGET_PATH         ${OUTPUT_PATH}/profiling/hw
    SOURCE_PATH         ${CAL_SOURCE_PATH}
    ORCC_SOURCE_PATH    ${ORCC_SOURCE_PATH}
    XDF_SOURCE_PATH     ${XDF_SOURCE_PATH}
  )

  # Software profiling target
  streamblocks(
    software_profiling
    QID                 ${NAMESPACE}.${NETWORK_NAME}
    TARGET_PATH         ${OUTPUT_PATH}/profiling/sw
    SOURCE_PATH         ${CAL_SOURCE_PATH}
    ORCC_SOURCE_PATH    ${ORCC_SOURCE_PATH}
    XDF_SOURCE_PATH     ${XDF_SOURCE_PATH}
    PLATFORM multicore
  )

endfunction()


