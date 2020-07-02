
ENTITY_NAMESPACE := hetero.decoder.jpeg
ENTITY_NETWORK := JpegDecoderNetwork
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)
SB_HOME ?= $(STREAMBLOCKS_HOME)
TARGET_PATH ?= ./generated
NUM_CORES ?= 2
CMAKE ?= cmake

SB_BIN := $(SB_HOME)/streamblocks-platforms/streamblocks
PARTITIONING_BIN ?= $(SB_HOME)/streamblocks-partitioning/partitioning/partition
SB_EXAMPLES_PATH := $(SB_HOME)/streamblocks-examples
ART_SOURCE_PATH := $(SB_HOME)/streamblocks-examples/system/art

SOURCE_PATH := $(ART_SOURCE_PATH):$(SB_EXAMPLES_PATH)/jpeg:$(SB_EXAMPLES_PATH)/hetero/utils:/$(SB_EXAMPLES_PATH)/hetero/decoder/jpeg

COMMON_SETTIGNS := --set partitioning=on  --set enable-systemc=on

MULTICORE_SETTINGS := $(COMMON_SETTIGNS)

HLS_SETTINGS := $(COMMON_SETTIGNS) --set enable-traces=on

$(ENTITY_NETWORK)_MUTICORE:
	$(SB_BIN) multicore  $(MULTICORE_SETTINGS) --source-path $(SOURCE_PATH) --target-path $(TARGET_PATH)  $(ENTITY) \

$(ENTITY_NETWORK)_HLS:
	$(SB_BIN) vivado-hls $(HLS_SETTINGS)       --source-path $(SOURCE_PATH) --target-path $(TARGET_PATH)  $(ENTITY) \


$(ENTITY_NETWORK): $(ENTITY_NETWORK)_HLS $(ENTITY_NETWORK)_MUTICORE
	cd $(TARGET_PATH);\
	mkdir build;\
	cd build;\
	$(CMAKE) .. -DCMAKE_BUILD_TYPE:STRING=Release -DUSE_SYSTEMC=ON -DHLS_CLOCK_PREIOD=3.3; \
	make $(ENTITY_NETWORK) -j



clean:
	rm -r $(TARGET_PATH)

