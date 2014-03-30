'''
Created on Oct 19, 2013

@author: Aakrati
'''
from UnionFind import UnionFind
from ProbabilityCalc import *
import TreeNode
import itertools
from collections import OrderedDict
import nltk
from scorers import *
Failed_due_to_perm = 0

def MinimumSpanningTree(prob,InputWords):
    """
    Return the minimum spanning tree of an undirected graph G.
    G should be represented in such a way that G[u][v] gives the
    length of edge u,v, and G[u][v] should always equal G[v][u].
    The tree is returned as a list of edges.
    """
    
   # Kruskal's algorithm: sort edges by weight, and add them one at a time.
    # We use Kruskal's algorithm, first because it is very simple to
    # implement once UnionFind exists, and second, because the only slow
    # part (the sort) is sped up by being built in to Python.
    #print "MST"
    subtrees = UnionFind()
    dictionary = {}
    tree = []
    edges = [(prob[InputWords.index(u)][InputWords.index(v)],u,v) for u in InputWords for v in InputWords]
    edges.sort()
    edges.reverse()
    for W,u,v in edges:
        if subtrees[u] != subtrees[v]:
            if u not in dictionary:
                tNode = TreeNode.TreeNode(u)
                dictionary[u] = tNode
                tNode.appendChild((v, W))
            else:
                tNode = dictionary[u]
                tNode.appendChild((v,W))
                
            if v not in dictionary:
                forParentNode = TreeNode.TreeNode(v)
                dictionary[v] = forParentNode
                forParentNode.appendParent((u, W))
            else:
                forParentNode = dictionary[v]
                forParentNode.appendParent((u,W))
            tree.append((u,v,W))
            subtrees.union(u,v)
    return tree,dictionary  

def removeZeroWtEdges(dictionary):
    orphanList=[]
    tempList=[]
    #print "zero "
    for key in dictionary.keys():
        c = dictionary[key].returnChild()
        
        for c1 in c:
            if c1[1]==-100:
                tempList.append((key,c1[0]))
    for key in tempList:
        dictionary[key[0]].removeChild((key[1],-100.0))
        dictionary[key[1]].removeParent((key[0],-100.0))
    for key in dictionary.keys():
        if not dictionary[key].returnParents() and not dictionary[key].returnChild():
            orphanList.append(key)
            del dictionary[key]
            
    return dictionary,orphanList
        
