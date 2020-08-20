cmake_minimum_required(VERSION 3.10)

project(hetero.simple)

include(../../Streamblocks.cmake)
# -- software profiling target for the PipelinedNetwork
streamblocks(
  PipelinedNetwork_SOFTWARE
  QID hetero.simple.pipes.PipelinedNetwork
  PLATFORM multicore
  SOURCE_PATH . 
  TARGET_PATH generated/profiling/sw
)


set(iter 1)
while(${iter} LESS_EQUAL 5)

  set(TARGET_NAME Loopback_${iter})
  streamblocks(
    ${TARGET_NAME}_HLS
    QID hetero.simple.loopback.Loopback${iter}
    PLATFORM vivado-hls
    SOURCE_PATH .
    TARGET_PATH generated/loopback${iter}
    PARTITIONING
  )
  streamblocks(
    ${TARGET_NAME}_MULTICORE
    QID hetero.simple.loopback.Loopback${iter}
    PLATFORM multicore
    SOURCE_PATH .
    TARGET_PATH generated/loopback${iter}
    PARTITIONING
  )

  add_custom_target(
    ${TARGET_NAME} ALL
    DEPENDS ${TARGET_NAME}_MULTICORE ${TARGET_NAME}_HLS
  )

  math(EXPR iter "${iter} + 1")
endwhile()
