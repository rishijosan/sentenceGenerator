'''
Created on Oct 20, 2013

@author: anchalagarwal
'''

class TreeNode(object):
    '''
    classdocs
    '''


    def __init__(self, Word):
        self.ParentNodesList = []
        self.ChildNodesList = []
        self.word = Word
    
    def appendParent(self,parentTuple):
        self.ParentNodesList.append(parentTuple)
        return
    
    def appendChild(self,childTuple):
        self.ChildNodesList.append(childTuple)
        return
    
    def returnParents(self):
        return self.ParentNodesList
    
    def returnChild(self):
        return self.ChildNodesList
    
    def removeChild(self,child):
        self.ChildNodesList.remove(child)
        return self
    
    def removeParent(self,parent):
        self.ParentNodesList.remove(parent)
        return self
      
    def removemychild(self,child):
        for i in self.ChildNodesList:
            if i[0] == child:
                self.removeChild(i)
                return
            
    def removemyparent(self,parent):
        for i in self.ParentNodesList:
            if i[0] == parent:
                self.removeParent(i)
                return