from __future__ import division
import pandas as pd
import numpy as np
from collections import defaultdict
import cPickle as p


transitionDictionary=dict()
emissionDictionary=dict()
countEmissionDictionary=dict()
countTransitionDictionary=dict()
WordDictionary=defaultdict(list)
emissionP=[]


with open("/Users/manasranjanmahanta/Desktop/hw6-dev-train/catalan_corpus_train_tagged.txt","r")as f:
    for line in f:
        prevTag='START'
        currTag=""
        word=""
        for y in line.split():
            word=y.rsplit("/",1)[0]
            currTag=y.split("/")[-1]
            emissionKey=y
            transitionKey=prevTag+"|"+currTag
            if(word in WordDictionary):
                listTags=WordDictionary[word]
                if(currTag not in listTags):
                     WordDictionary[word].append(currTag)
            else:
                WordDictionary[word].append(currTag)
            if(prevTag in countTransitionDictionary):
                countTransitionDictionary[prevTag]+=1
            else:
                countTransitionDictionary[prevTag]=1

            if(currTag in countEmissionDictionary):
                countEmissionDictionary[currTag]+=1
            else:
                countEmissionDictionary[currTag]=1

            if(emissionKey in emissionDictionary):
                emissionDictionary[emissionKey]+=1
            else:
                emissionDictionary[emissionKey]=1
            if(transitionKey in transitionDictionary):
                transitionDictionary[transitionKey]+=1
            else:
                transitionDictionary[transitionKey]=1
            prevTag=currTag

        currTag='END'
        if(prevTag in countTransitionDictionary):
                countTransitionDictionary[prevTag]+=1
        else:
                countTransitionDictionary[prevTag]=1
        transitionKey=prevTag+"|"+'END'
        if(transitionKey in transitionDictionary):
                transitionDictionary[transitionKey]+=1
        else:
                transitionDictionary[transitionKey]=1








model=[transitionDictionary,countTransitionDictionary,emissionDictionary,countEmissionDictionary,WordDictionary]
p.dump(model,open("modelp.txt","wb"))

'''
targetT=open('hmmModel.txt','w')
targetT.write(str(transitionDictionary)+"\n")
targetT.write(str(countTransitionDictionary)+"\n")
targetT.write(str(emissionDictionary)+"\n")
targetT.write(str(countEmissionDictionary)+"\n")
targetT.write(str(WordDictionary)+"\n")
targetT.close()'''






'''
SetWords=set(words)
ListWords=list(SetWords)
SetTags=set(tags)
ListTags=list(SetTags)
#print len(SetWords)

StartSetTags=SetTags|set(["START"])

stateTransitionmatrix=np.zeros(shape=(len(StartSetTags),len(SetTags)))
emissionTransitionmatrix=np.zeros(shape=(len(StartSetTags),len(SetWords)))

print emissionTransitionmatrix.shape


dictionaryTag={}
dictionaryWord={}

for i in range(0,len(ListTags)):
    dictionaryTag[str(ListTags[i])]=i

for i in range(0,len(ListWords)):
    dictionaryWord[str(ListWords[i])]=i


#print dictionaryTag
#print dictionaryWord[';']

for x in tags:
    if(x=='START'):
        rowIndex=dictionaryTag['START']
        continue
    colIndex=dictionaryTag[x]
    stateTransitionmatrix[rowIndex][colIndex]+=1
    rowIndex=colIndex

#print stateTransitionmatrix

for m in emissionP:
    tempy=m.rsplit("/",1)[0]
    y=dictionaryWord[tempy]
    tempx=m.split("/")[-1]
    x=dictionaryTag[tempx]
    emissionTransitionmatrix[x][y]+=1


print emissionTransitionmatrix
print np.count_nonzero(emissionTransitionmatrix)
np.savetxt("MatrixHMM",emissionTransitionmatrix)

'''
