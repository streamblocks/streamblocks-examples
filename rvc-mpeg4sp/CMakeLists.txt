cmake_minimum_required(VERSION 3.10)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)

option(REMOTE_XCLBIN "Remotely fetch generated xclbins" OFF)

# List of HLS_CLOCK_PERIOD settings to build binaries for
# Current clock speeds 300, 250, 200, 150 and 100 MHz

set(CONFIGURATION_PREFIX "configuration" CACHE STRING "XCF file prefix such as configuration or unique")
set(CONFIGURATIONS "0;1;2;3;4;5;6;7;8;9;10;11;12;13;14;15" CACHE STRING "List of ; separated configuration ids")
set(CONFIG_ROOT "." CACHE STRING "Root folder for the configurations name as configuration_N where N is a number")
set(CLOCK_LIST "3.3;10;5;2.5;1.667;6.667;13.333" CACHE STRING "List of ; seperated HLS clock settings")
set(CLOCK_IDS "1;3;4;5;6;0;2" CACHE STRING "List of clock ids coresponding to clocks")

set(FPGA_NAME "xczu7ev-ffvc1156-2-e" 
  CACHE STRING 
  "Name of Xilinx FPGA, e.g \"xcku115-flvb2104-2-e\", \"xcu250-figd2104-2L-e\", \"xczu7ev-ffvc1156-2-e\", \"xczu3eg-sbva484-1-e\", ...")

set(PLATFORM "xilinx_zcu106_base_dfx_202010_1" 
  CACHE STRING "Supported platform name, e.g \"xilinx_kcu1500_dynamic_5_0\", \"xilinx_u250_xdma_201830_2\", \"zcu102_base\", \"xilinx_zcu106_base_202010_1\", \"ultra96_base\",... ")


set(KERNEL_FREQ "150" CACHE STRING "Clock frequency in MHz.")

option(USE_VITIS "Build an RTL OpenCL Kernel for Vitis" OFF)
option(USE_SDACCEL "Build an RTL OpenCL Kernel for SDAccel" OFF)
option(IS_MPSOC "Vitis Embedded Platform" OFF)


set(REMOTE_USER "user" CACHE STRING "remote ssh username")
set(REMOTE_REPO "/scratch/mayy/streamblocks/streamblocks-examples/rvc-mpeg4sp/" CACHE STRING "remote xclbin repo")
set(REMOTE_IP   "iccluster126.iccluster.epfl.ch" CACHE STRING "remote server name")
set(FIFO_QUEUE_DEPTH 4096 CACHE STRING "Default buffer size")
set(OUTPUT_PATH "genx" CACHE STRING "Output path, where to generate the source code")



add_custom_target(all_xclbin) # build all xclbins
add_custom_target(all_bin)    # build all multicore hetero binaries
add_custom_target(all_sc_bin) # build all sc binaries
add_custom_target(all_sc_run) # run all sc simulations
add_custom_target(all_multicore)
add_custom_target(all_hls)


list(LENGTH CLOCK_LIST CLOCKS_COUNT)
math(EXPR MAX_CLOCK_INDEX "${CLOCKS_COUNT} - 1")

message(STATUS "Found ${CLOCKS_COUNT} clock configs (max index ${MAX_CLOCK_INDEX})")

# foreach(index RANGE 1 15)
#   foreach(CLK_IX RANGE 0 ${MAX_CLOCK_INDEX})

#     list(GET CLOCK_LIST ${CLK_IX} CLOCK_SETTING)
    
#     add_custom_target(all_configuration_${index}_${CLOCK_SETTING}_SC_sc_run)
  
#   endforeach()
# endforeach()

