from xml.dom import minidom
import com.boreport.read.readboxml_result 
import com.boreport.read.readboxml_operand
import com.boreport.read.readboxml_filter
import os

"""

def readboXml(mainfolder,fileName):
    
    _file = mainfolder+fileName
    xmldoc = minidom.parse(_file)
    grammerNode= xmldoc.firstChild
    resultfile = _file[:-4] +'_result.txt'
    filterfile = _file[:-4] +'_filter.txt'
    operandfile = _file[:-4] +'_operand.txt'
    _result = com.boreport.read.readboxml_result.readboxml_result(resultfile)
    _result.handleQueries(grammerNode)
    _operand = com.boreport.read.readboxml_operand.readboxml_operand(operandfile)
    _operand.handleQueries(grammerNode)
    _filter = com.boreport.read.readboxml_filter.readboxml_filter(filterfile)
    _filter.handleQueries(grammerNode)

"""

def readboXml(mainfolder,fileName):
    
    if not os.path.exists(mainfolder+ 'temp'):
        os.makedirs(mainfolder+ 'temp')
        os.chmod(mainfolder+ 'temp',0o777)
    _mainfile = mainfolder+fileName
    _file = mainfolder+ 'temp/'+ fileName
    xmldoc = minidom.parse(_mainfile)
    grammerNode= xmldoc.firstChild
    resultfile = _file[:-4] +'_result.txt'
    filterfile = _file[:-4] +'_filter.txt'
    operandfile = _file[:-4] +'_operand.txt'
    reportmeta = _file[:-4] +'_meta.txt'
    _result = com.boreport.read.readboxml_result.readboxml_result(resultfile,reportmeta)
    _result.handleQueries(grammerNode)
    _operand = com.boreport.read.readboxml_operand.readboxml_operand(operandfile)
    _operand.handleQueries(grammerNode)
    _filter = com.boreport.read.readboxml_filter.readboxml_filter(filterfile)
    _filter.handleQueries(grammerNode)



