
include ../common.mk

ENTITY_NAMESPACE := hetero.decoder.mpeg.parallel
ENTITY_NETWORK := ParallelNetwork
ENTITY := $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)


# PATH_SETTINGS := --source-path $(SOURCE_ART_PATH) --orcc-source-path $(ORCC_SOURCE_PATH) --xdf-source-path $(XDF_SOURCE_PATH) --target-path $(TARGET_PATH)


# parallel:
# 	$(SB_BIN) multicore $(PATH_SETTINGS) $(ENTITY);\
# 	cd $(TARGET_PATH)/build;\
# 	/home/mayy/cmake-3.15.5-Linux-x86_64/bin/cmake .. -DCMAKE_BUILD_TYPE:STRING=Release; \
# 	make -j

# partition: 
# 	$(PARTITIONING_BIN) \
# 	 --set num-cores=$(NUM_CORES) \
# 	 --set multicore-profile-path=$(TARGET_PATH)/bin/prof.xml \
# 	 --set core-communication-profile-path=$(SB_HOME)/streamblocks-partitioning/profiling/software/bin/bandwidth.xml \
# 	 --source-path $(SOURCE_ART_PATH) \
# 	 --orcc-source-path $(ORCC_SOURCE_PATH) \
# 	 --xdf-source-path $(XDF_SOURCE_PATH) \
# 	 --target-path $(TARGET_PATH) $(ENTITY)


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

$(ENTITY_NETWORK)_TEMP:
	$(SB_BIN) multicore $(PATH_SETTINGS) $(ENTITY)


clean:
	rm -r $(TARGET_PATH)