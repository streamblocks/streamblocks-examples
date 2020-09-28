cmake_minimum_required(VERSION 3.10)

project(jpegDecdoer)

include(../../../Streamblocks.cmake)


streamblocks(
  jpeg_hls
  PLATFORM multicore 
  QID hetero.decoder.jpeg.JpegNetwork
  TARGET_PATH generated/hetero
  SOURCE_PATH . ../../../jpeg ../../../system ../../utils
  PARTITIONING
)

streamblocks(
  jpeg_multicore
  PLATFORM vivado-hls 
  QID hetero.decoder.jpeg.JpegNetwork
  TARGET_PATH generated/hetero
  SOURCE_PATH . ../../../jpeg ../../../system ../../utils
  PARTITIONING
)

add_custom_target(
  jpeg
  DEPENDS jpeg_hls jpeg_multicore
)

streamblocks_systemc(
  jpeg_systemc
  QID hetero.decoder.jpeg.JpegNetwork
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH . ../../../jpeg ../../../system ../../utils

)

streamblocks(
  jpeg_software
  PLATFORM multicore
  QID hetero.decoder.jpeg.JpegNetwork
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH . ../../../jpeg ../../../system ../../utils
)




add_custom_command(
  OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/JpegNetwork
  COMMAND ${CMAKE_COMMAND} -E copy ${CMAKE_CURRENT_SOURCE_DIR}/foreman_qcif.mjpg ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin
  COMMAND ${CMAKE_COMMAND} -DHLS_CLOCK_PERIOD=3.3 -DCMAKE_BUILD_TYPE=Release -DDISPLAY=off ..
  COMMAND make JpegNetwork -j
  COMMENT "Buidling systemc binary"
  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/
  DEPENDS jpeg_systemc
)

add_custom_target(
  jpeg_systemc_bin
  DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/JpegNetwork
)


add_custom_target(jpeg_systemc_runs)

set(buff_sz 4096)
while(${buff_sz} LESS_EQUAL 134217728)

  configure_file(${CMAKE_CURRENT_SOURCE_DIR}/cmake/config.xml.in ${CMAKE_CURRENT_SOURCE_DIR}/configs/config_${buff_sz}.xml )

  
  

  add_custom_command(
    OUTPUT ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/profile_${buff_sz}.xml
    COMMAND ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/JpegNetwork --hardware-profile=profile_${buff_sz}.xml --cfile=${CMAKE_CURRENT_SOURCE_DIR}/configs/config_${buff_sz}.xml 2> run_${buff_sz}.log
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/
    COMMENT "Running sim ${buff_sz}"
    DEPENDS jpeg_systemc_bin
  )

  add_custom_target(
    run_${buff_sz}
    DEPENDS ${CMAKE_CURRENT_SOURCE_DIR}/generated/profiling/sc/bin/profile_${buff_sz}.xml
  )

  add_dependencies(jpeg_systemc_runs run_${buff_sz})


  math(EXPR buff_sz "${buff_sz}*2")
endwhile()


