import argparse
import Queue

class Node():
    def __init__(self,type):
        self.type = type 
        self.parents = []
        self.children = []
        self.CPT = {}
    def createCPT(self):
    	keys = ["pollutionHigh", "pollutionLow",
    		"smokerTrue", "smokerFalse"
    		"pollutionLow_smokerTrue", "pollutionLow_smokerFalse", 
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
    		self.CPT["pLsT_parents"] = 0.03 * p * s 
    		self.CPT["pHsT_parents"] = 0.05 * P * s
    		self.CPT["pLsF_parents"] = 0.001 * p * S 
    		self.CPT["pHsF_parents"] = 0.02 * P * S
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
	if arguments.set_prior != None:
		setPrior(arguments.set_prior)
	if arguments.conditional_probability != None:
		conditionalProbability(arguments.conditional_probability)
	if arguments.joint_probability != None:
		jointProbability(arguments.joint_probability)
	if arguments.marginal_probability != None:
		marginalProbability(arguments.marginal_probability)

def parseArguments(args):
	tilde = False
	parseMe = []
	for char in args:
		if char.isupper():
			parseMe.append((char,"distribution"))
		else:
			if char == '~':
				tilde = True
			else:
				if tilde == True:
					parseMe.append((char,"false"))
					tilde = False
				else: 
					parseMe.append((char,"true"))
	return parseMe

def parseConditionalArguments(args):
	tilde = False
	a = []
	b = []
	a1 = True
	for char in args:
		if char == "|":
			a1 = False
		else:	
			if a1 == True:
				if char == '~':
					tilde = True
				else:
					if tilde == True:
						a.append((char,"false"))
						tilde = False
					else: 
						a.append((char,"true"))
			else:
				if char == '~':
					tilde = True
				else:
					if tilde == True:
						b.append((char,"false"))
						tilde = False
					else: 
						b.append((char,"true"))
	return a,b

def getReasoningType(case):
	reasoningType = None
	if case == [("d","true")]:
		reasoningType = "diagnostic"
	elif case == [("s","true")]:
		reasoningType = "predictive"
	elif case == [("c","true")] or case == [("c","true"),("s","true")]:
		reasoningType = "intercausal"
	elif case == [("d","true"),("t","true")]:
		reasoningType = "intercausal"
	return reasoningType

def conditionalProbability(args):
	a,b = parseConditionalArguments(args)
	reasoningType = getReasoningType(b)
	if reasoningType == None:
		print "Invalid conditional probability input."
	else:
		print 'Computing conditional probability for:',args,"using",reasoningType,"reasoning."

def jointProbability(args):
	print 'Computing joint probability for:', args
	#product over i of (p(xi | Parents(xi)))
	#must assume that parents are in a certain state?
	jP = -1.0 #return -1 if something goes wrong in calcJoint()
	parseMe = parseArguments(args)
	jP = calcJoint(parseMe)
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
	if "pollutionHigh" in combinations and "smokerFalse" in combinations:
		CPT_entries.append("pollutionHigh_smokerFalse")
	if "pollutionLow" in combinations and "smokerTrue" in combinations:
		CPT_entries.append("pollutionLow_smokerTrue")
	if "pollutionLow" in combinations and "smokerFalse" in combinations:
		CPT_entries.append("pollutionLow_smokerFalse")
	if "cancerTrue" in combinations:
		CPT_entries.append("cancerTrue")
	if "cancerFalse" in combinations:
		CPT_entries.append("cancerFalse")
	return CPT_entries

def getMissingParents(args):
	missing = []
	if ("p","true") not in args and ("p","false") not in args:
		missing.append("pollution")
	if ("s","true") not in args and ("s","false") not in args:
		missing.append("smoker")
	if ("c","true") not in args and ("c","false") not in args:
		missing.append("cancer")
	return missing

#def jointHelper(parentList,childList):
	#PARENT
	#pollution | smoking | cancer
	#pollution | smoking
	#pollution | cancer
	#pollution
	#smoking | cancer
	#smoking
	#cancer
	#none
	###################
	#CHILD
	#d true | x false | cancer true 
	#d true | x false | cancer false
	#d true | x true | cancer true 
	#d true | x true | cancer false
	#d false | x false | cancer true 
	#d false | x false | cancer false
	#d false | x true | cancer true 
	#d false | x true | cancer false
	#d true | x true
	#d true | x false
	#d true | cancer true
	#d true | cancer false
	#x true | cancer true
	#x true | cancer false
	#d false | x true
	#d false | x false
	#d false | cancer true
	#d false | cancer false
	#x false | cancer true
	#x false | cancer false
	#d true
	#d false
	#x true
	#x false
	#cancer true
	#cancer false
	#none

	#if argument has d or x, 
		#
	#for every child node 
		#see what parents are missing 
		#probability of child given the parents 	


def calcJoint(args):
	lookup = getParentState(args)
	ommissions = getMissingParents(args)
	total = 1
	for item in args:
		if item == ("p","false"):
			total *= bayesnet[0].CPT["pollutionHigh"]
		elif item == ("p","true"):
			total *= bayesnet[0].CPT["pollutionLow"]

		elif item == ("s","false"):
			total *= bayesnet[1].CPT["smokerFalse"]
		elif item == ("s","true"):
			total *= bayesnet[1].CPT["smokerTrue"]

		elif item == ("c","true"):
			if "pollutionHigh_smokerTrue" in lookup:
				total *= bayesnet[2].CPT["pollutionHigh_smokerTrue"]
			elif "pollutionHigh_smokerFalse" in lookup:
				total *= bayesnet[2].CPT["pollutionHigh_smokerFalse"]
			elif "pollutionLow_smokerTrue" in lookup:
				total *= bayesnet[2].CPT["pollutionLow_smokerTrue"]
			elif "pollutionLow_smokerFalse" in lookup:
				total *= bayesnet[2].CPT["pollutionLow_smokerFalse"]
			'''
			##########################################################################################
			else: #unspecified parent state
				if "pollution" in ommissions and "smoker" in ommissions:
					getCPTentries = ["pHsT_parents",
									"pHsF_parents",
									"pLsT_parents",
									"pLsF_parents"]
					if ("x","true") in lookup and ("d","true") in lookup:
						for entry in getCPTentries:
							total *= bayesnet[2].CPT[entry] * bayesnet[3].CPT["xrayTrue"] * bayesnet[4].CPT["dysTrue"]
					if ("x","false") in lookup and ("d","true") in lookup:
						for entry in getCPTentries:
							total *= bayesnet[2].CPT[entry] * bayesnet[3].CPT["xrayTrue"] * bayesnet[4].CPT["dysTrue"]
			'''
			else: 
				total *= calcMarg([("c","true")])
		elif item == ("c","false"):
			if "pollutionHigh_smokerTrue" in lookup:
				total *= 1-bayesnet[2].CPT["pollutionHigh_smokerTrue"]
			elif "pollutionHigh_smokerFalse" in lookup:
				total *= 1-bayesnet[2].CPT["pollutionHigh_smokerFalse"]
			elif "pollutionLow_smokerTrue" in lookup:
				total *= 1-bayesnet[2].CPT["pollutionLow_smokerTrue"]
			elif "pollutionLow_smokerFalse" in lookup:
				total *= 1-bayesnet[2].CPT["pollutionLow_smokerFalse"]
			else: 
				total *= calcMarg([("c","false")])

		elif item == ("x","true"):
			if "cancerTrue" in lookup:
				total *= bayesnet[3].CPT["cancerTrue"]
			elif "cancerFalse" in lookup:
				total *= bayesnet[3].CPT["cancerFalse"]
			else: 
				total *= calcMarg([("x","true")])
		elif item == ("x","false"):
			if "cancerTrue" in lookup:
				total *= 1-bayesnet[3].CPT["cancerTrue"]
			elif "cancerFalse" in lookup:
				total *= 1-bayesnet[3].CPT["cancerFalse"]
			else: 
				total *= calcMarg([("x","false")])

		elif item == ("d","true"):
			if "cancerTrue" in lookup:
				total *= bayesnet[4].CPT["cancerTrue"]
			elif "cancerFalse" in lookup:
				total *= bayesnet[4].CPT["cancerFalse"]
			else: 
				total *= calcMarg([("d","true")])
		elif item == ("d","false"):
			if "cancerTrue" in lookup:
				total *= 1-bayesnet[4].CPT["cancerTrue"]
			elif "cancerFalse" in lookup:
				total *= 1-bayesnet[4].CPT["cancerFalse"]
			else: 
				total *= calcMarg([("d","false")])
	return total

def marginalProbability(args):
	print 'Computing marginal probability for:', args
	#sum out unwanted variables
	parseMe = parseArguments(args)
	mP = calcMarg(parseMe)
	print "Marginal Probability:",mP

def calcMarg(args):
	total = 0
	for item in args:
		if item == ("P","distribution"):
			print "Marginal probability distribution of pollution:"
			print "Low:",calcMarg([("p","true")]),"High:",calcMarg([("p","false")])
		elif item == ("S","distribution"):
			print "Marginal probability distribution of smoker:"
			print "True:",calcMarg([("s","true")]),"False:",calcMarg([("s","false")])
		elif item == ("C","distribution"):
			print "Marginal probability distribution of cancer:"
			print "True:",calcMarg([("c","true")]),"False:",calcMarg([("c","false")])
		elif item == ("X","distribution"):
			print "Marginal probability distribution of xray:"
			print "True:",calcMarg([("x","true")]),"False:",calcMarg([("x","false")])
		elif item == ("D","distribution"):
			print "Marginal probability distribution of dyspnoea:"
			print "True:",calcMarg([("d","true")]),"False:",calcMarg([("d","false")])

		elif item == ("p","true"):
			total += bayesnet[0].CPT["pollutionLow"] 
		elif item == ("p","false"):
			total = 1-calcMarg([("p","true")])

		elif item == ("s","true"):
			total += bayesnet[1].CPT["smokerTrue"] 
		elif item == ("s","false"):
			total = 1-calcMarg([("s","true")])

		elif item == ("c","true"):
			total += bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[0].CPT["pollutionHigh"] * bayesnet[1].CPT["smokerTrue"]
			total += bayesnet[2].CPT["pollutionHigh_smokerFalse"] * bayesnet[0].CPT["pollutionHigh"] * bayesnet[1].CPT["smokerFalse"]
			total += bayesnet[2].CPT["pollutionLow_smokerTrue"] * bayesnet[0].CPT["pollutionLow"] * bayesnet[1].CPT["smokerTrue"]
			total += bayesnet[2].CPT["pollutionLow_smokerFalse"] * bayesnet[0].CPT["pollutionLow"] * bayesnet[1].CPT["smokerFalse"]
		elif item == ("c","false"):
			total = 1-calcMarg([("c","true")])
		
		elif item == ("x","true"):
			total += bayesnet[3].CPT["cancerTrue"] * calcMarg([("c","true")])
			total += bayesnet[3].CPT["cancerFalse"] * calcMarg([("c","false")])
		elif item == ("x","false"):
			total = 1-calcMarg([("x","true")])

		elif item == ("d","true"):
			total += bayesnet[4].CPT["cancerTrue"] * calcMarg([("c","true")])
			total += bayesnet[4].CPT["cancerFalse"] * calcMarg([("c","false")])
		elif item == ("d","false"):
			total = 1-calcMarg([("d","true")])
	return total

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
		for node in bayesnet:
			node.CPT["pollutionHigh"] = val
			node.CPT["pollutionLow"] = 1-val
		P = val
		p = 1-P
		print 'Set p to',p,'and P to',P
	elif dest == 'S':
		for node in bayesnet:
			node.CPT["smokerFalse"] = 1-val
			node.CPT["smokerTrue"] = val
		s = val
		S = 1-s
		print 'Set s to',s,'and S to',S
	else:
		print 'Invalid input. Set either "P" or "S".'
'''
def genNet(): #pearl's network construction algorithm
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
	print bayesnet
	#setup conditional probability tables
	for node in bayesnet:
		node.createCPT()
'''
def main():
	#genNet()
	args = getArgs()
	performAction(args)
	#make sure to update nodes after setting priors

if __name__=="__main__":
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

	#pearl's network construction algorithm
	bayesnet = []
	pollution = Node("pollution")
	smoker = Node("smoker")
	cancer = Node("cancer")
	xray = Node("xray")
	dys = Node("dys")
	#specify network connections
	pollution.children = [cancer]
	smoker.children = [cancer]
	cancer.parents = [pollution,smoker]
	cancer.children = [xray,dys]
	xray.parents = [cancer]
	dys.parents = [cancer]
	#list of nodes in network
	bayesnet = [pollution,smoker,cancer,xray,dys]
	#setup conditional probability tables
	for node in bayesnet:
		node.createCPT()

	#call main
	main()

	

