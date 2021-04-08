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
  ${EXAMPLES_HOME}/hetero/stencil/utils/generators
  ${EXAMPLES_HOME}/hetero/stencil/test
  ${EXAMPLES_HOME}/converters/src
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/system/std
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

streamblocks(
  RgbTo420Mb
  PLATFORM multicore
  QID hetero.stencil.test.RgbTo420Mb
  SOURCE_PATH ${FormatIdentityTest_SOURCES}
  TARGET_PATH generated/test/RgbTo420Mb
)


set(BitmapTest_SOURCES
  ${EXAMPLES_HOME}/hetero/stencil/bitmap
  ${EXAMPLES_HOME}/hetero/stencil/test
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/system/std
)

streamblocks(
  BitMapHeaderParserTest_MC
  PLATFORM multicore
  QID hetero.stencil.bitmap.test.BitMapHeaderParserTest
  SOURCE_PATH ${BitmapTest_SOURCES}
  TARGET_PATH generated/test/BitMapHeaderParserTest
)


streamblocks(
  BitMapInfoHeaderParserTest_MC
  PLATFORM multicore
  QID hetero.stencil.bitmap.test.BitMapInfoHeaderParserTest
  SOURCE_PATH ${BitmapTest_SOURCES}
  TARGET_PATH generated/test/BitMapInfoHeaderParserTest
)


streamblocks(
  BitMapDecodeEncodeTest_MC
  PLATFORM multicore
  QID hetero.stencil.bitmap.test.BitMapDecodeEncodeTest
  SOURCE_PATH ${BitmapTest_SOURCES}
  TARGET_PATH generated/test/BitMapDecodeEncodeTest
)

set(BitmapBlur_SOURCES
  ${EXAMPLES_HOME}/hetero/stencil/bitmap
  ${EXAMPLES_HOME}/hetero/stencil/test
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/system/std
  ${EXAMPLES_HOME}/hetero/stencil/kernels
)



streamblocks(
  BitmapBlurNetwork_MC
  PLATFORM multicore
  QID hetero.stencil.kernels.BitmapBlurNetwork
  SOURCE_PATH ${BitmapBlur_SOURCES}
  TARGET_PATH generated/test/BitmapBlurNetwork
)