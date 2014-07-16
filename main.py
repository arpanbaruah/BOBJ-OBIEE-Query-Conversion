
from com.boreport.main.readboxml import readboXml
from com.obieereport.main.createOBIEEReport import createOBIEE
from com.obieereport.main.createLogical import createLogical
import os

class reportMain:
    
    def __init__(self,foldername):
        self.folderName = foldername
    
    
    def main(self):
        bofolder = self.folderName + 'boreport\\'
        files = [f for f in os.listdir(bofolder) if os.path.isfile(bofolder+f) if not f == '.DS_Store']
        for filename in files:
            readboXml(bofolder , filename)
            createOBIEE(self.folderName,bofolder, filename)
            createLogical(self.folderName,bofolder, filename)
        return 1