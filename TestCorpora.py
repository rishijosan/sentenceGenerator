'''
Created on Nov 10, 2013

@author: anchalagarwal
'''
import cPickle as pickle

sent_pic = None
with open('/Users/anchalagarwal/Documents/reuters_sents_mod2.pk', 'rb') as input:
    sent_pic = pickle.load(input)

print sent_pic[700]