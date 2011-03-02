from captureAgents import CaptureAgent
from random import choice
from util import Counter
from game import Actions
from baselineAgents import DefensiveReflexAgent

class InferenceAgent(DefensiveReflexAgent):

  def __init__(self, index, inferenceModule, timeForComputing = .1 ):
    CaptureAgent.__init__(self, index)
    self.inferenceModule = inferenceModule

  def chooseAction(self, gameState):
    # we're blue for now
    if self.red: return choice(gameState.getLegalActions(self.index))

    enemyIndices = []
    if self.red:
      enemyIndices = gameState.getBlueTeamIndices()
    else:
      enemyIndices = gameState.getRedTeamIndices()

    if self.inferenceModule.distributions == None:
      self.inferenceModule.initializeDistributions(gameState, enemyIndices)

    for agentIndex in enemyIndices:
      self.inferenceModule.observe(gameState, self.index, agentIndex)
      self.inferenceModule.elapseTime(gameState, agentIndex)

    # this is just to get the distribution in a format that is displayable
    distrToDisplay = []
    for i in xrange(gameState.getNumAgents()):
      if i in self.inferenceModule.distributions.keys():
        distrToDisplay.append(self.inferenceModule.distributions[i])
      else:
        distrToDisplay.append(None)
    self.displayDistributionsOverPositions(distrToDisplay)

    return DefensiveReflexAgent.chooseAction(self, gameState)



