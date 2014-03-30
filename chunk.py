# Author : Rishi Josan

import nltk
import itertools
from collections import OrderedDict
import urllib
import urllib2
import re


def permute(final):
    perm = itertools.permutations(final)
    return perm

# Categorize the determinants, adjectives, nouns and verbs in order()
def categorizeSent(sent):
    nn  = [[] for i in range(4)]
    # nn , vb, dt, jj
    count = 0
    
    for item in sent:
        
        if item[1] == 'DT' or item[1] =='PRP' :
            nn[0].append(count)
        elif item[1] == 'JJ' or item[1] == 'JJS' or item[1] == 'JJR':
            nn[1].append(count)
        elif item[1] == 'NN'  or item[1] == 'NNS' or item[1] == 'NNP' or item[1] == 'NNPS':
            nn[2].append(count)
        elif item[1] == 'VBD' or item[1] == 'VB' or item[1] == 'VBZ' or item[1] == 'VBG' or item[1] == 'VBP' or item[1] == 'VBN':
            nn[3].append(count)
        count = count + 1
    
    return nn


# Find all permutations of JJs
def JJPerm(catSent, orgSent):
    
    JJPerms = list()
    finalJJPerms = list()
    temp = list()
    
    for i in range(len(catSent)):
        JJPerms.append(list(itertools.permutations(catSent , i+1)))
   
    for i in JJPerms:
        for j in i:
            for k in j:
                temp.append(orgSent[k][0])
            finalJJPerms.append(temp)
            temp = []
            
    return finalJJPerms


def JJsList(JJP):
    JJList = list()
    JJs = ""
    for i in JJP:
        noWords = len(i)
        for j in i:
            JJs = JJs  + j + " "
        JJList.append(JJs[0:len(JJs)-1])
        JJs = ""
    return JJList

def calcProbMSBatchStr(InputWords):
    string = ""
    for word1 in InputWords:
        for word2 in word1:
            string = string+word2+" "+"\n"                               
    string = string[0:len(string)-2]
    probs =  urllib2.urlopen(urllib2.Request('http://web-ngram.research.microsoft.com/rest/lookup.svc/bing-body/apr10/5/jp?u=d3d00cdb-81f4-4260-8cc0-f461b87ef7c8&format=json',string)).read()
    
    pattern = re.compile('\s*,\s*')
    final_str = pattern.split(probs[1:len(probs)-1])
    return final_str




def findNPs(refSent):

    nn = categorizeSent(refSent)
    #print nn
    np = list()
    
    #Add consecutive nouns'
    #===========================================================================
    # JJPermsN = JJPerm(nn[2], refSent)
    # JJListN =  JJsList(JJPermsN)
    # print JJListN
    #===========================================================================
    
    # 0 - DT, 1 - JJ, 2 - NN
    #DT and JJ Do not Exist, NN Exist, HANDLE CONSECUTIVE NOUNS!
    #if len(nn[0]) == 0 and len(nn[1]) == 0 and len(nn[2]) > 0:
    for item in nn[2]:
        np.append([refSent[item][0]])
    #DT exist , no JJ , NN Exist , HANDLE SAME DTs  
    #elif len(nn[0]) > 0 and len(nn[1]) == 0 and len(nn[2]) > 0:
    for i in nn[0]:
        for j in nn[2]:
            np.append([refSent[i][0] + ' ' + refSent[j][0]] )
    #             np.append([refSent[i][0] + refSent[j][0]] )
    # JJ Exist, Handling DT or Not, NN Exist 
    if len(nn[1]) > 0 and len(nn[2]) > 0:
        JJPerms = JJPerm(nn[1], refSent)
        JJList =  JJsList(JJPerms)
        if len(nn[0]) > 0: 
            #print "In Part1" 
            for i in nn[0]:
                for j in nn[2]:
                    for k in JJList:
                        np.append([refSent[i][0] + " " + k + " " + refSent[j][0]] )
        else:
            #print "In Part2" 
            for j in nn[2]:
                for k in JJList:
                    np.append([k + " " + refSent[j][0]])
            
    return np





def gimmeSNPs(sentTok):
    sent_pos = nltk.pos_tag(sentTok)
    #print sent_pos
    nps =  findNPs(sent_pos) 
    #print nps
    probs =  calcProbMSBatchStr(nps)
    #print probs
    npProbs = list()
    count = 0
    for i in nps:
        noWords =  i[0].count(' ') + 1
        if noWords > 1:
            i.append(float(probs[count])/noWords)
            npProbs.append(i)
            count = count + 1
    #print "This is the shit"
    #print npProbs
    sorted_npProbs = sorted(npProbs, key=lambda x: x[1])
    return sorted_npProbs
    
# orgToks is the original sentence tokenized 



def topNPs(sentToks):
    finalNps = list()
    
    for q in range(1,3):
        sorted_npProbs1 = gimmeSNPs(sentToks) 
        #print sorted_npProbs1
    
        if len(sorted_npProbs1) != 0:
            final_np = sorted_npProbs1[len(sorted_npProbs1)-1]
            finalNps.append(final_np)
            
            toksFinal = nltk.word_tokenize(final_np[0])
                
            for word in toksFinal:
                ind = sentToks.index(word)
                del sentToks[ind]
             
            #print sentToks
            
    return finalNps

         
orgSent = 'the little yellow dog barked at the blue greedy cat in london'
orgToks = nltk.word_tokenize(orgSent)

newSent = 'market tom filthy went the to'
newToks = nltk.word_tokenize(newSent)

sent = "she sells sea shells at the sea shore"
new = nltk.word_tokenize(sent)

sent1 = "Judge Curry set the interest rate at 9%"
sentnew = nltk.word_tokenize(sent1)
print topNPs(sentnew)
        
            



#===============================================================================
# sentence = [("the", "DT"), ("little", "JJ"), ("yellow", "JJ"), ("dog", "NN"), ("barked", "VBD"), ("at", "IN"), ("the", "DT"), ("cat", "NN")]
# pattern = "NP: {<DT>?<JJ>*<NN>}"
# NPChunker = nltk.RegexpParser(pattern)
# with open('/home/rishi/brown_sents.pk', 'rb') as input:
#         sent_pic = pickle.load(input)
# goodSent =  sent_pic[3222]
# testSent = ['tom' , 'went' ,'to' ,'the' , 'filthy' , 'market']
# testSent_pos = nltk.pos_tag(testSent)
# print testSent_pos       
#===============================================================================

#===============================================================================
# testSentJ = permute(testSent)
# prospSent = list()
# for sent in testSentJ:
#     prospSent.append(nltk.pos_tag(sent))
#     
# checkSent =  prospSent[460]
# print checkSent
#===============================================================================

# result1 = NPChunker.parse(testSent_pos)
# result2 = NPChunker.parse(new)
# print result1
# print result2

    


