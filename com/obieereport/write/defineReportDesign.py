#!/usr/bin/env python

from xml.dom.minidom import Document
from com.inter.generic.filtermapper import filterMapper
from com.inter.readbo.readboxml_result_operand import combineOutput
from com.inter.readbo.readboxml_result_operand import filterRead

import re
import os

class defineReportDesign:
    
    def __init__(self, _doc):        
        self.doc = _doc

    def createcolumn(self , master, columnName, columnID):
        self.master = master
        self.columnName = columnName
        self.columnID = columnID
        column = self.doc.createElement('saw:column')
        self.master.appendChild(column)
        column.setAttribute('columnID',columnID)
        column.setAttribute('xsi:type','saw:regularColumn')
        column.setIdAttribute('columnID')
        _expr = self.createFormula(column, self.columnName)
        return

    def createFormula(self, master, columnname):
        self.master = master
        self.columnname = columnname
        _columnFormula = self.doc.createElement('saw:columnFormula')
        self.master.appendChild(_columnFormula)
        _expr = self.createExpr(_columnFormula, self.columnname)
        return

    
    def createExpr(self, master, columnName):  
        self.master = master
        self.columnName = columnName
        expr = self.doc.createElement('sawx:expr')
        expr.setAttribute('xsi:type','sawx:sqlExpression')
        self.master.appendChild(expr)
        column = self.doc.createTextNode('"%s"' % self.columnName.strip())
        expr.appendChild(column)
        return
    
    

    def createColumns(self, master, file,operandfile,filterfile):
        self.master = master
        self.file = file
        self.operandfile = operandfile
        self.filterfile = filterfile
        columns = self.doc.createElement('saw:columns')
        self.master.appendChild(columns)
        for line in self.file.readlines():
            _key, _value = line.split(',')
            self.createcolumn(columns, _value,_key)      
        #self.createCoveredFilter(self.master, self.operandfile, self.filterfile)
        #_filter = defineFilter(self.doc)
        #_filter.createCoveredFilter(self.master, self.operandfile, self.filterfile)
        return



    def createCoveredFilter(self ,master, _operandfile, _filterfile ):
        
        self.master = master
        self._operandfile = open(_operandfile,'r')
        self._filterfile = open(_filterfile,'r')
        l_column = self.doc.createElement('saw:filter')
        self.master.appendChild(l_column)
        _prompt = ''
        if not os.stat(_filterfile).st_size == 0:
            
            _dict = combineOutput(self._operandfile, self._filterfile)
            
            
            for key in _dict.keys():
                _prompt =''
                operandVal = _dict[key][0]
                operandType = _dict[key][1].strip()
                operation =  _dict[key][2][0]
                columnName = _dict[key][2][1][0].strip()
                if len(_dict[key][2]) == 3:
                    value = _dict[key][2][2]
                else:
                    value = 'IsNullCond'
                if len(_dict[key][2]) >= 4:
                    _prompt = _dict[key][2][3][0]
                if operandVal == '1':
                    l_column = self.createfilterHeader(l_column, operandVal,operandType.lower(), operation,columnName,value,_prompt)
                else:
                    self.createfilterExpr(l_column , operation,columnName,value,_prompt)
                
    
    def createfilterHeader(self, _master, _operandVal,_operandType, _operation,_columnName,_value,_prompt):
                
        self._master = _master
        self.operandVal = _operandVal
        self.operandType = _operandType
        self.operation = _operation
        self.columnName = _columnName
        self.value = _value
        c_column = self.doc.createElement('sawx:expr')
        self._master.appendChild(c_column)
        c_column.setAttribute('xsi:type', "sawx:logical")
        c_column.setAttribute('op', self.operandType.strip())
        self._master = c_column
        self.createfilterExpr(self._master , self.operation,self.columnName,self.value,_prompt)
        return c_column         


    def createfilterExpr(self, master, operation,columnName,values,prompt):
            
        self.master = master
        self.operation = operation
        self.columnName = columnName
        self.values = values
        #self.prompt = prompt
        cond = ['InList','NotInList','Like','NotLike','Equal','NotEqual']
        if self.operation.strip() in cond:
            _type = 'sawx:list'
        else:
            _type = 'sawx:comparison'
        
        if 'Date' in self.columnName or 'date' in self.columnName or 'dt' in self.columnName:
            exprtype = 'xsd:date'
        else:
            exprtype = 'xsd:string'
        #print self.operation , self.columnName , prompt
        if prompt.strip() == 'Yes':
            self.values = 'IsNullCond'
            _type = 'sawx:special'
            self.operation = 'prompted'
        #print self.operation , self.columnName  , prompt
        self.createExprFil( self.master ,_type , exprtype,  self.operation , self.columnName.strip(),self.values)   
        

    
    def createExprFil(self,master,_type, exprtype, operation, columnName,values):
            
        self.master = master
        self.type = _type
        self.exprtype =exprtype
        self.operation = operation
        self.columnName = columnName
        self.values = values
        _obieeval = filterMapper(self.operation.strip())
        if _obieeval == None:
            _obieeval = self.operation
        column = self.doc.createElement('sawx:expr')
        self.master.appendChild(column)
        column.setAttribute('xsi:type',self.type)
        column.setAttribute('op',_obieeval.strip())
        self.createexpressionExpr(column,  self.exprtype,self.columnName, self.values,self.operation.strip())
    
     


    def createexpressionExpr(self,master, exprtype,columnName,values,operation):
        self.master = master
        self.exprtype =exprtype
        self.columnName = columnName
        self.values = values
        self.operation = operation
            
        from com.inter.generic.parsedate import dateConvert
        pattern = re.compile(r",|;")
        column = self.doc.createElement('sawx:expr')
        self.master.appendChild(column)
        column.setAttribute('xsi:type','sawx:sqlExpression')
        value = self.doc.createTextNode('"%s"' % self.columnName.strip())
        column.appendChild(value)
        if not values == 'IsNullCond':      
            for val in values:
                for inval in re.split(pattern,val):
                    if exprtype == 'xsd:date':
                        inval = dateConvert(inval.strip())         
                    self.createvalueExpr(master,exprtype,inval.strip(),operation)

        


    
    def createvalueExpr(self,master,type, value,operation):
        self.master= master
        self.type = type
        self.value = value
        self.operation = operation
                
   
        column = self.doc.createElement('sawx:expr')
        self.master.appendChild(column)
        column.setAttribute('xsi:type',type)
        if self.operation == 'Like' or self.operation == 'NotLike':
            value = self.value[1:-1]
        value = self.doc.createTextNode('%s' % value)
        column.appendChild(value)

