cmake_minimum_required(VERSION 3.10)

project(rvc-mpgeg4sp)

include(../Streamblocks.cmake)

streamblocks(
  rvc-mpeg4sp_HLS
  PLATFORM vivado-hls
  QID RVC.decoderDemo
  TARGET_PATH generated
  SOURCE_PATH . ../system
  XCF_SOURCE_PATH configuration.xcf
  PARTITIONING
)

streamblocks(
  rvc-mpeg4sp_MULTICORE
  PLATFORM multicore
  QID RVC.decoderDemo
  TARGET_PATH generated
  SOURCE_PATH . ../system
  XCF_SOURCE_PATH configuration.xcf
  PARTITIONING
)
