from xml.dom import minidom
from com.inter.generic.randomgenerator import randomstring
from com.inter.generic.filecleansing import fileCleansing



class readboxml_result:
    
    def __init__(self,filename,reportmeta):
        self.resultfileName = filename
        self.result = open(self.resultfileName,'w')
        self.reportmeta = open(reportmeta,'w')
    
    def handleQueries(self,boquery):
        self.boquery = boquery
        Query = self.boquery.getElementsByTagName("Query")
        self.handleQuery(Query)
    

    def handleQuery(self, query):
        self.query = query
        for que in self.query:
            Result = que.getElementsByTagName("Results")
            self.univername = que.getAttribute('QueryUniverse')
            self.reportmeta.write("%s|%s\n" %('QueryUniverse',self.univername.strip()))
            self.handleResults(Result)
        self.result.close()
        fileCleansing(self.resultfileName)
    
    def handleResults(self, result):
    
        for res in result:
            objects = res.getElementsByTagName("Object")
            self.handleObjectsResults(objects)
     

    def handleObjectsResults(self,objects):
        for obj in objects:
            _id = randomstring()
            self.result.write( "%s,%s \n" %(_id.str, self.getText(obj.childNodes).strip()))
        
    
    

    def getText(self, nodelist):
        self.nodelist = nodelist
        self.rc = []
        for node in self.nodelist:
            if node.nodeType == node.TEXT_NODE:
                self.rc.append(node.data)
        return ''.join(self.rc)
    
    
    
        


#grammerNode= xmldoc.firstChild
#handleQueries(grammerNode)

