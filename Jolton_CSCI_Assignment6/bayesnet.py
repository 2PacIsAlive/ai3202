import argparse

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

def getArgs():
	parser = argparse.ArgumentParser(description='Specify program behavior.')
	#parser.add_argument('-g', action="store_true", default=False)
	parser.add_argument('-g', action="store", dest="conditional_probability")
	parser.add_argument('-j', action="store", dest="joint_probability")
	parser.add_argument('-m', action="store", dest="marginal_probability")
	parser.add_argument('-p', action="store", dest="set_prior")
	args=parser.parse_args()
	return args

def performAction(arguments):
	if arguments.conditional_probability != None:
		conditionalProbability(arguments.conditional_probability)
	if arguments.joint_probability != None:
		jointProbability(arguments.joint_probability)
	if arguments.marginal_probability != None:
		marginalProbability(arguments.marginal_probability)
	if arguments.set_prior != None:
		setPrior(arguments.set_prior)

def conditionalProbability(args):
	print 'do cond prob on:', args

def jointProbability(args):
	print 'do joint prob on:', args

def marginalProbability(args):
	print 'do marg prob on:', args

def setPrior(args):
	print 'set prior for:', args


if __name__=="__main__":
	performAction(getArgs())

	

