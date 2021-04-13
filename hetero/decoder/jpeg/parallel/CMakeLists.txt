cmake_minimum_required(VERSION 3.10)

project(jpegDecdoer_parallel)

set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

set(jpeg_SOURCES
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/system/std
  ${EXAMPLES_HOME}/jpeg/decoder/parallel
  ${EXAMPLES_HOME}/jpeg/io
  ${EXAMPLES_HOME}/hetero/decoder/jpeg/parallel
)
streamblocks(
  jpeg_hls
  PLATFORM multicore 
  QID hetero.decoder.jpeg.parallel.JpegParallelNetwork
  TARGET_PATH generated/hetero
  SOURCE_PATH ${jpeg_SOURCES}
  PARTITIONING
)

streamblocks(
  jpeg_multicore
  PLATFORM vivado-hls 
  QID hetero.decoder.jpeg.parallel.JpegParallelNetwork
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
  QID hetero.decoder.jpeg.parallel.JpegParallelNetwork
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH  ${jpeg_SOURCES}

)

streamblocks(
  jpeg_software
  PLATFORM multicore
  QID hetero.decoder.jpeg.parallel.JpegParallelNetwork
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH ${jpeg_SOURCES}
)





