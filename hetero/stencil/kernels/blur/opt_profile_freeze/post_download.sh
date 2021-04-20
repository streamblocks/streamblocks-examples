#!/bin/bash

root_dir=${PWD}

CMAKE=/scratch/software/cmake-3.20.0-rc1-linux-x86_64/bin/cmake
echo "$#"
if [ $# -ne 2 ]; then
  echo "Usage: ${0} GENPATH NETWORK"
fi

# for id in {0..0}
# do
#     cd ${root_dir}
#   if [ -d ${1}/unique_${id} ]; then
#     cd ${1}/unique_${id}
#     unzip artifacts.zip 
#     mv archive/project/bin bin 
#     rm bin/${2}_1_xclbin.tar.gz

#     mkdir -p build
#     cd build
#     ${CMAKE} .. -DCMAKE_BUIDL_TYPE=Release -DDISPLAY=off
#     make ${2} -j4
#   fi
  
# done