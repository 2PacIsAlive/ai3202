#Jared Jolton
#CSCI-3202
#Intro to AI
#Assignment 3

import sys
import math

#information about each space in the world is stored in an instance of this class
#class members are accessed within a 2D array, so that their location in the world can easily be paired with their index in the array
class SPACE():
    def __init__(self, value, x, y):
        self.value = value #empty space, mountain, or wall
        self.x = x #row
        self.y = y #column
        self.heuristic = None #eventually stores the total cost of a move to this node
        self.f = None #represents the simple cost to move from one space to the next
        self.parent = None #used to retrace the path
        self.end = False #true for the goal of the search
        self.visited = False
    #this function is used to create a visualization of the obstacles in the world and the path that A* finds
    def createDisplay(self):
        if self.value == '0': #space is empty
            display[self.x][self.y] = ' '
        elif self.value == '1': #space is a mountain
            display[self.x][self.y] = '^'
        else: #space is a wall
            display[self.x][self.y] = '|'
        if self.visited == True: #used to trace the chosen path
            display[self.x][self.y] = '*'
        if self.end == True: #goal space
            display[self.x][self.y] = '$'

#this function returns a list of all nodes adjacent to the node at a particular x,y location
#it uses exception handling to make sure items outside of the world array are not added to the list
#it also checks for explicit cases when it might be indexing in a negative direction
    #because rather than throwing an IndexError, python uses this method to access items in an array backwards
def Adjacent(line, column):
    #TOP LEFT
    try:
        topLeft = world3DArray[line-1][column-1]
    except IndexError:
        topLeft = None
    if line-1 < 0:
        topLeft = None
    if column-1 < 0:
        topLeft = None
    #TOP CENTER
    try:
        topCenter = world3DArray[line-1][column]
    except IndexError:
        topCenter = None
    if line-1 < 0:
        topCenter = None
    #TOP RIGHT
    try:
        topRight = world3DArray[line-1][column+1]
    except IndexError:
        topRight = None
    if line-1 < 0:
        topRight = None
    #MID LEFT
    try:
        midLeft = world3DArray[line][column-1]
    except IndexError:
        midLeft = None
    if column-1 < 0:
        midLeft = None

    #MID RIGHT
    try:
        midRight = world3DArray[line][column+1]
    except IndexError:
        midRight = None
    #BOTTOM LEFT
    try:
        bottomLeft = world3DArray[line+1][column-1]
    except IndexError:
        bottomLeft = None
    if column-1 < 0:
        bottomLeft = None

    #BOTTOM CENTER
    try:
        bottomCenter = world3DArray[line+1][column]
    except IndexError:
        bottomCenter = None
    #BOTTOM RIGHT
    try:
        bottomRight = world3DArray[line+1][column+1]
    except IndexError:
        bottomRight = None
    #all neighbors are added to the list, even if they do not exist
    adjacencyList = [topLeft,topCenter,topRight,midLeft,midRight,bottomLeft,bottomCenter,bottomRight]
    return adjacencyList

#this function calculates and sets the cost of a node, using the index to the adjacencyList
#because the adjacent nodes are always added to this list in the same order,
    #the index can be used to determine where they are in relation to the node that is searching for the next space
def setCost(node,index):
    #TOP LEFT, TOP RIGHT, BOTTOM LEFT, BOTTOM RIGHT
    if index == 0 or index == 2 or index == 5 or index == 7:
        if node.value == '0':
            node.f = 14 #diagonal empty space
        else:
            node.f = 24 #diagonal mountain space
    #TOP CENTER, MID LEFT, MID RIGHT, BOTTOM CENTER
    if index == 1 or index == 3 or index == 4 or index == 6:
        if node.value == '0':
            node.f = 10 #horizontal/vertical empty space
        else:
            node.f = 20 #horizontal/vertical mountain space

#this function returns the node in the list that has the minimum cost
def minCost(list):
    #set the minimum to the maximum system value
    min = sys.maxint
    for item in list:
        if item.f < min:
            #if any node's cost is less than the current minimum value, update it
            min = item.f
    #return the node with the lowest cost
    for item in list:
        if item.f == min:
            return item

#this function calculates the estimated distance to the goal in 4 different ways
#it can use several different heuristics depending on the second command line input
#for each heuristic, the x and y distances are calculated in such a way that the end goal can be anywhere
    #(above, below, and to the left or right of the node being calculated)
def estimatedDistanceToGoal(node, heuristicType):
    if heuristicType == 1:
        #manhattan distance
        if node.x < end.x:
            xdist = (end.x - node.x)*10
        else:
            xdist = (node.x - end.x)*10
        if node.y < end.y:
            ydist = (end.y - node.y)*10
        else:
            ydist = (node.y - end.y)*10
        #for manhattan distance, simply add the vertical and horizontal distances
        manhattanDist = xdist + ydist
        return manhattanDist
    elif heuristicType == 2:
        #approximate diagonal distance
        if node.x < end.x:
            xdist = (end.x - node.x)*10
        else:
            xdist = (node.x - end.x)*10
        if node.y < end.y:
            ydist = (end.y - node.y)*10
        else:
            ydist = (node.y - end.y)*10
        #this heuristic intends to get a more accurate estimation by calculating the straight line distance to the goal with the pythagorean theorem
        straightLineDist = math.sqrt((math.pow(xdist,2)+(math.pow(ydist,2))))
        return straightLineDist
    elif heuristicType == 3:
        #diagonal shortcut heuristic
        if node.x < end.x:
            xdist = (end.x - node.x)
        else:
            xdist = (node.x - end.x)
        if node.y < end.y:
            ydist = (end.y - node.y)
        else:
            ydist = (node.y - end.y)
        #this algorithm is adapted from a method mentioned in "A* Pathfinding for Beginners" by Patrick Lester
        #the original can be found at http://www.policyalmanac.org/games/heuristics.htm
        if xdist > ydist:
            diagonalShortcut = 14*ydist + 10*(xdist - ydist)
        else:
            diagonalShortcut = 14*xdist + 10*(ydist - xdist)
        return diagonalShortcut
    else:
        #chebyshev distance
        #compute distance if unable go diagonal
        #subtract the steps saved by going diagonal
        if node.x < end.x:
            xdist = (end.x - node.x)*10
        else:
            xdist = (node.x - end.x)*10
        if node.y < end.y:
            ydist = (end.y - node.y)*10
        else:
            ydist = (node.y - end.y)*10
        #this algorithm is adapted from a method mentioned in "Amit's Thoughts on Pathfinding"
        #the original can be found at http://theory.stanford.edu/~amitp/GameProgramming/Heuristics.html
        distList = [xdist,ydist]
        chebyshevDistance = (xdist + ydist) + (-1 * min(distList))
        return chebyshevDistance

