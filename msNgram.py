#Check out link http://web-ngram.research.microsoft.com/info/api.html
import MicrosoftNgram as mn

s = mn.LookupService()
s = mn.LookupService(model='bing-body/apr10/5')

#These will get conditional probabilities of the last word following the phrase

#===============================================================================
# print s.GetConditionalProbability('Hello World')
# print s.GetConditionalProbability('Hello me')
# print s.GetConditionalProbability('Brown Fox')
# print s.GetConditionalProbability('Musical Fox')
# print s.GetConditionalProbability('It is I')
#===============================================================================


#This gives suggestions for the next words
#for t in s.Generate('The quick brown fox', maxgen=5): print t


#This gives joint probability
#===============================================================================
# print s.GetJointProbability('Tom went to the market')
# print s.GetJointProbability('market went Tom the to')
# print s.GetJointProbability('to Tom the market went')
# print s.GetJointProbability('the Tom went to market')
# print s.GetJointProbability('went market Tom to the')
#===============================================================================

#===============================================================================
# print s.GetJointProbability('They refuse to give us the refuse permit')
# print s.GetJointProbability('the give refuse they permit us refuse to')
# print s.GetJointProbability('the give us permit refuse refuse to they')
# print s.GetJointProbability('us they refuse the permit refuse give to')
# print s.GetJointProbability('to us they the refuse give refuse permit')
#===============================================================================

print s.GetJointProbability('cat this running on is the field')
print s.GetJointProbability('this cat is running on the field')

print s.GetJointProbability('tom went to the market')
print s.GetJointProbability('the market went to tom')
print s.GetJointProbability('market went to the tom')
print s.GetJointProbability('the Tom went to market')
