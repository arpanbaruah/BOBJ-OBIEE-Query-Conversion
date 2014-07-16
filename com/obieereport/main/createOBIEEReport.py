from xml.dom.minidom import Document

from com.obieereport.write.defineReport import defineReport
#from com.obieereport.write.defineColumn import createColumns
#from com.obieereport.write.defineView import createViews
#from com.obieereport.write.definefilterComparison import createCoveredFilter


def createOBIEE(mainfolder,bofolder, fileName):
    doc = Document()
    _file = bofolder+ 'temp/'+ fileName
    resultfile1 = _file[:-4] +'_result_final.txt'
    resultfile2 = _file[:-4] +'_result_final.txt'
    operandfile = _file[:-4] +'_operand.txt'
    filterfile = _file[:-4] +'_filter.txt'
    reportmeta = _file[:-4] +'_meta.txt'
    folder = mainfolder + 'obieereport\\'
    filename = folder + fileName
    obieefile = open(filename,'w')
    createRep = defineReport(doc)
    createRep.createReport(resultfile1,resultfile2,operandfile, filterfile,reportmeta)
    obieefile.write(doc.toprettyxml())
