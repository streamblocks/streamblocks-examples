cmake_minimum_required(VERSION 3.10)

project(FIR_Filter)

include(../../../Streamblocks.cmake)


streamblocks(
  fir_hls
  PLATFORM multicore 
  QID fir.TopFIRThroughput
  TARGET_PATH generated/hetero
  SOURCE_PATH ../../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
  PARTITIONING
)

streamblocks(
  fir_multicore
  PLATFORM vivado-hls 
  QID fir.TopFIRThroughput
  TARGET_PATH generated/hetero
  SOURCE_PATH  ../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
  PARTITIONING
)


add_custom_target(
  fir
  DEPENDS fir_hls fir_multicore
)



streamblocks_systemc(
  fir_systemc
  QID fir.TopFIRThroughput
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH  ../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
)



streamblocks(
  fir_software
  PLATFORM multicore
  QID fir.TopFIRThroughput
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH ../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
)


# -- Compare

streamblocks(
  fir_compare_hls
  PLATFORM multicore 
  QID fir.TopFIRCompare
  TARGET_PATH generated/compare
  SOURCE_PATH ../../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
  PARTITIONING
)

streamblocks(
  fir_compare_multicore
  PLATFORM vivado-hls 
  QID fir.TopFIRCompare
  TARGET_PATH generated/compare
  SOURCE_PATH  ../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
  PARTITIONING
)

streamblocks_systemc(
  fir_compare_systemc
  QID fir.TopFIRCompare
  TARGET_PATH generated/profiling/compare/sc
  SOURCE_PATH  ../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
)

streamblocks(
  fir_compare_software
  PLATFORM multicore
  QID fir.TopFIRCompare
  TARGET_PATH generated/profiling/compare/sw
  SOURCE_PATH ../../../../filters ../../../../system ../../../utils
  EXPERIMENTAL
)


add_custom_target(
  fir_compare
  DEPENDS fir_compare_hls fir_compare_multicore
)


add_custom_command(
  OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/TopFIRThroughput
  COMMAND ${CMAKE_COMMAND} -DHLS_CLOCK_PERIOD=3.3 -DCMAKE_BUILD_TYPE=Release -DDISPLAY=off ..
  COMMAND make TopFIRThroughput -j
  COMMENT "Buidling systemc binary"
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/
  DEPENDS fir_systemc
)

add_custom_command(
  OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/comapre/sc/bin/TopFIRCompare
  COMMAND ${CMAKE_COMMAND} -DHLS_CLOCK_PERIOD=3.3 -DCMAKE_BUILD_TYPE=Release -DDISPLAY=off ..
  COMMAND make TopFIRThroughput -j
  COMMENT "Buidling systemc binary"
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/
  DEPENDS fir_comapre_systemc
)


add_custom_target(
  fir_systemc_bin
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/TopFIRThroughput
)

add_custom_target(
  fir_compare_systemc_bin
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/comapre/sc/bin/TopFIRCompare
)

add_custom_target(fir_systemc_runs)

set(buff_sz 4096)
while(${buff_sz} LESS_EQUAL 134217728)

  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.xml.in ${CMAKE_CURRENT_SOURCE_DIR}/configs/config_${buff_sz}.xml )

  
  

  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/profile_${buff_sz}.xml
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/TopFIRThroughput --hardware-profile=profile_${buff_sz}.xml --cfile=${CMAKE_CURRENT_SOURCE_DIR}/configs/config_${buff_sz}.xml 2> run_${buff_sz}.log
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/
    COMMENT "Running sim ${buff_sz}"
    DEPENDS fir_systemc_bin
  )

  add_custom_target(
    run_${buff_sz}
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/profile_${buff_sz}.xml
  )

  add_dependencies(fir_systemc_runs run_${buff_sz})


  math(EXPR buff_sz "${buff_sz}*2")
endwhile()


