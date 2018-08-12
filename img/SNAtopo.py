import re, os

source = ".//files_xml"
target = ".//SNA"

#create a dictionary to save the extracted information to
edgesDic = {} # dictionary for edges
edgesList = [] # list for toponyms

def updateDic(dic, key): # updating dictionary
	if key in dic:
		dic[key] += 1
	else:
		dic[key] = 1

def taggedToponyms(unitText): # define function to collect tagged toponyms in edgesList
	toponymsInUnit = [] #create list for toponyms in unit
	for toponyms in re.findall(r'<placeName([^<]+)', unitText, flags=0):
		if 'tgn,':
			match = re.search(r'reg="([\w,]+)"', toponyms)
			if match:
				toponym = match.group(1) #filter toponyms
				toponym = toponym.lower()
				toponymsInUnit.append(toponym)
	return toponymsInUnit

import itertools # creating edges from a list
def edges(edgesList, edgesDic):
	edges = list(itertools.combinations(edgesList, 2))
	for e in edges:
		key = "\t".join(sorted(list(e))) # A > B (sorted alphabetically, to avoid cases of B > A)
		updateDic(edgesDic, key)

lof = os.listdir(source)
lof.sort()

for file in lof:
	with open(source + "/" + file, "r", encoding="utf8") as f1:
		text = f1.read()

		split = re.split('<div3', text) # split the text into units
		for unit in split[1:]:
			unit = "<div3" + unit # restore the integrity of units
			# print(unit) #testing

			toponymsList = taggedToponyms(unit) # set value
			edges(toponymsList, edgesDic) #create edges from toponymsList

# print(edgesDic) #testing

with open(target+"/"+"result_topo.tsv", "w", encoding="utf8") as resultFile:
	resultFile.write("source\ttarget\tweight\n") #insert title line to final file
	for edge in edgesDic: # separate key, value with tabs in final file
		entry = edge+"\t"+str(edgesDic[edge])+"\n"
		resultFile.write(entry)
