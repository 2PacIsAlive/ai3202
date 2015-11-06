#!usr/bin/env python

import math

def sse(obs,exp):
	total = 0
	for i in range(0,len(obs)-1):
		total += math.pow(obs[i] - exp[i],2)
	return total

def parse(string):
	tmp = ""
	result = []
	for char in string:
		if char == " ":
			result.append(float(tmp))
			tmp = ""
		else:
			tmp += char
	result.append(float(tmp))
	return result

def main():
	observed = parse(raw_input("Enter the observed values, separated by spaces: "))
	expected = parse(raw_input("Enter the expected values, separated by spaces: "))
	error = sse(observed, expected)
	print "Error: ", error
	x = raw_input("Would you like me to do your homework, o wonderful and omniscient god? (y,n): ")
	if x == "y":
		hw = open("Assignment7.txt",'a')
		cases = ["p(c=True):","p(c=True|r=True):","p(s=True|w=True):","p(s=True|c=True,w=True"]
		prior_samples = ["0.48","0.75","0.4","0.0"]
		rejection_samples = ["0.49","0.703703703704","0.4","0.0"]
		bayesnet = ["0.5","0.8","0.135"]
		print "\nPRIOR SAMPLING:"
		for i in range(0,len(cases)-1):
			print cases[i], prior_samples[i]
		print "\nREJECTION SAMPLING:"
		for i in range(0,len(cases)-1):
			print cases[i], prior_samples[i]
		print "\nBAYESNET CALCULATIONS:"
		for i in range(0,len(cases)-1):
			print cases[i], bayesnet[i]
		print "\nSUM SQUARED ERROR FOR PRIOR SAMPLING:"
			

if __name__=="__main__":
	main()
