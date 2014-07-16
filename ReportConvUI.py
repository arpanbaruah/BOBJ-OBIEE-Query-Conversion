#!/usr/bin/env python

import wx
import os
import time
import shutil
from  main import reportMain

class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, title="Query Conversion Tool")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True
    
class MyFrame(wx.Frame):
    def __init__(self, parent, id=wx.ID_ANY, title="", 
                 pos=wx.DefaultPosition, 
                 style=wx.DEFAULT_FRAME_STYLE & ~ (wx.RESIZE_BORDER | 
                                                wx.RESIZE_BOX | 
                                                wx.MAXIMIZE_BOX),
                 name="MyFrame",
                 size = ( 700,270)):
        super(MyFrame, self).__init__(parent, id, title,
                                      pos, size, style, name)
        # Attributes
        self.panel = wx.Panel(self)
        self.panel.SetBackgroundColour(wx.RED)
       
        #sb1 = wx.StaticBox(self.panel, size = (550,60), pos = (110,15))
        #boxsizer1 = wx.StaticBoxSizer(sb1, wx.VERTICAL)
        #sb2 = wx.StaticBox(self.panel, size = (550,60), pos = (110,75))
        #boxsizer2 = wx.StaticBoxSizer(sb2, wx.VERTICAL)
        
        buttonpath = os.path.abspath(".\\img\\icon\\openfolder_35.gif")
        bmp = wx.Image(buttonpath, wx.BITMAP_TYPE_GIF).ConvertToBitmap()
        
        tool_img_path = os.path.abspath(".\\img\\icon\\frog_red.png")
        png = wx.Image(tool_img_path, wx.BITMAP_TYPE_ANY).ConvertToBitmap()
        
        self.image = wx.StaticBitmap(self.panel , -1, png, size = (100,100), pos = (10,35))
        #self.Bind(wx.EVT_PAINT, self.OnPaint)
        
        self.sourceCtrl = wx.TextCtrl(self.panel, -1, "", pos=(130, 37), size = (470,35),style = wx.TE_READONLY)
        self.destCtrl = wx.TextCtrl(self.panel, -1, "", pos=(130, 97), size = (470,35),style = wx.TE_READONLY)
        
        
        
        src_button = wx.BitmapButton(self.panel, -1,bmp, pos = (620,35), style = 0 )
        src_button.Bind(wx.EVT_ENTER_WINDOW, self.onsrcMouseOver)
        src_button.Bind(wx.EVT_LEAVE_WINDOW, self.onsrcMouseLeave)
        src_button.Bind(wx.EVT_BUTTON, self.sourceOnDir)
        src_button.SetBackgroundColour(wx.WHITE)
        
        
        des_button = wx.BitmapButton(self.panel, -1,bmp , pos = (620,95), style = 0)   
        des_button.Bind(wx.EVT_ENTER_WINDOW, self.ondestMouseOver)
        des_button.Bind(wx.EVT_LEAVE_WINDOW, self.ondestMouseLeave) 
        des_button.Bind(wx.EVT_BUTTON, self.destOnDir)
        des_button.SetBackgroundColour(wx.WHITE)
        
        
        
        #MENUS
        fileMenu = wx.Menu()  #create menu for file
        helpMenu = wx.Menu()  #create a menu for view
        aboutMenu = wx.Menu()  #create a menu for help

    #FILE MENU
        menusrcOpen = fileMenu.Append(wx.ID_NEW, "&Source Folder"," Add Source Folder")  #add open to File
        self.Bind(wx.EVT_MENU, self.sourceOnDir,menusrcOpen)
        
        menutarOpen = fileMenu.Append(wx.ID_OPEN, "&Target Folder"," Add Target Folder")  #add open to File
        self.Bind(wx.EVT_MENU, self.destOnDir, menutarOpen)
        
        
        menuExit = fileMenu.Append(wx.ID_EXIT, "E&xit"," Terminate the program")  #add exit to File

    #VIEW MENU
        menuhelp = helpMenu.Append(wx.ID_ANY, "Help", "Step and process")

    #HELP MENU
        menuAbout = aboutMenu.Append(wx.ID_ABOUT, "&About", "About Link")  #add about menu item

    #MENUBAR
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File") # Adding the "filemenu" to the MenuBar
        menuBar.Append(helpMenu, "&Help")
        menuBar.Append(aboutMenu, "&About")
        self.SetMenuBar(menuBar)  # Adding the MenuBar to the Frame content.

        self.Bind(wx.EVT_MENU, self.OnAbout, menuAbout)
        self.Bind(wx.EVT_MENU, self.OnExit, menuExit)
        self.Bind(wx.EVT_MENU, self.onHelp, menuhelp)
        
        path = os.path.abspath(".\\img\\icon\\frog.png")
        icon = wx.Icon(path,wx.BITMAP_TYPE_PNG)
        self.SetIcon(icon)
        
        
        
        
        
        ok_button = wx.Button(self.panel, label = "Execute", pos = (325,160) , size = (100,25))
        ok_button.Bind(wx.EVT_BUTTON, self.onExecute)
        
        Cancel_button = wx.Button(self.panel, label = "Cancel", pos = (445,160) , size = (100,25))
        Cancel_button.Bind(wx.EVT_BUTTON, self.onClose)
        Help_button = wx.Button(self.panel, label = "Help", pos = (565,160) , size = (100,25))
        Help_button.Bind(wx.EVT_BUTTON, self.onHelp)
        
       
        
    def onsrcMouseLeave(self, event ):
        
        
        self.src.Show(False) 
        event.Skip()
    

    def onsrcMouseOver(self, event):
        
        
        self.src = wx.PopupWindow(self, wx.RAISED_BORDER) 
        src = wx.TextCtrl(self.src, -1, pos=(-1,-1), size=(115,25),style=wx.TE_RICH) 
        src.SetValue("Source Folder")
        src.SetBackgroundColour(wx.NullColour)
        self.src.SetPosition((660,35))
        self.src.SetSize((120,30))
        
        
        self.src.Show(True) 
        event.Skip()
        
    
    def ondestMouseLeave(self, event ):
        self.dest.Show(False) 
        event.Skip()
    

    def ondestMouseOver(self, event):
        
        self.dest = wx.PopupWindow(self, wx.RAISED_BORDER) 
        dest = wx.TextCtrl(self.dest, -1, pos=(-1,-1), size=(145,25),style=wx.TE_RICH) 
        dest.SetValue("Destination Folder")
        dest.SetBackgroundColour(wx.NullColour)
        self.dest.SetPosition((660,95))
        self.dest.SetSize((150,30))
        
        
        self.dest.Show(True) 
        event.Skip()
        
   
        #----------------------------------------------------------------------
    def sourceOnDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        srcdlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if srcdlg.ShowModal() == wx.ID_OK:
            self.srcpath = srcdlg.GetPath()
            self.sourceCtrl.SetValue("%s" % (self.srcpath))
        srcdlg.Destroy()
        
        
    def destOnDir(self, event):
        """
        Show the DirDialog and print the user's choice to stdout
        """
        desdlg = wx.DirDialog(self, "Choose a directory:",
                           style=wx.DD_DEFAULT_STYLE)
        if desdlg.ShowModal() == wx.ID_OK:
            self.destpath = desdlg.GetPath()
            self.destCtrl.SetValue("%s" % (self.destpath))
        desdlg.Destroy()
    
    
    def onHelp(self, event):
        
        filename = 'README.txt'
        os.system("start "+filename)
        
    
    
    
    def onExecute(self, event):
        
        try:
            if  not self.srcpath == ''  or not  self.destpath == '' :
                #files = [f for f in os.listdir(self.srcpath) if f.endswith('.xml')]   
                bopath = os.path.join(self.destpath, 'boreport')
                if not os.path.exists(bopath):
                    os.mkdir(bopath)
                    os.chmod(bopath, 0o777)
    
                obieepath = os.path.join(self.destpath, 'obieereport')
                if not os.path.exists(obieepath):
                    os.mkdir(obieepath)
                    os.chmod(obieepath, 0o777)
            
                files = [f for f in os.listdir(self.srcpath) if f.endswith('.xml')]
                for filename in files:
                    shutil.copy(os.path.join(self.srcpath,filename), os.path.join(bopath,filename))
        
        
                msg = "Please wait while we process your request..."
                busyDlg = wx.BusyInfo(msg) 
                test = reportMain(self.destpath+'\\')
                status = test.main()
                time.sleep(2)
                if status == 1:
                    busyDlg = None
                    dlg = wx.MessageDialog(self,"Conversion is complete","Confirm Exit", wx.OK)
                    result = dlg.ShowModal()
                    dlg.Destroy()
                    if result == wx.ID_OK:
                        self.sourceCtrl.SetValue("")
                        self.destCtrl.SetValue("")                       
                        foldername = os.path.join(self.destpath,'obieereport')
                        os.startfile(foldername)
                        self.srcpath = ''
                        self.destpath = ''
        
        except:

            dlg = wx.MessageDialog(self,"Either source or destination folder is empty","Confirm Exit", wx.ICON_ERROR)
            result = dlg.ShowModal()
            dlg.Destroy()
            
     
    def onClose(self, event):
        dlg = wx.MessageDialog(self,"Do you really want to close this application?", "Confirm Exit", wx.OK|wx.CANCEL|wx.ICON_QUESTION)
        result = dlg.ShowModal()
        dlg.Destroy()
        if result == wx.ID_OK:
            self.Destroy()
            
    
    def OnExit(self,e):
        self.Close(True)
        
    
    def OnAbout(self,e):
        #dlg = wx.MessageDialog(self, "Version v0.1 \n Date 06/20/2014 \n Created By Arpan Baruah", "About", wx.OK)  #create a dialog (dlg) box to display the message, and ok button
        dlg = wx.MessageDialog(self, "Version v1.0 \n Date 07/02/2014 \n Created By Arpan B , Krishna S", "About", wx.OK)  #create a dialog (dlg) box to display the message, and ok button
        dlg.ShowModal()  #show the dialog box, modal means cannot do anything on the program until clicks ok or cancel
        dlg.Destroy()  #destroy the dialog box when its not needed
        
#if_name__ == "__main__":
app = MyApp(False)
app.MainLoop()