def parse1(dictionary):
    #print "parse 1"
    rootNodeLists = []
    copyDictionary = {}
    for word, tNode in dictionary.items():
        parentNodes = tNode.returnParents()
        childNodes = tNode.returnChild()
        if len(parentNodes) == 0 and len(childNodes) <=1:
            rootNodeLists.append((word, tNode))
        elif ((len(childNodes)==0 or (len(childNodes)==1 and len(dictionary[childNodes[0][0]].returnParents())==1))) and len(parentNodes)>1:
            rootNodeLists.append((word, tNode))
        elif (len(childNodes)==0 or (len(childNodes)==1 and (len(dictionary[childNodes[0][0]].returnParents())==1))) and len(parentNodes)==1 and len(dictionary[parentNodes[0][0]].returnChild())>1:
            rootNodeLists.append((word, tNode))
        elif len(parentNodes) > 1 and len(childNodes) > 1:
            copyDictionary[word] = tNode
        elif (len(parentNodes)==0 or (len(parentNodes)==1 and len(dictionary[parentNodes[0][0]].returnChild())>1)) and (len(childNodes) > 1 or (len(childNodes)==1 and (len(dictionary[childNodes[0][0]].returnParents())>1))):
            copyDictionary[word] = tNode
        elif len(parentNodes)>1 and (len(childNodes)==1 and (len(dictionary[childNodes[0][0]].returnParents())>1)):
            copyDictionary[word] = tNode
        
    for rootNode in rootNodeLists:
        rootWord, rootTNode = rootNode
        originalParentNode = rootTNode.returnParents()
        mergedWord = str(rootWord)
        
        tempWeight = -100
        while(True):
            childNodes = rootTNode.returnChild()
            if len(childNodes) == 0:
                break
            
            if len(childNodes)==1:
                grandChildNodes = dictionary[childNodes[0][0]] # getting the TNode of the child
                StepParentNodes = grandChildNodes.returnParents()
                
                if len(StepParentNodes) == 1: 
                    mergedWord = mergedWord + " " + childNodes[0][0]
                    tempWeight = tempWeight  + childNodes[0][1]
                else:
                    lastWeight = rootTNode.returnChild()[0][1]
                    #grandChildNodes.removemyparent(rootTNode.word)
                    #grandChildNodes.ParentNodesList.remove((rootTNode.word, rootTNode.returnChild()[0][1]))
                    #grandChildNodes.appendParent((mergedWord, lastWeight))
                    for keys in copyDictionary.keys():
                        for word,prob in copyDictionary[keys].returnParents():
                            if word == rootTNode.word:
                                copyDictionary[keys].removemyparent(rootTNode.word)
                                copyDictionary[keys].appendParent((mergedWord,lastWeight))
                                
                    for keys in dictionary.keys():
                        for word,prob in dictionary[keys].returnParents():
                            if word == rootTNode.word:
                                dictionary[keys].removemyparent(rootTNode.word)
                                dictionary[keys].appendParent((mergedWord,lastWeight))
                    
                    break
            else:
                lastWeight = rootTNode.returnChild()[0][1]
                for keys in copyDictionary.keys():
                    for word,prob in copyDictionary[keys].returnParents():
                        if word == rootTNode.word:
                            copyDictionary[keys].removemyparent(rootTNode.word)
                            copyDictionary[keys].appendParent((mergedWord,lastWeight))
                for keys in dictionary.keys():
                    for word,prob in dictionary[keys].returnParents():
                        if word == rootTNode.word:
                            dictionary[keys].removemyparent(rootTNode.word)
                            dictionary[keys].appendParent((mergedWord,lastWeight))            
            
                break
            rootTNode = grandChildNodes
        
        if originalParentNode:
            for keys in copyDictionary.keys():
                for word,prob in copyDictionary[keys].returnChild():
                    if word == rootWord:
                        copyDictionary[keys].removemychild(rootWord)
                        copyDictionary[keys].appendChild((mergedWord,tempWeight))
            
            for keys in dictionary.keys():
                for word,prob in dictionary[keys].returnChild():
                    if word == rootWord:
                        dictionary[keys].removemychild(rootWord)
                        dictionary[keys].appendChild((mergedWord,tempWeight))            
            
            rootTNode.ParentNodesList = originalParentNode
            dictionary[mergedWord] = rootTNode
            
                
        rootTNode.ParentNodesList = originalParentNode
        copyDictionary[mergedWord] = rootTNode
    
#     print "Key is "
#     for key in copyDictionary.keys():
#         print key#, copyDictionary[key].returnChild(), copyDictionary[key].returnParents()

    return copyDictionary

def combine(dictionary):
    #print "combine"
    rootNodeLists = []
    copyDictionary = {}
    #print "dictionary items ", dictionary.items()
    for word, tNode in dictionary.items():
        parentNodes = tNode.returnParents()
        childNodes = tNode.returnChild()
        if len(parentNodes) == 0 and len(childNodes) <=1:
            rootNodeLists.append((word, tNode))
        
    for rootNode in rootNodeLists:
        rootWord, rootTNode = rootNode
        originalParentNode = rootTNode.returnParents()
        mergedWord = str(rootWord)
        
        tempWeight = -100
        while(True):
            childNodes = rootTNode.returnChild()
            if len(childNodes) == 0:
                break
            
            if len(childNodes)==1:
                grandChildNodes = dictionary[childNodes[0][0]] # getting the TNode of the child
                StepParentNodes = grandChildNodes.returnParents()
                
                if len(StepParentNodes) == 1:
                    mergedWord = mergedWord + " " + childNodes[0][0]
                    tempWeight = tempWeight  + childNodes[0][1]
                else:
                    lastWeight = rootTNode.returnChild()[0][1]
                    for keys in copyDictionary.keys():
                        for word,prob in copyDictionary[keys].returnParents():
                            if word == rootTNode.word:
                                copyDictionary[keys].removemyparent(rootTNode.word)
                                copyDictionary[keys].appendParent((mergedWord,lastWeight))
                    for keys in dictionary.keys():
                        for word,prob in dictionary[keys].returnParents():
                            if word == rootTNode.word:
                                dictionary[keys].removemyparent(rootTNode.word)
                                dictionary[keys].appendParent((mergedWord,lastWeight))            
                
                    break
            else:
                lastWeight = rootTNode.returnChild()[0][1]
                for keys in copyDictionary.keys():
                    for word,prob in copyDictionary[keys].returnParents():
                        if word == rootTNode.word:
                            copyDictionary[keys].removemyparent(rootTNode.word)
                            copyDictionary[keys].appendParent((mergedWord,lastWeight))
                for keys in dictionary.keys():
                    for word,prob in dictionary[keys].returnParents():
                        if word == rootTNode.word:
                            dictionary[keys].removemyparent(rootTNode.word)
                            dictionary[keys].appendParent((mergedWord,lastWeight))            
            
                break
            rootTNode = grandChildNodes
        
        if originalParentNode:
            for keys in copyDictionary.keys():
                for word,prob in copyDictionary[keys].returnChild():
                    if word == rootWord:
                        copyDictionary[keys].removemychild(rootWord)
                        copyDictionary[keys].appendChild((mergedWord,tempWeight))
            
            for keys in dictionary.keys():
                for word,prob in dictionary[keys].returnChild():
                    if word == rootWord:
                        dictionary[keys].removemychild(rootWord)
                        dictionary[keys].appendChild((mergedWord,tempWeight))            
            
            rootTNode.ParentNodesList = originalParentNode
            dictionary[mergedWord] = rootTNode
            
                
        rootTNode.ParentNodesList = originalParentNode
        copyDictionary[mergedWord] = rootTNode
    
    return copyDictionary

