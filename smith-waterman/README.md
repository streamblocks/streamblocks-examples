Smith-Waterman in CAL
=====================

This README file contains the following sections:

1. Overview
2. Design file hierarchy
3. Compilation and execution
4. Acknowledgments

### 1. Overview

![Alt text](img/top_sw.jpg?raw=true "Flatten Network of the CAL implementation of the Smith-Waterman Algorithm.")

A systolic implementation of the Smith-Waterman algorithm implemented in CAL. The main design is composed of 8 actors, arrayStreamer and display instances are used for feeding the design with two input sequences and displaying the aligned sequence respectively. The image above represents the flatten design of the dataflow network. 

### 2. Design file hierarchy

Application code is located in the src directory. A listing of all the files in this example is show below.

````
sw/configuration/Configuration.cal
sw/dut/ArrayStreamer.cal
sw/dut/Top_SW_array.cal
sw/io/Display.cal
sw/systolic/Aligner.cal
sw/systolic/Controller.cal
sw/systolic/Decoder.cal
sw/systolic/LeftBuffer.cal
sw/systolic/SW.cal
sw/systolic/SwCell.cal
sw/utils/Utils.cal
````
The SW.cal file represents the systolic Smith-Watermam dataflow network. The Top_SW_array.cal represents the top application for testing the implementation.
This design depends on the [system/][] project for printing values in the console.

### 3. Compilation and execution

To use this design, first you need to compile the Streamblocks compiler. See instructions on [streamblocks-platfroms](https://github.com/streamblocks/streamblocks-platforms).

To generate the C code of the Smith-Waterman design do the following:
```
streamblocks --source-path <cloned path of examples>/smith-waterman/src:<cloned path of examples>/system --target-path <target path>/sw_array sw.dut.Top_SW_array
```

To compile and execute the generated code:

````
cd <target path>/sw_array
cd build
ccmake ..
make
cd ../bin
./Top_SW_array
````

### 4. Acknowledgments

This design was adapted to work with StremBlocks. The original version of this deisgn has been published in IEEE SIPS 2017, the bibtex of this paper is the following.

````
@INPROCEEDINGS{8109982, 
author={S. {Casale-Brunet} and E. {Bezati} and M. {Mattavelli}}, 
booktitle={2017 IEEE International Workshop on Signal Processing Systems (SiPS)}, 
title={Design space exploration of dataflow-based Smith-Waterman FPGA implementations}, 
year={2017}, 
volume={}, 
number={}, 
pages={1-6}, 
keywords={biology computing;data flow computing;DNA;field programmable gate arrays;molecular biophysics;proteins;pipelinable multistage processing element;resource utilization;DNA sequence sizes;performance requirements;design space explorations;dynamic dataflow program;direct high-level synthesis;FPGA HDL;dataflow-based Smith-Waterman FPGA implementations;protein sequence alignment;DNA sequence alignment;HLS;S-W core;frequency 250.0 MHz;Heuristic algorithms;Field programmable gate arrays;Algorithm design and analysis;DNA;Bioinformatics;Proteins;Genomics}, 
doi={10.1109/SiPS.2017.8109982}, 
ISSN={2374-7390}, 
month={Oct},}
````

[.]:.
[system/]:system/