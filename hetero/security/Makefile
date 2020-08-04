
ENTITY_NETWORK = SHANetwork
ENTITY_NAMESPACE = hetero.security.sha
ENTITY = $(ENTITY_NAMESPACE).$(ENTITY_NETWORK)

CAL_DEPS := sha-1.cal ParallelSHA.cal

include ../common.mk

SOURCE_PATH_SETTINGS = --source-path $(shell pwd):$(ART_SOURCE_PATH)

NUM_PES ?= 8
MIN_STRING_SIZE ?= 4096
MAX_STRING_SIZE ?= 4096
STRINGS_PER_PE ?= 2048

PYTHON_SOURCES = scripts/HashCollector.py scripts/ParallelSHANetwork.py scripts/StreamDispatcher.py scripts/StringGenerator.py



$(ENTITY_NETWORK)_GENERATOR: $(PYTHON_SOURCES)
	echo "Generating ParallelSHA.cal"
	cd scripts; \
	python ParallelSHANetwork.py --min-size $(MIN_STRING_SIZE) --max-size $(MAX_STRING_SIZE) --num-pes $(NUM_PES) --strings-per-pe $(STRINGS_PER_PE) > ../ParallelSHA.cal 
	


PROFILING_TARGET_PATH := $(TARGET_PATH)/profiling
SW_PARTITIONING_SETTINGS := --set multicore-profile-path=$(PROFILING_TARGET_PATH)/sw/bin/multicore-profile.xml
SW_PARTITIONING_SETTINGS := $(SW_PARTITIONING_SETTINGS) --set core-communication-profile-path=$(SB_HOME)/streamblocks-partitioning/profiling/software/bin/bandwidth.xml
SW_PARTITIONING_SETTINGS := $(SW_PARTITIONING_SETTINGS) --set num-cores=$(NUM_CORES)
include ../rules.mk
