


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