#this function adds the distance to node and the heuristic
def F(node, heuristicType):
    totalCost = node.f + estimatedDistanceToGoal(node, heuristicType)
    return totalCost

#this function recursively collects the locations of all nodes in the path
    #by traversing the path backwards from child to parent
    #and adding each node to a global list
def tracePath(node):
    if node.x == start.x and node.y == start.y:
        printPath.append(node)
        return
    else:
            printPath.append(node)
            tracePath(node.parent)

#each time AStar is called,
    #it searches through the neighboring nodes
    #calculates the total cost of a move to each node (including the direct cost and the estimated distance to the goal)
    #recursively calls AStar with the node that has the lowest total cost
#returns once the neighbor that happens to be the end of the search is evaluated
def AStar(node,counter, totalCost, hType):
    counter = counter + 1 #used for keeping track of the number of moves/items in the path
    node.visited = True
    Display(counter) #the display function provides a convenient visualization of the world and the path as it is built
    index = 0 #index needs to be reset to 0 because it is used to access items in the list of adjacent nodes
    costList = [] #holds the possible moves and their associated costs for each search
    lowestCost = None
    for item in Adjacent(node.x,node.y):
        if item != None: #some of the items in the adjacencyList get set to None if they do not exist
            #if the node is not the goal...
            if item.end != True:
                #if the node is not a wall...
                if item.value != '2':
                    setCost(item, index) #determines the direct cost of the move, without adding the heuristic
                    item.heuristic = F(item, hType) #this line of code sets the estimated distance to goal, adds it to the direct cost, and puts the totalCost into item.heuristic
                    costList.append(item.heuristic)
                    if min(costList) == item.heuristic: #if the totalCost is lower than any of the other costs, assign the node as the node to be moved to
                        lowestCost = item
            else:
                #if the node is the goal...
                print 'AStar found a solution!'
                print 'World:', file
                if heuristicType == 1:
                    print 'Heuristic: Manhattan Distance'
                elif heuristicType == 2:
                    print 'Heuristic: Approximate Diagonal Distance'
                elif heuristicType == 3:
                    print 'Heuristic: Diagonal Shortcut'
                else:
                    print 'Heuristic: Chebyshev Distance'
                print 'Number of locations in solution path:', counter
                #assigning the goal node's parent to the current node ensures the path can be traced
                item.parent = node
                setCost(item, index)
                item.heuristic = F(item, hType)
                totalCost = totalCost + item.f #add this final step to the total cost of the path
                print 'Total cost:', totalCost
                tracePath(item) #collects the path from start to end using child/parent connections
                return
        index = index + 1
    lowestCost.visited = True
    lowestCost.parent = node
    totalCost = totalCost + lowestCost.f
    AStar(lowestCost,counter,totalCost, hType)

#this function used to visualize the world and the path
def Display(step):
    print '_______',step,'________'
    for x in range(8):
        for y in range(10):
            world3DArray[x][y].createDisplay()
    for x in range(8):
        print ' '.join(display[x])

#main
file = sys.argv[1] #1st command line arg is the filename
heuristicType = int(sys.argv[2]) #second command line arg is the heuristic type
printPath = [] #initial empty global path list
world3DArray = [] #all nodes are stored in this array
worldFile = open(file, 'r')
lineCount = 0
#loop through the world file and create SPACEs for each
#line count is x
#node count is y
for line in worldFile:
    if lineCount < 8: #this condition needed to ensure an extra line is not created, and should be removed if bigger or smaller worlds are used
        world3DArray.append([])
        nodeCount = 0
        for char in line:
            if char != '\n' and char != ' ':
                #instantiate the SPACE
                #add the value, row number, and column number of the node to the list of attributes...
                space = SPACE(char, lineCount, nodeCount)
                world3DArray[lineCount].append(space)
                nodeCount = nodeCount + 1
        lineCount = lineCount + 1
worldFile.close()
#start and end are the same for each world
#this should be changed to allow for different starts and ends
start = world3DArray[7][0]
end = world3DArray[0][9]
end.end = True #signifies that the end is the end
display = [[0 for x in range(10)] for x in range(8)] #initialize display
print 'Initial Map:'
Display(0)
print 'Running mySearch...'
#call A* with the start node, counter and totalCost set to 0, and the heuristic type taken from the command line
AStar(start,0,0, heuristicType)
print 'Printing locations in path from start to finish...'
#global list printPath is set in the tracePath function
while printPath != []:
    node = printPath.pop()
    print 'x:', node.x, ' y:', node.y








