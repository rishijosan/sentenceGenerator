'''
Created on Oct 19, 2013

@author: anchalagarwal
'''
'''
Created on Oct 19, 2013

@author: Aakrati
'''
import random

from DependencyTree import *
from ProbabilityCalc import *
import cPickle as pickle
import xlwt

def sentenceRealiser(InputWords,pos):
    
    refSent = list(InputWords)
    random.shuffle(InputWords, random.random)
    print InputWords
    prob = calcProbMSBatch(InputWords)
    tree, dictionary = MinimumSpanningTree(prob,InputWords)
         
    dictionary,orphanList = removeZeroWtEdges(dictionary)     
    
    dictionary = parse1(dictionary)    

    dictionary = parse2t(dictionary,orphanList)

    dictionary = parse3t(dictionary,orphanList)

    dictionary = combine(dictionary)
        
    orphanList = parse4(dictionary,orphanList)   
    perm = permute(orphanList)
#     for sent in perm:
#         print sent
     
    probPhrases = calcProbMSBatch(orphanList)
    top = topN2Sentence(perm, InputWords, orphanList,probPhrases)
    finalSentences=tokenizeRankedSentence(refSent, top)
    print "finalSentences:" +str(pos) + "*****" + str(finalSentences) + "** correct sent **" +str(refSent)
    return finalSentences

def main():
    sent_pic = None
    with open('/Users/anchalagarwal/Desktop/CompBio/brown_sents.pk', 'rb') as input:
        sent_pic = pickle.load(input)
        
    count = 0
    wb = xlwt.Workbook()
    ws = wb.add_sheet('A Test Sheet')
    rowCount =2
    f = open('/Users/anchalagarwal/Desktop/CompBio/trigram_reuters_error3.txt', 'w')
    ws.write(0,0,"Original Sentence")
    ws.write(0,1,"Original length")
    ws.write(0,2,"rougeS Sentence")
    ws.write(0,3,"rougeS Score")
    ws.write(0,4,"rougeL Sentence")
    ws.write(0,5,"rougeL Score")
    ws.write(0,6,"ngramCo Sentence")
    ws.write(0,7,"ngramCo Score")
    Failed_due_to_perm=0
    
    for i in range(1, 2):
#        for phrase in sent_pic[i]:
#            if phrase == "...":
#                continue
        final_str =""
        final_str_L =""
        final_str_N =""
        ref_str=""
        try:
            refSent = list(sent_pic[i]) 
            #InputWords = sent_pic[i]  
            InputWords = "When in the course of human events it becomes necessary for one nation to dissolve its bonds"
            InputWords =  word_tokenize(InputWords);
            finalSentence = sentenceRealiser(InputWords,i)  
            #print finalSentence              
            for phrase in refSent:
                ref_str=ref_str+" "+phrase
            #print finalSentence  
            for phrase in refSent:
                ref_str=ref_str+" "+phrase
            for phrase in finalSentence[0][1]:
                final_str=final_str+" "+phrase
            for phrase in finalSentence[1][1]:
                final_str_L=final_str_L+" "+phrase
            for phrase in finalSentence[2][1]:
                final_str_N=final_str_N+" "+phrase
                
            #print i,"-> ",final_str
            ws.write(rowCount,0,ref_str)
            #print ref_str
            ws.write(rowCount,1,len(sent_pic[i]))
            
            #rougeS
            ws.write(rowCount,2,final_str)
            ws.write(rowCount,3,finalSentence[0][0])
            #rougeL
            ws.write(rowCount,4,final_str_L)
            ws.write(rowCount,5,finalSentence[1][0])
            #ngramCo
            ws.write(rowCount,6,final_str_N)
            ws.write(rowCount,7,finalSentence[2][0])
            rowCount = rowCount+1
        except IndexError:
            count= count+1
        except LargePermException:
            Failed_due_to_perm = Failed_due_to_perm +1
            f.write("large perm error occurred for sentence "+str(i) + "\n")
        except:
            pass
            
    f.close()        
    wb.save('/Users/anchalagarwal/Desktop/compBio_results/Trigram_results_brown.xls')       
    print "no of connection failure",count
    print "no of sent having large no of perm ", Failed_due_to_perm 
            
if __name__ == '__main__':
    main()
