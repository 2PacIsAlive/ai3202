import argparse
import Queue

class Node():
    def __init__(self,type):
        self.type = type 
        self.parents = []
        self.children = []
        self.CPT = {}
    def createCPT(self):
    	keys = ["pollutionLow_smokerTrue", "pollutionLow_smokerFalse", 
    		"pollutionHigh_smokerTrue", "pollutionHigh_smokerFalse", 
    		"cancerTrue", "cancerFalse", 
    		"xrayTrue", "xrayFalse", 
    		"dysTrue", "dysFalse"]
    	self.CPT = dict.fromkeys(keys, None)
    	#generate CPT values
    	#must specify all possible combinations of parent states 
    	if self.type == "pollution":
    		self.CPT["pollutionHigh"] = P
    		self.CPT["pollutionLow"] = p
    	elif self.type == "smoker":
    		self.CPT["smokerTrue"] = s
    		self.CPT["smokerFalse"] = S
    	elif self.type == "cancer":
    		self.CPT["pollutionLow_smokerTrue"] = 0.03
    		self.CPT["pollutionHigh_smokerTrue"] = 0.05
    		self.CPT["pollutionLow_smokerFalse"] = 0.001
    		self.CPT["pollutionHigh_smokerFalse"] = 0.02
    	elif self.type == "xray":
    		self.CPT["cancerTrue"] = 0.90
    		self.CPT["cancerFalse"] = 0.20
    	elif self.type == "dys":
    		self.CPT["cancerTrue"] = 0.65
    		self.CPT["cancerFalse"] = 0.30



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
	jP = -1.0 
	tilde = False
	parseMe = []
	for char in args:
		if char == '~':
			tilde = True
		else:
			if tilde == True:
				parseMe.append((char,"false"))
				#compute probability of char given chars parents
				tilde = False
			else: 
				parseMe.append((char,"true"))
	jp = calcJoint(parseMe)
	print 'Joint Probability:',jP

def getParentState(args):
	combinations = []
	CPT_entries = []
	for item in args:
		if item == ("p","false"):
			combinations.append("pollutionHigh")
		elif item == ("p","true"):
			combinations.append("pollutionLow")
		elif item == ("s","false"):
			combinations.append("smokerFalse")
		elif item == ("s","true"):
			combinations.append("smokerTrue")
		elif item == ("c","true"):
			combinations.append("cancerTrue")
		elif item == ("c","false"):
			combinations.append("cancerFalse")
	if "pollutionHigh" in combinations and "smokerTrue" in combinations:
		CPT_entries.append("pollutionHigh_smokerTrue")
	elif "pollutionHigh" in combinations and "smokerFalse" in combinations:
		CPT_entries.append("pollutionHigh_smokerFalse")
	elif "pollutionLow" in combinations and "smokerTrue" in combinations:
		CPT_entries.append("pollutionLow_smokerTrue")
	elif "pollutionLow" in combinations and "smokerFalse" in combinations:
		CPT_entries.append("pollutionLow_smokerFalse")
	elif "cancerTrue" in combinations:
		CPT_entries.append("cancerTrue")
	elif "cancerFalse" in combinations:
		CPT_entries.append("cancerFalse")
	return CPT_entries

def calcJoint(args):
	total = 0
	for item in args:
		if item == ("p","false"):
			total *= pollution.CPT[pollutionHigh]
		elif item == ("p","true"):
			total *= pollution.CPT[pollutionLow]
		elif item == ("s","false"):
			total *= smoker.CPT[smokerFalse]
		elif item == ("s","true"):
			total *= smoker.CPT[smokerTrue]
		elif item == ("c","true"):
			lookup = getParentState(args)
			for state in lookup:
				total *= cancer[state]
		elif item == ("c")
		#need to implement conditional probability first?


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

def genNodes(): #pearl's network construction algorithm
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
		print "node: ",node.type
		print "CPT: "
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

	

