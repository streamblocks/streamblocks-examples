StreamBlocks Example Repository
===============================

Welcome to the StreamBlocks examples repository. This repository contains a set of dataflow applications that you can use with the StreamBlocks dataflow compiler. 

This README file is organized as follows:
1. Getting started
2. How to download this repository
3. Available applications
4. Dependencies
5. Support

### 1. Getting started

This is a collection of examples geared at teaching the user to code in CAL. This is a under developement repository and more examples are going to follow.

To use these applications, first you need to compile the Streamblocks compiler. See instructions on [streamblocks-platfroms](https://github.com/streamblocks/streamblocks-platforms/blob/master/README.md).

### 2. How to download this repository

To get a local copy of the StreamBlocks examples repository, clone this repository to the local system with the following commmand:
```
git clone https://github.com/streamblocks/streamblocks-examples streamblocks-examples
```

### 3. Available applications

Example        | Description           | Key Concepts | Keywords
---------------|-----------------------|--------------|----------
[system/][]    | A project for using external actors, functions, and procedures supported by the actors runtime <br>   |  How to write external actors function and procedures  |  external<br> 
[simple/][]    | Simple examples of Dataflow Applications | How to define actors, processes and how to connect them|  actor<br>  action<br>  process<br>  network<br>  import <br>
[jpeg/][]      | A 4:2:0 YUV movie JPEG decoder description in CAL<br> | How to define state machines in CAL, functions, procedures, instantiation of networks and external actors |  import entity <br>  fsm<br>  priority<br>  function<br>  procedure<br> 
[smith-waterman/][] | A systolic array implementation of Smith-Waterman algorithm in CAL<br> | Mixing actors and processes. Defining hierarchical namespaces, global procedures and functions |  import entity <br>  fsm<br>  priority<br>  function<br>  procedure<br> 
### 4. Dependencies

The generated C multithread source code of Streamblocks has the following dependencies: CMake, libxml2 and (optionaly) libsdl2.

On Ubuntu :

```
sudo apt-get install libxml2-dev libsdl2-dev cmake cmake-curses-gui
```
On Mac :

```
brew install libxml2 sdl2 cmake
```

### 5. Support

If you have an issue with one of the CAL examples please create a new issue in this repository.

[.]:.
[system/]:system/
[simple/]:simple/
[jpeg/]:jpeg/
[smith-waterman/]:smith-waterman/