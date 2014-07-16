#!/usr/bin/env python

def subjectMapper(input):
    
    path = '.\\mapping\\rpdmapping.txt'
    
    mapperfile = open(path,'r')
    _boinput = input
    
    for _val in mapperfile.readlines():
        if not _val == '\n':
            if _boinput == _val.split('|')[0]:
                return _val.split('|')[1]
            
            

def logicalMapper(input):
    
    path = '.\\mapping\\logicalmapping.txt'
    
    mapperfile = open(path,'r')
    _boinput = input
    #print _boinput
    
    for _val in mapperfile.readlines():
        if not _val == '\n':
            if _boinput == _val.split('|')[0]:
                return _val.split('|')[1]
            
            
def findunvName(metafile):
        mapperfile = open(metafile,'r')
        _boinput = 'QueryUniverse'
    
        for _val in mapperfile.readlines():
            if not _val == '\n':
                if _boinput == _val.split('|')[0]:
                    return _val.split('|')[1]
                else:
                    return _boinput