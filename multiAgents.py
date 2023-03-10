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

        food = newFood.asList()
        foodDistances = []
        ghostDistances = []
        count = 0

        for item in food:
            foodDistances.append(manhattanDistance(newPos,item))

        for i in foodDistances:
            if i <= 4:
                count += 1
            elif i > 4 and i <= 15:
                count += 0.2
            else:
                count += 0.15

        for ghost in successorGameState.getGhostPositions():
            ghostDistances.append(manhattanDistance(ghost,newPos))

        for ghost in successorGameState.getGhostPositions():
            if ghost == newPos:
                count = 2 - count

            elif manhattanDistance(ghost,newPos) <= 3.5:
                count = 1 - count

        return successorGameState.getScore()

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
        """
            miniMax: receives state, agent(0,1,2...) and current depth
            miniMax: returns a list: [cost,action]
            Example with depth: 3
            That means pacman played 3 times and all ghosts played 3 times
        """

        def miniMax(gameState,agent,depth):
            result = []
            previousValue = 0
            if (not gameState.getLegalActions(agent)) or (depth == self.depth):
                return self.evaluationFunction(gameState),0

            if agent == gameState.getNumAgents() - 1:
                depth += 1
                nextAgent = self.index

            else:
                nextAgent = agent + 1

            for action in gameState.getLegalActions(agent):

                if not result:
                    nextValue = miniMax(gameState.generateSuccessor(agent,action),nextAgent,depth)

                    result.append(nextValue[0])
                    result.append(action)
                else:
                    previousValue = result[0]
                    nextValue = miniMax(gameState.generateSuccessor(agent,action),nextAgent,depth)

                if (nextValue[0] > previousValue and agent == self.index) or (nextValue[0] < previousValue and agent != self.index):
                    result[0] = nextValue[0]
                    result[1] = action

            return result

        return miniMax(gameState,self.index,0)[1]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        def AB(gameState,agent,depth,a,b):
            result = []

            if not gameState.getLegalActions(agent) or depth == self.depth:
                return self.evaluationFunction(gameState),0

            if agent == gameState.getNumAgents() - 1:
                depth += 1

            if agent == gameState.getNumAgents() - 1:
                nextAgent = self.index

            else:
                nextAgent = agent + 1

            for action in gameState.getLegalActions(agent):
                if not result:
                    nextValue = AB(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)

                    result.append(nextValue[0])
                    result.append(action)

                    if agent == self.index:
                        a = max(result[0],a)
                    else:
                        b = min(result[0],b)
                else:
                    if result[0] > b and agent == self.index:
                        return result

                    if result[0] < a and agent != self.index:
                        return result

                    previousValue = result[0] 
                    nextValue = AB(gameState.generateSuccessor(agent,action),nextAgent,depth,a,b)

                    if agent == self.index:
                        if nextValue[0] > previousValue:
                            result[0] = nextValue[0]
                            result[1] = action
                            a = max(result[0],a)

                    else:
                        if nextValue[0] < previousValue:
                            result[0] = nextValue[0]
                            result[1] = action
                            # b may change #
                            b = min(result[0],b)
            return result

        return AB(gameState,self.index,0,-float("inf"),float("inf"))[1]

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
        def ExpecAgent(gameState,agent,depth):
            result = []

            if not gameState.getLegalActions(agent) or depth == self.depth:
                return self.evaluationFunction(gameState),0

            if agent == gameState.getNumAgents() - 1:
                depth += 1

            if agent == gameState.getNumAgents() - 1:
                nextAgent = self.index

            else:
                nextAgent = agent + 1

            for action in gameState.getLegalActions(agent):
                if not result:
                    nextValue = ExpecAgent(gameState.generateSuccessor(agent,action),nextAgent,depth)
                    if(agent != self.index):
                        result.append((1.0 / len(gameState.getLegalActions(agent))) * nextValue[0])
                        result.append(action)
                    else:
                        result.append(nextValue[0])
                        result.append(action)
                else:

                    previousValue = result[0] 
                    nextValue = ExpecAgent(gameState.generateSuccessor(agent,action),nextAgent,depth)

                    if agent == self.index:
                        if nextValue[0] > previousValue:
                            result[0] = nextValue[0]
                            result[1] = action

                    else:
                        result[0] = result[0] + (1.0 / len(gameState.getLegalActions(agent))) * nextValue[0]
                        result[1] = action
            return result

        return ExpecAgent(gameState,self.index,0)[1]                


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    food = currentGameState.getFood().asList()
    ghosts = currentGameState.getGhostStates()
    pacPos = currentGameState.getPacmanPosition()
    chasingGhosts = [] 
    blueGhosts = [] 
    totalNumCapsules = len(currentGameState.getCapsules())
    totalNumFood = len(food) 
    score = 0 

    for ghost in ghosts:
        if ghost.scaredTimer:
            blueGhosts.append(ghost)
        else:
            chasingGhosts.append(ghost)
    #begin with the current score. double it, as it indicates the general value as decided by the game itself
    score = 2 * currentGameState.getScore()

    #subtract the amount of food left and the amount of capsules left
    score -= 5 * totalNumFood + 10 * totalNumCapsules

    #depending on how close point getting objectives are and the ghost, alter the score
    foodDist = []
    chasingGhostsDist = []
    blueGhostsDist = []


    for item in food:
        foodDist.append(manhattanDistance(pacPos,item))

    for item in chasingGhosts:
        chasingGhostsDist.append(manhattanDistance(pacPos, item.getPosition()))

    for item in blueGhosts:
        blueGhostsDist.append(manhattanDistance(pacPos,item.getPosition()))

    #we want food to also be quite far, as it gives the least amount of points
    for item in foodDist:
        if item < 3:
            score -= item
        if item < 7:
            score -= 0.5 * item
        else:
            score -= 0.2 * item

    #we want blue ghosts as close as possible
    for item in blueGhostsDist:
        if item < 3:
            score -= 20 * item
        else:
            score -= 10 * item

    #we want chasing ghosts to  be as far as possible
    for item in chasingGhostsDist:
        if item < 3:
            score += 3 * item
        elif item < 7:
            score += 2 * item
        else:
            score += 0.5 * item
    
    return score
# Abbreviation
better = betterEvaluationFunction
