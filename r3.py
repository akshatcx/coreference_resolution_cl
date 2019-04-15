import os
import pickle

with open('./pronouns/relatives','rb') as f:
    relatives = pickle.load(f)

def r3():
    sc=[]
    for word in var.globalWordList:
        if word.word in relatives:
            sc.append([word.sentenceNum, word.chunkNum])
    for _ in sc:
        s = var.sentenceList[_[0]]
        c = s.chunkList[_[1]]
        n = s.nodeDict[c.nodeName]
        x = s.nodeDict[n.nodeParent]
        fans={}
        fans['sentence'] = _[0]
        fans['pronoun'] = _[1]
        fans['referents'] = []
        flag = 1
        while(flag):
            if x.nodeName[:3] == 'VGF' or x.nodeName[:4] == 'VGNF':
                if x.nodeRelation == 'nmod__relc':
                    fans['referents'].append(s.nodeDict[x.nodeParent].chunkNum)
                    flag = 0
            if x.nodeParent == "None":
                break
            x = s.nodeDict[x.nodeParent]
        res.append(fans)

for f in os.listdir("DATA/PROCESSED-DATA/collection/"):
    res=[]
    try:
        ofile=open("DATA/PROCESSED-DATA/collection/"+f,"rb")
        var=pickle.load(ofile)    
        r3()

        for entry in res:
            s = var.sentenceList[entry['sentence']]
            c = s.chunkList[entry['pronoun']]
            r = []
            for i in entry['referents']:
                r.append(s.chunkList[i])

            cc = "".join([var.globalWordList[i].word for i in c.wordNumList])
            rr = "".join([var.globalWordList[i].word for i in r[0].wordNumList])
            print cc + " -> " + rr

    except:
        continue