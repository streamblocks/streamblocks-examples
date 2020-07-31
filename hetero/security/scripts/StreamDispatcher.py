class StreamDispatcher():



  def __init__(self, N):

    self.fanout = N
  

  def getReadSize(self, ix):

    return """
    readSize{index}: action stringStream:[b] repeat 4 ==> stream{index}:[b] repeat 4
    do
      counter := bytesToWord(b);
    end    
    """.format(index=ix)
  
  def getEmitStream(self, ix):
    return """
    emitStream{index}: action stringStream:[ch] ==> stream{index}:[ch]
    guard counter > 0
    do
      counter := counter - 1;
    end
    """.format(index = ix)
  
  def getActions(self):
    
    actions = ""
    for ix in range(0, self.fanout):
      actions += self.getReadSize(ix)
      actions += self.getEmitStream(ix)
    return actions

  def getFsm(self):
    
    fsm = """
    schedule fsm init:
      init(readSize0) --> s0;
    """

    for ix in range(0, self.fanout):

      fsm += """
      s{index} (emitStream{index}) --> s{index};
      s{index} (readSize{indexPlus}) --> s{indexPlus};
      """.format(index = ix, indexPlus = (ix + 1) % self.fanout)
    
    fsm += """
    end
    """
    return fsm

  def getPriority(self):

    priority = """
    priority
    """

    for ix in range(0, self.fanout):
      
      priority += """
      emitStream{index} > readSize{indexPlus};
      """.format(index = ix, indexPlus = (ix + 1) % self.fanout)
    
    priority ="""
    end
    """
    return priority
    
  def getPorts(self):

    ports = ""

    for ix in range(0, self.fanout):
      delim = ", " if (ix < self.fanout - 1) else ""

      ports += """
        uint(size = 8) stream{index}{delimeter}
      """.format(index=ix, delimeter=delim)
    return ports
  
  def getActor(self):


    actor = """
  actor StreamDispatcher()
    uint(size = 8) stringStream
    ==>
    {ports}:

    uint(size = 32) counter := 0;

    {actions}

    {fsm}

    {priority}
  end
    """.format(
      ports = self.getPorts(),
      actions = self.getActions(),
      fsm = self.getFsm(),
      priority = self.getPriority())
    return actor



def getStreamDispatcher(n):
  return StreamDispatcher(n).getActor()