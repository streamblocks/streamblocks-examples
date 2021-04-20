stencil_dir=${STREAMBLOCKS_HOME}/streamblocks-examples/hetero/stencil/


for id in {0..34}
do
  cd ${stencil_dir}/build/generated/jpegblur/unique_${id}
  unzip artifacts.zip
  mv archive/project/bin bin
  rm bin/JpegBlurNetwork_1_xclbin.tar.gz
done

