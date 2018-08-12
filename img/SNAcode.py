import re, os

source = ".//files_xml"
target = ".//SNA"

#create a dictionary to save the extracted information to
edgesDic = {} # dictionary for edges
edgesList = [] # list for names

def updateDic(dic, key): # updating dictionary
	if key in dic:
		dic[key] += 1
	else:
		dic[key] = 1

def taggedNames(unitText): # define function to collect tagged names in edgesList
	namesInUnit = [] #create list for names in unit
	for names in re.findall(r'<[pP]ers[nN]ame[^<]+', unitText, flags=0):
		match = re.search(r'authname="([\w,]+)"', names)
		if match:
			name = match.group(1) #filter names
			name = name.lower()
			namesInUnit.append(name)
	return namesInUnit

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

			namesList = taggedNames(unit) # set value
			edges(namesList, edgesDic) #create edges from nameslist

# print(edgesDic) #testing

with open(target+"/"+"result.tsv", "w", encoding="utf8") as resultFile:
	resultFile.write("source\ttarget\tweight\n")
	for edge in edgesDic: # separate key, value with tabs
		entry = edge+"\t"+str(edgesDic[edge])+"\n"
		resultFile.write(entry)
