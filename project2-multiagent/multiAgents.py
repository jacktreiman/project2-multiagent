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


from cmath import inf
from xmlrpc.client import MAXINT
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
        minFoodDist = 10000
        minPacDist = 10000
        ghostTimer = 0
        for i in newFood.asList():
            if util.manhattanDistance(i, newPos) < minFoodDist:
        
                minFoodDist = util.manhattanDistance(i, newPos)
        
        score = 0
        for i in successorGameState.getGhostPositions():
            if util.manhattanDistance(i, newPos) < minPacDist:
        
                minPacDist = util.manhattanDistance(i, newPos)
        for i in newGhostStates:
            ghostTimer += i.scaredTimer

        if minPacDist == 0:
            return -inf
        if len(newFood.asList()) == 0:
            return inf
        stopScore = 0
        if action == 'Stop':
            stopScore = -1000
        score = (1/minFoodDist) - minPacDist/10 + successorGameState.getScore() + stopScore  + ghostTimer
        
        return score

        "*** YOUR CODE HERE ***"
        #return successorGameState.getScore()

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
        
        val, act = self.value(gameState, 0, 0)
        return act

        

        #util.raiseNotDefined()
    def value(self, gameState, player, depth):
        if depth == self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #or is terminal node
            return (self.evaluationFunction(gameState), 'Stop')
        if player == 0:
            return self.maxValue(gameState, player, depth)
        else:
            return self.minValue(gameState, player, depth)


    def maxValue(self, gameState, player, depth):
        v = -inf
        for moves in gameState.getLegalActions(player):
            #print(type(self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)))
            val = self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)[0]
            if v < val:
                action = moves
            v = max(v, val)
                #store the action not just the eval function
        return (v, action)

    def minValue(self, gameState, player, depth):
        v = inf
        for moves in gameState.getLegalActions(player):
            #print(type(self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)))
            val = self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)[0]
            if v > val:
                action = moves
            v = min(v, val)
        return (v, action)


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        val, act = self.value(gameState, 0, 0, -inf, inf)
        return act


    def value(self, gameState, player, depth, alpha, beta):
        if depth == self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #or is terminal node
            return (self.evaluationFunction(gameState), 'Stop')
        if player == 0:
            return self.maxValue(gameState, player, depth, alpha, beta)
        else:
            return self.minValue(gameState, player, depth, alpha, beta)


    def maxValue(self, gameState, player, depth, alpha, beta):
        v = -inf
        for moves in gameState.getLegalActions(player):
            #print(type(self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)))
            val = self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1, alpha, beta)[0]
            if v < val:
                action = moves
            v = max(v, val)
                #store the action not just the eval function
            alpha = max(v,alpha)
            if(alpha>beta):
                return (v,action)
        return (v, action)

    def minValue(self, gameState, player, depth, alpha, beta):
        v = inf
        for moves in gameState.getLegalActions(player):
            #print(type(self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)))
            val = self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1, alpha, beta)[0]
            if v > val:
                action = moves
            v = min(v, val)
            beta = min(v,beta)
            if(alpha>beta):
                return (v,action)
        return (v, action)


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
        val, act = self.value(gameState, 0, 0)
        return act

        

        #util.raiseNotDefined()
    def value(self, gameState, player, depth):
        if depth == self.depth*gameState.getNumAgents() or gameState.isWin() or gameState.isLose(): #or is terminal node
            return (self.evaluationFunction(gameState), 'Stop')
        if player == 0:
            return self.maxValue(gameState, player, depth)
        else:
            return self.exp_Value(gameState, player, depth)


    def maxValue(self, gameState, player, depth):
        v = -inf
        action = 'Stop'
        for moves in gameState.getLegalActions(player):
            #print(type(self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)))
            val = self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)[0]
            if v < val:
                action = moves
            v = max(v, val)
                #store the action not just the eval function
        return (v, action)

    def exp_Value(self, gameState, player, depth):
        v = 0
        length = len(gameState.getLegalActions(player))
        for moves in gameState.getLegalActions(player):
            #print(type(self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)))
            v += (1/length)*self.value(gameState.generateSuccessor(player, moves), (player+1)%gameState.getNumAgents(), depth+1)[0]
        return (v, "Stop")

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    
    What we did for our better evaluation function is create a linear combination of 
    the min food distance, the min ghost distance, current score, and ghost timer. For the min 
    food distance, we used 1/minFood, because closer food would be better, while for ghost we did
    -1/minghostdist, because closer ghosts should be higher negative. Lastly, we added to the score
    the total number of seconds the scaredghosts had left. 
    """


    "*** YOUR CODE HERE ***"
    #successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    minFoodDist = 10000
    minPacDist = 10000
    ghostTimer = 0
    for i in newFood.asList():
        if util.manhattanDistance(i, newPos) < minFoodDist:
        
            minFoodDist = util.manhattanDistance(i, newPos)
        
    score = 0
    for i in currentGameState.getGhostPositions():
        if util.manhattanDistance(i, newPos) < minPacDist:
        
            minPacDist = util.manhattanDistance(i, newPos)
    for i in newGhostStates:
        ghostTimer += i.scaredTimer

    if minPacDist == 0:
        return -inf
    if len(newFood.asList()) == 0:
        return inf
    score = (1/minFoodDist) - 1/(minPacDist) + currentGameState.getScore()  + ghostTimer
    
    return score
    #return 0
    

# Abbreviation
better = betterEvaluationFunction
