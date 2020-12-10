cmake_minimum_required(VERSION 3.10)


option(REMOTE_XCLBIN "Remotely fetch generated xclbins" OFF)

# List of HLS_CLOCK_PERIOD settings to build binaries for
# Current clock speeds 300, 250, 200, 150 and 100 MHz

set(CONFIGURATIONS "0;1;2;3;4;5;6;7;8;9;10;11;12;13" CACHE STRING "List of ; separated configuration ids")
set(CONFIG_ROOT "." CACHE STRING "Root folder for the configurations name as configuration_N where N is a number")
set(CLOCK_LIST "3.3;10;5;2.5;1.667;6.667;13.333" CACHE STRING "List of ; seperated HLS clock settings")
set(CLOCK_IDS "1;3;4;5;6;0;2" CACHE STRING "List of clock ids coresponding to clocks")

set(FPGA_NAME "xczu7ev-ffvc1156-2-e" 
  CACHE STRING 
  "Name of Xilinx FPGA, e.g \"xcku115-flvb2104-2-e\", \"xcu250-figd2104-2L-e\", \"xczu7ev-ffvc1156-2-e\", \"xczu3eg-sbva484-1-e\", ...")

set(PLATFORM "xilinx_zcu106_base_dfx_202010_1" 
  CACHE STRING "Supported platform name, e.g \"xilinx_kcu1500_dynamic_5_0\", \"xilinx_u250_xdma_201830_2\", \"zcu102_base\", \"xilinx_zcu106_base_202010_1\", \"ultra96_base\",... ")


set(KERNEL_FREQ "150" CACHE STRING "Clock frequency in MHz.")

option(USE_VITIS "Build an RTL OpenCL Kernel for Vitis" OFF)
option(USE_SDACCEL "Build an RTL OpenCL Kernel for SDAccel" OFF)
option(IS_MPSOC "Vitis Embedded Platform" OFF)


set(REMOTE_USER "user" CACHE STRING "remote ssh username")
set(REMOTE_REPO "/scratch/mayy/streamblocks/streamblocks-examples/rvc-mpeg4sp/" CACHE STRING "remote xclbin repo")
set(REMOTE_IP   "iccluster126.iccluster.epfl.ch" CACHE STRING "remote server name")
set(FIFO_QUEUE_DEPTH 4096 CACHE STRING "Default buffer size")
set(OUTPUT_PATH "genx" CACHE STRING "Output path, where to generate the source code")



add_custom_target(all_xclbin) # build all xclbins
add_custom_target(all_bin)    # build all multicore hetero binaries
add_custom_target(all_sc_bin) # build all sc binaries
add_custom_target(all_sc_run) # run all sc simulations


list(LENGTH CLOCK_LIST CLOCKS_COUNT)
math(EXPR MAX_CLOCK_INDEX "${CLOCKS_COUNT} - 1")

message(STATUS "Found ${CLOCKS_COUNT} clock configs (max index ${MAX_CLOCK_INDEX})")


