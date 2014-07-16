#!/usr/bin/env python

#!/usr/bin/env python

import sys
import re
import datetime
from com.inter.generic.parsedate import dateConvert
from com.inter.generic.querymapper import subjectMapper
from com.inter.generic.querymapper import logicalMapper
from com.inter.readbo.readboxml_result_operand import filterRead
from com.inter.readbo.readboxml_result_operand import combineOutput

from com.obieereport.write.defineLogicalQuery import createLogicalQuery


def createLogical(mainfolder,bofolder,fileName):

    _file = bofolder+ 'temp/'+ fileName
    _resultfile1 = _file[:-4] +'_result_final.txt'
    _operandfile = _file[:-4] +'_operand.txt'
    _filterfile = _file[:-4] +'_filter.txt'
    _reportmeta = _file[:-4] +'_meta.txt'
    folder = mainfolder + 'obieereport\\'
    filename = folder + fileName[:-4]+'.lql'
    logicalquery = createLogicalQuery(filename)
    logicalquery.logicalQuery(_resultfile1, _operandfile, _filterfile,_reportmeta)
    
    
