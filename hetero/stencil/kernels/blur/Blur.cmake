


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
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/test/JpegBlurNetwork
)


streamblocks_systemc(
  JpegBlurNetwork_systemc
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/systemc/JpegBlurNetwork
)



add_custom_target(all_jpegblur_gen_hls)
add_custom_target(all_jpegblur_gen_multicore)

function(jpegblur_gen CONFIG_IDX)

  
  
  set(CONFIG_ROOT ${EXAMPLES_HOME}/hetero/stencil/kernels/blur/profiled_data/unique/)
  set(THIS_CONFIG ${CONFIG_ROOT}/unique_${CONFIG_IDX}.xcf)
  set(OUTPUT_PATH build/generated/jpegblur/unique_${CONFIG_IDX})


  set(__THIS_TARGET__ jpeg_unique_${CONFIG_IDX})
  streamblocks(
    ${__THIS_TARGET__}_hls
    PLATFORM vivado-hls
    QID hetero.stencil.kernels.GuassianBlur.JpegBlurNetwork
    PARTITIONING
    SOURCE_PATH ${JpegBlurNetwork_SOURCES}
    TARGET_PATH ${OUTPUT_PATH}
    XCF_SOURCE_PATH ${THIS_CONFIG}
  )

  streamblocks(
    ${__THIS_TARGET__}_multicore
    PLATFORM multicore
    QID hetero.stencil.kernels.GuassianBlur.JpegBlurNetwork
    PARTITIONING
    SOURCE_PATH ${JpegBlurNetwork_SOURCES}
    TARGET_PATH ${OUTPUT_PATH}
    XCF_SOURCE_PATH ${THIS_CONFIG}
  )

  add_dependencies(all_jpegblur_gen_hls ${__THIS_TARGET__}_hls)
  add_dependencies(all_jpegblur_gen_multicore ${__THIS_TARGET__}_multicore)
endfunction()


foreach(index RANGE 0 34)  
  jpegblur_gen(${index})
endforeach()