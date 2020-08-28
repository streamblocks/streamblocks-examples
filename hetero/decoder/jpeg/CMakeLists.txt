cmake_minimum_required(VERSION 3.10)

project(jpegDecdoer)

include(../../../Streamblocks.cmake)


streamblocks_systemc(
  jpeg_systemc
  QID hetero.decoder.jpeg.JpegNetwork
  TARGET_PATH generated/profiling/sc2
  SOURCE_PATH . ../../../jpeg ../../../system ../../utils

)

streamblocks(
  jpeg_software
  PLATFORM multicore
  QID hetero.decoder.jpeg.JpegNetwork
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH . ../../../jpeg ../../../system ../../utils
)