cmake_minimum_required(VERSION 3.10)

project(BITONIC8)


set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

set(DESIGN_SOURCES
  ${EXAMPLES_HOME}/sort/bitonic/src
  ${EXAMPLES_HOME}/system/art/
  ${EXAMPLES_HOME}/system/std/counters
)
streamblocks(
  bitonic_hls
  PLATFORM vivado-hls 
  QID sort.TopBitonicSort
  TARGET_PATH generated/hetero
  SOURCE_PATH ${DESIGN_SOURCES}
  PARTITIONING
)

streamblocks(
  bitonic_multicore
  PLATFORM multicore
  QID sort.TopBitonicSort
  TARGET_PATH generated/hetero
  SOURCE_PATH  ${DESIGN_SOURCES}
  PARTITIONING
)


add_custom_target(
  bitonic
  DEPENDS bitonic_hls bitonic_multicore
)



streamblocks_systemc(
  bitonic_systemc
  QID sort.TopBitonicSort
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH  ${DESIGN_SOURCES}
)



streamblocks(
  bitonic_software
  PLATFORM multicore
  QID sort.TopBitonicSort
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH ${DESIGN_SOURCES}
)
