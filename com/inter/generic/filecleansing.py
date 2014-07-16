import re

def fileCleansing(_fileName):
    newfile = _fileName[:-4]+'_final.txt'
    _file = open(_fileName,'r')
    newfile = open(newfile,'w')
    pattern = re.compile(r",|\\\\")
    for line in _file.readlines():
        (_key, _value1, _value2) = re.split(pattern,line)
        _value1 = columnMapper(_value1.strip())
        newfile.write(('%s,%s"."%s \n')  % (_key, _value1.strip(), _value2.strip()))
        
    _file.close()
    
    
    
def columnMapper(_columnName):
    
    mapperfile = open('.\\mapping\\detailobjects.txt','r')
    column = _columnName.strip()
    for _val in mapperfile.readlines():
        if not _val == '\n':
            if column == _val.split('|')[1].strip():
                return _val.split('|')[0].strip()
    return column


