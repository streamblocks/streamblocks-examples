StreamBlocks Example Repository
===============================

Welcome to the StreamBlocks example repository. This repository contains a set of dataflow applications that you can use with the StreamBlocks dataflow compiler. The repository is organized as follows:

1. Getting started
2. Available applications
3. Dependencies
4. Support

### 1. Getting started

This is a collection of examples geared at teaching the user to code in CAL. This is a under developement repository and more examples are going to follow.

To use these applications, first you need to compile the Streamblocks compiler. See instructions on [streamblocks-platfroms](https://github.com/streamblocks/streamblocks-platforms/blob/master/README.md).

### 2. Available applications

Example        | Description           | Key Concepts | Keywords
---------------|-----------------------|--------------|----------
[system/][]    | A project for using external actors, functions, and procedures supported by the actors runtime <br>   |  How to write external actors function and procedures  |  external<br> 
[simple/][]    |  Simple examples of Dataflow Applications | How to define actors, processes and how to connect them|  actor<br>  action<br>  process<br>  network<br>  import <br>
[jpeg/][]      |  A 4:2:0 YUV movie JPEG decoder description in CAL<br> | How to define state machines in CAL, functions, procedures, instantiation of networks and external actors |  import entity <br>  fsm<br>  priority<br>  function<br>  procedure<br> 

### 3. Dependencies

The generated C multithread source code of Streamblocks has the following dependencies: CMake, libxml2 and (optionaly) libsdl2.

On ubuntu :

```
sudo apt-get install libxml2-dev libsdl2-dev cmake cmake-curses-gui
```
On Mac :

```
brew install libxml2 sdl2 cmake
```

### 4. Support

If you have an issue with one of the CAL examples please create a new issue in this repository.

[.]:.
[system/]:system/
[simple/]:simple/
[jpeg/]:jpeg/