cmake_minimum_required(VERSION 3.10)

project(FIR_Filter)


set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

set(fir_SOURCES
  ${EXAMPLES_HOME}/filters/fir/src
  ${EXAMPLES_HOME}/system/art/
  ${EXAMPLES_HOME}/system/std/counters
)
streamblocks(
  fir_hls
  PLATFORM vivado-hls 
  QID fir.TopFIRThroughput
  TARGET_PATH generated/hetero
  SOURCE_PATH ${fir_SOURCES}
  EXPERIMENTAL
  PARTITIONING
)

streamblocks(
  fir_multicore
  PLATFORM multicore
  QID fir.TopFIRThroughput
  TARGET_PATH generated/hetero
  SOURCE_PATH  ${fir_SOURCES}
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
  SOURCE_PATH  ${fir_SOURCES}
  EXPERIMENTAL
)



streamblocks(
  fir_software
  PLATFORM multicore
  QID fir.TopFIRThroughput
  TARGET_PATH generated/profiling/sw
  SOURCE_PATH ${fir_SOURCES}
  EXPERIMENTAL
)


# -- Compare

streamblocks(
  fir_compare_hls
  PLATFORM multicore 
  QID fir.TopFIRCompare
  TARGET_PATH generated/compare
  SOURCE_PATH ${fir_SOURCES}
  EXPERIMENTAL
  PARTITIONING
)

streamblocks(
  fir_compare_multicore
  PLATFORM vivado-hls 
  QID fir.TopFIRCompare
  TARGET_PATH generated/compare
  SOURCE_PATH  ${fir_SOURCES}
  EXPERIMENTAL
  PARTITIONING
)

streamblocks_systemc(
  fir_compare_systemc
  QID fir.TopFIRCompare
  TARGET_PATH generated/profiling/compare/sc
  SOURCE_PATH  ${fir_SOURCES}
  EXPERIMENTAL
)

streamblocks(
  fir_compare_software
  PLATFORM multicore
  QID fir.TopFIRCompare
  TARGET_PATH generated/profiling/compare/sw
  SOURCE_PATH ${fir_SOURCES}
  EXPERIMENTAL
)


add_custom_target(
  fir_compare
  DEPENDS fir_compare_hls fir_compare_multicore
)




