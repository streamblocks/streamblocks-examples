#include "device-handle.h"
#include <iostream>
#include <memory>
#include <sstream>
#include <vector>

class BandwidthTester {

public:
  BandwidthTester(const int num, const std::string kernel_name,
                  const std::string dir, std::string result_file)
      : num(num) {

    dev = std::make_unique<ocl_device::DeviceHandle>(num, num, 0, kernel_name,
                                                     dir);
    os.open(result_file, std::ios::out);

    if (!os.is_open()) {
      OCL_ERR("Could not open file %s\n", result_file.c_str());
      std::exit(-1);
    }

    os << "<bandwidth>" << std::endl;
    for (int ix = 0; ix < num; ix++) {
      std::stringstream builder;
      builder << "input_" << ix;
      input_ports.emplace_back(builder.str());
    }
    for (int ix = 0; ix < num; ix++) {
      std::stringstream builder;
      builder << "output_" << ix;
      output_ports.emplace_back(builder.str());
    }

    dev->buildPorts(input_ports, output_ports);
  }

  void runTest(const int buffer_size, const int repeats) {

    os << "\t<test size=\"" << buffer_size << "\" num=\"" << num << "\">" << std::endl;

    std::cout << "Allocating buffers (" << buffer_size << " bytes)"
              << std::endl;

    int num_tokens = buffer_size / sizeof(int);
    for (auto &input : input_ports) {
      dev->allocateInputBuffer(input, buffer_size);
      dev->setUsableInput<int>(input, buffer_size / sizeof(int));
    }

    for (auto &output : output_ports) {
      dev->allocateOutputBuffer(output, buffer_size);
      dev->setUsableOutput<int>(output, buffer_size / sizeof(int));
    }

    for (int r = 0; r < repeats; r++) {
      os << "\t\t<experiment index=\"" << r << "\">" << std::endl;

      dev->enqueueWriteBuffers();
      dev->setArgs();
      dev->enqueueExecution();
      dev->enqueueReadSize();
      dev->waitForSize();
      dev->enqueueReadBuffers();
      dev->waitForReadBuffers();

      for (int ix = 0; ix < num; ix++) {
        auto produced = dev->getUsedOutput<int>(output_ports[ix]);
        auto consumed = dev->getUsedInput<int>(input_ports[ix]);
        OCL_ASSERT(produced == consumed,
                   "invalid prodcution consumption pair\n");
      }

      auto kernel_time = dev->getKernelTime();
      auto kernel_diff = std::get<1>(kernel_time) - std::get<0>(kernel_time);

      std::cout << "Kernel time: " << kernel_diff << " ns" << std::endl;

      os << "\t\t\t<kernel start=\"" << std::get<0>(kernel_time) << "\" end=\""
         << std::get<1>(kernel_time) << "\"/>" << std::endl;

      int ix = 0;
      for (auto &input : input_ports) {
        auto write_time = dev->getWriteTime(input);
        auto write_diff = std::get<1>(write_time) - std::get<0>(write_time);
        std::cout << input.toString() << " write time " << write_diff << " ns"
                  << std::endl;

        os << "\t\t\t<write id=\"" << ix << "\" ";
        os << "start=\"" << std::get<0>(write_time) << "\" ";
        os << "end=\"" << std::get<1>(write_time) << "\"/>" << std::endl;
        ix++;
      }

      ix = 0;
      for (auto &output : output_ports) {
        auto read_time = dev->getReadTime(output);
        auto read_diff = std::get<1>(read_time) - std::get<0>(read_time);
        std::cout << output.toString() << " read time " << read_diff << " ns"
                  << std::endl;
        os << "\t\t\t<read id=\"" << ix << "\" ";
        os << "start=\"" << std::get<0>(read_time) << "\" ";
        os << "end=\"" << std::get<1>(read_time) << "\"/>" << std::endl;
        ix++;
      }
      dev->releaseEvents();
      os << "\t\t</experiment>" << std::endl;
    }
    os << "\t</test>" << std::endl;
  }
  ~BandwidthTester() {
    os << "</bandwidth>" << std::endl;
    os.close();
  }

private:
  std::unique_ptr<ocl_device::DeviceHandle> dev;
  std::vector<ocl_device::PortAddress> input_ports;
  std::vector<ocl_device::PortAddress> output_ports;
  std::ofstream os;
  const int num;
};
int main(int argc, char *argv[]) {

  const int num_repeeats = 2;
  const int buffer_size_min = sizeof(int);
  const int buffer_size_max = sizeof(int) * 4;

  BandwidthTester tester(2, "Loopback2_kernel", "xclbin", "res.xml");
  for (int buffer_size = buffer_size_min; buffer_size <= buffer_size_max;
       buffer_size <<= 1) {
    tester.runTest(buffer_size, num_repeeats);
  }
}