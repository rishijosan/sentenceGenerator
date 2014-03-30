# Author : Rishi Josan

from collections import OrderedDict
import nltk
import urllib
import urllib2
import re

#--------------------------------------------------- Test Sentences-------------------------------------------------------#


finSent = nltk.word_tokenize('No price for the new shares has been set')
newList = [' price for the new shares No has been set', ' price for the new shares has been set No', ' has been set No price for the new shares', ' has been set No shares price for the new', ' shares has been set No price for the new', ' price for the new No shares has been set', ' No price for the new shares has been set', ' has been set shares No price for the new', ' price for the new has been set No shares', ' has been set price for the new shares No', ' No shares has been set price for the new', ' shares No has been set price for the new', ' price for the new No has been set shares', ' No has been set price for the new shares', ' shares No price for the new has been set', ' No has been set shares price for the new', ' shares price for the new No has been set', ' has been set price for the new No shares', ' price for the new has been set shares No', ' No shares price for the new has been set', ' shares has been set price for the new No', ' has been set shares price for the new No', ' shares price for the new has been set No', ' No price for the new has been set shares']
finList = list()
for item in newList:
    tok = nltk.word_tokenize(item)
    finList.append(tok)

#--------------------------------------------------- End of Test Sentences------------------------------------------------#


#----------------------------------------------Support Functions-----------------------------------------------------------#

#===============================================================================
# Function to create all possible subsequences for a sentences. Ignoring one word subsequences
#===============================================================================
def subSeq(refSent):
    refLen = len(refSent)
    subSeqDict = OrderedDict()
    for i in range(refLen):
        for j in range(i+1 , refLen+1):
            tempStr = ""
            for k in refSent[i+1:j]:
                tempStr = tempStr + '_' + k
                
            if (len(tempStr[1:len(tempStr)]) != 0):    
                subSeqDict.update({refSent[i] + '_' + tempStr[1:len(tempStr)] : True})
                
    return subSeqDict

#===============================================================================
# Function to calculate 5 gram probabilities of a list of sentences
#===============================================================================
def calcProbMS(InputWords):
    string = ""
    
    for word1 in InputWords:
        sent = ""
        for word2 in word1:
            sent = sent+ " " +word2
        string = string+sent+"\n"                                 
    string = string[0:len(string)-2]
    #print string
    probs =  urllib2.urlopen(urllib2.Request('http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/apr10/5/jp?u=d3d00cdb-81f4-4260-8cc0-f461b87ef7c8&format=json',string)).read()
    
    pattern = re.compile('\s*,\s*')
    final_str = pattern.split(probs[1:len(probs)-1])
    return final_str


#----------------------------------------------End of Support Functions-----------------------------------------------------------#




#===============================================================================
# Returns the Rouge score based on Skip bigrams without any limitation on the gap 
#===============================================================================
def rougeS(refSent , sents):
    skip2 = list()
    newDict = OrderedDict()
    refLen = len(refSent)
    noSents = len(sents)
    noComb = (refLen*(refLen - 1)/2)

    
    for i in range(refLen):
        for j in range(i+1 , refLen):
            newDict.update({refSent[i] + '_' + refSent[j] : True})
            
    
    for sent in sents:
        sentLen = len(sent)
        count = 0
        for p in range(sentLen):
            for q in range(p+1 , sentLen):
                if newDict.has_key(sent[p] + '_' + sent[q]):
                    count = count + 1
        skip2.append((float(count)/noComb,sent))
                    
                    
    
    return skip2
        
# rougeS test
 



#===============================================================================
# Returns the fraction of bigrams in candidate sentence present in the original sentence
#===============================================================================
def ngramCo(refSent , sents):
    coOcc = list()
    newDict = OrderedDict()
    refLen = len(refSent) - 1

    for i in range(refLen):
        newDict.update({refSent[i] + '_' + refSent[i+1] : True})
            
    #print newDict
    
    for sent in sents:
        sentLen = len(sent)
        count = 0
        for p in range(sentLen-1):
            if newDict.has_key(sent[p] + '_' + sent[p+1]):
                count = count + 1
        coOcc.append((float(count)/refLen,sent))
                     
                     
     
    return coOcc
    

# ngramCo test

#print ngramCo(new1 , new2 )
     





#===============================================================================
# Returns the length of the Longest common subsequence of the candidate sentence divided by the length of the reference sentence
#===============================================================================
def rougeL(refSent , sents):
    rougeLScore = list()
    refLen = len(refSent)

    #print refLen
    
    refSubSeq = subSeq(refSent)
    #print refSubSeq
    
    noSubSeq = len(refSubSeq)
    #print noSubSeq
    
    #
    for sent in sents:
        sentSubSeq = subSeq(sent)
        #print sentSubSeq
        lcsLen = 1   
        for item in sentSubSeq:
            if refSubSeq.has_key(item):
                if (item.count('_')+1 > lcsLen):
                    lcsLen=item.count('_')+1
        rougeLScore.append((float((lcsLen))/refLen,sent))
        
    return rougeLScore
                
    
# RougeL Test

#print rougeL(new1, new2)


#===============================================================================
# Returns the 5 gram probability of the candidate sentence divided by the 5 gram probability of the reference sentence
#===============================================================================
def ngramProb(refSent , sents):

    finScore = list()
    sent = ""
    for word in refSent:
            sent = sent+ " " +word
    refProb =  urllib2.urlopen(urllib2.Request('http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/apr10/5/jp?u=d3d00cdb-81f4-4260-8cc0-f461b87ef7c8&format=json',sent)).read()
        
    refProbF = float(refProb[1:(len(refProb)-1)])
    probs = calcProbMS(sents)
    
    for item in probs:
        finScore.append(refProbF/float(item))
        
    return finScore

#ngram Test

