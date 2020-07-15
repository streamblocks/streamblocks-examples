include ../common.mk

ENTITY_NAMESPACE := hetero.decoder.mpeg.serial
ENTITY_NETWORK := SerialNetwork
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)

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


$(ENTITY_NETWORK)_PARTITION_ANALYSIS:
	$(PARTITIONING_BIN) \
	--set num-cores=$(NUM_CORES) \
	--set multicore-profile-path=$(TARGET_PATH)/bin/prof.xml \
	--set core-communication-profile-path=$(SB_HOME)/streamblocks-partitioning/profiling/software/bin/bandwidth.xml \
	$(PATH_SETTINGS) $(ENTITY)


$(ENTITY_NETWORK)_TEMP:
	$(SB_BIN) multicore                      $(PATH_SETTINGS) $(ENTITY)

clean:
	rm -r $(TARGET_PATH)