import argparse
import Queue

class Node():
    def __init__(self,type):
        self.type = type 
        self.parents = []
        self.children = []
        self.CPT = {}
    def createCPT(self):
    	keys = ["pollutionLow", "pollutionHigh", 
    			"smokerTrue", "smokerFalse", 
    			"cancerTrue", "cancerFalse", 
    			"xrayTrue", "xrayFalse", 
    			"dysTrue", "dysFalse"]
    	self.CPT = dict.fromkeys(keys, [])
    	#specify CPT values
    	if node.type == pollution:
    		


class QueueClass():
    def __init__(self,size):
        self.queue = Queue.Queue()
        self.size = size 
    def addChar(self,char):  
        self.queue.put(char)

def getArgs():
	parser = argparse.ArgumentParser(description='Specify program behavior.')
	#parser.add_argument('-g', action="store_true", default=False)
	parser.add_argument('-g', action="store", dest="conditional_probability", help="must put bar in quotes!")
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
	#product over i of (p(xi | Parents(xi)))
	#must assume that parents are in a certain state?
	jP = 1 
	prob = None
	tilde = False
	for char in args:
		if char == '~':
			tilde = True
		else:
			if tilde == True:
				print "getting",char,"false"
				#compute probability of char given chars parents
				jp *= 1
				tilde = False
			else: 
				print "getting",char,"true"
				if char == 'c':
					for item in cDist_cond:
						print "item in cDist_cond", item
						jP += item
						print jP
	print 'Joint Probability:',jP

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
	val = float(val) 
	if dest == 'P':
		P = val
		p = 1-P
		print 'Set p to',p,'and P to',P
	elif dest == 'S':
		S = val
		s = 1-S
		print 'Set s to',s,'and S to',S
	else:
		print 'Invalid input. Set either "P" or "S".'

def genNodes():
	#instantiate nodes
	pollution = Node("pollution")
	smoking = Node("smoking")
	cancer = Node("cancer")
	xray = Node("xray")
	dys = Node("dys")
	#specify network connections
	pollution.children = [cancer]
	smoking.children = [cancer]
	cancer.parents = [pollution,smoking]
	cancer.children = [xray,dys]
	xray.parents = [cancer]
	dys.parents = [cancer]
	#list of nodes in network
	bayesnet = [pollution,smoking,cancer,xray,dys]
	#setup conditional probability tables
	for node in bayesnet:
		node.createCPT()
		print node.CPT

def main():
	genNodes()
	args = getArgs()
	performAction(args)
	#make sure to update nodes after setting priors

if __name__=="__main__":
	#global network
	bayesnet = []
	#set known probabilities
	#POLLUTION
	P = 0.1 #high pollution
	p = 1-P #0.9 #low pollution
	pDist = [P,p]
	#SMOKER
	S = 0.70 #smoker false
	s = 1-S #0.30 #smoker true
	sDist = [S,s]
	#CANCER
	cPs = 0.05 #pollution high, smoker true
	cPs_cond = cPs * P * s
	cPS = 0.02 #pollution high, smoker false
	cPS_cond = cPS * P * S
	cps = 0.03 #pollution low, smoker true
	cps_cond = cps * p * s
	cpS = 0.001 #pollution high, smoker false
	cpS_cond = cpS * p * S
		#cancer distributions
	cDist = [cPs,cPS,cps,cpS]
	cDist_cond = [cPs_cond,cPS_cond,cps_cond,cpS_cond]
	#XRAY
	xCT = 0.90 #cancer true
	xCF = 0.20 #cancer false
	xDist = [xCT,xCF]
	#BREATHING DIFFICULTY
	dCT = 0.65 #cancer true
	dCF = 0.30 #cancer false
	dDist = [dCT,dCF]
	#call main
	main()

	

