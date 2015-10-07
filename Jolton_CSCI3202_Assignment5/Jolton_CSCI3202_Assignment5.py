

import sys
import math

#information about each space in the world is stored in an instance of this class
#class members are accessed within a 2D array, so that their location in the world can easily be paired with their index in the array
class SPACE():
    def __init__(self, value, x, y):
        self.value = value #empty space, mountain, or wall
        self.x = x #row
        self.y = y #column
        self.visited = False
        self.utility = 0.0
        self.nextUtility = 0.0
        self.reward = 0.0
        #these directional booleans are used by the transition function to determine where adjacent states are located
        self.isUp = False
        self.isDown = False
        self.isLeft = False
        self.isRight = False

    #this function is used to create a visualization of the obstacles in the world and the path that value iteration finds
    def createDisplay(self):
        if self.value == '0': #space is empty
            display[self.x][self.y] = ' '
        elif self.value == '1': #space is a mountain
            display[self.x][self.y] = '^'
        elif self.value == '2': #space is a wall
            display[self.x][self.y] = '|'
        elif self.value == '3': #space is a snake
            display[self.x][self.y] = '~'
        elif self.value == '4': #space is a barn
            display[self.x][self.y] = 'B'
        else: #goal space
            display[self.x][self.y] = '$'
        if self.visited == True: #used to trace the chosen path
            display[self.x][self.y] = '*'

    #this function can be used to create a display of the utility values for each state in the world
    def setRewardDisplay(self):
        rewardDisp[self.x][self.y] = str(self.nextUtility).zfill(9)

    #calculate innate rewards
    def getReward(self):
        if self.value == '0': #empty space
            self.reward = self.reward
        elif self.value == '1': #mountain
            self.reward = self.reward - 1
        elif self.value == '2': #wall
            self.reward = 0
        elif self.value == '3': #snake
            self.reward = self.reward - 2
        elif self.value == '4': #barn
            self.reward = self.reward + 1
        else: #goal
            self.reward = 50

#this function returns a list of all nodes adjacent to the node at a particular x,y location
#it uses exception handling to make sure items outside of the world array are not added to the list
#it also checks for explicit cases when it might be indexing in a negative direction
    #because rather than throwing an IndexError, python uses this method to access items in an array backwards
def Adjacent(line, column):
    #TOP CENTER
    try:
        topCenter = world3DArray[line-1][column]
        topCenter.isUp = True
    except IndexError:
        topCenter = None
    if line-1 < 0:
        topCenter = None
    #MID LEFT
    try:
        midLeft = world3DArray[line][column-1]
        midLeft.isLeft = True
    except IndexError:
        midLeft = None
    if column-1 < 0:
        midLeft = None
    #MID RIGHT
    try:
        midRight = world3DArray[line][column+1]
        midRight.isRight = True
    except IndexError:
        midRight = None
    #BOTTOM CENTER
    try:
        bottomCenter = world3DArray[line+1][column]
        bottomCenter.isDown = True
    except IndexError:
        bottomCenter = None
    #all neighbors are added to the list, even if they do not exist
    adjacencyList = [topCenter,midLeft,midRight,bottomCenter]
    return adjacencyList

#this function used to visualize the world and the path
def Display(step):
    print '_______',step,'________'
    for x in range(8):
        for y in range(10):
            world3DArray[x][y].createDisplay()
    for x in range(8):
        print ' '.join(display[x])
    print '###################'
    print

#this function can be used to display the utilities of all states
def rewardDisplay():
    print '________________'
    for x in range(8):
        for y in range(10):
            world3DArray[x][y].setRewardDisplay()
    for x in range(8):
        print ' '.join(rewardDisp[x])

#it is necessary to reset the directional values when calling the Adjacent() function
    #so that the transition function does not mistakenly compute states that were previously assigned a particular direction
def resetAdjacents():
    for list in world3DArray:
        for state in list:
            state.isUp = False
            state.isDown = False
            state.isLeft = False
            state.isRight = False

