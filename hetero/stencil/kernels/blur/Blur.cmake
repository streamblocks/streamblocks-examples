


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
  QID hetero.stencil.kernels.Blur.BitmapBlurNetwork
  SOURCE_PATH ${BitmapBlur_SOURCES}
  TARGET_PATH generated/test/BitmapBlurNetwork
)


set(JpegBlurNetwork_SOURCES
  ${EXAMPLES_HOME}/hetero/stencil/bitmap
  ${EXAMPLES_HOME}/converters/src
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/system/std
  ${EXAMPLES_HOME}/jpeg/decoder/parallel
  ${EXAMPLES_HOME}/jpeg/io
  ${EXAMPLES_HOME}/hetero/stencil/kernels
)

streamblocks(
  JpegBlurNetwork_MC
  PLATFORM multicore
  QID hetero.stencil.kernels.Blur.JpegBlurNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/test/JpegBlurNetwork
)

