from com.obieereport.write.defineReportDesign import defineReportDesign
from xml.dom.minidom import Document
from com.inter.generic.querymapper import subjectMapper
from com.inter.generic.querymapper import findunvName



class defineReport:
    
    def __init__(self, doc):
        self.doc = doc
        
            

    def createReport(self, resultfile1, resultfile2,operandfile,filterfile,reportmeta):
        
        self.resultfile1 = resultfile1
        self.resultfile2 = resultfile2
        self.operandfile = operandfile
        self.filterfile = filterfile
        self.reportmeta = reportmeta
        self.file1 = open(self.resultfile1,'r')
        self.promptfilter = open(self.filterfile,'r')
        _report = self.doc.createElement('saw:report')
        self.doc.appendChild(_report)
        _report.setAttribute('xmlns:saw',"com.seibel.analytics.web/report/v1.1")
        _report.setAttribute('xmlns:xsi', "http://www.w3.org/2001/XMLSchema-instance")
        _report.setAttribute('xmlns:xsd', "http://www.w3.org/2001/XMLSchema")
        _report.setAttribute('xmlVersion', "201201160")
        _report.setAttribute('xmlns:sawx', "com.siebel.analytics.web/expression/v1.1")
        #print self.resultfile1
        _criteria = self.createCriteria(_report,self.file1,self.resultfile1,self.operandfile,self.filterfile,self.reportmeta,self.promptfilter)


    def createCriteria(self, master, _file1,_file2,operandfile,filterfile,reportmeta,promptfilter):
        self.master = master
        self._file1 = _file1
        self._file2 = _file2
        self.operandfile = operandfile
        self.filterfile = filterfile
        self.promptfilter = promptfilter
        _bouniverse = findunvName(reportmeta)
        _rpdname = subjectMapper(_bouniverse.strip())
        _criteria = self.doc.createElement('saw:criteria')
        self.master.appendChild(_criteria)
        _criteria.setAttribute('xsi:type',"saw:simpleCriteria")
        _criteria.setAttribute('subjectArea',_rpdname)
        _report = defineReportDesign(self.doc)
        _report.createColumns(_criteria, self._file1,self.operandfile, self.filterfile)
        _report.createCoveredFilter(_criteria, self.operandfile, self.filterfile)
        _report.createViews(self.master, self._file2)
        _report.createCoveredPrompts(self.master,self.promptfilter, self.filterfile,_rpdname)
        
        
        #_filter = defineFilter(self.doc)
        #_filter.createCoveredFilter(_criteria, self.operandfile, self.filterfile)
        #_columns = createColumns(_criteria,self._file)
        #_filters = createCoveredFilter(_criteria,  self.operandfile, self.filterfile)
        
        
            