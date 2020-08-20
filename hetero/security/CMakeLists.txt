cmake_minimum_required(VERSION 3.10)

project(SHA1)

include(../../Streamblocks.cmake)

streamblocks(
  SHANetwork_HLS 
  PLATFORM vivado-hls
  QID hetero.security.sha.SHANetwork
  SOURCE_PATH ../../system .
  TARGET_PATH generated)

streamblocks_systemc(
  SHANetwork_SYSTEMC
  QID hetero.security.sha.SHANetwork
  SOURCE_PATH ../../system .
  TARGET_PATH generated/profiling/sc
)
