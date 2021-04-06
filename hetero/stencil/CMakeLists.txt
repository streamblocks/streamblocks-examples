cmake_minimum_required(VERSION 3.10)

project(Stencil)

set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

include(../../Streamblocks.cmake)
set(CAL_SOURCE_PATH 
 ${CMAKE_SOURCE_DIR}
)


streamblocks_systemc(
  denoise2d_systemc
  QID hetero.stencil.denoise2d.Denoise2D_5x5
  SOURCE_PATH ${CAL_SOURCE_PATH}
  TARGET_PATH generated/sc
)

streamblocks(
  denoise2d_hls_systemc
  PLATFORM vivado-hls
  SYSTEMC
  QID hetero.stencil.denoise2d.Denoise2D_5x5
  SOURCE_PATH ${CAL_SOURCE_PATH}
  TARGET_PATH generated/sc
)


set(FormatIdentityTest_SOURCES
  ${EXAMPLES_HOME}/hetero/stencil/utils/formats
  ${EXAMPLES_HOME}/hetero/stencil/test
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/jpeg/decoder/serial
  ${EXAMPLES_HOME}/jpeg/io
)
streamblocks(
  FormatIdentityTest_MC
  PLATFORM multicore
  QID hetero.stencil.test.FormatIdentityTest
  SOURCE_PATH ${FormatIdentityTest_SOURCES}
  TARGET_PATH generated/test/FormatIdentityTest
)



