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
while(${iter} LESS_EQUAL 7)

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
  
  file(MAKE_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/loopback${iter}/build)

  add_custom_command(
    TARGET ${TARGET_NAME}
    POST_BUILD
    COMMAND ${CMAKE_COMMAND} -DHLS_CLOCK_PERIOD=10 -DUSE_SDACCEL=true ..
    COMMAND make Loopback${iter}_kernel_xclbin
    WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}/generated/loopback${iter}/build
    COMMENT "Configuring generated cmake project ${TARGET_NAME}"
  )

  math(EXPR iter "${iter} + 1")
endwhile()
