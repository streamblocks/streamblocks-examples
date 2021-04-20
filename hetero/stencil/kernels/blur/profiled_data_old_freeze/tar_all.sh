stencil_dir=${STREAMBLOCKS_HOME}/streamblocks-examples/hetero/stencil/

tar_dirs=""
cd ${stencil_dir}/build/generated/jpegblur/

for id in {0..2}
do
  if [ -d "unique_${id}/multicore" ]; then
    if [ -d "unique_${id}/vivado-hls" ]; then
      tar_dirs="unique_${id}/multicore ${tar_dirs}"
      tar_dirs="unique_${id}/vivado-hls ${tar_dirs}"
      tar_dirs="unique_${id}/CMakeLists.txt unique_${id}/bin ${tar_dirs}"
    else
      echo "unique_${id}/vivado-hls does not exits"
    fi
  else
    echo "unique_${id}/multicore does not exits"
  fi
done
echo "At ${PWD}"
echo "tar -czvf jpegblur_bins.tar.gz ${tar_dirs}"
ls
tar -czvf jpegblur_bins.tar.gz ${tar_dirs}

