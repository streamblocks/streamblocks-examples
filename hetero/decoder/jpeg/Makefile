
ENTITY_NAMESPACE := hetero.decoder.jpeg
ENTITY_NETWORK := JpegNetwork
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)

include ../../common.mk

CAL_SOURCE_PATH := $(SB_EXAMPLES_PATH)/jpeg:$(shell pwd):$(ART_SOURCE_PATH):$(UTILS_PATH)

PATH_SETTINGS := --source-path $(CAL_SOURCE_PATH) --target-path $(TARGET_PATH)

include ../../rules.mk