def parse2t(dictionary,orphanList):
    #print "parse 2"
    plist = []
    phraseList = []
    for i in dictionary.keys():
        #print "keys is : ",i
        parent = list(dictionary[i].returnParents())
        nop = len(dictionary[i].returnParents())
        if nop>1:   
            #print "parent > 1 for ", i
            noc = len(dictionary[i].returnChild())
            child = list(dictionary[i].returnChild())
            
            for p in parent:
                if noc > 0:
                    for c in child:
                        new_list = [p[0],i,c[0]]
                        phraseList.append(new_list)
                else:
                    new_list = [p[0],i,""]
                    phraseList.append(new_list)
            
            #print "phraseList ",phraseList
            prob = calcTrigramProbMSBatch(phraseList)
            sortedlist =  sorted(prob,key=lambda x: x[1])
            #print "list after sorting trigrams ",sortedlist   
            maxProbChild = sortedlist[len(sortedlist)-1][0][2]
            maxProbParent = sortedlist[len(sortedlist)-1][0][0]
            
            for c in child:
                if c[0] != maxProbChild:
                    dictionary[i].removemychild(c[0])
                    dictionary[c[0]].removemyparent(i)
                    
            for p in parent:
                if p[0] != maxProbParent:
                    dictionary[i].removemyparent(p[0])
                    dictionary[p[0]].removemychild(i)
                
            phraseList = []               

    # remove node from dictionary which has 0 child and 0 parent    
    for key in dictionary.keys():
        if not dictionary[key].returnParents() and not dictionary[key].returnChild():
            orphanList.append(key)
            del dictionary[key]
    
    return dictionary

def parse3t(dictionary,orphanList):
    #print "parse 2"
    clist = []
    phraseList = []
    for i in dictionary.keys():
        #print "keys is : ",i
        child = list(dictionary[i].returnChild())
        noc = len(dictionary[i].returnChild())
        if noc>1:   
            #print "child > 1 for ", i
            nop = len(dictionary[i].returnParents())
            parent = dictionary[i].returnParents()
            
            for c in child:
                if nop > 0:
                    new_list = [parent[0][0],i,c[0]]
                    phraseList.append(new_list)
                else:
                    new_list = ["",i,c[0]]
                    phraseList.append(new_list)
            
            prob = calcTrigramProbMSBatch(phraseList)
            sortedlist =  sorted(prob,key=lambda x: x[1])  
            maxProbChild = sortedlist[len(sortedlist)-1][0][2]
            for c in child:
                if c[0] is not maxProbChild:
                    dictionary[i].removemychild(c[0])
                    dictionary[c[0]].removemyparent(i)          
                    
            phraseList = []               

    # remove node from dictionary which has 0 child and 0 parent    
    for key in dictionary.keys():
        if not dictionary[key].returnParents() and not dictionary[key].returnChild():
            orphanList.append(key)
            del dictionary[key]
    
    return dictionary

