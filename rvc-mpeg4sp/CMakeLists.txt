cmake_minimum_required(VERSION 3.10)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)


macro(rvc_generate CONFIG_PATH)

    # -- Heterogeneous HLS target
  streamblocks(
    rvc-mpeg4sp_HLS_${CONFIG_PATH}
    generated_rvc_hls
    PLATFORM vivado-hls
    QID RVC.decoderDemo
    TARGET_PATH generated/${CONFIG_PATH}
    SOURCE_PATH . ../system
    XCF_SOURCE_PATH ${CONFIG_PATH}.xcf
    PARTITIONING
  )

  # -- Heterogeneous MULTICORE target
  streamblocks(
    rvc-mpeg4sp_MULTICORE_${CONFIG_PATH}
    PLATFORM multicore
    QID RVC.decoderDemo
    TARGET_PATH generated/${CONFIG_PATH}
    SOURCE_PATH . ../system
    XCF_SOURCE_PATH ${CONFIG_PATH}.xcf
    PARTITIONING
  )

  # -- Heterogenous target, generates both software and hardware
  add_custom_target(
    rvc-mpeg4sp_${CONFIG_PATH} ALL
    DEPENDS rvc-mpeg4sp_MULTICORE_${CONFIG_PATH} rvc-mpeg4sp_HLS_${CONFIG_PATH}
  )
endmacro()

rvc_generate(configuration_1)
rvc_generate(configuration_2)


# -- SystemC simulation target

streamblocks_systemc(
  rvc-mpeg4sp_SYSTEMC
  QID RVC.decoderDemo
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH . ../system
  XCF_SOURCE_PATH configuration_1.xcf
)

