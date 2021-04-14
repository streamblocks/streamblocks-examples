cmake_minimum_required(VERSION 3.10)

project(jpegDecdoer_serial)

set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

set(jpeg_SOURCES
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/system/std
  ${EXAMPLES_HOME}/jpeg/decoder/serial
  ${EXAMPLES_HOME}/jpeg/io
  ${EXAMPLES_HOME}/hetero/decoder/jpeg/serial
)
streamblocks(
  jpeg_hls
  PLATFORM multicore 
  QID hetero.decoder.jpeg.serial.JpegSerialNetwork
  TARGET_PATH generated/hetero
  SOURCE_PATH ${jpeg_SOURCES}
  PARTITIONING
)

streamblocks(
  jpeg_multicore
  PLATFORM vivado-hls 
  QID hetero.decoder.jpeg.serial.JpegSerialNetwork
  TARGET_PATH generated/hetero
  SOURCE_PATH  ${jpeg_SOURCES}
  PARTITIONING
)

add_custom_target(
  jpeg
  DEPENDS jpeg_hls jpeg_multicore
)

streamblocks_systemc(
  jpeg_systemc
  QID hetero.decoder.jpeg.serial.JpegSerialNetwork
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH  ${jpeg_SOURCES}

)

streamblocks(
  jpeg_software
  PLATFORM multicore
  QID hetero.decoder.jpeg.serial.JpegSerialNetwork
  TARGET_PATH generated/sw
  SOURCE_PATH ${jpeg_SOURCES}
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



