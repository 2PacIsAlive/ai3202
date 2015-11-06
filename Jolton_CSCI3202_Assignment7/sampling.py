#!usr/bin/env python

class Node:
	def __init__(self,val):
		self.val = val
		self.children = []
		self.parents = []
		self.state = False

	def setConnections(self,children,parents):
		for edge in children:
			self.children.append(edge)
		for edge in parents:
			self.parents.append(edge)

def priorSample():
	output = []
	sample = 0
	while sample < len(samples):
		#sample cloudy
		if samples[sample] < 0.5:
			cloudy.state = True
		sample += 1
		if cloudy.state == True:
			#sample sprinkler
			if samples[sample] < 0.1:
				sprinkler.state = True
			#sample rain
			if samples[sample+1] < 0.8:
				rain.state = True
		else:	
			#sample sprinkler
			if samples[sample] < 0.5:
				sprinkler.state = True
			#sample rain
			if samples[sample+1] < 0.2:
				rain.state = True
		sample += 2
		#sample wet grass given parent states
		if sprinkler.state == True and rain.state == False:	
			if samples[sample] < 0.9:
				wetGrass.state = True
		elif sprinkler.state == True and rain.state == True:
			if samples[sample] < 0.99:
				wetGrass.state = True
		elif sprinkler.state == False and rain.state == True:
			if samples[sample] < 0.9:
				wetGrass.state = True
		sample += 1
		output.append([cloudy.state,sprinkler.state,rain.state,wetGrass.state])
		resetState()
	return output

def priorSampleCalc(output):
	c = 0.0
	s = 0.0
	r = 0.0
	w = 0.0
	cr = 0.0
	rc = 0.0
	sw = 0.0
	wc = 0.0
	wcs = 0.0
	for sample in output:
		if sample[0] == True:
			c += 1
			if sample[2] == True:
				cr += 1
		if sample[1] == True:
			s += 1
			if sample[3] == True:
				sw += 1
		if sample[2] == True:
			r += 1
			if sample[0] == True:
				rc += 1
		if sample[3] == True:
			w += 1
			if sample[0] == True:
				wc += 1
				if sample[1] == True:
					wcs += 1
	n = float(len(samples))/4 #25 individual samples
	print "P(c=True):", c/n
	print "P(c=True|r=True):", rc/r
	print "P(s=True|w=True):", sw/w   
	print "P(s=True|c=True,w=True):", wcs/wc 

def resetState():
	for node in bayesnet:
		node.state = False

def rejectC():
	output = []
	c = 0
	for sample in samples:
		if sample < 0.5:
			cloudy.state = True
		output.append(cloudy.state)
		resetState()
	for item in output: 
		if item == True:
			c += 1
	return c / float(len(output))

def rejectCR():
	output = []
	cr = 0
	n = 0.0
	sample = 0 
	while sample < len(samples):
		if samples[sample] < 0.5:
			cloudy.state = True
		sample += 1
		if cloudy.state == True:
                        if samples[sample] < 0.8:
                                rain.state = True
				output.append([cloudy.state,rain.state])
                else:
                        if samples[sample] < 0.2:
                                rain.state = True
				output.append([cloudy.state,rain.state])
                sample += 1
		resetState()
	for samp in output:
		if samp[1] == True:
			n += 1
			if samp[0] == True:
				cr += 1
	return cr/n

def rejectSW():
	output = []
	sw = 0
	n = 0.0
	sample = 0	
	sample = 0
	while sample < len(samples):
		#sample cloudy
		if samples[sample] < 0.5:
			cloudy.state = True
		sample += 1
		if cloudy.state == True:
			#sample sprinkler
			if samples[sample] < 0.1:
				sprinkler.state = True
			#sample rain
			if samples[sample+1] < 0.8:
				rain.state = True
		else:	
			#sample sprinkler
			if samples[sample] < 0.5:
				sprinkler.state = True
			#sample rain
			if samples[sample+1] < 0.2:
				rain.state = True
		sample += 2
		#sample wet grass given parent states
		if sprinkler.state == True and rain.state == False:	
			if samples[sample] < 0.9:
				wetGrass.state = True

		elif sprinkler.state == True and rain.state == True:
			if samples[sample] < 0.99:
				wetGrass.state = True
		elif sprinkler.state == False and rain.state == True:
			if samples[sample] < 0.9:
				wetGrass.state = True
		sample += 1
		if wetGrass.state == True:
			output.append([sprinkler.state,wetGrass.state])
		resetState()
	for samp in output:
		if samp[1] == True:
			n += 1
			if samp[0] == True:
				sw += 1
	return sw/n

def rejectSCW():
	cw = 0.0
	scw = 0.0
	output = priorSample()
	#reject unwanted samples
	i = 0
	length = len(output)
	while i < length:
		if output[i][0] == False:
			output.pop(i)
			length -= 1
		elif output[i][3] == False:
			output.pop(i)
			length -= 1
		i += 1
	#calculate totals in new output
	for sample in output:
		if sample[0] == True:
			if sample[3] == True:
				cw += 1
				if sample[1] == True:
					scw += 1
	return scw/cw 	

def rejectionSample(): 
	pC = rejectC()
	print "P(c=True):", pC
	pCR = rejectCR()
	print "P(c=True|r=True):", pCR
	pSW = rejectSW()
	print "P(s=True|w=True):", pSW	
	pSCW = rejectSCW()
	print "P(s=True|c=True,w=True):", pSCW	

if __name__=="__main__":
	cloudy = Node("c")
	sprinkler = Node("s")
	rain = Node("r")
	wetGrass = Node("w")
	cloudy.setConnections([sprinkler,rain],[None])
	sprinkler.setConnections([wetGrass],[cloudy])
	rain.setConnections([wetGrass],[cloudy])
	wetGrass.setConnections([None],[sprinkler,rain])
	bayesnet = [cloudy,sprinkler,rain,wetGrass]
	samples = [0.82,  0.56,	0.08,	0.81,	0.34,	0.22,	0.37,	0.99,	0.55,	0.61,	0.31,	0.66,	0.28,	1.0,	0.95,	
	0.71,	0.14,	0.1,	1.0,	0.71,	0.1,	0.6,	0.64,	0.73,	0.39,	0.03,	0.99,	1.0,	0.97,	0.54,	0.8,
	0.97,	0.07,	0.69,	0.43,	0.29,	0.61,	0.03,	0.13,	0.14,	0.13,	0.4,	0.94,	0.19,   0.6,	0.68,	0.36,
	0.67,	0.12,	0.38,	0.42,	0.81,	0.0,	0.2,	0.85,	0.01,	0.55,	0.3,	0.3,	0.11,	0.83,	0.96,	0.41,
	0.65,	0.29,	0.4,	0.54,	0.23,	0.74,	0.65,	0.38,	0.41,	0.82,	0.08,	0.39,	0.97,	0.95,	0.01,	0.62,
	0.32,	0.56,	0.68,	0.32,	0.27,	0.77,	0.74,	0.79,	0.11,	0.29,	0.69,	0.99,	0.79,	0.21,	0.2,	0.43,
	0.81,	0.9,	0.0,	0.91,	0.01]
	print "prior sampling..."
	priorSampleCalc(priorSample())
	print "rejection sampling..."
	rejectionSample()	 
