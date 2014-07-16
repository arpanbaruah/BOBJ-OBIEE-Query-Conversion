

def filterRead(filename):
    
    _dict = {}
    for line in filename.readlines():
        key = int(line.split('\t')[0])
        if not key in _dict.keys():
            _dict[key] = line.split('\t')[1:]
        else:
            _dict[key].append(line.split('\t')[1:])
    
    return _dict

        

def combineOutput(operandfile, resultfile):
    _operand = filterRead(operandfile)
    _result = filterRead(resultfile)
    if len(_operand) == 0:
        _operand[1]=['1', ' \n']
    #print _result
    _finalfile = {}
    
    for operkey ,filterkey  in zip(_result.keys(),_operand.keys()):
        if operkey == filterkey:
            _operand[operkey].append(_result[operkey])
            _finalfile[operkey] = _operand[operkey]
        #_finalfile[len(_result)] = _result[len(_result)]
    return _finalfile

