cmake_minimum_required(VERSION 3.10)


project(XilinxMpeg)

# Streamblocks build command
include(../../../../Streamblocks.cmake)


# Common options
include(../../../../common.cmake)



set(ORCC_APPS_PATH ${CMAKE_SOURCE_DIR}/../../../../orc-apps)
set(ORCC_DESIGN_PATH ${CMAKE_SOURCE_DIR}/../../../../orcc-designs)

set(ORCC_SOURCE_PATH 
  ${ORCC_APPS_PATH}/Research/src
  ${ORCC_APPS_PATH}/System/src
  ${ORCC_APPS_PATH}/RVC/src
  ${ORCC_DESIGN_PATH}/Research/src
)

set(XDF_SOURCE_PATH
  ${ORCC_DESIGN_PATH}/Research/src
  ${ORCC_APPS_PATH}/Research/src
  ${CMAKE_SOURCE_DIR}../../../../
)

set(CAL_SOURCE_PATH 
  ${CMAKE_SOURCE_DIR}
  ${CMAKE_SOURCE_DIR}/../../../../system/art
  ${CMAKE_SOURCE_DIR}/../../../utils
)

function(generate CLOCK) 


  set(__TARGET__ configuration_${CLOCK})
  set(TARGET_PATH generated/configuration_${CLOCK})

  
  streamblocks(
    ${TARGET}_HLS
    PLATFORM vivado-hls
    QID hetero.decoder.mpeg.xilinx.XilinxNetwork
    SOURCE_PATH ${CAL_SOURCE_PATH}
    ORCC_SOURCE_PATH ${ORCC_SOURCE_PATH}
    XDF_SOURCE_PATH ${XDF_SOURCE_PATH}
    TARGET_PATH ${TARGET_PATH}
    PARTITIONING
  )

endfunction()



# SystemC profiling target
streamblocks_systemc(
  hardware_profiling
  QID                 hetero.decoder.mpeg.xilinx.XilinxNetwork
  TARGET_PATH         ${OUTPUT_PATH}/profiling/hw
  SOURCE_PATH         ${CAL_SOURCE_PATH}
  ORCC_SOURCE_PATH    ${ORCC_SOURCE_PATH}
  XDF_SOURCE_PATH     ${XDF_SOURCE_PATH}
)

# Software profiling target
streamblocks(
  software_profiling
  QID                 hetero.decoder.mpeg.xilinx.XilinxNetwork
  TARGET_PATH         ${OUTPUT_PATH}/profiling/sw
  SOURCE_PATH         ${CAL_SOURCE_PATH}
  ORCC_SOURCE_PATH    ${ORCC_SOURCE_PATH}
  XDF_SOURCE_PATH     ${XDF_SOURCE_PATH}
  PLATFORM multicore
)

# generate(3.3)


# rules for different buffer configuration runs

add_custom_target(all_runs)
set(buff_sz 4096)
while(${buff_sz} LESS_EQUAL 134217728)

  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.xml.in ${CMAKE_CURRENT_SOURCE_DIR}/configs/config_${buff_sz}.xml)
  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config_sw.xml.in ${CMAKE_CURRENT_SOURCE_DIR}/configs/config_sw_${buff_sz}.xml)

  add_custom_command(
    OUTPUT 
      ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/profile_${buff_sz}.xml 
      ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/XilinxNetwork_${buff_sz}.log
    COMMAND ./XilinxNetwork --cfile=${CMAKE_CURRENT_SOURCE_DIR}/configs/config_${buff_sz}.xml --hardware-profile=profile_${buff_sz}.xml &> XilinxNetwork_${buff_sz}.log
    
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin
    COMMENT "Executing SystemC simulation, see ${CMAKE_CURRENT_SOURCE_DIR}/${__TARGET_SC_PATH__}/bin/XilinxNetwork_${buff_sz}.log"
  )
  add_custom_target(
    run_${buff_sz}
    DEPENDS 
      ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/profile_${buff_sz}.xml 
      ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/XilinxNetwork_${buff_sz}.log
  )

  add_dependencies(
    all_runs run_${buff_sz}
  )

  math(EXPR buff_sz "${buff_sz}*2")

endwhile()