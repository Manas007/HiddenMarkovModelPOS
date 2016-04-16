from __future__ import division
import pandas as pd
import numpy as np
from collections import defaultdict
import ast
import cPickle as p
import math

transitionDictionary=dict()
countTransitionDictionary=dict()
emissionDictionary=dict()
countEmissionDictionary=dict()
WordDictionary=defaultdict(list)

listModels=[]

listModels=p.load(open("modelp.txt","rb"))
transitionDictionary=listModels[0]
countTransitionDictionary=listModels[1]
emissionDictionary=listModels[2]
countEmissionDictionary=listModels[3]
WordDictionary=listModels[4]
setTags=countTransitionDictionary.keys()

with open("/Users/manasranjanmahanta/Desktop/hw6-dev-train/catalan_corpus_dev_raw.txt","r")as f,open("hmmoutput.txt","w")as r:
    for line in f:
        prevTag='START'
        count=0
        viterbi=[]
        backpointer=[]
        for word in line.split():
            count+=1
            tempTags=WordDictionary[word]
            if not tempTags:
                tempTags=setTags
            if(count==1):
                first_viterbi={}
                first_backpointer={}
                for tag in tempTags:
                    if tag=='START':
                        continue
                    if prevTag+"|"+tag in transitionDictionary:
                            Num1=transitionDictionary[prevTag+"|"+tag]
                    else:
                            Num1=0.000001
                    Den1=countTransitionDictionary[prevTag]
                    if word+"/"+tag in emissionDictionary:
                        Num2=emissionDictionary[word+"/"+tag]
                    else:
                        Num2=0.000001
                    Den2=countEmissionDictionary[tag]
                    Prob=(Num1/Den1)*(Num2/Den2)
                    first_viterbi[tag]=Prob
                    first_backpointer[ tag ] = 'START'
                viterbi.append(first_viterbi)
                backpointer.append(first_backpointer)
            else:
                this_viterbi = {}
                this_backpointer = {}
                prev_viterbi = viterbi[-1]
                for tag in tempTags:
                    if tag=='START':
                        continue
                    max=0
                    best_previous=""
                    for key in prev_viterbi:
                        if key+"|"+tag in transitionDictionary:
                            Num1=transitionDictionary[key+"|"+tag]
                        else:
                            Num1=0.000001
                        Den1=countTransitionDictionary[key]
                        if word+"/"+tag in emissionDictionary:
                            Num2=emissionDictionary[word+"/"+tag]
                        else:
                            Num2=0.000001
                        Den2=countEmissionDictionary[tag]
                        if prev_viterbi[key]< math.pow(10,-300):
                            prev_viterbi[key]*=math.pow(10,100)
                        Prob=prev_viterbi[key]*(Num1/Den1)*(Num2/Den2)
                        if (Prob>max):
                            max=Prob
                            best_previous=key
                    #best_previous = max(prev_viterbi.keys(),key = lambda prevtag:prev_viterbi[prevtag] * (transitionDictionary[prevtag+"|"+tag]/countTransitionDictionary[prevtag])*(emissionDictionary[word+"/"+tag]/countEmissionDictionary[tag]))
                    this_viterbi[tag] = max#prev_viterbi[best_previous] * (transitionDictionary[best_previous+"|"+tag]/countTransitionDictionary[best_previous])*(emissionDictionary[word+"/"+tag]/countEmissionDictionary[tag])
                    this_backpointer[tag] = best_previous
                viterbi.append(this_viterbi)
                backpointer.append(this_backpointer)

        #print backpointer
        prev_viterbi = viterbi[-1]
        currMax=0
        best_previous=""
        for key in prev_viterbi:
            transitionKey=key+"|"+"END"
            if(transitionKey not in transitionDictionary):
               value=0;
            else:
               value=prev_viterbi[key]*(transitionDictionary[transitionKey]/countTransitionDictionary[key])
            if(value>currMax):
                currMax=value
                best_previous=key



        #prob_tagsequence = prev_viterbi[ best_previous ] * cpd_tags[ best_previous].prob("END")

        # best tagsequence: we store this in reverse for now, will invert later
        best_tagsequence = [ "END", best_previous ]
        # invert the list of backpointers
        backpointer.reverse()

        # go backwards through the list of backpointers
        # (or in this case forward, because we have inverter the backpointer list)
        # in each case:
        # the following best tag is the one listed under
        # the backpointer for the current best tag
        current_best_tag = best_previous
        print line
        if(line is 'SI base units'):
            print "hello"
        for bp in backpointer:
            best_tagsequence.append(bp[current_best_tag])
            current_best_tag = bp[current_best_tag]

        tempL=best_tagsequence[::-1]
        tempx=tempL[1:-1]
        #print tempx
        count1=0
        for word in line.split():
            r.write(word+"/"+tempx[count1]+" ")
            count1+=1
        r.write("/n")





