from util import Counter
from distanceCalculator import Distancer
from game import Actions

class InferenceModule():
  def __init__(self):
    self.distributions = None

  def initializeDistributions(self, gameState, enemyIndices):
    self.distributions = {}
    for enemyIndex in enemyIndices:
      uniformBeliefs = Counter()
      for x in xrange(gameState.data.layout.width):
        for y in xrange(gameState.data.layout.height):
          if not gameState.hasWall(x, y):
            position = (x, y)
            uniformBeliefs[position] = 1.0
      uniformBeliefs.normalize()
      self.distributions[enemyIndex] = uniformBeliefs

  # used if we know exactly where the agent is
  def useExactDistribution(self, gameState, agentIndex, agentPosition):
    exactDistribution = Counter()
    for x in xrange(gameState.data.layout.width):
      for y in xrange(gameState.data.layout.height):
        if not gameState.hasWall(x, y):
          position = (x, y)
          if (position == agentPosition):
            exactDistribution[position] = 1.0
          else:
            exactDistribution[position] = 0.0
    exactDistribution.normalize()
    self.distributions[agentIndex] = exactDistribution

  def observe(self, gameState, selfIndex, agentIndex):
    noisyAgentDistance = gameState.getAgentDistances()[agentIndex]
    
    distribution = Counter()
    pacmanPosition = gameState.getAgentState(selfIndex).getPosition()
    distancer = Distancer(gameState.data.layout)
    for x in xrange(gameState.data.layout.width):
      for y in xrange(gameState.data.layout.height):
        if not gameState.hasWall(x, y):
          position = (x, y)
          trueDistance = distancer.getDistance(position, pacmanPosition)
          distribution[position] = gameState.getDistanceProb(trueDistance, noisyAgentDistance) * self.distributions[agentIndex][position]
    distribution.normalize()
    self.distributions[agentIndex] = distribution

  def elapseTime(self, gameState, agentIndex):
    distribution = Counter()
    for x in xrange(gameState.data.layout.width):
      for y in xrange(gameState.data.layout.height):
        if not gameState.hasWall(x, y):
          position = (x, y)
          newPositionDistribution = self.getPositionDistribution(gameState, position)
          for newPosition, probability in newPositionDistribution.items():
            distribution[newPosition] += probability * self.distributions[agentIndex][position]
    distribution.normalize()
    self.distributions[agentIndex] = distribution
  
  def getPositionDistribution(self, gameState, ghostPosition):
    legalPositions = Actions.getLegalNeighbors(ghostPosition, gameState.getWalls())

    # assume equal probablity of choosing any of the legal actions for now
    randomProb = 1.0 / len(legalPositions)
    
    positionDistribution = Counter()
    for legalPosition in legalPositions:
      positionDistribution[legalPosition] = randomProb 

    return positionDistribution