set(CAL_SOURCE_PATH
  ${CMAKE_SOURCE_DIR}
  ${CMAKE_SOURCE_DIR}/../system
)
macro(rvc_generate CONFIG_PATH CLK_IX)


  list(GET CLOCK_LIST ${CLK_IX} CLOCK_SETTING)
  list(GET CLOCK_IDS ${CLK_IX} CLK_ID)
  set(__TARGET_PATH__ ${OUTPUT_PATH}/${CONFIG_PATH}_${CLOCK_SETTING})

  set(__TARGET__ ${CONFIG_PATH}_${CLOCK_SETTING})
  
  # -- Heterogeneous HLS target
  streamblocks(
    ${__TARGET__}_HLS
    PLATFORM vivado-hls
    QID RVC.Top_RVC_Decoder
    TARGET_PATH ${__TARGET_PATH__}
    SOURCE_PATH ${CAL_SOURCE_PATH}
    XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${CONFIG_ROOT}/${CONFIG_PATH}.xcf
    PARTITIONING
    QUEUE_DEPTH ${FIFO_QUEUE_DEPTH}
  )

  # -- Heterogeneous MULTICORE target
  streamblocks(
    ${__TARGET__}_MULTICORE
    PLATFORM multicore
    QID RVC.Top_RVC_Decoder
    TARGET_PATH ${__TARGET_PATH__}
    SOURCE_PATH ${CAL_SOURCE_PATH}
    XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${CONFIG_ROOT}/${CONFIG_PATH}.xcf
    PARTITIONING
  )

  add_dependencies(all_multicore ${__TARGET__}_MULTICORE)
  add_dependencies(all_hls ${__TARGET__}_HLS)


  
  # Make directories

  set(__TARGET_DIRS_FILES__
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin 
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/foreman_qcif_30.bit 
    xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}
  )

  add_custom_command(
    OUTPUT ${__TARGET_DIRS_FILES__}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/foreman_qcif_30.bit
    COMMENT "Making directories for ${__TARGET__} ${CMAKE_COMMAND} -E make_directory ${__TARGET_PATH__}/build ${__TARGET_PATH__}/bin ${__TARGET_PATH__}/bin/xclbin xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}"
    DEPENDS ${__TARGET__}_MULTICORE ${__TARGET__}_HLS
  )

 

  # -- Heterogenous target, generates both software and hardware
  add_custom_target(
    ${__TARGET__} ALL
    DEPENDS ${__TARGET__}_HLS ${__TARGET__}_MULTICORE ${__TARGET_DIRS_FILES__}
  )  



  if (REMOTE_XCLBIN)

    # -- remotely copy xclbin
    add_custom_command(
      OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/Top_RVC_Decoder_kernel.hw.xclbin
      COMMAND scp ${REMOTE_USER}@${REMOTE_IP}:${REMOTE_REPO}/${__TARGET_PATH__}/bin/xclbin/Top_RVC_Decoder_kernel.hw.xclbin ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/
      DEPENDS ${__TARGET__}
      COMMENT "Fetching ${__TARGET__} xclbin from ${REMOTE_IP}"
    )
    add_custom_target(
      ${__TARGET__}_xclbin ALL
      DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/Top_RVC_Decoder_kernel.hw.xclbin
    )
  else()
    # -- command to build FPGA binary
    add_custom_command(
      OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/Top_RVC_Decoder_kernel.hw.xclbin
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
      COMMAND make Top_RVC_Decoder_kernel_xclbin -j
      DEPENDS ${__TARGET__}
      WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
      COMMENT "Building FPGA binary for ${__TARGET__}"
    
    )
    add_custom_target(
      ${__TARGET__}_xclbin ALL
      DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/xclbin/Top_RVC_Decoder_kernel.hw.xclbin
    )

  endif()
  
  # -- software binary
  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/Top_RVC_Decoder
    COMMAND ${CMAKE_COMMAND} -DDISPLAY=off -DCMAKE_BUILD_TYPE=Release .. > cmake.bin.config.log
    COMMAND make Top_RVC_Decoder -j &> cmake.make.log
    DEPENDS ${__TARGET__}_MULTICORE
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/build
  )
  
  add_custom_target(
    ${__TARGET__}_bin ALL
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin/Top_RVC_Decoder ${__TARGET_DIRS_FILES__}
  )

  
  
  add_custom_target(
    ${__TARGET__}_run
    DEPENDS ${__TARGET__}_bin
  )
  add_custom_command(
    TARGET ${__TARGET__}_run
    PRE_BUILD
    COMMAND time ./Top_RVC_Decoder > Top_RVC_Decoder.out
    DEPENDS ${__TARGET__}_bin
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_PATH__}/bin
  )
  
  add_dependencies(all_xclbin ${__TARGET__}_xclbin)
  add_dependencies(all_bin ${__TARGET__}_bin)



  # -- SystemC build and run commands

  set(__TARGET_SC_PATH__ ${__TARGET_PATH__}_SC)
  set(__TARGET_SC__ ${__TARGET__}_SC)

  streamblocks_systemc(
    ${__TARGET_SC__}
    QID RVC.Top_RVC_Decoder
    TARGET_PATH ${__TARGET_SC_PATH__}
    SOURCE_PATH ${CAL_SOURCE_PATH}
    XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/${CONFIG_ROOT}/${CONFIG_PATH}.xcf
    
  )

  # Make directories

  set(__TARGET_SC_DIRS_FILES__
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/build
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin
    ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/foreman_qcif_30.bit 
    xclbin_repo/${CONFIG_PATH}_${CLOCK_SETTING}
  )

  add_custom_command(
    OUTPUT ${__TARGET_SC_DIRS_FILES__}
    COMMAND ${CMAKE_COMMAND} -E make_directory ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/build ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin 
    COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif_30.bit ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/foreman_qcif_30.bit
    COMMENT "Making directories for ${__TARGET__} ${CMAKE_COMMAND} -E make_directory ${__TARGET_SC_PATH__}/build ${__TARGET_SC_PATH__}/bin"
    DEPENDS ${__TARGET_SC__}
  )

  add_custom_target(
    ${__TARGET_SC__}_DIRS_FILES__
    DEPENDS ${__TARGET_SC__} ${__TARGET_SC_DIRS_FILES__}
  )
  # build the sc binary command

  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder
    COMMAND ${CMAKE_COMMAND} -DDISPLAY=off -DFPGA_NAME=${FPGA_NAME} -DCMAKE_BUILD_TYPE=Release -DHLS_CLOCK_PERIOD=${CLOCK_SETTING} .. &> cmake.sc.config.log
    COMMAND make Top_RVC_Decoder -j &> cmake.sc.make.log
    DEPENDS ${__TARGET_SC__} ${__TARGET_SC__}_DIRS_FILES__
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/build
    COMMENT "Building SystemC binary for ${__TARGET_SC__}"
  )

  add_custom_target(
    ${__TARGET_SC__}_bin
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder ${__TARGET_SC__}_DIRS_FILES__
  )

  add_dependencies(all_sc_bin ${__TARGET_SC__}_bin)

  # Run the simulation command

  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/systemc-profile.xml ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder.log
    COMMAND ./Top_RVC_Decoder --hardware-profile=systemc-profile.xml &> Top_RVC_Decoder.log
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin
    COMMENT "Executing SystemC simulation ${__TARGET_SC__}"
    DEPENDS ${__TARGET_SC__}_bin
  )

  add_custom_target(
    ${__TARGET_SC__}_run
    DEPENDS
      ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/systemc-profile.xml 
      ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder.log
      ${__TARGET_SC__}_bin
  )

  add_dependencies(all_sc_run ${__TARGET_SC__}_run)
  # rules for different buffer configuration runs
  # set(buff_sz 4096)
  # while(${buff_sz} LESS_EQUAL 134217728)

  #   configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/${CONFIG_PATH}.xml.in ${CMAKE_CURRENT_SOURCE_DIR}/configs/${CONFIG_PATH}_${buff_sz}.xml)

  #   add_custom_command(
  #     OUTPUT 
  #       ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/profile_${buff_sz}.xml 
  #       ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder_${buff_sz}.log
  #     COMMAND ./Top_RVC_Decoder --cfile=${CMAKE_CURRENT_SOURCE_DIR}/configs/${CONFIG_PATH}_${buff_sz}.xml --hardware-profile=profile_${buff_sz}.xml &> Top_RVC_Decoder_${buff_sz}.log
  #     DEPENDS ${__TARGET_SC__}_bin
  #     WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin
  #     COMMENT "Executing SystemC simulation for ${__TARGET_SC__} see ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder_${buff_sz}.log"
  #   )
  #   add_custom_target(
  #     ${__TARGET_SC__}_run_${buff_sz}
  #     DEPENDS 
  #       ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/profile_${buff_sz}.xml 
  #       ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/Top_RVC_Decoder_${buff_sz}.log
  #   )

  #   add_dependencies(
  #     all_sc_run ${__TARGET_SC__}_run_${buff_sz}
  #   )

  #   add_dependencies(
  #     all_${__TARGET_SC__}_sc_run
  #     ${__TARGET_SC__}_run_${buff_sz}
  #   )


  #   math(EXPR buff_sz "${buff_sz}*2")

  # endwhile()
  
