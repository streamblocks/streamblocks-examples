include ../common.mk

ENTITY_NAMESPACE := hetero.decoder.mpeg.xilinx
ENTITY_NETWORK := Top_Xilinx
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)
CAL_SOURCE_PATH := $(CAL_SOURCE_PATH):.
PATH_SETTINGS := --source-path $(CAL_SOURCE_PATH) --orcc-source-path $(ORCC_SOURCE_PATH) --xdf-source-path $(XDF_SOURCE_PATH) --target-path $(TARGET_PATH)

$(ENTITY_NETWORK)_HLS:
	$(SB_BIN) vivado-hls $(HLS_SETTINGS) $(PATH_SETTINGS) $(ENTITY)
$(ENTITY_NETWORK)_MULTICORE:
	$(SB_BIN) multicore $(MULTICORE_SETTIGS) $(PATH_SETTINGS) $(ENTITY)

$(ENTITY_NETWORK)_SC:
	cd $(TARGET_PATH); \
	mkdir -p build; \
	cd build; \
	$(CMAKE) .. -DCMAKE_BUILD_TYPE:STRING=Release -DUSE_SYSTEMC=ON -DHLS_CLOCK_PREIOD=3.3; \
	make $(ENTITY_NETWORK) -j

clean:
	rm -r $(TARGET_PATH)