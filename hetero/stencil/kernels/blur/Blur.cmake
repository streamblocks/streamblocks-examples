


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
  ${EXAMPLES_HOME}/jpeg/decoder/serial
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

function(jpegblur_gen CONFIG_IDX NETWORK PREFIX)

  
  
  set(CONFIG_ROOT ${EXAMPLES_HOME}/hetero/stencil/kernels/blur/${PREFIX}/unique/)
  set(THIS_CONFIG ${CONFIG_ROOT}/unique_${CONFIG_IDX}.xcf)
  set(OUTPUT_PATH build/${PREFIX}/jpegblur/unique_${CONFIG_IDX})


  set(__THIS_TARGET__ jpeg_unique_${CONFIG_IDX})
  streamblocks(
    ${__THIS_TARGET__}_hls
    PLATFORM vivado-hls
    QID hetero.stencil.kernels.GuassianBlur.${NETWORK}
    PARTITIONING
    SOURCE_PATH ${JpegBlurNetwork_SOURCES}
    TARGET_PATH ${OUTPUT_PATH}
    XCF_SOURCE_PATH ${THIS_CONFIG}
    QUEUE_DEPTH 1024
  )

  streamblocks(
    ${__THIS_TARGET__}_multicore
    PLATFORM multicore
    QID hetero.stencil.kernels.GuassianBlur.${NETWORK}
    PARTITIONING
    SOURCE_PATH ${JpegBlurNetwork_SOURCES}
    TARGET_PATH ${OUTPUT_PATH}
    XCF_SOURCE_PATH ${THIS_CONFIG}
  )

  add_dependencies(all_jpegblur_gen_hls ${__THIS_TARGET__}_hls)
  add_dependencies(all_jpegblur_gen_multicore ${__THIS_TARGET__}_multicore)
endfunction()




streamblocks(
  JpegNaiveBlurNetwork_MC
  PLATFORM multicore
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurNaiveNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/test/JpegBlurNaiveNetwork
  
)


streamblocks(
  JpegNaiveNaiveNetwork_multicore
  PLATFORM multicore
  PARTITIONING
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurNaiveNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH build/naive_profile/jpegblur/fpga_only
  
)

streamblocks(
  JpegNaiveNaiveNetwork_hls
  PLATFORM vivado-hls
  PARTITIONING
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurNaiveNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH build/naive_profile/jpegblur/fpga_only
  
)

streamblocks_systemc(
  JpegNaiveBlurNetwork_systemc
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurNaiveNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/systemc/JpegBlurNaiveNetwork
  
)


streamblocks(
  JpegBlurOptNetwork_MC
  PLATFORM multicore
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurOptNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/test/JpegBlurOptNetwork
  
)

streamblocks_systemc(
  JpegBlurOptNetwork_systemc
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurOptNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/systemc/JpegBlurOptNetwork
)

streamblocks(
  JpegBlurOptNetwork_multicore
  PLATFORM multicore
  PARTITIONING
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurOptNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH build/opt_profile/jpegblur/fpga_only
)

streamblocks(
  JpegBlurOptNetwork_hls
  PLATFORM vivado-hls
  PARTITIONING
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurOptNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH build/opt_profile/jpegblur/fpga_only
)

streamblocks(
  JpegBlurSerialNetwork_MC
  PLATFORM multicore
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurSerialNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/test/JpegBlurSerialNetwork
  
)

streamblocks_systemc(
  JpegBlurSerialNetwork_systemc
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurSerialNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH generated/systemc/JpegBlurSerialNetwork
)


streamblocks(
  JpegBlurSerialNetwork_hls
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurSerialNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH build/serial_profile/jpegblur/fpga_only
  PARTITIONING
  PLATFORM vivado-hls
)

streamblocks(
  JpegBlurSerialNetwork_multicore
  QID hetero.stencil.kernels.GuassianBlur.JpegBlurSerialNetwork
  SOURCE_PATH ${JpegBlurNetwork_SOURCES}
  TARGET_PATH build/serial_profile/jpegblur/fpga_only
  PARTITIONING
  PLATFORM multicore
)



foreach(index RANGE 0 12)  
  jpegblur_gen(${index} JpegBlurNetwork profiled_data_zcu)
endforeach()
