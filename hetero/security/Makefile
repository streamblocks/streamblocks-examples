
ENTITY_NETWORK = SHANetwork
ENTITY_NAMESPACE = hetero.security.sha
ENTITY = $(ENTITY_NAMESPACE).$(SHANetwork)

CAL_DEPS := sha-1.cal ParallelSHA.cal

include ../common.mk

PATH_SETTINGS = --source-path $(shell pwd) --target-path $(TARGET_PATH) 

NUM_PES ?= 16
MIN_STRING_SIZE ?= 1024
MAX_STRING_SIZE ?= 1024
STRINGS_PER_PE ?= 128

PTYHON_SOURCES = scripts/HashCollector.py scripts/ParallelSHA.py scripts/StreamDispatcher.py scripts/StringGenerator.py



$(ENTITY_NETWORK)_GENERATOR: $(PTYHON_SOURCES)
	echo "Generating ParallelSHA.cal"
	cd scripts; \
	python StringGenerator.py --min-size $(MIN_STRING_SIZE) --max-size $(MAX_STRING_SIZE) --num-pes $(NUM_PES) --strings-per-pe $(STRINGS_PER_PE); \
	python ParallelSHA.py $(NUM_PES) > ../ParallelSHA.cal ;\

include ../rules.mk