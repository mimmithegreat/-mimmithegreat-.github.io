import re, os

source = ".//files_xml"

topoDict = {}
def updateDic(dic, key):
    if key in dic:
        dic[key] += 1
    else:
        dic[key]  = 1

def loadMapLayer(fileName):
    dic = {}

    with open(fileName, "r", encoding="utf8") as f1:
        data = f1.read().split("\n")

        for d in data:
            d1 = d.split("\t")
            if d1[4] == "y":
                key = d1[2]
                val = "\t".join([d1[3], d1[5], d1[6]])
                dic[key] = val

    return(dic)

mapData = loadMapLayer("matchedResults.csv")

def collectTaggedToponyms(xmlText, dic, dateFilter):
    xmlText = re.sub("\s+", " ", xmlText)
    date = re.search(r'<date value="([\d-]+)"', xmlText).group(1)

    for t in re.findall(r"<placeName[^<]+</placeName>", xmlText):
        t = t.lower()

        if re.search(r'"(tgn,\d+)', t):
            reg = re.search(r'"(tgn,\d+)', t).group(1)

            if reg in mapData:
                updateDic(topoDict, mapData[reg])

def collectMappableLayers(source, dateTest):
    lof = os.listdir(source)
    lof = sorted(lof, reverse=False)
    counter = 0

    for f in lof:
        if f.startswith("dltext"): # fileName test
            with open(source +'/'+ f, "r", encoding="utf8") as f1:
                text = f1.read()

                # date filter
                date = re.search(r'<date value="([\d-]+)"', text).group(1)
                if date.startswith(dateTest):
                    collectTaggedToponyms(text, topoDict, dateTest)

    freqList = []
    thresh = 1
    for k,v in topoDict.items():
        if v >= thresh:
            freqList.append("%09d\t%s\t%d" % (v,k, v//20))

    freqList = "\n".join(sorted(freqList, reverse=True))
    with open("Dispatch_Geo_%s.csv" % dateTest, "w", encoding="utf8") as f9:
        f9.write(freqList)


collectMappableLayers(source, "1863")
