import argparse
import Queue
import ipdb
breakP = ipdb.set_trace
#breakP()

class Node():
    def __init__(self,type):
        self.type = type 
        self.parents = []
        self.children = []
        self.CPT = {}
    	self.CPT = {"cT":0.5, "cF":0.5,
    		"sT_cT":0.1, "sT_cF":0.5, 
		"rT_cT":0.8, "rT_cF":0.2,
		"wgT_sT_rT":0.99, "wgT_sT_rF":0.90,
		"wgT_sF_rT":0.99}

def conditionalProbability(args):
	cP = 0
	a,b = parseConditionalArguments(args)
	reasoningType = getReasoningType(b)
	if reasoningType == None:
		print "Invalid conditional probability input."
	else:
		print 'Computing conditional probability for:',args,"using",reasoningType,"reasoning."
	for arg in a:
		for arg2 in b:
			if arg == arg2:
				cP = 1
				reasoningType = None #skip other calculations if reasoning with a known belief
	if reasoningType == "predictive":
		if a == [("p","false")]:
			cP = bayesnet[0].CPT["pollutionHigh"]
		elif a == [("x","true")]:
			cP = calcMarg([("x","smokerTrue")])
			#p(x=pos | smoker) = p(x,s,c,p) / p(s,c,p)
		elif a == [("d","true")]:
			cP = calcMarg([("d","smokerTrue")])
		elif a == [("c","true")]:
			cP = calcMarg([("c","smokerTrue")])
	elif reasoningType == "diagnostic":
		if a == [("c","true")]:
			#cancer given dyspnoea
			cP = (bayesnet[4].CPT["cancerTrue"] * calcMarg([("c","true")])) / calcMarg([("d","true")])
	elif reasoningType == "intercausal":
		if ("s","true") not in b:
			if a == [("p","false")]:
			#pollution high given cancer
			#bayes rule <3
				cP = (calcMarg([("c","pollutionHigh")]) * bayesnet[0].CPT["pollutionHigh"]) / calcMarg([("c","true")])
			elif a == [("s","true")]:
			#smoker given cancer
			#bayes rule <3
				cP = (calcMarg([("c","smokerTrue")]) * bayesnet[1].CPT["smokerTrue"]) / calcMarg([("c","true")])
			elif a == [("x","true")]:
				cP = bayesnet[3].CPT["cancerTrue"]
			elif a == [("d","true")]:
				cP = bayesnet[4].CPT["cancerTrue"]
		else:
			if a == [("p","false")]:
				#p(c|~p,s) * p(~p) / p(c|s)
				cP = (bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]) / calcMarg([("c","smokerTrue")])
			elif a == [("x","true")]: 
				cP = bayesnet[3].CPT["cancerTrue"]
			elif a == [("d","true")]:
				cP = bayesnet[4].CPT["cancerTrue"]

	print "Conditional Probability:",cP

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
			CPT_entries.append("pollutionHigh")
		elif item == ("p","true"):
			combinations.append("pollutionLow")
			CPT_entries.append("pollutionLow")
		elif item == ("s","false"):
			combinations.append("smokerFalse")
			CPT_entries.append("smokerFalse")
		elif item == ("s","true"):
			combinations.append("smokerTrue")
			CPT_entries.append("smokerTrue")
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

