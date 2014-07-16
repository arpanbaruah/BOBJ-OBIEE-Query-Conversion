import os

def filterMapper(input):
    
    path = os.path.abspath('.\mapping\operationmapping.txt')
    mapperfile = open(path,'r')
    _boinput = input
    
    for _val in mapperfile.readlines():
        if not _val == '\n':
            if _boinput == _val.split('|')[0]:
                return _val.split('|')[1]
    
          

    