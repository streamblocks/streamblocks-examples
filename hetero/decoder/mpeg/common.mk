

SB_HOME ?= $(STREAMBLOCKS_HOME)
CMAKE ?= cmake

TARGET_PATH ?= ./generated

NUM_CORES ?= 2


SB_BIN := $(SB_HOME)/streamblocks-platforms/streamblocks

PARTITIONING_BIN ?= $(SB_HOME)/streamblocks-partitioning/partitioning/partition

SB_EXAMPLES_PATH := $(SB_HOME)/streamblocks-examples


SB_ORCC_APPS_PATH := $(SB_EXAMPLES_PATH)/orc-apps

SB_ORCC_DESIGNS_PATH := $(SB_EXAMPLES_PATH)/orcc-designs

ORCC_SOURCE_PATH := $(SB_ORCC_APPS_PATH)/Research/src
ORCC_SOURCE_PATH := $(ORCC_SOURCE_PATH):$(SB_ORCC_APPS_PATH)/System/src
ORCC_SOURCE_PATH := $(ORCC_SOURCE_PATH):$(SB_ORCC_APPS_PATH)/RVC/src
ORCC_SOURCE_PATH := $(ORCC_SOURCE_PATH):$(SB_ORCC_DESIGNS_PATH)/Research/src



XDF_SOURCE_PATH := $(SB_ORCC_DESIGNS_PATH)/Research/src
XDF_SOURCE_PATH := $(XDF_SOURCE_PATH):$(SB_ORCC_APPS_PATH)/Research/src
XDF_SOURCE_PATH := $(XDF_SOURCE_PATH):$(SB_EXAMPLES_PATH)/


SOURCE_ART_PATH := $(SB_EXAMPLES_PATH)/system/art


COMMON_SETTIGNS := --set partitioning=on

MULTICORE_SETTIGS := $(COMMON_SETTIGNS)

HLS_SETTINGS := $(COMMON_SETTIGNS)

# HLS_SETTINGS := $(COMMON_SETTIGNS) --set enable-action-profile=off --set max-bram=8MiB


PATH_SETTINGS := --source-path $(SOURCE_ART_PATH) --orcc-source-path $(ORCC_SOURCE_PATH) --xdf-source-path $(XDF_SOURCE_PATH) --target-path $(TARGET_PATH)