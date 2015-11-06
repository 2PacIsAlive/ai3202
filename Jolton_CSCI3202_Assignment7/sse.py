#!usr/bin/env python

import math

def sse(obs,exp):
	total = 0
	for i in range(0,len(obs)-1):
		total += (math.pow(obs[i] - exp[i],2)) / len(obs)
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
		hw = open("Assignment7.txt",'w')
		hw.write("Jared Jolton\n")
		hw.write("CSCI 3202\n")
		hw.write("Assignment 7\n")
		hw.write("11/6/15\n")
		hw.write("___________\n")
		cases = ["p(c=True):","p(c=True|r=True):","p(s=True|w=True):","p(s=True|c=True,w=True):"]
		prior_samples = ["0.48","0.75","0.4","0.0"]
		rejection_samples = ["0.49","0.703703703704","0.4","0.0"]
		bayesnet = ["0.5","0.8","0.135","0.00621"]
		hw.write("\nPRIOR SAMPLING:\n")
		for i in range(0,len(cases)):
			hw.write(cases[i] + " " + prior_samples[i] + "\n")
		hw.write("\nREJECTION SAMPLING:\n")
		for i in range(0,len(cases)):
			hw.write(cases[i] + " " + rejection_samples[i] + "\n")
		hw.write("\nBAYESNET CALCULATIONS:\n")
		for i in range(0,len(cases)):
			hw.write(cases[i] + " " + bayesnet[i] + "\n")
		hw.write("\nSUM SQUARED ERROR FOR PRIOR SAMPLING:\n")
		obs = []
		for item in prior_samples:
			obs.append(float(item))
		exp = []
		for item in bayesnet:
			exp.append(float(item))
		error = sse(obs, exp)
		hw.write(str(error))
		hw.write("\nSUM SQUARED ERROR FOR REJECTION SAMPLING:\n")
		obs2 = []
		for item in rejection_samples:
			obs2.append(float(item))
		error2 = sse(obs2,exp)
		hw.write(str(error2))
		hw.close()
		print "Homework written!"

if __name__=="__main__":
	main()
