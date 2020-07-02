

TOP_NETWORK := jpeg.decoder.Top_Decoder

SB_HOME := /home/mayy/streamblocks

SB_BIN := $(SB_HOME)/streamblocks-platforms/streamblocks
SB_EXAMPLES_PATH := $(SB_HOME)/streamblocks-examples


SB_ORCC_APPS_PATH := $(SB_EXAMPLES_PATH)/orc-apps

SB_ORCC_DESIGNS_PATH := $(SB_EXAMPLES_PATH)/orcc-designs

ORCC_SOURCE_PATH := $(SB_ORCC_APPS_PATH)/JPEG/src:$(SB_ORCC_APPS_PATH)/System/src

XDF_SOURCE_PATH := $(SB_ORCC_APPS_PATH)/JPEG/src

SOURCE_ART_PATH := $(SB_EXAMPLES_PATH)/system/art

TARGET_PATH ?= ./generated

PLATFORM ?= Orcc

parallel:
	$(SB_BIN) $(PLATFORM) --orcc-source-path $(ORCC_SOURCE_PATH) --xdf-source-path $(XDF_SOURCE_PATH) --target-path $(TARGET_PATH) $(TOP_NETWORK);\
	# cd $(TARGET_PATH)/build;\
	# /home/mayy/cmake-3.15.5-Linux-x86_64/bin/cmake .. -DCMAKE_BUILD_TYPE:STRING=Release; \
	# make -j


