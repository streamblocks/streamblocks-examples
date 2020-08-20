cmake_minimum_required(VERSION 3.10)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)

# -- Heterogeneous HLS target
streamblocks(
  rvc-mpeg4sp_HLS
  generated_rvc_hls
  PLATFORM vivado-hls
  QID RVC.decoderDemo
  TARGET_PATH generated
  SOURCE_PATH . ../system
  XCF_SOURCE_PATH configuration.xcf
  PARTITIONING
)

# -- Heterogeneous MULTICORE target
streamblocks(
  rvc-mpeg4sp_MULTICORE
  PLATFORM multicore
  QID RVC.decoderDemo
  TARGET_PATH generated
  SOURCE_PATH . ../system
  XCF_SOURCE_PATH configuration.xcf
  PARTITIONING
)

# -- Heterogenous target, generates both software and hardware
add_custom_target(
  rvc-mpeg4sp 
  DEPENDS rvc-mpeg4sp_HLS rvc-mpeg4sp_MULTICORE
)


# -- SystemC simulation target

streamblocks_systemc(
  rvc-mpeg4sp_SYSTEMC
  QID RVC.decoderDemo
  TARGET_PATH generated/profiling/sc
  SOURCE_PATH . ../system
  XCF_SOURCE_PATH configuration.xcf
)

