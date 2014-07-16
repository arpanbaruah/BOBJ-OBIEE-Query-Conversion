#!/usr/bin/env python

import os
from distutils.core import setup
import py2exe
   
Mydata_files = []
for files in os.listdir('.\\img\\icon\\'):
    f1 = '.\\img\\icon\\' + files
    if os.path.isfile(f1): # skip directories
        f2 = 'img/icon', [f1]
        Mydata_files.append(f2)
   
        setup(
            windows = [{"script":'ReportConvUI.py',
                      "icon_resources": [(1, "frog.ico")],
                      "dest_base": "QConvert",
                        }],
            name = "Query Converter ver 0.1", 
            options={
                "py2exe":{
                    "unbuffered": True,
                    "optimize": 2,
                    "excludes": ["email"],
                    "includes": "os,time,shutil,re,xml.dom"
                         }
                    },
            description = "Query Conversion Tool.Converts BO XML to OBIEE XML and OBIEE Logical query",
            author = "Arpan Baruah",
            author_email ="arpan.baruah@oracle.com",
            maintainer = "OBIEE Team",
            license = "Oracle Licence",
            )