def parse2(dictionary,orphanList):
    #print "parse 2"
    plist = []
    for i in dictionary.keys():
        nop = len(dictionary[i].returnParents())
        if nop>1:
            noc = len(dictionary[i].returnChild())
            plist.append((i,noc))
    
    sortedlist = sorted(plist,key=lambda x: x[1])
    # Take highest prob parent, discard others
    for i in sortedlist:
        node = dictionary[i[0]].returnParents()
        sortednode = sorted(node,key=lambda x: x[1])
        for j in range(len(sortednode)-1):
            dictionary[i[0]].removeParent(sortednode[j])
            if dictionary[sortednode[j][0]]:
                dictionary[sortednode[j][0]].removemychild(i[0])

    # remove node from dictionary which has 0 child and 0 parent    
    for key in dictionary.keys():
        if not dictionary[key].returnParents() and not dictionary[key].returnChild():
            orphanList.append(key)
            del dictionary[key]
    
    return dictionary
    
    
def remChild(dictionary,orphanList):
    #print "remChild"
    clist = []
    for i in dictionary.keys():
        noc = len(dictionary[i].returnChild())
        if noc>1:
            nop = len(dictionary[i].returnParents())
            clist.append((i,nop))

    sortedlist = sorted(clist,key=lambda x: x[1])
    
    for i in sortedlist:
        node = dictionary[i[0]].returnChild()
        sortednode = sorted(node,key=lambda x: x[1])
        for j in range(len(sortednode)-1):
            
            dictionary[i[0]].removeChild(sortednode[j])
            dictionary[sortednode[j][0]].removemyparent(i[0])
            mergedWord = i[0] + sortednode[-1][0]
        
    # remove node from dictionary which has 0 child and 0 parent    
    for key in dictionary.keys():
        if not dictionary[key].returnParents() and not dictionary[key].returnChild():
            orphanList.append(key)
            del dictionary[key]
    
    return dictionary
    
def parse4(dictionary,orphanList):
    #print "parse 4"
    for key in dictionary.keys():
        if dictionary[key].returnParents() and dictionary[key].returnChild():
            print "!!!! this shd never happen!!!"
        else:
            orphanList.append(key)
            
    return orphanList
            
def permute(final):
    #print "permute"
    perm = itertools.permutations(final)
    return perm

class LargePermException(Exception):
    def __init__(self, value):
        self.parameter = value
    def __str__(self):
        return repr(self.parameter)

def topN2Sentence(permSent, InputWords, orphanList,probPhrases):
    #print "topn2 sent"
    topSents = []
    rank = []
    totPerm = 0
    length = len(InputWords)
    for sent in permSent:
        totPerm = totPerm+1
        score = 0
        if totPerm > length**4:
            raise LargePermException("large no of perm")
        for i in range(len(orphanList)-1):
            index1 = orphanList.index(sent[i])
            index2 = orphanList.index(sent[i+1])
            score = score + probPhrases[index1][index2]
        rank.append((score,sent))
    #print "before sort"
    sortedList = sorted(rank,key=lambda x: x[0])
    length = len(InputWords)

    for i in range(min(totPerm,length**2)):
        topSents.append(sortedList[totPerm - i -1][1])
 
    return topSents

def tokenizeRankedSentence(finalSents, rankedSents):
    #"tokenise"
    rankedSentList=[]
    rankedTokenizedList=[]
    finalList=[]
    for sent in rankedSents:
        str =""
        for phrase in sent:
            str=str+" "+phrase
        rankedSentList.append(str)
        
    for sent in rankedSentList:
        tok = nltk.word_tokenize(sent)
        rankedTokenizedList.append(tok)
        
    finalList = rougeS(finalSents, rankedTokenizedList)
    finalList =  sorted(finalList,key=lambda x: x[0])
    finalListL = rougeL(finalSents, rankedTokenizedList)
    finalListL =  sorted(finalListL,key=lambda x: x[0])
    finalListN = ngramCo(finalSents, rankedTokenizedList)
    finalListN =  sorted(finalListN,key=lambda x: x[0])
    
    return [finalList[len(finalList)-1],finalListL[len(finalListL)-1],finalListN[len(finalListN)-1]]
