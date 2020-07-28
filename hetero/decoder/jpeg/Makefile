
ENTITY_NAMESPACE := hetero.decoder.jpeg
ENTITY_NETWORK := JpegDecoderTester
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)

include ../../../common.mk

CAL_SOURCE_PATH := $(SB_EXAMPLES_PATH)/jpeg:$(shell pwd)

PATH_SETTINGS := --source-path $(CAL_SOURCE_PATH) --target-path $(TARGET_PATH)

include ../../../rules.mk

