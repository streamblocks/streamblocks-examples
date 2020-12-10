cmake_minimum_required(VERSION 3.10)


project(XilinxMpeg)

set(NAMESPACE "hetero.decoder.mpeg.xilinx")
set(NETWORK_NAME "XilinxNetwork")

# Common options
include(../common.cmake)



generate_profiliing(${NAMESPACE} ${NETWORK_NAME} XilinxNetwork)


foreach(index ${CONFIGURATIONS})
  foreach(CLK_IX RANGE 0 ${MAX_CLOCK_INDEX})

    generate_network(${NAMESPACE} ${NETWORK_NAME} configuration_${index} ${CLK_IX})

  endforeach()
endforeach()

