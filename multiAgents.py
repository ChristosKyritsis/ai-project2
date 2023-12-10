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
import math

from game import Agent
from pacman import GameState

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState: GameState):
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

    def evaluationFunction(self, currentGameState: GameState, action):
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
        foodList = newFood.asList()
        foodDistance = []

        for item1 in foodList:
            foodDistance.append(manhattanDistance(item1, newPos))

        # case where all food has been picked-up
        if len(foodDistance) == 0:
            return math.inf
        
        if currentGameState.getPacmanPosition() == newPos:
            return (-math.inf)
        
        for item3 in successorGameState.getGhostPositions():
            if item3 == newPos:
                return (-math.inf)

        #return 1000/sum(foodDistance) +10000/len(foodDistance)
        return successorGameState.getScore() + len(newGhostStates)/len(newScaredTimes)
        #return successorGameState.getScore() original

def scoreEvaluationFunction(currentGameState: GameState):
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

    def getAction(self, gameState: GameState):
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
        # max_value is the move for Pac-Man, so the id is equal to zero
        def max_value(gameState: GameState, depth):
            # legal moves for Pac-Man
            actions = gameState.getLegalActions(0)
            move = None
            res = (None, move)
            # Terminal test
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == self.depth:
                res = (self.evaluationFunction(gameState), move)
                return res

            # v needs to be small enough in order to make sure a min value will replace it  
            v = (-math.inf)
            # res = ( -inf, None)
            res = (v, move)
            # Getting all the legal action from the list
            for action in actions:
                # [0] because we only care about the value and not the move itself
                temp = min_value(gameState.generateSuccessor(0, action), depth, 1)[0]
                # Getting the max value
                if (temp > v):
                    v = temp
                    move = action

            res = (v, move)
            return res


        # min_value represents the ghosts, so the id is >= 1
        # There is also an id parameter because there can be more than 1 ghosts
        def min_value(gameState: GameState, depth, id):
            # legal moves of Ghost
            actions = gameState.getLegalActions(id)
            move = None
            res = (None, move)
            # Terminal test
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == self.depth:
                res = (self.evaluationFunction(gameState), move)
                return res

            # v needs to be big enough in order to make sure a max value will replace it  
            v = math.inf
            res = (v, move)
            # For every legal move
            for action in actions:
                if id == gameState.getNumAgents() - 1:
                    # Pac-Man's turn
                    temp = max_value(gameState.generateSuccessor(id, action), depth + 1)[0]
                    # min value
                    if (temp < v):
                        v = temp
                        move = action
                else:
                    # Next ghost
                    temp = min_value(gameState.generateSuccessor(id, action), depth, id + 1)[0]
                    # min value
                    if (temp < v):
                        v = temp
                        move = action

            res = (v, move)
            return res
        
        # return the move not the value
        return max_value(gameState, 0)[1]

        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        # Here with the same logic as minimax we have two functions with the addition of the a, b parameters
        def max_value(gameState: GameState, depth, a, b):
            actions = gameState.getLegalActions(0)
            move = None
            res = (None, move)
            # Terminal test
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == self.depth:
                res = (self.evaluationFunction(gameState), move)
                return res
            
            v = (-math.inf)
            res = (v, move)

            for action in actions:
                temp = min_value(gameState.generateSuccessor(0, action), depth, a, b, 1)[0]
                if temp > v:
                    v = temp
                    move = action
                if v > b:
                    return (v, move)
                
                a = max(a, v)

            res = (v, move)
            return res
        


        def min_value(gameState: GameState, depth, a, b, id):
            actions = gameState.getLegalActions(id)
            move = None
            res = (None, move)
            # Terminal test
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == self.depth:
                res = (self.evaluationFunction(gameState), move)
                return res
            
            v = math.inf
            res = (v, move)

            for action in actions:
                if id == gameState.getNumAgents() - 1:
                    temp = max_value(gameState.generateSuccessor(id, action), depth + 1, a, b)[0]
                    if temp < v:
                        v = temp
                        move = action
                else:
                    temp = min_value(gameState.generateSuccessor(id, action), depth, a, b, id + 1)[0]
                    if temp < v:
                        v = temp
                        move = action

                if v < a:
                    return (v, move)
                
                b = min(b, v)

            res = (v, move)
            return res
        

        return max_value(gameState, 0, (-math.inf), math.inf)[1]

            

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def max_value(gameState: GameState, depth):
            actions = gameState.getLegalActions(0)
            move = None
            res = (None, move)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == self.depth:
                res = (self.evaluationFunction(gameState), move)
                return res
            
            v = (-math.inf)
            res = (v, move)

            for action in actions:
                temp = chance(gameState.generateSuccessor(0, action), depth, 1)[0]
                # Getting the max value
                if (temp > v):
                    v = temp
                    move = action

            res = (v, move)
            return res
        

        def chance(gameState: GameState, depth, id):
            actions = gameState.getLegalActions(id)
            move = None
            res = (None, move)
            if gameState.isWin() or gameState.isLose() or len(actions) == 0 or depth == self.depth:
                res = (self.evaluationFunction(gameState), move)
                return res

            v = 0
            res = (v, move)
            for action in actions:
                if id == gameState.getNumAgents() - 1:
                    temp = max_value(gameState.generateSuccessor(id, action), depth + 1)[0]
                    move = action
                else:
                    temp = chance(gameState.generateSuccessor(id, action), depth, id + 1)[0]
                    move = action

                chanceNode = temp/len(actions)
                v = v + chanceNode

            res = (v, move)
            return res
        
        return max_value(gameState, 0)[1]

        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Checking if Game is over
    if currentGameState.isWin():
        return math.inf
    
    if currentGameState.isLose():
        return (-math.inf)
    
    # if Game not over
    # Position of the Pac-Man
    pacPos = currentGameState.getPacmanPosition()
    # Taking in consideration the States rather than the Positions as instructed
    ghosts = currentGameState.getGhostStates()
    food = currentGameState.getFood().asList()

    # Keeping track of the distance between Pac-Man and all of the food
    foodDistance = []
    for f in food:
        foodDistance.append(manhattanDistance(f, pacPos))

    # Keepin Trsck of the distance between Pac-Man and the ghosts
    regularGhosts = []
    scaredGhosts = []
    for gh in ghosts:
        if gh.scaredTimer > 0:
            scaredGhosts.append(manhattanDistance(pacPos, gh.getGhostPosition()))
        elif gh.scaredTimer == 0:
            regularGhosts.append(manhattanDistance(pacPos, gh.getGhostPosition()))

    if len(scaredGhosts) == 0:
        sGhostEval = 2.0 * min(scaredGhosts)
    
    if len(regularGhosts) == 0:
        rGhostEval = 0.5 * min(regularGhosts)

    newScore = scoreEvaluationFunction(currentGameState) 
    newScore -= rGhostEval + sGhostEval + 5 * min(foodDistance)
    return newScore




    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
