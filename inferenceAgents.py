from inferenceAgent import InferenceAgent
from inference import InferenceModule
from baselineAgents import DefensiveReflexAgent
from captureAgents import AgentFactory

class InferenceAgents(AgentFactory):

  def __init__(self, **args):
    AgentFactory.__init__(self, **args)
    self.inferenceModule = InferenceModule()

  def getAgent(self, index):
    if index % 2 == 0: # red
      return DefensiveReflexAgent(index)
    else:
      return InferenceAgent(index, self.inferenceModule)

