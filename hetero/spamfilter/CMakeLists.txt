cmake_minimum_required(VERSION 3.10)

project(spamfilter)

set(STREAMBLOCKS_HOME $ENV{STREAMBLOCKS_HOME})

set(EXAMPLES_HOME ${STREAMBLOCKS_HOME}/streamblocks-examples)

include(${EXAMPLES_HOME}/Streamblocks.cmake)

set(spamfilter_SORUCES
  ${EXAMPLES_HOME}/system/art
  ${EXAMPLES_HOME}/hetero/spamfilter/
)


streamblocks(
  spamfilter_software
  QID hetero.spamfilter.SimpleSpamFilterEpochs
  PLATFORM multicore
  SOURCE_PATH ${spamfilter_SORUCES}
  TARGET_PATH build/generated/sw
  EXPERIMENTAL
)




streamblocks(
  spamfilter_multicore
  QID hetero.spamfilter.SimpleSpamFilterEpochs
  PLATFORM multicore
  SOURCE_PATH ${spamfilter_SORUCES}
  TARGET_PATH build/generated/hetero
  EXPERIMENTAL
  PARTITIONING
)

streamblocks(
  spamfilter_hls
  QID hetero.spamfilter.SimpleSpamFilterEpochs
  PLATFORM vivado-hls
  SOURCE_PATH ${spamfilter_SORUCES}
  TARGET_PATH build/generated/hetero
  EXPERIMENTAL
  PARTITIONING
)

add_custom_target(spamfilter_hetero
  DEPENDS spamfilter_multicore spamfilter_hls
)