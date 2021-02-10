
ENTITY_NAMESPACE := hetero.decoder.mpeg.xilinx
ENTITY_NETWORK := Top_Xilinx
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)

CAL_SOURCE_PATH := $(shell pwd)

include ../common.mk


PROFILE_TARGET_PATH := $(TARGET_PATH)/profiling
SW_PARTITIONING_SETTINGS := --set num-cores=$(NUM_CORES)
SW_PARTITIONING_SETTINGS := $(SW_PARTITIONING_SETTINGS) --set multicore-profile-path=$(PROFILE_TARGET_PATH)/sw/bin/multicore-profile.xml
SW_PARTITIONING_SETTINGS := $(SW_PARTITIONING_SETTINGS) --set core-communication-profile-path=$(SB_HOME)/streamblocks-partitioning/profiling/software/bin/bandwidth.xml

include ../rules.mk

# ENTITY_NETWORK := XilinxTester
# ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)


# include ../rules.mk
