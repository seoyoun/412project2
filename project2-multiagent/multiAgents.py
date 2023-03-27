# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"

        # find closest food
        newFoodList = newFood.asList()
        minFood = float("inf")

        for newFood in newFoodList:
            distToNewFood = manhattanDistance(newPos, newFood)
            minFood = min(minFood, distToNewFood)

        # if any ghost is too close (right next to pacman), avoid by returning smallest number
        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            distToGhost = manhattanDistance(ghostPos, newPos)
            if distToGhost <= 1:
                return -float('inf')
        
        # farther the food, smaller the score
        return successorGameState.getScore() + 1.0/minFood

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        bestAction, terminalStateValue = self.maxValue(0, gameState)

        return bestAction

    # max-value function for pacman 
    def maxValue(self, depthValue, gameState): 
        #terminal state base case
        if depthValue == self.depth or gameState.isWin() or gameState.isLose(): 
            ## check if it is a win or loss first
            return "Stop", self.evaluationFunction(gameState)

        v = -999999
        bestAction = "Stop"

        # generating legal actions for pacman
        legalActions = gameState.getLegalActions(0)
        
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(0, action)
            
            numGhosts = gameState.getNumAgents() - 1
            
            # going to the min-value layer starting with the first ghost
            actionChoice, successorStateValue = self.minValue(depthValue, numGhosts, 1, successorState)
            if successorStateValue > v:
                v = successorStateValue
                bestAction = action
        
        return bestAction, v
    
    #min-value function for the ghosts
    def minValue(self, depthValue, numGhosts, ghostValue, gameState):
        #terminal state base case
        if depthValue == self.depth or gameState.isWin() or gameState.isLose(): 
            ## check if it is a win or loss first
            return "Stop", self.evaluationFunction(gameState)

        v = 999999
        bestAction = "Stop"

        # generating legal actions for ghost
        legalActions = gameState.getLegalActions(ghostValue)

        for action in legalActions:
            successorState = gameState.generateSuccessor(ghostValue, action)

            # if not the last ghost, iterate recursively call the minvalue of the next ghost
            if ghostValue == numGhosts:
                actionChoice, successorStateValue = self.maxValue(depthValue + 1, successorState)
                if successorStateValue < v: 
                    v = successorStateValue
                    bestAction = action
            else: 
                actionChoice, successorStateValue = self.minValue(depthValue, numGhosts, ghostValue + 1, successorState)
                if successorStateValue < v: 
                    v = successorStateValue
                    bestAction = action
            
        return bestAction, v
    

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestAction, terminalStateValue = self.maxValue(0, gameState)
        
        return bestAction
    
    # max-value function for pacman 
    def maxValue(self, depthValue, gameState): 
        #terminal state base case
        if depthValue == self.depth or gameState.isWin() or gameState.isLose(): 
            ## check if it is a win or loss first
            return "Stop", self.evaluationFunction(gameState)

        v = -999999
        bestAction = "Stop"

        # generating legal actions for pacman
        legalActions = gameState.getLegalActions(0)
        
        for action in legalActions:
            successorState = gameState.generateSuccessor(0, action)
            
            numGhosts = gameState.getNumAgents() - 1
            
            # going to the min-value layer starting with the first ghost
            actionChoice, successorStateValue = self.expValue(depthValue, numGhosts, 1, successorState)
            if successorStateValue > v:
                v = successorStateValue
                bestAction = action
        
        return bestAction, v
    
    #exp-value function for the ghosts
    def expValue(self, depthValue, numGhosts, ghostValue, gameState):
        #terminal state base case
        if depthValue == self.depth or gameState.isWin() or gameState.isLose(): 
            ## check if it is a win or loss first
            return "Stop", self.evaluationFunction(gameState)

        v = 0.0
        bestAction = "Stop"

        # generating legal actions for ghost and getting the count for probability
        legalActions = gameState.getLegalActions(ghostValue)
        legalActionsCount = len(legalActions)

        for action in legalActions:
            successorState = gameState.generateSuccessor(ghostValue, action)

            # if not the last ghost, iterate recursively call the expValue of the next ghost
            # otherwise get the maxValue of pacman, saving the best pacman action
            if ghostValue == numGhosts:
                actionChoice, successorStateValue = self.maxValue(depthValue + 1, successorState)
                v += (1/legalActionsCount) * successorStateValue
                bestAction = actionChoice
            else: 
                actionChoice, successorStateValue = self.expValue(depthValue, numGhosts, ghostValue + 1, successorState)
                v += (1/legalActionsCount) * successorStateValue
            
        return bestAction, v
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This betterEvaluationFunction builds upon the evaluation function from Question 1.
    - This first accounts for the distance between the pacman position of the current state and the nearest food item
    - Then, it accounts for the largestScaredTime of the ghosts (if any), as the longer the scared time the
      ghost has, the more time the pacman has to move and to even capture the ghost
    - Last, it accounts for position of the non-scared ghosts itself, returning the smallest number possible altogether 
      if the ghost is near the pacman to avoid the move, and finding the min distance if not too close
    - To calculate the final evaluation value, the sum of the current score, the reciprocal of the minFood distance
      (the closer the food, the higher the score will be), the reciprocal of the minimum distance between pacman and ghost, 
      and the longest scared time (since it is almost like "bonus" score) are taken.

    """
    "*** YOUR CODE HERE ***"
    
    # Useful information you can extract from a GameState (pacman.py)
    currPos = currentGameState.getPacmanPosition()
    currFood = currentGameState.getFood()
    currGhostStates = currentGameState.getGhostStates()
    currScaredTimes = [ghostState.scaredTimer for ghostState in currGhostStates]

    # find closest food
    currFoodList = currFood.asList()
    minFood = float("inf")

    for currFoodItem in currFoodList:
        distToNewFood = manhattanDistance(currPos, currFoodItem)
        minFood = min(minFood, distToNewFood)


    # getting the largest scared time, as larger scared time have an opportunity to escape
    largestScaredTime = -float('inf')
    
    for ghostScaredTime in currScaredTimes:
        if ghostScaredTime > largestScaredTime:
            largestScaredTime = ghostScaredTime

        
    # if any ghost is too close (right next to pacman), avoid by returning smallest number
    minGhostDistance = float('inf')
    for ghost in currGhostStates:
        ghostPos = ghost.getPosition()
        distToGhost = manhattanDistance(ghostPos, currPos)
        if distToGhost <= 1:
            return -float('inf')
        else: 
            if distToGhost < minGhostDistance:
                minGhostDistance = distToGhost
        

    # farther the food, smaller the score
    return currentGameState.getScore() + 1.0/minFood + 1.0/minGhostDistance + largestScaredTime
    

# Abbreviation
better = betterEvaluationFunction
