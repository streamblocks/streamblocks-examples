
ENTITY_NETWORK = hetero.security.sha.SHANetwork
SB_HOME ?= $(STREAMBLOCKS_HOME)
CMAKE ?= cmake

TARGET_PATH ?= $(shell pwd)/generated

NUM_CORES ?= 2


SB_BIN := $(SB_HOME)/streamblocks-platforms/streamblocks

PARTITIONING_BIN ?= $(SB_HOME)/streamblocks-partitioning/partitioning/partition

SB_EXAMPLES_PATH := $(SB_HOME)/streamblocks-examples


SOURCE_ART_PATH := $(SB_EXAMPLES_PATH)/system/art
UTILS_PATH := $(SB_EXAMPLES_PATH)/hetero/utils
SOURCE_PATH := $(SB_EXAMPLES_PATH)/hetero/security:$(SOURCE_ART_PATH):$(UTILS_PATH)

SYSTEMC_SETTIGNS := --set enable-systemc=on --set max-bram=128MiB

COMMON_SETTIGNS := --set partitioning=on 

MULTICORE_SETTIGS := $(COMMON_SETTIGNS)

HLS_SETTINGS := $(COMMON_SETTIGNS) --set enable-action-profile=off 


PATH_SETTINGS := --source-path $(SOURCE_PATH) --target-path $(TARGET_PATH)


sha_1_software:
	$(SB_BIN) multicore $(PATH_SETTINGS) $(ENTITY_NETWORK)

sha_1_systemc:
	$(SB_BIN) vivado-hls $(SYSTEMC_SETTIGNS) $(HLS_SETTINGS) $(PATH_SETTINGS) $(ENTITY_NETWORK)
	$(SB_BIN) multicore $(SYSTEMC_SETTIGNS) $(MULTICORE_SETTIGS) $(PATH_SETTINGS) $(ENTITY_NETWORK)

sha_1_hetero:
	$(SB_BIN) vivado-hls $(HLS_SETTINGS) $(PATH_SETTINGS) $(ENTITY_NETWORK)
	$(SB_BIN) multicore $(MULTICORE_SETTIGS) $(PATH_SETTINGS) $(ENTITY_NETWORK)
