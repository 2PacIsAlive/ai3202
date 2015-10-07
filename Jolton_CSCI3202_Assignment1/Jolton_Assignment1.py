
#Jared Jolton // 101910583
#CSCI-3202
#Introduction to Artificial Intelligence
#Assignment 1
 
import Queue
import random

#QUEUE
##############################################
#FIFO, oldest members dequeued first
class QUEUE():
    def __init__(self):
        self.queue = Queue.Queue()
    def addNum(self):
        self.size = 10   
        print ('creating queue from random list...')
        #loop through the list of random numbers and put them on the queue
        for item in queueList:
            self.queue.put(item)
        print ('dequeueing...')
        while not self.queue.empty():
            #the get() method is used to retrieve the oldest entries first
            print self.queue.get()  
    
#STACK
##############################################
#LIFO, newest members popped off first
class STACK():
    def __init__(self):
        #stack implemented with a python list
        self.items = []
    def push(self, integer):
        #add the item to the list
        self.items.append(integer)
    def pop(self):
        #the pop() method is used to return the most recently pushed item
        return self.items.pop()
    def checkSize(self):
        return len(self.items)
    def isEmpty(self):
        #only return true if the list is empty
        return self.items == []

#BINARY TREE
##############################################
class treeNode():
    def __init__(self, value):
        #each node is created with these default values
        self.integerKey = value
        self.left = None
        self.right = None
        self.parent = None

class BINARY_TREE():
    def __init__(self, rootValue):
        #root node automatically instantiated
        self.root = treeNode(rootValue)
        #nodes stored in a list
        self.nodeList = []
        self.nodeList.append(self.root)
    def addNode(self, value, parentValue):
        success = False
        for node in self.nodeList:
            #only continue searching if the node has not already been added
            if success == False:
                #if the parent value is found in the tree
                if node.integerKey == parentValue:
                    #if the node does not have a left child, create the new node as the left child
                    if node.left == None:
                        #set the current node's left child to the new node
                        node.left = treeNode(value)
                        #set the new node's parent to the parent value passed into the function
                        node.left.parent = parentValue
                        #add the node to the node list
                        self.nodeList.append(node.left)
                        success = True
                    #if the node has a left child but not a right child, create the new node as the left child
                    elif node.right == None:
                        #set the current node's right child to the new node
                        node.right = treeNode(value)
                        #set the new node's parent to the parent value passed into the function
                        node.right.parent = parentValue
                        #add the node to the node list
                        self.nodeList.append(node.right)
                        success = True
                    else:
                        print 'Parent has two children, node not added.'
                        success = True
        if success == False:
            print 'Parent not found, node not added.'

    def deleteNode(self, value):
        success = False
        children = False
        #create copy of the list for iterating while removing an item
        for node in self.nodeList[:]:
            #does node exist?
            if node.integerKey == value:
                #does node have children?
                if node.left is None and node.right is None:
                    #looping through all nodes, removing the value if stored as a child
                    for item in self.nodeList:
                        #only assign values for deletion if the nodes exist
                        if item.left is not None:
                            #reset the child if its integerKey is the value being deleted
                            if item.left.integerKey == value:
                                item.left.integerKey = None
                        if item.right is not None:
                            if item.right.integerKey == value:
                                item.right.integerKey = None
                    #deleting node by removing it from the list
                    self.nodeList.remove(node)
                    success = True
                else:
                    print 'Node has children, not deleted.'
                    #booleans used to control error messages
                    success = False
                    children = True
        if success == True:
            print 'Node:', value, 'deleted.'
        else:
            #only print this error message if the other messages were not triggered
            if children == False:
                print 'Node not found.'

    def printRoot(self):
        print 'root is:', self.root.integerKey

    def printTree(self):
        print 'printing tree...'
        #since the nodes are in a list, the parents will always print before the children
        for node in self.nodeList:
            #these variables needed to access the integerKey of the left and right nodes,
            #some of these nodes are set to None, and do not have integerKeys
            self.leftNode = None
            self.rightNode = None
            #only assign values for printing if the nodes exist
            if node.left is not None:
                self.leftNode = node.left.integerKey
            if node.right is not None:
                self.rightNode = node.right.integerKey
            print 'Node:', node.integerKey, '  Parent:', node.parent, '  Left child:', self.leftNode, '  Right child:', self.rightNode