endmacro()


foreach(index ${CONFIGURATIONS})
  foreach(CLK_IX RANGE 0 ${MAX_CLOCK_INDEX})

    rvc_generate(${CONFIGURATION_PREFIX}_${index} ${CLK_IX})

  endforeach()
endforeach()


# -- software only target
streamblocks(
  rvc-mpeg4sp_SOFTWARE
  PLATFORM multicore
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${OUTPUT_PATH}/profiling/sw
  SOURCE_PATH ${CMAKE_SOURCE_DIR}/. ${CMAKE_SOURCE_DIR}/../system
)

streamblocks(
  hardware_only_HLS
  PLATFORM vivado-hls
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${OUTPUT_PATH}/hardware
  SOURCE_PATH ${CMAKE_SOURCE_DIR}/. ${CMAKE_SOURCE_DIR}/../system
  XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/configuration_0.xcf
  PARTITIONING
)

streamblocks(
  hardware_only_multicore
  PLATFORM multicore
  QID RVC.Top_RVC_Decoder
  TARGET_PATH ${OUTPUT_PATH}/hardware
  SOURCE_PATH ${CMAKE_SOURCE_DIR}/. ${CMAKE_SOURCE_DIR}/../system
  XCF_SOURCE_PATH ${CMAKE_SOURCE_DIR}/configuration_0.xcf
  PARTITIONING
)


