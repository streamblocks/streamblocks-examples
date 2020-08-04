from xml.dom import minidom
import argparse
import matplotlib.pyplot as plt
import numpy as np

class ActorStat():

  def __init__(self, element):
    
    self.id = element.attributes["id"].value
    self.total_cycles = int(element.attributes["clockcycles-total"].value)
    
    self.firings = int(element.attributes["firings"].value)
  
  def getId(self):
    return self.id
  
  def getCycles(self):
    return self.total_cycles
  
  def getFirings(self):
    return self.firings

def parseProfileXml(file_name):

  profile = minidom.parse(file_name)

  actorElements = profile.getElementsByTagName("actor")

  actors = [ActorStat(elem) for elem in actorElements]
  
  
  networkElement = profile.getElementsByTagName("network")[0]

  network_name = networkElement.attributes["name"].value

  network_cycles = int(networkElement.attributes["clockcycles-total"].value)

  labels = [actor.getId() for actor in actors]
  activities = [actor.getCycles() / network_cycles for actor in actors]

  x = [i for i in range(0, len(labels))]

  fig, ax = plt.subplots()

  barplot = ax.bar(x, activities)
  print(labels)
  ax.set_xticks(x)
  ax.set_xticklabels(labels, rotation=90)

  for bar in barplot:
    height = bar.get_height()
    ax.annotate("{:.2f}".format((height * 100.0)), xy=(bar.get_x() + bar.get_width() / 2, 
    height), xytext=(0, 3), textcoords="offset points", ha='center', va='bottom')

  plt.show()
  
if __name__ == "__main__":

  argsParser = argparse.ArgumentParser(description="Create a bar plot of SystemC actor activity ratios")
  argsParser.add_argument("profile_xml", metavar="FILE", type=str, help="profile xml file")
  args = argsParser.parse_args()
  parseProfileXml(args.profile_xml)


