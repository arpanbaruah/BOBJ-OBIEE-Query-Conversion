from xml.dom import minidom
from com.inter.generic.randomgenerator import randomstring
import re



class readboxml_operand:
    
    def __init__(self,filename):
        operandfileName = filename
        self.operandfile = open(operandfileName,'w')
        

    def handleQueries(self, boquery):
        
        self.boquery= boquery
        Query = self.boquery.getElementsByTagName("Query")
        self.handleQuery(Query)
    

    def handleQuery(self,query):
        self.query = query
        for que in self.query:
            Filters = que.getElementsByTagName("Filters")
            if Filters:
                self.handleFilters(Filters)
        self.operandfile.close()
        

    def handleFilters(self,Filters):
        self.Filters = Filters
        for fil in self.Filters:
            operand = fil.getElementsByTagName("Operand")
            if operand:
                self.handleOperand(operand)
       

    def handleOperand(self,operand):
        self.operand = operand
        n=1
        for obj in self.operand:
            if n == 1:
                parent = 1
            else:
                parent = self.getParentObjectNode(obj)
            self.operandfile.write("%d\t%d\t%s \n" % (n,int(parent),self.getText(obj.childNodes).strip()))
            n+=1
        self.operandfile.write("%d\t%d\t%s \n" % (n,0,self.getText(obj.childNodes).strip()))
        
    
        
        
    def getText(self, nodelist):
        self.rc = []
        self.nodelist=nodelist
        for node in self.nodelist:
            if node.nodeType == node.TEXT_NODE:
                self.rc.append(node.data)
            
        return ''.join(self.rc)


    def getParentObjectNode(self,node):
        self.node = node
        while self.node.parentNode:
            self.node = self.node.parentNode
            if self.node.nodeName == "nestedconditions":
                return 1
            else:
                return 0

#grammerNode= xmldoc.firstChild
#handleQueries(grammerNode)