def calcJoint(args):
	lookup = getParentState(args)
	ommissions = getMissingParents(args)
	total = 1
	for item in args:
		if item == ("p","false"):
			if "smoker" not in ommissions:
				total *= bayesnet[0].CPT["pollutionHigh"]
			if "smoker" in ommissions and "cancer" in ommissions:
				total *= bayesnet[0].CPT["pollutionHigh"] * 0.1
		elif item == ("p","true"):
			if "smoker" not in ommissions:
				total *= bayesnet[0].CPT["pollutionLow"]
			if "smoker" in ommissions and "cancer" in ommissions:
				total *= bayesnet[0].CPT["pollutionLow"] * 0.1

		if item == ("s","false"):
			if "pollution" not in ommissions:
				total *= bayesnet[1].CPT["smokerFalse"]
			if "pollution" in ommissions and "cancer" in ommissions:
				total *= bayesnet[1].CPT["smokerFalse"] * 0.1
		elif item == ("s","true"):
			if "pollution" not in ommissions:
				total *= bayesnet[1].CPT["smokerTrue"]
			if "pollution" in ommissions and "cancer" in ommissions:
				total *= bayesnet[1].CPT["smokerTrue"] * 0.1

		elif item == ("c","true"):
			if "pollutionHigh_smokerTrue" in lookup:
				total *= bayesnet[2].CPT["pollutionHigh_smokerTrue"]
			elif "pollutionHigh_smokerFalse" in lookup:
				total *= bayesnet[2].CPT["pollutionHigh_smokerFalse"]
			elif "pollutionLow_smokerTrue" in lookup:
				total *= bayesnet[2].CPT["pollutionLow_smokerTrue"]
			elif "pollutionLow_smokerFalse" in lookup:
				total *= bayesnet[2].CPT["pollutionLow_smokerFalse"]
			else: 
				if "pollution" in ommissions and "smoker" in ommissions:
					total *= calcMarg([("c","true")])
				elif "pollution" in ommissions:
					if ("smokerTrue") in lookup:
						total *= calcMarg([("c","smokerTrue")])
					if ("s","false") in lookup:
						total *= calcMarg([("c","smokerFalse")])
				elif "smoker" in ommissions:
					if ("pollutionLow") in lookup:
						total *= calcMarg([("c","pollutionLow")])
					if ("pollutionHigh") in lookup:
						total *= calcMarg([("c","pollutionHigh")])

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
				if "pollution" in ommissions and "smoker" in ommissions:
					total *= calcMarg([("c","false")])
				elif "pollution" in ommissions:
					if ("smokerTrue") in lookup:
						total *= calcMarg([("~c","smokerTrue")])
					if ("smokerFalse") in lookup:
						total *= calcMarg([("~c","smokerFalse")])
				elif "smoker" in ommissions:
					if ("pollutionLow") in lookup:
						total *= calcMarg([("~c","pollutionLow")])
					if ("pollutionHigh") in lookup:
						total *= calcMarg([("~c","pollutionHigh")])

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
				print "marg d true", calcMarg([("d","true")])
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
		#cloudy
		if item == ("c",True):
			total += bayesnet[0].CPT["cT"] 
		elif item == ("c",False):
			total = 1-calcMarg([("c",True)])
		
		#sprinkler
		elif item == ("s",True):
			total += sprinkler.CPT["sT_cT"] * cloudy.CPT["cT"] 
			total += sprinkler.CPT["sT_cF"] * cloudy.CPT["cF"]
		elif item == ("s",False):
			total = 1-calcMarg([("s",True)])
		
		#rain
		elif item == ("r",True):
			total += rain.CPT["rT_cT"] * cloudy.CPT["cT"] 
			total += rain.CPT["rT_cF"] * cloudy.CPT["cF"]
		elif item == ("r",False):
			total = 1-calcMarg([("r",True)])
		
		#rain cloudy
		elif item == ("r","cT"):
			total += rain.CPT["rT_cT"] * cloudy.CPT["cT"]
			total = total / calcMarg([("c",True)])

		#wetgrass
		elif item == ("w",True):
			total += wetgrass.CPT["wgT_sT_rT"] * calcMarg([("s",True)]) * calcMarg([("r",True)])	
			total += wetgrass.CPT["wgT_sT_rF"] * calcMarg([("s",True)]) * calcMarg([("r",False)])
			total += wetgrass.CPT["wgT_sF_rT"] * calcMarg([("s",False)]) * calcMarg([("r",True)])
		
		elif item == ("w","sT"):
			total += wetgrass.CPT["wgT_sT_rT"] * calcMarg([("s",True)]) * calcMarg([("r",True)])	
			total += wetgrass.CPT["wgT_sT_rF"] * calcMarg([("s",True)]) * calcMarg([("r",False)])	





		elif item == ("c","smokerTrue"):
			total = bayesnet[2].CPT["pollutionLow_smokerTrue"] * bayesnet[0].CPT["pollutionLow"] * bayesnet[1].CPT["smokerTrue"]
			total += bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[0].CPT["pollutionHigh"] * bayesnet[1].CPT["smokerTrue"]
			total = total / calcMarg([("s","true")])
		elif item == ("c","smokerFalse"):
			total += bayesnet[2].CPT["pollutionHigh_smokerFalse"] * bayesnet[0].CPT["pollutionHigh"] * bayesnet[1].CPT["smokerFalse"]
			total += bayesnet[2].CPT["pollutionLow_smokerFalse"] * bayesnet[0].CPT["pollutionLow"] * bayesnet[1].CPT["smokerFalse"]
		elif item == ("~c","pollutionLow"):
			total = 1-calcMarg([("c","pollutionLow")])
		elif item == ("~c","pollutionHigh"):
			total = 1-calcMarg([("c","pollutionHigh")])
		elif item == ("~c","smokerTrue"):
			total = 1-calcMarg([("c","smokerTrue")])
		elif item == ("~c","smokerFalse"):
			total = 1-calcMarg([("c","smokerFalse")])
		elif item == ("c","false"):
			total = 1-calcMarg([("c","true")])

		#rain
		elif item == ("x","true"):
			total += bayesnet[3].CPT["cancerTrue"] * calcMarg([("c","true")])
			total += bayesnet[3].CPT["cancerFalse"] * calcMarg([("c","false")])
		elif item == ("x","false"):
			total = 1-calcMarg([("x","true")])
		elif item == ("x","smokerTrue"):
			total += bayesnet[3].CPT["cancerTrue"] * bayesnet[2].CPT["pollutionLow_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			total += bayesnet[3].CPT["cancerTrue"] * bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			total += bayesnet[3].CPT["cancerFalse"] * (1-bayesnet[2].CPT["pollutionLow_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			total += bayesnet[3].CPT["cancerFalse"] * (1-bayesnet[2].CPT["pollutionHigh_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			denom = bayesnet[2].CPT["pollutionLow_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			denom += bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			denom += (1-bayesnet[2].CPT["pollutionLow_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			denom += (1-bayesnet[2].CPT["pollutionHigh_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			total = total / denom
		
		#wetgrass
		elif item == ("d","true"):
			total += bayesnet[4].CPT["cancerTrue"] * calcMarg([("c","true")])
			total += bayesnet[4].CPT["cancerFalse"] * calcMarg([("c","false")])
		elif item == ("d","false"):
			total = 1-calcMarg([("d","true")])
		elif item == ("d","smokerTrue"):
			total += bayesnet[4].CPT["cancerTrue"] * bayesnet[2].CPT["pollutionLow_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			total += bayesnet[4].CPT["cancerTrue"] * bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			total += bayesnet[4].CPT["cancerFalse"] * (1-bayesnet[2].CPT["pollutionLow_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			total += bayesnet[4].CPT["cancerFalse"] * (1-bayesnet[2].CPT["pollutionHigh_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			denom = bayesnet[2].CPT["pollutionLow_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			denom += bayesnet[2].CPT["pollutionHigh_smokerTrue"] * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			denom += (1-bayesnet[2].CPT["pollutionLow_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionLow"]
			denom += (1-bayesnet[2].CPT["pollutionHigh_smokerTrue"]) * bayesnet[1].CPT["smokerTrue"] * bayesnet[0].CPT["pollutionHigh"]
			total = total / denom
	return total

def combinedReasoning():
	total = sprinkler.CPT["sT_cT"] * cloudy.CPT["cT"] * ((wetgrass.CPT["wgT_sT_rT"] * sprinkler.CPT["sT_cT"] * rain.CPT["rT_cT"]) + (wetgrass.CPT["wgT_sT_rF"] * sprinkler.CPT["sT_cT"] * rain.CPT["sT_cF"]))
	return total

def main():
	print "bayes net calculations..."
	#performAction(args)
	pC = calcMarg([("c",True)])
	print "P(c=True):", pC
	pCR = (calcMarg([("r","cT")]) * cloudy.CPT["cT"]) / calcMarg([("r",True)])
	#print "wct", calcMarg([("w","sT")])
	#print "st", calcMarg([("s",True)])
	#print "numerator", (calcMarg([("w","sT")]) * calcMarg([("s",True)])) 
	#print "denominator", calcMarg([("w",True)])
	print "P(c=True|r=True):", pCR	
	pSW = (calcMarg([("w","sT")]) * calcMarg([("s",True)])) / calcMarg([("w",True)])
	#pSW = (wetgrass.CPT["cancerTrue"] * calcMarg([("c","true")])) / calcMarg([("d","true")]) 
	print "P(s=True|w=True):", pSW
	pSCW = combinedReasoning()
	print "P(s=True|c=True,w=True):", pSCW	

if __name__=="__main__":
	#pearl's network construction algorithm
	bayesnet = []
	cloudy = Node("c")
	sprinkler = Node("s")
	rain = Node("r")
	wetgrass = Node("w")
	#specify network connections
	cloudy.children = [sprinkler,rain]
	sprinkler.parents = [cloudy]
	rain.parents = [cloudy]
	sprinkler.children = [wetgrass]
	rain.children = [wetgrass]
	wetgrass.parents = [sprinkler,rain]
	#list of nodes in network
	bayesnet = [cloudy,sprinkler,rain,wetgrass]

	#call main
	main()

	

