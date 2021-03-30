from xml.dom import minidom
import argparse
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
import matplotlib
class ActorStat():

  def __init__(self, element):
    
    self.id = element.attributes["id"].value
    self.total_cycles = int(element.attributes["clockcycles-total"].value)
    
    self.firings = int(element.attributes["firings"].value)

    triggerElement = element.getElementsByTagName("trigger")[0]
    self.trigger = {
        "IDLE_STATE": int(triggerElement.attributes["IDLE_STATE"].value),
        "LAUNCH": int(triggerElement.attributes["LAUNCH"].value),
        "CHECK": int(triggerElement.attributes["CHECK"].value),
        "SLEEP": int(triggerElement.attributes["SLEEP"].value),
        "SYNC_LAUNCH": int(triggerElement.attributes["SYNC_LAUNCH"].value),
        "SYNC_CHECK": int(triggerElement.attributes["SYNC_CHECK"].value),
        "SYNC_WAIT": int(triggerElement.attributes["SYNC_WAIT"].value),
        "SYNC_EXEC": int(triggerElement.attributes["SYNC_EXEC"].value)
      }
  
  def getId(self):
    return self.id
  
  def getCycles(self):
    return self.total_cycles
  
  def getFirings(self):
    return self.firings
  
  def getSleeps(self):
    return self.trigger["SLEEP"]
  
  def getSyncCycles(self):
    return self.trigger["SYNC_EXEC"] + self.trigger["SYNC_WAIT"]


class SimStats():

  def __init__(self, path, run_size):
    
    file_name = path + '/profile_' + str(run_size) + '.xml'
    
    profile = minidom.parse(file_name)

    network_elem = profile.getElementsByTagName("network")[0]

    self.network_cycles = int(network_elem.attributes["clockcycles-total"].value)

    self.network_runs = int(network_elem.attributes["runs"].value)

    actor_elems = profile.getElementsByTagName("actor")

    actor_stats = [ActorStat(elem) for elem in actor_elems]

    actor_cycles = [actor.total_cycles for actor in actor_stats]

    critical_index = np.argmax(actor_cycles)

    self.critical_actor = actor_stats[critical_index]

    self.buffer_size = run_size


def plot(stats):

  # font = {'family' : 'normal',
  #       'weight' : 'bold',
  #       'size'   : 12}

  font = {'family':'sans-serif',
          'sans-serif':['Helvetica'],
          'size' : 14}
  matplotlib.rc('font', **font)
  
  freq = 279.6
  clk = 1000. / freq * 1e-9
  frames = 600.

  dev_fps = [
    510.344071,
    641.866243,
    678.040245,
    685.537373,
    716.321343,
    788.536544,
    828.507795,
    856.984888,
    871.194379,
    882.855515,
    883.107017,
    891.573195,
    892.428750,
    896.299152,
    894.919169,
    892.257507
  ]

  sim_fps = [frames / (stat.network_cycles * clk) for stat in stats]

  # sim_fit = gaussian_filter(sim_fps, sigma=1)

  
  buffer_size = [stat.buffer_size * 4 for stat in stats]

  fig, ax = plt.subplots()


  fps_normal = [dev_fps[ix] / sim_fps[ix] for ix in range(0, len(sim_fps))]
  
  # normplot = ax.plot(buffer_size, fps_normal, marker='o', markersize=8., linewidth=2.0, alpha=1, linestyle=':', color='tab:green', label='theoretical') 

  simplot = ax.plot(buffer_size, sim_fps, marker='o', markersize=8., linewidth=2.0, alpha=1, linestyle=':', color='tab:green', label='theoretical')

  devplot = ax.plot(buffer_size, dev_fps, marker='x', markersize=8., linewidth=2.0, alpha=1, linestyle="--", color='tab:blue', label='real-world')
  
  # simfit = ax.plot(buffer_size, sim_fit, color='tab:cyan', linewidth=6.0, alpha=0.5)
  
  ax.set_xscale('log', basex=2)

  for ix in range(0, len(buffer_size)):
    x = buffer_size[ix]
    y_sim = sim_fps[ix]
    y_dev = dev_fps[ix]
    sync = stats[ix].critical_actor.trigger["SYNC_LAUNCH"]
    sync_mode = stats[ix].critical_actor.getSleeps() / stats[ix].critical_actor.getCycles() * 100.
    run = stats[ix].network_runs
    text = '({:d}, {:.2f}%)'.format(sync, sync_mode)
    ax.annotate(
      text=text, 
      xy=(x, y_sim - 50),
      horizontalalignment='center',
      rotation=-45,
      size=12)
    
    diff = 100. - (y_dev / y_sim) * 100.
    diff_text = "{:2.1f}%".format(-diff)
    ax.annotate(text=diff_text, 
      xy=(x, y_dev - 40),
      horizontalalignment='center',
      rotation=-45,
      size=12)
  
  arrow_x = buffer_size[2]
  arrow_y = sim_fps[2]
  ax.annotate(
      text='(# sync barriers hit, % sleep cycles)', 
      xy = (arrow_x , arrow_y - 40), 
      xytext=(arrow_x , arrow_y - 200),
      horizontalalignment='center',
      arrowprops=dict(facecolor='black', shrink=0.0005, width=4.0, headwidth=10., headlength=10.),
      size=12)
  
  ax.set_xticklabels([makeLabel(x) for x in buffer_size], rotation=-90)
  
  arrow_xx = buffer_size[9]
  arrow_yy = dev_fps[9]
  ax.annotate(
    text="% difference with \ntheoretical",
    xy = (arrow_xx, arrow_yy - 40),
    xytext = (arrow_xx , arrow_yy - 200),
    horizontalalignment='center',
    arrowprops=dict(facecolor='black', shrink=0.0005, width=4.0, headwidth=10., headlength=10.),
    size=12)
  


  ax.grid()

  ax.set_xlabel('Hardware-software buffer size')
  ax.set_ylabel('Frames per second', rotation=90)
  ax.legend(loc='lower right', markerscale=1.0)
  plt.tight_layout()
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

if __name__ == "__main__":


  argsParser = argparse.ArgumentParser(description="Compare Jpeg runs")
  argsParser.add_argument("profile_xml_path", metavar="PATH", type=str, help="path to simulation profile xmls")
  args = argsParser.parse_args()

  buffer_size = [
    1 << i for i in range(12, 28)
  ]

  stats = [SimStats(args.profile_xml_path, sz) for sz in buffer_size]


  plot(stats)


