
class HashCollector():

  def __init__(self, N):
    self.fanin = N

  def getActions(self):

    actions ="""
    stop: action ==>
    guard counter = HASH_STREAM_SIZE
    do
      counter := 0;
    end
    """

    for ix in range(0, self.fanin):
      actions +=  """
      collectStream{index}: action stream{index}:[h] ==> hashStream:[h]
      do
        counter := counter + 1;
      end
      """.format(index = ix)
    
    return actions
  
  def getFsm(self):

    fsm = """
    schedule fsm s0:
    """

    for ix in range(0, self.fanin):
      
      fsm += """
      s{index}(collectStream{index}) --> s{index};
      s{index}(stop) --> s{indexPlus};
      """.format(index = ix, indexPlus = (ix + 1) % self.fanin)
    
    fsm += """
    end
    """
    return fsm
  

  def getPriority(self):

    priority = """
    priority
    """

    for ix in range(0, self.fanin):
      
      priority += """
      stop > collectStream{index};   
      """.format(index = ix)
    
    priority += """
    end
    """
    return priority
  

  def getPorts(self):

    ports = ""

    for ix in range(0, self.fanin):
      ports += """
        uint(size = 32) stream{index}{delim}
      """.format(index = ix, delim=(", " if (ix < self.fanin - 1) else ""))
    
    return ports
  

  def getActor(self):

    actor = """

  actor HashCollector()
    {ports}
    ==>
    uint(size = 32) hashStream:

    uint(size = 32) counter := 0;
    uint HASH_STREAM_SIZE = 5;

    {actions}

    {fsm}

    {priority}
  end
  """.format(ports = self.getPorts(), 
            actions = self.getActions(), 
            fsm = self.getFsm(), 
            priority = self.getPriority())
    return actor

def getHashCollector(n):
  return HashCollector(n).getActor()


