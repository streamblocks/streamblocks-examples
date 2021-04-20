
qid=hetero.stencil.kernels.GuassianBlur.JpegBlurNaiveNetwork
config_root=/home/mayy/streamblocks/streamblocks-examples/hetero/stencil/kernels/blur/naive_profile

partition_exe=${STREAMBLOCKS_HOME}/streamblocks-partitioning/partitioning/partition
config_path=${config_root}/profiled_data.json
source_path=/home/mayy/streamblocks/streamblocks-examples/hetero/stencil/bitmap:/home/mayy/streamblocks/streamblocks-examples/converters/src:/home/mayy/streamblocks/streamblocks-examples/system/art:/home/mayy/streamblocks/streamblocks-examples/system/std:/home/mayy/streamblocks/streamblocks-examples/jpeg/decoder/parallel:/home/mayy/streamblocks/streamblocks-examples/jpeg/io:/home/mayy/streamblocks/streamblocks-examples/hetero/stencil/kernels
target_path=${config_root}

echo "${partition_exe} --set config=${config_path} --source-path ${source_path} --target-path ${config_root} ${qid}"
${partition_exe} --set config=${config_path} --source-path ${source_path} --target-path ${config_root} ${qid}
