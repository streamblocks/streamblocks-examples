stencil_dir=${STREAMBLOCKS_HOME}/streamblocks-examples/hetero/stencil/

CMAKE=/scratch/software/cmake-3.20.0-rc1-linux-x86_64/bin/cmake
for id in {0..34}
do
  cd ${stencil_dir}/build/generated/jpegblur/unique_${id}
  mkdir -p build
  cd build
  ${CMAKE} .. -DCMAKE_BUILD_TYPE=Release -DDISPLAY=off
  make JpegBlurNetwork -j 4
done