#the transition function computes the utility of each possible move, using probabilistic reasoning
#it returns a list of all possible utilities
def transition(state):
    resetAdjacents()
    possibleMoves = Adjacent(state.x,state.y)
    upReward = 0.0
    downReward = 0.0
    leftReward = 0.0
    rightReward = 0.0
    for move in possibleMoves:
        if move != None:
            if move.isUp:
                upReward = move.utility
            elif move.isDown:
                downReward = move.utility
            elif move.isLeft:
                leftReward = move.utility
            elif move.isRight:
                rightReward = move.utility
    #there is an 80% chance the agent will go the direction it intends
    #and 10% chances it will accidentally go left or right of its intended direction
    upReward = (.8 * upReward) + (.1 * rightReward) + (.1 * leftReward)
    downReward = (.8 * downReward) + (.1 * rightReward) + (.1 * leftReward)
    rightReward = (.8 * rightReward) + (.1 * upReward) + (.1 * downReward)
    leftReward = (.8 * leftReward) + (.1 * upReward) + (.1 * downReward)
    rewardList = [upReward,downReward,rightReward,leftReward]
    return rewardList

#this function implements the Bellman equation to compute the next utility of a state
def calculateUtility(state, rewardList):
    state.nextUtility = state.reward + (gamma * max(rewardList))

#value iteration loops through all states and updates their utilities using the Bellman equation (implemented with functions transition() and calculateUtility())
def ValueIteration():
    convergenceCounter = 0 #counter used to determine how many complete iterations were required
    convergence = False #controls termination of the main loop
    while convergence == False: #run the algorithm until it converges...
        #loop through all states and progress their utilities...
        #this can be considered as moving to the next time step
        for list in world3DArray:
            for state in list:
                state.utility = state.nextUtility
        #delta must be initialized each time the main loop runs
        delta = 0
        for list in world3DArray:
            for state in list:
                rewardList = transition(state) #return list of utilities 
                calculateUtility(state,rewardList)
                #uncomment the line below to watch the algorithm progress through the world, updating the utility of each state
                #rewardDisplay()
                if abs(state.nextUtility-state.utility) > delta:
                    delta = abs(state.nextUtility-state.utility)
        convergenceCounter += 1
        #rewardDisplay()
        if delta < epsilon*((1-gamma)/gamma):
            print 'Success! Number of MDP iterations to convergence:', convergenceCounter
            #rewardDisplay()
            convergence = True
        #print 'delta:', delta

def performActions(state,step):
    state.utility = state.nextUtility
    print 'Utility of state:', state.utility
    state.visited = True
    possibleMoves = Adjacent(state.x,state.y)
    max = -sys.maxint
    for move in possibleMoves:
        if move != None:
            if move.value != '2':
                if move.visited == False:
                    move.utility = move.nextUtility
                    if move.utility > max:
                        max = move.utility
    for move in possibleMoves:
        if move != None:
            if move.value != '2':
                if move.utility == max:
                    action = move
    action.visited = True
    Display(step)
    step += 1
    if action != end:
        performActions(action,step)

#main
file = sys.argv[1] #1st command line arg is the filename
epsilon = float(sys.argv[2])
delta = 0.0
gamma = 0.9
world3DArray = [] #all nodes are stored in this array
worldFile = open(file, 'r')
lineCount = 0
#loop through the world file and create SPACEs for each
#line count is x
#node count is y
for line in worldFile:
    goal = False
    if lineCount < 8: #this condition needed to ensure an extra line is not created, and should be removed if bigger or smaller worlds are used
        world3DArray.append([])
        nodeCount = 0
        for char in line:
            if char != '\n' and char != ' ':
                if goal == False:
                    #instantiate the SPACE
                    #add the value, row number, and column number of the node to the list of attributes...
                    space = SPACE(char, lineCount, nodeCount)
                    world3DArray[lineCount].append(space)
                    nodeCount = nodeCount + 1
                    if char == '5':
                        goal = True
        lineCount = lineCount + 1
worldFile.close()
#start and end are the same for each world
#this should be changed to allow for different starts and ends
start = world3DArray[7][0]
end = world3DArray[0][9]
display = [[0 for x in range(10)] for x in range(8)] #initialize display
print 'Initial Map:'
Display(0)
rewardDisp = [[0 for x in range(10)] for x in range(8)] #initialize reward display
#initialize rewards for all states
for line in world3DArray:
    for state in line:
        state.getReward()
print 'Running value iteration...'
print
ValueIteration()
print 'Printing the path acquired and the utility of each move...'
print
performActions(start,0)