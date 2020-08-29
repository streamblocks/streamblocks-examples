cmake_minimum_required(VERSION 3.10)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)

# List of HLS_CLOCK_PERIOD settings to build binaries for
# Current clock speeds 300, 250, 200, 150 and 100 MHz
set(CLOCK_LIST 3.3 10)



add_custom_target(all_xclbin) # build all xclbins
add_custom_target(all_bin)    # build all multicore hetero binaries
add_custom_target(all_sc_bin) # build all sc binaries
add_custom_target(all_sc_run) # run all sc simulations


macro(rvc_generate CONFIG_PATH CLOCK_SETTING)

  set(__TARGET_PATH__ generated/${CONFIG_PATH}_${CLOCK_SETTING})
  set(__TARGET__ ${CONFIG_PATH}_${CLOCK_SETTING})
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
  file(MAKE_DIRECTORY ${__TARGET_PATH__}/bin)
  file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit 
    DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/)

  # -- command to build FPGA binary
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/decoderDemo_kernel.hw.xclbin
    COMMAND ${CMAKE_COMMAND} -DHLS_CLOCK_PERIOD=${CLOCK_SETTING} -DUSE_SDACCEL=true -DTARGET=hw .. > cmake.xclbin.config.log
    COMMAND make decoderDemo_kernel_xclbin -j
    DEPENDS ${__TARGET__}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
    COMMENT "Building FPGA binary for ${__TARGET__}"
  
  )
  add_custom_target(
    ${__TARGET__}_xclbin ALL
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/decoderDemo_kernel.hw.xclbin
  )

  # -- software binary
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/decoderDemo
    COMMAND ${CMAKE_COMMAND} -DDISPLAY=off -DCMAKE_BUILD_TYPE=Release .. > cmake.bin.config.log
    COMMAND make decoderDemo -j &> cmake.make.log
    DEPENDS ${__TARGET__}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
  )
  
  add_custom_target(
    ${__TARGET__}_bin ALL
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/decoderDemo
  )

  
  
  add_custom_target(
    ${__TARGET__}_run
    DEPENDS ${__TARGET__}_bin
  )
  add_custom_command(
    TARGET ${__TARGET__}_run
    PRE_BUILD
    COMMAND time ./decoderDemo > decoderDemo.out
    DEPENDS ${__TARGET__}_bin
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin
  )
  
  add_dependencies(all_xclbin ${__TARGET__}_xclbin)
  add_dependencies(all_bin ${__TARGET__}_bin)



  # -- SystemC build and run commands

  set(__TARGET_SC_PATH__ generated/${CONFIG_PATH}_${CLOCK_SETTING}_sc)
  set(__TARGET_SC__ ${__TARGET__}_SC)

  streamblocks_systemc(
    ${__TARGET_SC__}
    QID RVC.decoderDemo
    TARGET_PATH ${__TARGET_SC_PATH__}
    SOURCE_PATH . ../system
    XCF_SOURCE_PATH ${CONFIG_PATH}.xcf
  )

  file(MAKE_DIRECTORY ${__TARGET_SC_PATH__}/build)
  file(MAKE_DIRECTORY ${__TARGET_SC_PATH__}/bin)
  file(COPY ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit 
    DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/)

  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/decoderDemo
    COMMAND ${CMAKE_COMMAND} -DDISPLAY=off -DCMAKE_BUILD_TYPE=Release -DHLS_CLOCK_PERIOD=${CLOCK_SETTING} .. &> cmake.sc.config.log
    COMMAND make decoderDemo -j &> cmake.sc.make.log
    DEPENDS ${__TARGET_SC__}
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/build
    COMMENT "Building SystemC binary for ${__TARGET_SC__}"
  )

  add_custom_target(
    ${__TARGET_SC__}_bin
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/decoderDemo
  )

  add_dependencies(all_sc_bin ${__TARGET_SC__}_bin)

  add_custom_command(
    OUTPUT 
      ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/systemc-profile.xml 
      ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/decoderDemo.log
    COMMAND ./decoderDemo --hardware-profile=systemc-profile.xml &> decoderDemo.log
    DEPENDS ${__TARGET_SC__}_bin
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin
    COMMENT "Executing SystemC simulation for ${__TARGET_SC__} see ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/decoderDemo.log"
  )
  add_custom_target(
    ${__TARGET_SC__}_run
    DEPENDS 
      ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/systemc-profile.xml 
      ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/decoderDemo.log
  )

  add_dependencies(
    all_sc_run ${__TARGET_SC__}_run
  )
endmacro()


foreach(index RANGE 1 5)
  foreach(CLK ${CLOCK_LIST})

    rvc_generate(configuration_${index} ${CLK})

  endforeach()
endforeach()


# -- software only target
streamblocks(
  rvc-mpeg4sp_SOFTWARE
  PLATFORM multicore
  QID RVC.decoderDemo
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH . ../system
)