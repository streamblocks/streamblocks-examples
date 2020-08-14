from xml.dom import minidom
import argparse
import matplotlib.pyplot as plt
import numpy as np

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



def parseProfileXml(file_name):

  profile = minidom.parse(file_name)

  actorElements = profile.getElementsByTagName("actor")

  actors = [ActorStat(elem) for elem in actorElements]
  
  
  networkElement = profile.getElementsByTagName("network")[0]

  network_name = networkElement.attributes["name"].value

  network_cycles = int(networkElement.attributes["clockcycles-total"].value)

  labels = np.array([actor.getId() for actor in actors])
  execs = np.array([actor.getCycles() / network_cycles for actor in actors])
  sleeps = np.array([actor.getSleeps() / network_cycles for actor in actors])
  syncs = np.array([actor.getSyncCycles() / network_cycles for actor in actors])
  testWaits = np.array([1.0 for actor in actors]) - execs - sleeps - syncs 
  print(testWaits)
  print(execs)
  print(labels)
  width = 0.35
  x = np.arange(len(labels))

  fig, ax = plt.subplots()

  testWaitBars = ax.bar(x, testWaits, width, label='TEST*WAIT cycles', color='red')
  sleepBars = ax.bar(x, sleeps, width, bottom=testWaits, label='SLEEP cycles', color='blue')
  execBars = ax.bar(x, execs, width, bottom=testWaits + sleeps, label='TEST*EXEC cycles', color='green')
  syncBars = ax.bar(x, syncs, width, bottom=testWaits + sleeps + execs, label='SYNC cycles', color='black')

  ax.set_xticks(x)
  ax.set_xticklabels(labels, rotation=90)

  def labelBars(bars):
    for bar in bars:
      height = bar.get_height()
      ax.annotate("{:.2f}".format((height * 100.0)), xy=(bar.get_x() + bar.get_width() / 2, 
      height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')
  ax.legend()
  ax.yaxis.grid()
  # labelBars(execBars)
  # labelBars(sleepBars)

  plt.show()
  
if __name__ == "__main__":

  argsParser = argparse.ArgumentParser(description="Create a bar plot of SystemC actor activity ratios")
  argsParser.add_argument("profile_xml", metavar="FILE", type=str, help="profile xml file")
  args = argsParser.parse_args()
  parseProfileXml(args.profile_xml)


