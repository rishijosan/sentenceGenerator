'''
Created on Oct 19, 2013

@author: Aakrati
'''
import nltk
import nltk.data
import MicrosoftNgram as mn
import time
import os
import re
import sys
import urllib
import urllib2
from nltk.corpus import brown
from nltk.corpus import treebank
from nltk.collocations import  *
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

def calcProb(InputWords):
    probMatrix = []
    count=0
    countMatrix = countBigram(InputWords)
    
  #  print countMatrix
    
    for word1 in InputWords:
        #print word1[0]+'/'+word1[1]
        count_word1 = nltk.corpus.treebank.tagged_words().count(word1)
        #print "word is : "+str(word1)+" its count is "+str(count_word1)
        i=InputWords.index(word1)
        probMatrix.append([])
        for word2 in InputWords:
            j=InputWords.index(word2)
            if not count_word1 == 0:
                probMatrix[i].append(float(countMatrix[i][j])/float(count_word1))
            else:
                probMatrix[i].append(0)
            
    return probMatrix

def calcProbMS(InputWords):
    probMatrix = []
    count=0
    s = mn.LookupService()
    s = mn.LookupService(model='bing-body/apr10/5')
    print "calcProbMS"
  #  print countMatrix
    for word1 in InputWords:
        i=InputWords.index(word1)
        probMatrix.append([])
        for word2 in InputWords:
            j = InputWords.index(word2)
            if i!=j:
                probMatrix[i].append(s.GetJointProbability(word1+" "+word2))     
            else:
                probMatrix[i].append(-100)    
                         
    return probMatrix

def calcProbMSBatch(InputWords):
    #print "calcProbMS batch"
    probMatrix = []
    count =0
    string = ""
    for word1 in InputWords:
        for word2 in InputWords:
            string = string+word1+" "+word2+"\n"                            
    string = string[0:len(string)-2]
    start = time.time()
    #newVar =  urllib2.urlopen(urllib2.Request('http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/apr10/5/jp?u=8ed951ac-10ab-47c3-ab4f-35daea6da47d8&format=json',string)).read()
    newVar =  urllib2.urlopen(urllib2.Request('http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/apr10/5/jp?u=d3d00cdb-81f4-4260-8cc0-f461b87ef7c8&format=json',string)).read()
    stop = time.time()
    pattern = re.compile('\s*,\s*')
    final_str = pattern.split(newVar[1:len(newVar)-1])
    for word1 in InputWords:
        i=InputWords.index(word1)
        probMatrix.append([])
        for word2 in InputWords:
            j = InputWords.index(word2)
            if i!=j:
                probMatrix[i].append(float(final_str[count]))    
            else:
                probMatrix[i].append(-100)    
            count = count+1             
    return probMatrix
          
def calcTrigramProbMSBatch(phraseList):
    #print "calcProbMS batch"
    probMatrix = []
    string = ""
    for phrase in phraseList:
        string = string+phrase[0]+" "+phrase[1]+" "+phrase[2]+"\n"                            
    string = string[0:len(string)-2]
    start = time.time()
    newVar =  urllib2.urlopen(urllib2.Request('http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/apr10/5/jp?u=d3d00cdb-81f4-4260-8cc0-f461b87ef7c8&format=json',string)).read()
    stop = time.time()
    pattern = re.compile('\s*,\s*')
    final_str = pattern.split(newVar[1:len(newVar)-1])
    count=0
    for phrase in phraseList:
        probMatrix.append((phrase,float(final_str[count])))    
        count = count+1             
    return probMatrix
          
def countBigram(InputWords):
    count=0
    countMatrix=[]
    #nltk.corpus.brown.tagged_words()
    for w1 in InputWords:
        i=InputWords.index(w1)
        countMatrix.append([])
        for w2 in InputWords:
            i=InputWords.index(w1)
            j=InputWords.index(w2)
            countMatrix[i].append(0)
            
    for w1, w2 in nltk.bigrams(nltk.corpus.treebank.tagged_words()):
        if w1 in InputWords and w2 in InputWords:
            i=InputWords.index(w1)
            j=InputWords.index(w2)
            countMatrix[i][j]=countMatrix[i][j]+1
    
    return countMatrix

def sentenceRealiser(probMatrix,InputWords):
    all_sentences = {}
    col =0 
    for w1 in InputWords:
        word_index = InputWords.index(w1)
        all_sentences[InputWords[word_index]]=[InputWords[word_index],1]
        for i in range(len(InputWords)-1):
            max_for_this_word = 0
            max_index = 0
            for col in range(len(InputWords)):
                if col != word_index:
                    if probMatrix[word_index][col] > max_for_this_word:
                        max_for_this_word = probMatrix[word_index][col]
                        max_index = col
                
            all_sentences[w1][0]= all_sentences[w1][0]+" " +InputWords[max_index]
            all_sentences[w1][1]*=max_for_this_word
            word_index = max_index
            
    return all_sentences

def tagWords(InputWords):
    taggedList = nltk.pos_tag(InputWords)   
    return taggedList
