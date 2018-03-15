# myTeam.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import random, time, util
from game import Directions
import game
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'DummyAgent', second = 'DummyAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """

  # The following line is an example only; feel free to change it.
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

##########
# Agents #
##########

class DummyAgent(CaptureAgent):
  """
  A Dummy agent to serve as an example of the necessary agent structure.
  You should look at baselineTeam.py for more details about how to
  create an agent as this is the bare minimum.
  """

  def registerInitialState(self, gameState):
    """
    This method handles the initial setup of the
    agent to populate useful fields (such as what team
    we're on).

    A distanceCalculator instance caches the maze distances
    between each pair of positions, so your agents can use:
    self.distancer.getDistance(p1, p2)

    IMPORTANT: This method may run for at most 15 seconds.
    """

    '''
    Make sure you do not delete the following line. If you would like to
    use Manhattan distances instead of maze distances in order to save
    on initialization time, please take a look at
    CaptureAgent.registerInitialState in captureAgents.py.
    '''
    CaptureAgent.registerInitialState(self, gameState)

    currentFood = self.getFood(gameState).asList()
    value = 0
    for food in currentFood:
      value += food[1]
    average = value/len(currentFood)
    self.average = average

    '''
    Your initialization code goes here, if you need any.
    '''

  ################
  # Main Methods #
  ################

  def chooseAction(self, gameState):
    """
    Picks among actions with highest Q(s,a) same one as in baseline Team.
    """
    # If the value returns smaller eval deems better
    actions = gameState.getLegalActions(self.index)
    actionList = []
    qValuesList = []
    for action in actions:
      if action is not 'Stop':
        actionList.append(action)
        currentState = self.getCurrentObservation()
        successorState = gameState.generateSuccessor(self.index, action)
        qValue = self.evaluate(currentState, successorState, action)
        qValuesList.append(qValue)
        maxValue = max(qValuesList)
        maxIndex = qValuesList.index(maxValue)
        bestAction = actionList[maxIndex]
    #print ("Best Action:", bestAction)
    opponents = self.getOpponents(gameState)
    '''
    for opponent in opponents:
      enemyPosition = successorState.getAgentState(opponent).getPosition()
      print enemyPosition
    '''
    return bestAction

  def evaluate(self, currentState, successorState, action):
    # action is the action taken to get to the successorState
    """
    Uses a gameState and an action.
    Returns value to choose action.
    """
    qVal = 0
    features = self.getFeatures(currentState, successorState, action)
    weights = self.getWeights(currentState, action)
    qVal += features['closestFood'] * weights['closestFood']
    qVal += features['closestCapsule'] * weights['closestCapsule']
    qVal += features['enemyDistance'] * weights['enemyDistance']
    qVal += features['trapped'] * weights['trapped']
    return qVal


  def getFeatures(self, currentState, successorState, action):
    """
    Places characteristics in counter data.
    Things to calculate every move.
    """
    # Modify values returned by the functions to create a meaning
    # These values get multiplied by the weights to get an evaluation
    # EX) Food is a distance closest to 1. Either find a value for it
    # or check if the action taken gets you closer to the closest food?
    features = util.Counter()
    features['closestFood'] = self.getClosestFood(currentState, successorState, self.average)
    features['closestCapsule'] = self.getClosestCapsule(currentState, successorState)
    features['enemyDistance'] = self.stayAway(currentState, successorState)
    features['trapped'] = self.calculateTrapped(successorState, currentState, action)
    return features

  def getWeights(self, gameState, action):
    """
    Returns a dict of values that deem how important a charateristic is.
    """
    # Holds a dict of weights for features. Change these to reflect importance.
    return {'closestFood': 1.0, 'closestCapsule': 1.0, 'enemyDistance': -2.0, 'trapped': -2.0}

  ####################
  # HELPER FUNCTIONS #
  ####################

  """
  List of Characters to Compute:
  1) Get closest food - closest path to other side
  2) Get Noise - approximate position of enemies
  3) Get Capusle - While invulnerable, eat as much food as can
            while always moving towards noise (chase opponent if found)
  """
  def getClosestFood(self, currentState, successorState, average):
    # CHANGE NUMBERS TO FIT INTO THE FITNESS SECTION
    totalEval = 0
    curState = currentState.getAgentState(self.index)
    currentPos = curState.getPosition()
    succState = successorState.getAgentState(self.index)
    newPos = succState.getPosition()
    currentFood = self.getFood(currentState).asList()

    tempFood = []
    for food in currentFood:
      if self.index < 2:
        if food[1] >= average:
          tempFood.append(food)
      else:
        if food[1] < average:
          tempFood.append(food)

    if len(tempFood) > 0:
      currentFood = tempFood

    # If Pacman can get food in its next state increase priority
    for food in currentFood:
      if newPos == food:
        totalEval = totalEval + 5
    # If Pacman moves towards the closest food deem action valuable
    closestFoodDist = float("inf")
    closestFood = [(0,0)]
    for food in currentFood:
      currentDist = self.getMazeDistance(currentPos, food)
      if currentDist < closestFoodDist:
        closestFoodDist = currentDist
        closestFood[0] = food
    if self.getMazeDistance(newPos, closestFood[0]) < closestFoodDist:
      totalEval = totalEval + 5
    return totalEval


    '''
    # Variables needed for computation
    foodList = self.getFood(currentState).asList()
    myState = successorState.getAgentState(self.index)
    myPos = myState.getPosition()
    closestFoodDist = float("inf")
    for food in foodList:
      if self.getMazeDistance(myPos, food) < closestFoodDist:
        closestFoodDist = self.getMazeDistance(myPos, food)
    foodFactor = 1.0 - float(closestFoodDist)/75.0
    #foodFactor = foodFactor * 1
    #print("Food:", foodFactor)
    return foodFactor
    '''

  def getClosestCapsule(self, currentState, successorState):
    # Maybe do same as food and check if moving towards?
    # Or check if move towards if ghost is visible?
    capsules = self.getCapsules(currentState)
    curr = successorState.getAgentState(self.index).getPosition()
    #if capsules is []:
      #return 0
    #print capsules

    minimum_distance = float("inf")
    for capsule in capsules:
        distance = self.getMazeDistance(curr, capsule)
        if distance < minimum_distance:
            minimum_distance = distance

    #print minimum_distance
    if not capsules:
      #print 0
      return 0

    capsuleFactor = 1 - float(minimum_distance)/100.0
    capsuleFactor = capsuleFactor * 1
    #print ("capsule:", capsuleFactor)
    return capsuleFactor

  def getApproximateEnemy(self, gameState, index):
    """#####################################
        Edited Code:
            My plan is to check whether the next move is going to be
            trapped or not. If it's trapped and noise is less than 4,
            (4 is just my estimate distance) then it will return -inf
            because you will die automatically if you go into that trapped
            area. The trapped function is at "calculateTrapped" function.
    """
    values = gameState.getAgentDistances()
    #print values
    if gameState.isOnRedTeam(self.index):
        #print values[self.index]
        return values[self.index]
    else:
        #print values[self.index-1]
        return values[self.index-1]

    #print index, values[index]
    return values[index]

  def getEnemyDistance(self, currentState, successorState, action):
    distance_away_from_enemy = self.getApproximateEnemy(successorState, self.index)
    if distance_away_from_enemy <= 6 and distance_away_from_enemy >= -6:
        return float("-inf")
    elif distance_away_from_enemy <= 9 and distance_away_from_enemy >= -3:
        if self.calculateTrapped(successorState, currentState, action):
            return float("-inf")
    return distance_away_from_enemy


  def stayAway(self, currentState, successorState):
    currentPos = currentState.getAgentState(self.index).getPosition()
    newPos = successorState.getAgentState(self.index).getPosition()
    enemyPositions = self.newEnemyDistance(currentState, successorState)
    opponents = self.getOpponents(currentState)
    if len(enemyPositions) == 0:
      return 0
    else:
      for opponent in opponents:
        if not currentState.getAgentState(opponent).isPacman:
          if currentState.getAgentState(opponent).scaredTimer > 0:
            return 0
      if currentState.getAgentState(self.index).isPacman:
        for enemy in enemyPositions:
          if self.getMazeDistance(currentPos, enemy) < 6:
            factor = 1.0 - float(self.getMazeDistance(currentPos, enemy))/75.0
            return factor
          #if abs(self.getMazeDistance(newPos, enemy) - self.getMazeDistance(currentPos, enemy)) < 3:
            #return self.getMazeDistance(newPos, enemy)
    #print("How did I get here?")
    return 0

  def newEnemyDistance(self, currentState, successorState):
    opponents = self.getOpponents(currentState)
    enemyPositions = []
    for opponent in opponents:
      enemyPosition = successorState.getAgentState(opponent).getPosition()
      if enemyPosition is not None:
        enemyPositions.append(enemyPosition)
    return enemyPositions

  def calculateTrapped(self, successorState, currentState, action):
      """
            To know whether you are going to be trapped or not,
            I said that if possible actions in successorState has
            one legal action and taking that action brings back to
            the currentState position, then you know you are trapped.
            However, this doesnt calculate if the trapped space is
            bigger, not just one spot.
      """
      trapped = self.goThroughSuccessorForTrap(successorState, action, count=5)
      if trapped == True:
        enemyPositions = self.newEnemyDistance(currentState, successorState)
        opponents = self.getOpponents(currentState)
        currentPos = currentState.getAgentState(self.index).getPosition()
        for enemy in enemyPositions:
          if self.getMazeDistance(currentPos, enemy) < 6:
            return 10
      return 0

  def goThroughSuccessorForTrap(self, successorState, prevAction, count):
      """
            prevAction is a previous action that it took to create successorState.
            This action is passed down from the chooseAction function from the
            way beginning. Count is basically how much are you willing to travel
            deep down to check whether if it's trapped or not.
      """
      if count >= 1:
          actions = successorState.getLegalActions(self.index)
          actions.remove('Stop')
          converted_action = 'Stop'
          """
                Here, if prevAction was South, that means the possible action
                in successorState must contain opposite direction of prevAction.
                I am going to remove the opposite direction, which is North from
                actions in successorState. Now, if there are no actions to take,
                it means that you're trapped. But if there is 1 legal action, it
                is the case where the trap space is a long hallway. I said count
                equal to 4, hoping that the hallway is not longer than 4.

                If there are more than 1 actions even after deleting the opposite
                direction of previous action, that means you are heading into a
                2D space, which pacman can run away from the ghost even if it takes
                the path that is surrounded by wall.

                This function still returns true or false if its trapped or not.

                Problem: when there is one trap space like below drawing, pacman
                still takes that trap space. I think it has to do with the
                noise function. Might want to fix the constraint.

                __   __
                  |_|

          """

          if prevAction == 'North':
              converted_action = 'South'
          elif prevAction == 'South':
              converted_action = 'North'
          elif prevAction == 'East':
              converted_action = 'West'
          elif prevAction == 'West':
              converted_action = 'East'

          if converted_action in actions:
              actions.remove(converted_action)
          if len(actions) == 0:
              position = successorState.getAgentState(self.index).getPosition()
              #print "trapped place found!", self.index, position
              #print "trapped found near 5 distance"
              return True
          elif len(actions) == 1:
              next_successor_state = successorState.generateSuccessor(self.index, actions[0])
              return self.goThroughSuccessorForTrap(next_successor_state, actions[0], count-1)
          else:
              return False
      else:
          return False
