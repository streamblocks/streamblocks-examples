
SB_HOME ?= $(STREAMBLOCKS_HOME)
CMAKE ?= cmake

TARGET_PATH ?= $(shell pwd)/generated

NUM_CORES ?= 2

HLS_CLOCK_PERIOD ?= 3.3



SB_BIN := $(SB_HOME)/streamblocks-platforms/streamblocks
PARTITIONING_BIN ?= $(SB_HOME)/streamblocks-partitioning/partitioning/partition
SB_EXAMPLES_PATH := $(SB_HOME)/streamblocks-examples
ART_SOURCE_PATH := $(SB_HOME)/streamblocks-examples/system/
UTILS_PATH := $(SB_EXAMPLES_PATH)/hetero/utils


SYSTEMC_SETTIGNS := --set enable-systemc=on --set max-bram=128MiB


COMMON_SETTINGS := --set partitioning=on

MULTICORE_SETTIGS := #Nothing


HLS_SETTINGS := --set enable-action-profile=off 