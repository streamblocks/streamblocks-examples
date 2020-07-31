
import StreamDispatcher
import HashCollector

class ParallelSHA():


  def __init__(self, N):
    self.size = N

  def getPEInstances(self):

    pes = ""
    for ix in range(0, self.size):
      pes += """
      pe{index} = SHA1();
      """.format(index = ix)
    return pes
  

  def getConnections(self):

    connections = ""

    for ix in range(0, self.size):

      connections += """
      dispatcher.stream{index} --> pe{index}.text;
      pe{index}.hash --> collector.stream{index};
      """.format(index = ix)
    return connections
  
  def getNetwork(self):

    actor = """
  network ParallelSHA() uint strings ==> uint hashes:

    entities
      cast = IntToCharCast();

      dispatcher = StreamDispatcher();

      collector = HashCollector();

      // processing elements
      {peInstances}
    
    structure

      strings --> cast.In;
      cast.Out -->dispatcher.stringStream;
      {connections}
      collector.hashStream --> hashes;
  end
  """.format(peInstances = self.getPEInstances(), 
    connections = self.getConnections())
    return actor

  def getActors(self):
    
    return """
namespace hetero.security.sha:
 
  actor IntToCharCast() uint In ==> uint(size = 8) Out:
    action In:[t] ==> Out:[(t::uint(size = 8))]
    end
  end
    {dispatcher}
    {collector}
    {network}
end
    """.format(
      dispatcher = StreamDispatcher.getStreamDispatcher(self.size),
      collector = HashCollector.getHashCollector(self.size),
      network = self.getNetwork())


if __name__ == "__main__":

  import argparse

  parser = argparse.ArgumentParser(description="Generate a parallel SHA1 network")
  parser.add_argument('N', type=int, help="number of SHA1 processing elements")
  
  args = parser.parse_args()
  print(ParallelSHA(args.N).getActors())