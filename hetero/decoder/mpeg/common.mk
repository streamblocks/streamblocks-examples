


include ../../../common.mk





SB_ORCC_APPS_PATH := $(SB_EXAMPLES_PATH)/orc-apps

SB_ORCC_DESIGNS_PATH := $(SB_EXAMPLES_PATH)/orcc-designs

ORCC_SOURCE_PATH := $(SB_ORCC_APPS_PATH)/Research/src
ORCC_SOURCE_PATH := $(ORCC_SOURCE_PATH):$(SB_ORCC_APPS_PATH)/System/src
ORCC_SOURCE_PATH := $(ORCC_SOURCE_PATH):$(SB_ORCC_APPS_PATH)/RVC/src
ORCC_SOURCE_PATH := $(ORCC_SOURCE_PATH):$(SB_ORCC_DESIGNS_PATH)/Research/src



XDF_SOURCE_PATH := $(SB_ORCC_DESIGNS_PATH)/Research/src
XDF_SOURCE_PATH := $(XDF_SOURCE_PATH):$(SB_ORCC_APPS_PATH)/Research/src
XDF_SOURCE_PATH := $(XDF_SOURCE_PATH):$(SB_EXAMPLES_PATH)/


SOURCE_PATH := $(ART_SOURCE_PATH):$(UTILS_PATH):$(CAL_SOURCE_PATH)


PATH_SETTINGS := --source-path $(SOURCE_PATH) --orcc-source-path $(ORCC_SOURCE_PATH) --xdf-source-path $(XDF_SOURCE_PATH) --target-path $(TARGET_PATH)

