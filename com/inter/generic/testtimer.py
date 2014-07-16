import time
import wx
 
########################################################################
class MyForm(wx.Frame):
 
    #----------------------------------------------------------------------
    def __init__(self):
        wx.Frame.__init__(self, None, wx.ID_ANY,
                          "BusyDialog Tutorial")
        panel = wx.Panel(self, wx.ID_ANY)
 
        busyBtn = wx.Button(panel, label="Show Busy Dialog")
        busyBtn.Bind(wx.EVT_BUTTON, self.onBusy)
 
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(busyBtn, 0, wx.ALL|wx.CENTER, 5)
        panel.SetSizer(sizer)
 
    #----------------------------------------------------------------------
    def onBusy(self, event):
        self.Hide()
        msg = "Please wait while we process your request..."
        busyDlg = wx.BusyInfo(msg)
        time.sleep(5)
        busyDlg = None
        self.Show()
 
# Run the program
if __name__ == "__main__":
    app = wx.App(False)
    frame = MyForm()
    frame.Show()
    app.MainLoop()#!/usr/bin/env python

