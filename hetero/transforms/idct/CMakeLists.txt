cmake_minimum_required(VERSION 3.10)

project(IDCT)


set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

set(DESIGN_SOURCES
  ${EXAMPLES_HOME}/transforms/dct/src
  ${EXAMPLES_HOME}/system/art/
  ${EXAMPLES_HOME}/system/std/counters
)
streamblocks(
  idct_hls
  PLATFORM vivado-hls 
  QID RVC.TopIDCT
  TARGET_PATH generated/hetero
  SOURCE_PATH ${DESIGN_SOURCES}
  PARTITIONING
)

streamblocks(
  idct_multicore
  PLATFORM multicore
  QID RVC.TopIDCT
  TARGET_PATH generated/hetero
  SOURCE_PATH  ${DESIGN_SOURCES}
  PARTITIONING
)


add_custom_target(
  idct
  DEPENDS idct_hls idct_multicore
)



streamblocks_systemc(
  idct_systemc
  QID RVC.TopIDCT
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH  ${DESIGN_SOURCES}
)



streamblocks(
  idct_software
  PLATFORM multicore
  QID RVC.TopIDCT
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH ${DESIGN_SOURCES}
)
