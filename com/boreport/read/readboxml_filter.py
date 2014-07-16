from xml.dom import minidom
from com.inter.generic.randomgenerator import randomstring
from com.inter.generic.filecleansing import columnMapper
import re


class readboxml_filter:
    
    def __init__(self,filename):
        filterfileName = filename
        self.filter = open(filterfileName,'w')
    
    def handleQueries(self,boquery):
        self.boquery = boquery
        Query = self.boquery.getElementsByTagName("Query")
        self.handleQuery(Query)
    

    def handleQuery(self,query):
        self.query = query
        for que in self.query:
            Filters = que.getElementsByTagName("Filters")
            self.handleFilters(Filters)
        self.filter.close()
  

    def handleFilters(self, Filters):
        self.Filters = Filters
        for fil in self.Filters:
            condition = fil.getElementsByTagName("Condition")
            self.handleCondition(condition)


    def handleCondition(self,condition):
        self.condition = condition
        n=1
        for res in self.condition:
            _predefine = res.getAttribute("type")
            if not _predefine:
                objects = res.getElementsByTagName("Object")
                operator = res.getElementsByTagName("Operator")
                rightsideoperand = res.getElementsByTagName("right_side_operand")
                self.handleObjectConditions( n, objects, operator, rightsideoperand)
                n+=1


        

    def handleObjectConditions( self,n, objects,operator,rightsideoperand):
        self.n = n
        self.objects = objects
        self.operator = operator
        self.rightsideoperand = rightsideoperand
        for obj in self.operator:
            self.filter.write("%d\t%s\n" % (self.n, self.getText(obj.childNodes).strip()))
        for obj in self.objects:
            self.filter.write("%d\t%s\n" % (self.n, self.getTextObject(obj.childNodes).strip()))
        for obj in self.rightsideoperand:
            _prompt = obj.getAttribute("IsPrompt")
            _IsOptional = obj.getAttribute("IsOptional")
            if not _prompt:
                self.filter.write("%d\t%s\n" % (self.n, self.getText(obj.childNodes).strip()))
            else:
                self.filter.write("%d\t%s\n" % (self.n, self.getText(obj.childNodes).strip()))
                self.filter.write("%d\t%s\n" % (self.n,_prompt))
                self.filter.write("%d\t%s\n" % (self.n,_IsOptional))
        
    def getText(self,nodelist):
        self.rc = []
        self.nodelist = nodelist
        for node in self.nodelist:
            if node.nodeType == node.TEXT_NODE:
                self.rc.append(node.data)            
        return ''.join(self.rc)



    def getTextObject(self,nodelist):
        self.nodelist = nodelist
        self.rc = []
        pattern = re.compile(r",|\\\\")
        for node in self.nodelist:
            if node.nodeType == node.TEXT_NODE:
                (_value1, _value2) = re.split(pattern,node.data)
                _final = columnMapper(_value1.strip())+'"."'+_value2.strip()
                self.rc.append(_final)
        return ''.join(self.rc)


#grammerNode= xmldoc.firstChild
#handleQueries(grammerNode)