## View Definition 

    def createcvTable(self,master):
        self.master = master
        _cvtable = self.doc.createElement("saw:cvTable")
        self.master.appendChild(_cvtable)
        _cvrow = self.createcvRow(_cvtable,"titleView!1")
        _cvrow = self.createcvRow(_cvtable,"tableView!1")
    

    def createcvRow(self,master,name):
        self.master = master
        self.name = name
        _cvrow = self.doc.createElement("saw:cvRow")
        self.master.appendChild(_cvrow)
        self.createcvCell(_cvrow,name)
         
    
    def createcvCell(self,master,name):
        self.master = master
        self.name = name
        _cvcell = self.doc.createElement("saw:cvCell")
        self.master.appendChild(_cvcell)
        _cvcell.setAttribute('viewName', self.name)
        self.createdisplayFormat(_cvcell)
        


    def createdisplayFormat(self,master):
        self.master = master
        _displayFormat = self.doc.createElement('saw:displayFormat')
        self.master.appendChild(_displayFormat)
        self.createformatSpec(_displayFormat)
        

    def createformatSpec(self , master):
        self.master = master
        _formatSpec = self.doc.createElement('saw:formatSpec')
        self.master.appendChild(_formatSpec)
        
    


    def createView(self, master, type, _file2 = 'NULL'):
        
        self.master = master
        self.type = type
        self._file2 = _file2
        if self.type == 'saw:compoundView' :
            _view = self.doc.createElement("saw:view")
            self.master.appendChild(_view)
            _view.setAttribute('xsi:type','saw:compoundView')
            _view.setAttribute('name','compoundView!1')
            _table = self.createcvTable(_view)
        elif self.type == 'saw:titleView' :
            _view = self.doc.createElement("saw:view")
            self.master.appendChild(_view)
            _view.setAttribute('xsi:type',self.type)
            _view.setAttribute('name','titleView!1')
        elif self.type == 'saw:tableView':
            _view = self.doc.createElement('saw:view')
            self.master.appendChild(_view)
            _view.setAttribute('xsi:type', self.type)
            _view.setAttribute('name','tableView!1')
            _view.setAttribute('scrollingEnabled','true')
            
            _view_child = self.createEdges(_view, self._file2)
        return 

    def createEdges(self, master,_file3):
        self.master = master
        self._file3 = _file3
        _edges = self.doc.createElement('saw:edges')
        self.master.appendChild(_edges)
        _edge = self.createEdge(_edges,self._file3)


    def createEdge(self, master, _file4):
        self.master = master
        self._file4 = _file4
        _edge_1 = self.doc.createElement('saw:edge')
        self.master.appendChild(_edge_1)
        _edge_1.setAttribute('axis','page')
        _edge_1.setAttribute('showColumnHeader','true')
        _edge_2 = self.doc.createElement('saw:edge')
        self.master.appendChild(_edge_2)
        _edge_2.setAttribute('axis','section')
        _edge_3 = self.doc.createElement('saw:edge')
        self.master.appendChild(_edge_3)
        _edge_3.setAttribute('axis','row')
        _edge_3.setAttribute('showColumnHeader','true')
        _edgeLayers = self.createedgeLayers(_edge_3,self._file4)    

    def createedgeLayers(self, master,file):
        self.master = master
        self.file = file
        _edges = self.doc.createElement('saw:edgeLayers')
        self.master.appendChild(_edges)
        filterfile = open(self.file,'r')
        for line in filterfile.readlines():
            (_key, _value) = line.split(',')
            edge = self.createedgeLayer( _edges, _key)

    def createedgeLayer(self, master, columnID):
        self.master = master
        self.columnID = columnID
        _edge = self.doc.createElement('saw:edgeLayer')
        self.master.appendChild(_edge)
        _edge.setAttribute('type','column')
        _edge.setAttribute('columnID', self.columnID)
    

    

    def createallView(self, master, _file1):
        self.createView( master,"saw:compoundView")
        #self.createtitleView(master,"saw:titleView")
        self.createView( master,"saw:titleView")    
        self.createView(master,"saw:tableView",_file1)


    def createtitleView(self ,master, _type):
        
        self.master = master
        self._type = _type
        _view = self.doc.createElement("saw:view")
        self.master.appendChild(_view)
        _view.setAttribute('xsi:type',self._type)
        _view.setAttribute('name','titleView!1')
        
    
    def createViews(self, master, _file):
        self.master = master
        self.file = _file
        _views = self.doc.createElement("saw:views")
        self.master.appendChild(_views)
        _views.setAttribute('currentView',"0")
        self.createallView( _views,self.file)

    
    
    def createCoveredPrompts(self ,master, promptfilter, _filterfile ,rpdname):
        
        self.master = master
        self._filterfile = _filterfile
        v_file = promptfilter
        v_prompt = 'N'
        _dict = filterRead(v_file)
        for key in _dict.keys():
            if len(_dict[key]) > 3:
                v_prompt = 'Y'
        v_file.close()
        if v_prompt == 'Y':
            l_column = self.doc.createElement('saw:prompts')
            self.master.appendChild(l_column)
            l_column.setAttribute('scope',"report")
            l_column.setAttribute('subjectArea',rpdname)
            l_column.setAttribute('layout',"vertical")
            self.createPromptStep(l_column, self._filterfile,rpdname)
        
    
    def createPromptStep(self, master, _filterfile,rpdname):
        
        self.master = master
        self._filterfile = _filterfile
        l_column = self.doc.createElement('saw:promptStep')
        self.master.appendChild(l_column)
        self.createIndividualPrompts(l_column, self._filterfile ,rpdname)
    
    def createIndividualPrompts(self, master, _filterfile,rpdname):
        
        self.master = master
        self._filterfile = _filterfile
        self._filterfile = open(_filterfile,'r')
        l_column = self.doc.createElement('saw:individualPrompts')
        self.master.appendChild(l_column)
        _dict = filterRead(self._filterfile)
        for key in _dict.keys():
            
            if len(_dict[key]) > 3:
                columnID = 'c'+str(key)
                _columnname =  _dict[key][1]
                _promptname =  _dict[key][2]
                _isoptional =  _dict[key][4]
                _operand = _dict[key][0]
                self.createPrompt(l_column,_columnname, _operand, _promptname, _isoptional, columnID,  rpdname)
        
    def createPrompt(self, master, columnname, operand, promptname , isoptional, columnID, rpdname):
        
        self.master = master
        #print isoptional[0].strip()
        if isoptional[0].strip() =='Yes':
            required = 'false'
        else:
            required = 'true'
        l_column = self.doc.createElement('saw:prompt')
        self.master.appendChild(l_column)
        l_column.setAttribute('xsi:type',"saw:columnFilterPrompt")
        l_column.setAttribute('subjectArea',rpdname)
        l_column.setAttribute('required',required)
        l_column.setAttribute('noAutoPopulateLabel',"true")
        l_column.setAttribute('columnID',columnID)
        self.createPromptFormula(l_column, columnname)
        self.createPromptOperator(l_column, operand)
        self.createpromptUIControl(l_column)
        self.createPromptLabel(l_column, promptname)
        self.createPromptDefaultValues( l_column)
        self.createconstrainPrompt( l_column)
        self.createSetPromptVariables( l_column)
        self.createPromptSource(l_column)
        
    
    def createPromptFormula(self, master, columnname):
        
        self.master = master
        l_column = self.doc.createElement('saw:formula')
        self.master.appendChild(l_column)
        self.createPromptExpr(l_column,columnname)
        
    
    def createPromptExpr(self,master,columnname):
        
        self.master = master
        l_column = self.doc.createElement('sawx:expr')
        self.master.appendChild(l_column)
        l_column.setAttribute('xsi:type',"sawx:sqlExpression")
        column = self.doc.createTextNode('"%s"' % columnname[0].strip())
        l_column.appendChild(column)
        
    def createPromptOperator(self, master, operand):
        
        self.master = master
        l_column = self.doc.createElement('saw:promptOperator')
        self.master.appendChild(l_column)
        _obieeval = filterMapper(operand.strip())
        if _obieeval == None:
            _obieeval = operand
        l_column.setAttribute('op',_obieeval.strip())
        
    
    def createpromptUIControl(self,master):
        
        self.master = master
        l_column = self.doc.createElement('saw:promptUIControl')
        self.master.appendChild(l_column)
        l_column.setAttribute('xsi:type',"saw:browse")
        l_column.setAttribute('maxChoices',"-1")
        l_column.setAttribute('includeAllChoices',"false")
        
    def createCustomWidth(self, master):
        
        self.master = master
        l_column = self.doc.createElement('saw:customWidth')
        self.master.appendChild(l_column)
        l_column.setAttribute('width',"120")
        l_column.setAttribute('using',"custompixels")
        
    
    def createPromptLabel(self, master, promptname):
        
        self.master = master
        l_column  = self.doc.createElement('saw:label')
        self.master.appendChild(l_column)
        self.createPromptCaption(l_column, promptname)
        
    
    def createPromptCaption(self, master, promptname):
        
        self.master = master
        l_column  = self.doc.createElement('saw:caption')
        self.master.appendChild(l_column)
        self.createPromptText(l_column, promptname)
        
        
    def createPromptText(self, master, promptname):
        
        self.master = master
        l_column  = self.doc.createElement('saw:text')
        self.master.appendChild(l_column)
        column = self.doc.createTextNode('"%s"' % promptname[0].strip())
        l_column.appendChild(column)

    def createPromptDefaultValues(self, master):
        
        self.master = master
        l_column  = self.doc.createElement('saw:promptDefaultValues')
        self.master.appendChild(l_column)
        l_column.setAttribute('type',"reportDefault")
        l_column.setAttribute('usingCodeValue',"false")
        
        
    def createconstrainPrompt(self, master):
        
        self.master = master
        l_column  = self.doc.createElement('saw:constrainPrompt')
        self.master.appendChild(l_column)
        l_column.setAttribute('type',"none")
        
    
    def createSetPromptVariables(self, master):
        
        self.master = master
        l_column  = self.doc.createElement('saw:setPromptVariables')
        self.master.appendChild(l_column)
        self.createSetPromptVariable(l_column)
          
          
    def createSetPromptVariable(self, master):
        
        self.master = master
        l_column  = self.doc.createElement('saw:setPromptVariable')
        self.master.appendChild(l_column)
        l_column.setAttribute('location',"value")
        l_column.setAttribute('type',"none")
        l_column.setAttribute('variableFormula',"")
        
        
    def createPromptSource(self, master):
        
        self.master = master
        l_column  = self.doc.createElement('saw:promptSource')
        self.master.appendChild(l_column)
        l_column.setAttribute('xsi:type',"saw:allChoices")
 
 


