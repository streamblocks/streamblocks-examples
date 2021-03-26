cmake_minimum_required(VERSION 3.10)

project(Smith-Waterman)

include(../../Streamblocks.cmake)

set(CAL_SOURCE_PATH 
  ../
  ../../../system
  ../../../smith-waterman
)


streamblocks(
  SWNetwork_HLS
  PLATFORM vivado-hls
  QID hetero.sw.SWNetwork
  SOURCE_PATH ${CAL_SOURCE_PATH}
  TARGET_PATH generated/hetero
  PARTITIONING
  )


streamblocks(
  SWNetwork_MULTICORE
  PLATFORM multicore
  QID hetero.sw.SWNetwork
  SOURCE_PATH ${CAL_SOURCE_PATH}
  TARGET_PATH generated/hetero
  PARTITIONING
  
  )

add_custom_target(
  SWNetwork
  DEPENDS SWNetwork_HLS SWNetwork_MULTICORE
)

streamblocks_systemc(
  SWNetwork_systemc
  QID hetero.sw.SWNetwork
  SOURCE_PATH ${CAL_SOURCE_PATH}
  TARGET_PATH generated/profiling/sc
)


streamblocks(
  SWNetwork_SOFTWARE
  PLATFORM multicore
  QID hetero.sw.SWNetwork
  SOURCE_PATH ${CAL_SOURCE_PATH}
  TARGET_PATH generated/profiling/sw
)
