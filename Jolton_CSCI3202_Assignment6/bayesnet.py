import argparse
import Queue

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


class Node():
    def __init__(self,type):
        self.type = type 
        self.parents = []
        self.children = []

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
	jP = 0
	tilde = False
	for char in args:
		if char == '~':
			tilde = True
		else:
			if tilde == True:
				print "getting",char,"false"
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



def main():
	

	args = getArgs()
	performAction(args)
	#make sure to update nodes after setting priors

if __name__=="__main__":
	main()

	