#GRAPH
##############################################
class GRAPH():
    def __init__(self):
        #instantiate dictionary
        self.graph = {}
    def addVertex(self, value):
        if value in self.graph:
            print 'Vertex already exists.'
        else:
            #add the vertex with an empty list to store connections
            self.graph.update({value: []})
    def addEdge(self, value1, value2):
        if value1 and value2 in self.graph:
            #add both nodes to connection lists to ensure unweighted, bidirectional graph
            self.graph[value1].append(value2)
            self.graph[value2].append(value1)
        else:
            print 'One or more vertices not found.'
    def findVertex(self, value):
        if value in self.graph:
            #keys() function used to access all vertices in graph
            for vertex in self.graph.keys():
                if vertex == value:
                    print 'Found vertex:', vertex, 'and shared edge(s) with:', self.graph[vertex]
        else: 
            print 'Vertex not found.'

##############################################

#                  TESTING                   #

##############################################

    #QUEUE

print ('TESTING QUEUE')    
#generating random number array...
n = random.randint(10,20)
#select n random numbers from population (0,100)
queueList = random.sample(xrange(0,100),n)
print ('printing initial random list...')
print queueList
#instantiating queue class...
queue = QUEUE()
#updating size...
queue.size = n
#adding numbers to queue and dequeue...
queue.addNum()

    #STACK

print ''
print ('TESTING STACK')
#instantiating stack...
stack = STACK()
#generating random number array...
#array will be of random size at least 10
n = random.randint(10,20)
stackList = random.sample(xrange(0,100),n)
print ('printing initial random list...')
print stackList
#adding numbers to stack...
print ('creating stack from random list...')   
for item in stackList:
    stack.push(item)
#popping numbers off of stack...
print ('popping items off of stack...')
while not stack.isEmpty():
    print(stack.pop())
 
    #TREE

print ''
print ('TESTING BINARY TREE')
tree = BINARY_TREE(10)
tree.printRoot()
#the addNode function takes two arguments, the node to be added and the value of its parent
print 'adding node 9, parent 10'
tree.addNode(9,10)
print 'adding node 8, parent 10'
tree.addNode(8,10)
print 'adding node 7, parent 9'
tree.addNode(7,9)
print 'adding node 6, parent 8'
tree.addNode(6,8)
print 'adding node 6, parent 8'
tree.addNode(5,8)
print 'adding node 4, parent 5'
tree.addNode(4,5)
print 'adding node 3, parent 4'
tree.addNode(3,4)
print 'adding node 2, parent 3'
tree.addNode(2,3)
print 'adding node 1, parent 3'
tree.addNode(1,3)
#testing to see if a node is added if it already has two children
print 'adding node 13, parent 10'
tree.addNode(13,10)
#testing to see if a node will be added if its parent is not found
print 'adding node 14, parent 12'
tree.addNode(14,12)
#printing the tree...
tree.printTree()
#testing delete functionality...
print 'deleting node 7...'
tree.deleteNode(7)
tree.printTree()
print 'deleting node 1...'
tree.deleteNode(1)
tree.printTree()
print 'deleting node 100...'
tree.deleteNode(100)
print 'deleting node 10...'
tree.deleteNode(10)

#automated testing for binary tree
'''
treeList = random.sample(xrange(0,100),10)
tree = BINARY_TREE(treeList[0])
tree.printRoot()
#ensure that at least 10 nodes get added by checking the size of the node list
print 'adding nodes...'
while len(tree.nodeList) < 10:
    for item in treeList:
        #the arguments to addNode are value and parent value
        #in this case, each item in the treeList serves as a value,
        #and a random parent is selected for each value
        tree.addNode(item,random.choice(treeList))
tree.printTree()
'''

    #GRAPH

print ''
print ('TESTING GRAPH')
#instantiating the graph
graph = GRAPH()
#creating random list of 10 numbers
vertexList = random.sample(xrange(0,100),10)
print 'adding vertices...'
#adding each number as a vertex in the graph
for vertex in vertexList:
    graph.addVertex(vertex)
    print graph.graph
print 'adding edges...'
#select 20 random edges to add from the list of vertices
for x in range(20):
    randomEdge1 = random.choice(vertexList)
    randomEdge2 = random.choice(vertexList)
    graph.addEdge(randomEdge1, randomEdge2)
    print graph.graph
print 'finding vertices...'
for y in range(5):
    #pick a random vertex to search for
    randomVertex = random.choice(vertexList)
    print 'looking for', randomVertex, '...'
    graph.findVertex(randomVertex)

    













