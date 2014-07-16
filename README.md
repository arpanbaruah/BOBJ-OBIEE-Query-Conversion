BOBJ-OBIEE-Query-Conversion
===========================

This tool converts BOBJ XML to OBIEE XML and OBIEE Logical Query for BIP.

Limitation
1.  Works on windows. You may update the ReportConvUI.py to make it work for mac/linux.

Setup process
==============


You may directly execute the ReportConvUI.py. This will pop up an interactive UI. 
Source Folder - Folder where the BO xml are placed
Target Folder - Folder where OBIEE xml will be generated


execute in command line
(need py2exe in order to create the executable)

>> python setup.py py2exe



Please populate

mapping/rpdmapping.txt
>> mapping between BOBJ universe name and RPD Name

mapping/detailobjects.txt
>> detail object parent/detail object name ( this file is optional)



