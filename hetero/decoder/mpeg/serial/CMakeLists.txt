cmake_minimum_required(VERSION 3.10)


project(SerialMpeg)

set(NAMESPACE "hetero.decoder.mpeg.parallel")
set(NETWORK_NAME "SerialNetwork")

# Common options
include(../common.cmake)



generate_profiliing(${NAMESPACE} ${NETWORK_NAME})


foreach(index ${CONFIGURATIONS})
  foreach(CLK_IX RANGE 0 ${MAX_CLOCK_INDEX})

    generate_network(${NAMESPACE} ${NETWORK_NAME} configuration_${index} ${CLK_IX})

  endforeach()
endforeach()

