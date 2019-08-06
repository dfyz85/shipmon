import wx
import platform

class MyFrame(wx.Frame):
  def __init__(self, title='ADD VESSEL'):
    #vessel = ''
    #imo = ''
    wx.Frame.__init__(self, None, title=title,size=(650,400))
    self.panel = wx.Panel.__init__(self)
    b = wx.Button(self, -1, "ADD Vessel", (10,130))
    self.Bind(wx.EVT_BUTTON, self.MyOnButton, b)
    self.Bind(wx.EVT_WINDOW_MODAL_DIALOG_CLOSED, self.OnWindowModalDialogClosed)
    
    sizer = wx.BoxSizer(wx.VERTICAL)
    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self, -1, "Vessel name:", (10,10))
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    text1 = wx.TextCtrl(self, -1, "", size=(80,-1),pos=(80,10))
    self.vessel = text1
    box.Add(text1, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    self.Bind(wx.EVT_TEXT, self.EvtText1, text1)

    box = wx.BoxSizer(wx.HORIZONTAL)
    label = wx.StaticText(self, -1, "IMO:", pos=(10,40))
    box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)
    text2 = wx.TextCtrl(self, -1, "", size=(80,-1),pos=(80,40))
    self.imo = text2
    box.Add(text2, 1, wx.ALIGN_CENTRE|wx.ALL, 5)
    sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    self.Bind(wx.EVT_TEXT, self.EvtText2, text2)
    
    self.Show() 
    
  def MyOnButton(self, evt):
    textDl = ''
    for i in dir(self.vessel):
     textDl = textDl+i+' '
    
    dlg = wx.MessageDialog(self, self.vessel,
                            'A Message Box',
                            wx.OK | wx.ICON_INFORMATION
                            #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
                            )
    dlg.ShowModal()
    self.vessel.WriteText("TEXT")
    dlg.Destroy()

  def OnWindowModalDialogClosed(self, evt):
    dialog = evt.GetDialog()
    dialog.Destroy()
  
  def EvtText1(self, evt):
    self.vessel = evt.GetString()
  
  def EvtText2(self, evt):
    self.imo = evt.GetString()
      
    
if __name__ == '__main__':
  app = wx.App(False)
  MyFrame()
  app.MainLoop()