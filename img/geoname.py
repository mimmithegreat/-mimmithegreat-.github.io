# I originally tried to write and compile everthing in one modified py file, but this led to memory error, which is due to the RAM, so i proceeded writing 3 different files as shown on the github page

import re
import os
#relative path again
source = ".//files_xml"
placeDict = {} # creates the dictionary, I tried to do it with a list at first but it became clear it wouldn´t work
#create the function

def updateDic(dic, key):
    updateVar = 1 # makes more sense to me, or else I will constantly think that in the else condition, the key will be set back to 1
    if key in dic:
        dic[key] += updateVar

    else:
        dic[key] = updateVar

def collectTaggedToponyms(xmlText, dic): #Function for the regex
    xmlText = re.sub("\s+", " ", xmlText) # re.sub = replace with white space
    date = re.search(r'<date value="([\d-]+)"', xmlText).group(1) #searches the regex and takes only the regex ([d-]+) due to .group
    count1, count2 = 0,0 # two counters, although later argued in the final code not necessary, because it´s only a control measurement
    #that is useful in the first steps and later control runs
    for t in re.findall(r"<placeName[^<]+</placeName>", xmlText): # for loop: to find all those regex including <placename tags
        t = t.lower() # because of case sensitivity this makes the letters lower case
        if 'tgn,' in t: # Question: apparantly there is no switch: case in Python? this is unfortunate because I think in the following if statements it would be more elegantly
            if re.search(r'reg="([^"]+)"', t): # searches the regex and groups them
                reg = re.search(r'reg="([^"]+)"', t).group(1)
            else:
                #print(t)  control measures
                reg = 0

            if re.search(r'key="([^"]+)"', t):
                key = re.search(r'key="([^"]+)"', t).group(1)
            else:
                print(t) #control measures
                key = 0
            #if reg == 0 or key == 0: tried something different
            if reg == 0:
                count1 += 1
            elif key == 0:
                count1 += 1
            else:
                count2 += 1 # as argued above
                keyNew = reg+"\t"+key # \t = tap
                updateDic(placeDict, keyNew) # updates the dictionary placeDict with the function updateDic with the new Key = the tap
            ##if count1 >= 0:
                ##print("%s: %d out of %d toponyms misstagged." % (date, count1, count2))

# here comes the actual collecting of the toponyms

def collectRawToponyms(source): #creates the function with the parameter source
#lof =listA (I used those names before so I am going to do so in this piece of code as well, so I won´t get confuesed)
#f = fileName
    listA = os.listdir(source) #listdir searches files in a given path (source) and adds them to a new list-> listA
    listA = sorted(listA, reverse=False) # sorts the list
    counter = 0

    for fileName in listA:
    #    if fileName.startswith("dltext"): #fileName test  also a control measure and it slows down the process, this time I keep it in, because I need the control

            with open(source+"/"+fileName, "r", encoding="utf8") as f1: # open file as new file = f1
                text = f1.read()     # just reading not writing
                collectTaggedToponyms(text, placeDict)

    freqList = [] # List of the frequencies with the names of the places
    threshold = 100 # anything under 100 won´t be added
    for k,v in placeDict.items(): # displays dictionary keys and values as tuple pairs (google tuple)
        if v >= threshold:
            freqList.append("%09d\t%s" % (v,k)) # is % in this line a TupleOperand or Dict Operand? .append modifies the list
    print("Number of unique items with freq at least %d: %d" % (threshold, len(freqList))) # i got 411

    freqList = "\n".join(sorted(freqList, reverse = True)) # \n = new line,
    with open("freqList.csv", "w", encoding="utf8") as f9: # creates the list as a file
            f9.write(freqList) # writes the findings in the list

collectRawToponyms(source)

def loadGeoData(another): #I already used the var name fileName so, I will use the var Name:
    dic = {} #new dictionary

    with open(another, "r", encoding="utf8") as f1: # see above
        data = f1.read().split("\n") # breakes the text down into smaller parts with end line; also Memory error - so the ram has too many shortcomings
        for d in data:
            d1 = d.split("\t") # here a tab is used
            if len(d1) == 19: #there are 19 columns in the US file, that means and it means if there there are exactly 19 columns
                val = "\t".join([[d1]+", "+d1[10], d1[4], d1[5]]) # appends geoname, countrycode, longitude, latitude
                test = d1[1].lower() # makes the text lower case

                if test in dic:
                    dic[test].append(val) #see above
                else:
                    dic[test] = [val]

    return(dic) # returns the dictionary

geoDataFile = os.path.abspath('US.csv') # there were several problem: one the relative path would not work sec. the name of the file was US.txt
#windows doesn´t like it when I try to change the ending apparantly so solving those two took quite some time
geoData = loadGeoData(geoDataFile)
def processResults(another):
    with open(another, "r", encoding="utf8") as f1:
        data = f1.read().split("\n") # here again read and split it with break line

        newData=[] # list

        noResult = "\t".join(["NA", "NA", "NA"]) # when tab join with NA

        for d in data:
            d1 = d.split("\t") # when tab split Line
            if "," in d[1]: # again why doesn´t have python the switch case? this bugs me
                test = d1[1].split(",")[0]
            else:
                test = d1[1]

            if test in geoData:
                for i in geoData[test]:
                    newData.append(d+"\t"+i)
            else:
                newData.append(d+"\t" + noResult)
                with open("matchedResults.csv", "w", encoding="utf8") as f9:
                    f9.write("\n".join(newData))

processResults("freqList.csv")
