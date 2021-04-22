cmake_minimum_required(VERSION 3.10)

project(sha1)

set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)


set(sha1_SOURCES
  ${EXAMPLES_HOME}/system
  ${EXAMPLES_HOME}/hetero/security
)



streamblocks(
  SHANetwork_HLS 
  PLATFORM vivado-hls
  QID hetero.security.sha.SHA1Network
  SOURCE_PATH ${sha1_SOURCES}
  TARGET_PATH generated/hetero
  PARTITIONING
  )

streamblocks(
    SHANetwork_multicore 
    PLATFORM multicore
    QID hetero.security.sha.SHA1Network
    SOURCE_PATH ${sha1_SOURCES}
    TARGET_PATH generated/hetero
    PARTITIONING
    )

streamblocks_systemc(
  SHANetwork_SYSTEMC
  QID hetero.security.sha.SHA1Network
  SOURCE_PATH ${sha1_SOURCES}
  TARGET_PATH generated/sc
)

streamblocks(
    SHANetwork_software
    PLATFORM multicore
    QID hetero.security.sha.SHA1Network
    SOURCE_PATH ${sha1_SOURCES}
    TARGET_PATH generated/sw
)


streamblocks(
    ParallelSHANetwork_software
    PLATFORM multicore
    QID hetero.security.sha.ParallelSHA1Network
    SOURCE_PATH ${sha1_SOURCES}
    TARGET_PATH generated/parallelsha/software
)


streamblocks_systemc(
    ParallelSHANetwork_SYSTEMC
    QID hetero.security.sha.ParallelSHA1Network
    SOURCE_PATH ${sha1_SOURCES}
    TARGET_PATH generated/parallelsha/systemc
)

streamblocks(
  ParallelSHA1Network_HLS 
  PLATFORM vivado-hls
  QID hetero.security.sha.ParallelSHA1Network
  SOURCE_PATH ${sha1_SOURCES}
  TARGET_PATH generated/parallelsha/hetero
  PARTITIONING
)

streamblocks(
    ParallelSHA1Network_multicore 
    PLATFORM multicore
    QID hetero.security.sha.ParallelSHA1Network
    SOURCE_PATH ${sha1_SOURCES}
    TARGET_PATH generated/parallelsha/hetero
    PARTITIONING
)