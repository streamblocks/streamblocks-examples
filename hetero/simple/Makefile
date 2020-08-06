
ENTITY_NETWORK = PipelinedNetwork
ENTITY_NAMESPACE = hetero.simple.pipes
ENTITY = $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)

CAL_DEPS := Pipes.cal

include ../common.mk

SOURCE_PATH_SETTINGS = --source-path $(shell pwd):$(ART_SOURCE_PATH)

SYSTEM_PROFILE_PATH = $(SB_HOME)/streamblocks-partitioning/profiling/

PROFILING_TARGET_PATH := $(TARGET_PATH)/profiling
SW_PARTITIONING_SETTINGS := --set num-cores=$(NUM_CORES) --set multicore-profile-path=$(PROFILING_TARGET_PATH)/sw/bin/multicore-profile.xml
SW_PARTITIONING_SETTINGS := $(SW_PARTITIONING_SETTINGS) --set core-communication-profile-path=$(SB_HOME)/streamblocks-partitioning/profiling/software/bin/bandwidth.xml
SW_PARTITIONING_SETTINGS := $(SW_PARTITIONING_SETTINGS) 

# HW_PARTITIONING_SETTINGS := --set systemc-profile-path=$(PROFILING_TARGET_PATH)/hw/bin/systemc-profile.xml
# HW_PARTITIONING_SETTINGS := --set ocl-profile-path=$(SYSTEM_PROFILE_PATH)/hardware/bin/bandwidth.xml $(HW_PARTITIONING_SETTINGS)



include ../rules.mk
