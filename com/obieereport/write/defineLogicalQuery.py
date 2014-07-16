#!/usr/bin/env python

import sys
import re
import os
import datetime
from com.inter.generic.parsedate import dateConvert
from com.inter.generic.querymapper import subjectMapper
from com.inter.generic.querymapper import logicalMapper
from com.inter.readbo.readboxml_result_operand import filterRead
from com.inter.readbo.readboxml_result_operand import combineOutput
from com.inter.generic.querymapper import findunvName




class createLogicalQuery:
    
    def __init__(self, filename):
        self.filew = open(filename,'w')
    
    
    def logicalQuery(self, resultfile, operandfile, filterfile,reportmeta):
        self._file = open(resultfile,'r')
        self._operandfile = open(operandfile,'r')
        self._filterfile = open(filterfile,'r')
        self._reportmeta = reportmeta
        univname = findunvName(self._reportmeta)
        count=1
        rpd = subjectMapper(univname.strip())
        self.filew.write('select\n')
        for line in self._file.readlines():
            _key, _value = line.split(',')
            val =  rpd+'."'+_value.strip()+ '" s_' + str(count)+ ",\n"
            self.filew.write(val)
            count+=1

        _prompt =''
        self.filew.write('0 s_0\nfrom\n')
        self.filew.write(rpd+'\n')

        pattern = re.compile(r",|;")
        operandVal_nxt = ''
        if not os.stat(filterfile).st_size == 0:
            self.filew.write('where'+'\n')
            _dict = combineOutput(self._operandfile, self._filterfile)

            max_key = max(_dict.keys())
            for key in _dict.keys():
                operandVal = _dict[key][0]
                if key+1<=max_key:
                    operandVal_nxt = _dict[key+1][0]
                if key==max_key:
                    operandType = ''
                else:
                    operandType = _dict[key][1].strip()
                operation =  _dict[key][2][0]
                operation = logicalMapper(operation.strip())
                columnName = _dict[key][2][1][0]
                if len(_dict[key][2])==3:
                    value = _dict[key][2][2]
                else:
                    value = 'IsNullCond'
                
                if len(_dict[key][2])==4:
                    value = _dict[key][2][2]
                    _prompt = _dict[key][2][3]
                    
                if len(_dict[key][2])==5 or len(_dict[key][2]) == 6:
                    value = _dict[key][2][2]
                    if _dict[key][2][3][0].strip()=='Yes' or _dict[key][2][4][0].strip() == 'Yes':
                        #print value
                        _prompt = 'Yes'
                    
        
                if operandVal == '1':
                    self.filew.write('(')
                if value =='IsNullCond':
                    self.filew.write('('+'"'+columnName.strip()+'"'+'\t'+operation.strip()+')')
                    self.filew.write('\t'+operandType+'\n')
                else:
                    
                    if operation.strip() == 'BETWEEN':
                        
                        if _prompt == '':
                            for val in  value:
                                inval1, inval2= re.split(pattern,val.strip())
                            if 'Date' in columnName.strip():
                                inval1='date '+"'"+dateConvert(inval1.strip())+"'"
                                inval2='date '+"'"+dateConvert(inval2.strip())+"'"
                        else:
                            for val in value:
                                inval1 = ":"+val.strip()
                                inval2 = ":"+val.strip()
                        self.filew.write('('+'"'+columnName.strip()+'"'+'\t'+operation.strip()+'\t'+ inval1 + ' AND ' + inval2 +')')


                    else:
                        self.filew.write('('+'"'+columnName.strip()+'"'+'\t'+operation.strip()+'\t'+ '(')
                        count = 1
                        max_count = len([re.split(pattern, v2.strip()) for v2 in(val1 for val1 in value)][0])
                        for val2 in value:
                            for inval in re.split(pattern,val2.strip()):
                                if _prompt == '':
                                    self.filew.write("'"+inval+"'")
                                else:
                                    self.filew.write(":"+inval)
                                if count < max_count:
                                    self.filew.write(',')
                                count+=1
                        self.filew.write(')'+')'+'\n') 
                
                    if operandVal_nxt == '1':
                        self.filew.write(')')
                    self.filew.write('\t'+operandType+'\n')
            self.filew.write(')')