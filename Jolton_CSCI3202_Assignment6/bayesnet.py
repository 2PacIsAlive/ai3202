import argparse
import Queue

class Graph():
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
            self.graph[value1].append(value2)
            #self.graph[value2].append(value1)
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

class QueueClass():
    def __init__(self,size):
        self.queue = Queue.Queue()
        self.size = size 
    def addChar(self,char):  
        self.queue.put(char)

def getArgs():
	parser = argparse.ArgumentParser(description='Specify program behavior.')
	#parser.add_argument('-g', action="store_true", default=False)
	parser.add_argument('-g', action="store", dest="conditional_probability", help="must put argument in quotes!")
	parser.add_argument('-j', action="store", dest="joint_probability")
	parser.add_argument('-m', action="store", dest="marginal_probability")
	parser.add_argument('-p', action="store", dest="set_prior")
	args=parser.parse_args()
	return args

def performAction(arguments):
	#arguments is the namespace parsed from the command line
	if arguments.conditional_probability != None:
		conditionalProbability(arguments.conditional_probability)
	if arguments.joint_probability != None:
		jointProbability(arguments.joint_probability)
	if arguments.marginal_probability != None:
		marginalProbability(arguments.marginal_probability)
	if arguments.set_prior != None:
		setPrior(arguments.set_prior)

def conditionalProbability(args):
	print 'Computing conditional probability for:', args

def jointProbability(args):
	print 'Computing joint probability for:', args

def marginalProbability(args):
	print 'Computing marginal probability for:', args

def setPrior(args):
	print 'Setting prior for:', args
	priorQueue = QueueClass(len(args))
	for char in args:
		priorQueue.addChar(char)
	first = True
	dest = ''
	val = ''
	while first:
		current = priorQueue.queue.get()
		if current != '=':
			dest += current
		else:
			first = False
	while not priorQueue.queue.empty():
		val += priorQueue.queue.get()
	print "dest:",dest," val:",val


def graphSetup(args):
	g = Graph()
	g.addVertex("Pollution")
	g.addVertex("Smoker")
	g.addVertex("Cancer")
	g.addVertex("XRay")
	g.addVertex("BreathingDifficulty")
	g.addEdge("Pollution","Cancer")
	g.addEdge("Smoker","Cancer")
	g.addEdge("Cancer","XRay")
	g.addEdge("Cancer","BreathingDifficulty")
	print g.graph

def main():
	#set known probabilities
	pollutionLow = 0.09
	pollutionHigh = 0.01
	smokerTrue = 0.30
	smokerFalse = 0.70

	args = getArgs()
	performAction(args)
	graphSetup(args)

if __name__=="__main__":
	main()

	

