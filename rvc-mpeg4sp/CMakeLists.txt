cmake_minimum_required(VERSION 3.10)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)

# List of HLS_CLOCK_PERIOD settings to build binaries for
set(CLOCK_LIST 3.3 10)

macro(rvc_generate CONFIG_PATH CLOCK_SETTING)

  set(__TARGET_PATH__ generated/${CONFIG_PATH}_${CLOCK_SETTING})
  set(__TARGET__ rvc-mpeg4sp_${CONFIG_PATH}_${CLOCK_SETTING})
  # message(STATUS "")
    # -- Heterogeneous HLS target
  streamblocks(
    ${__TARGET__}_HLS
    PLATFORM vivado-hls
    QID RVC.decoderDemo
    TARGET_PATH ${__TARGET_PATH__}
    SOURCE_PATH . ../system
    XCF_SOURCE_PATH ${CONFIG_PATH}.xcf
    PARTITIONING
  )

  # -- Heterogeneous MULTICORE target
  streamblocks(
    ${__TARGET__}_MULTICORE
    PLATFORM multicore
    QID RVC.decoderDemo
    TARGET_PATH ${__TARGET_PATH__}
    SOURCE_PATH . ../system
    XCF_SOURCE_PATH ${CONFIG_PATH}.xcf
    PARTITIONING
  )

  # -- Heterogenous target, generates both software and hardware
  add_custom_target(
    ${__TARGET__} ALL
    DEPENDS ${__TARGET__}_HLS ${__TARGET__}_MULTICORE
  )

  file(MAKE_DIRECTORY ${__TARGET_PATH__}/build)
  add_custom_command(
    TARGET ${__TARGET__}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -DHLS_CLOCK_PERIOD=${CLOCK_SETTING} -DUSE_SDACCEL=true ..
    COMMAND make decoderDemo_kernel_xclbin -j
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
    COMMENT "Building FPGA binary for ${__TARGET__}"
  )
endmacro()


foreach(index RANGE 1 5)
  foreach(CLK ${CLOCK_LIST})

    rvc_generate(configuration_${index} ${CLK})

  endforeach()
endforeach()

# -- SystemC simulation target

macro(rvc_generate_sc CONFIG_PATH)
  streamblocks_systemc(
    rvc-mpeg4sp_SYSTEMC_${CONFIG_PATH}
    QID RVC.decoderDemo
    TARGET_PATH generated/profiling/${CONFIG_PATH}/sc
    SOURCE_PATH . ../system
    XCF_SOURCE_PATH ${CONFIG_PATH}.xcf
  )
endmacro()

# rvc_generate_sc(configuration_1)
# rvc_generate_sc(configuration_2)


# -- software only target
streamblocks(
  rvc-mpeg4sp_SOFTWARE
  PLATFORM multicore
  QID RVC.decoderDemo
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH . ../system
)