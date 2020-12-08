from xml.dom import minidom
import argparse
# import matplotlib.pyplot as plt
import numpy as np
# import matplotlib
from scipy.ndimage import gaussian_filter

import lxml.etree as ET

class TestStats():

    def __init__(self, test_elem):
      
      START = "start"
      END = "end"
      self.kernel_duration = []
      self.write_duration = []
      self.read_duration = []
      self.read_size_duration = []
      self.num = int(test_elem.attributes["num"].value)
      self.size = int(test_elem.attributes["size"].value) * self.num
      experiments = test_elem.getElementsByTagName("experiment")
      for expr in experiments:
        
        # Get the kernel time     
        self.kernel_duration.append(self.getDuration(expr, "kernel"))

        # Get the write time
        self.write_duration.append(self.getDuration(expr, "write-summary"))

        # Get the read time
        self.read_duration.append(self.getDuration(expr, "read-summary"))

        # Get the read size time
        self.read_size_duration.append(self.getDuration(expr, "read-size-summary"))

      k_m = np.mean(self.kernel_duration)
      w_m = np.mean(self.write_duration)
      r_m = np.mean(self.read_duration)

      k_std = np.std(self.kernel_duration)
      w_std = np.std(self.write_duration)
      r_std = np.std(self.read_duration)

  
      
      self.kernel_mean = np.mean(self.kernel_duration) * 1e-9
      self.write_mean = np.mean(self.write_duration) * 1e-9
      self.read_mean = np.mean(self.read_duration) * 1e-9
      self.read_size_mean = np.mean(self.read_size_duration) * 1e-9

      self.kernel_bw = self.size / 1024. /1024. / self.kernel_mean
      self.write_bw = self.size / 1024. / 1024. / self.write_mean
      self.read_bw = self.size / 1024. /1024. / self.read_mean

      # print("{sz} : {k} {w} {r} MiB/s\n".format(sz=self.size, k=self.kernel_bw, w=self.write_bw, r=self.read_bw))
        
    def getDuration(self, expr, element_type):

      elem = expr.getElementsByTagName(element_type)[0]
      elem_start = int(elem.attributes["start"].value)
      elem_end = int(elem.attributes["end"].value)

      return elem_end - elem_start

    def filter(self, data, mean, std):
      return list(
        filter(lambda x: (x > mean + 3 * std) or (x < mean - 3 * std), data))

class LoopbackStats():


  def __init__(self, file_name):

    stats = minidom.parse(file_name)

    test_elems = stats.getElementsByTagName("test")
    self.tests = [TestStats(t) for t in test_elems]



def plotAll(stats):

  font = {'family':'sans-serif',
          'sans-serif':['Helvetica'],
          'size' : 12}
  matplotlib.rc('font', **font)

  fig, ax = plt.subplots()
  ix = 1
  colors = [
    'tab:blue', 'tab:orange', 'tab:green', 'tab:red', 'tab:purple', 'tab:brown',
    'tab:pink', 'tab:gray', 'tab:olive', 'tab:cyan'
  ]
  color_ix = 0
  for stat in stats:

    tests = stat.tests
    x_test_sz = [test.size for test in tests]
    y_write_points = [test.write_bw for test in tests]
    y_read_points = [test.read_bw for test in tests]
    y_write_bw = gaussian_filter(y_write_points, 0.80)
    y_read_bw = gaussian_filter(y_read_points, 0.80)


    ax.plot(x_test_sz, y_write_bw,  color = colors[color_ix], linewidth=5.0, alpha=0.70, label='write x' + str(ix))
    # ax.plot(x_test_sz, y_write_points, marker='x', color=colors[color_ix], linestyle=' ', label='write x' + str(ix) + ' (MiB/s)')
    color_ix += 1
    ax.plot(x_test_sz, y_read_bw,  color = colors[color_ix], linewidth=5.0, alpha=0.70, label='read x' + str(ix))
    # ax.plot(x_test_sz, y_read_points, marker='o', color=colors[color_ix], linestyle=' ', label='read x' + str(ix) + ' (MiB/s)')
    color_ix += 1

    ix = ix + 1
    
  # import pdb; pdb.set_trace()
  ax.legend()
  ax.set_xscale('log', basex=2)
  xtks = [2 ** x for x in range(0, 31, 4)]
  ax.set_xticks(xtks)
  xlabels = [makeLabel(x) for x in xtks]
  ax.set_xticklabels(xlabels, rotation=-90)
  # ax.set_title("Bandwidth measuresments")
  ax.set_xlim(2**2, 2**29)
  ax.grid(True)

  ax.set_xlabel('PCIe payload size')
  ax.set_ylabel('PCIe read/write bandwidth')
  plt.show()

def makeLabel(x):

  if x >= 2 ** 30:
    return str(int(x / 2 ** 30)) + "GiB"
  elif x >= 2 ** 20:
    return str(int(x / 2 ** 20)) + "MiB"
  elif x >= 2 ** 10:
    return str(int(x / 2 ** 10)) + "KiB"
  else :
    return str(x) + "B"

def crunch(stat):

  profile_data = ET.Element('profile-data')
  bw_test =ET.SubElement(profile_data, 'bandwidth-test')
  bw_test.set('type', 'FPGA')

  for test in stat.tests:
    num_bytes = test.size
    kernel = int(test.kernel_mean * 1e+9)
    write = int(test.write_mean * 1e+9)
    read = int(test.read_mean * 1e+9)
    read_size = int(test.read_size_mean * 1e+9)
    reps = 1
    con = ET.SubElement(bw_test, 'Connection')
    con.set('kernel-total', str(kernel))
    con.set('write-total', str(write))
    con.set('read-total', str(read))
    con.set('read-size-total', str(read_size))
    con.set('repeats', str(reps))
    con.set('buffer-size', str(num_bytes))

  profile_data_raw = ET.tostring(profile_data, pretty_print=True)
  myfile = open("opencl-bandwidth.xml", "wb")
  myfile.write(profile_data_raw)


def parseProfile(file_name):

  return LoopbackStats(file_name)

if __name__ == "__main__":

  argsParser = argparse.ArgumentParser(description="Create a plot of bandwidth test")
  argsParser.add_argument("profile_xml", metavar="FILE", type=str, help="profile xml file")
  args = argsParser.parse_args()
  
  
  stats = [parseProfile(args.profile_xml + str(i) + ".xml") for i in range(1, 2)]
  # plotAll(stats)
  crunch(stats[0])
