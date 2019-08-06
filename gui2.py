import wx
import wx.aui as aui
import wx.grid
from addVessels import db_connect

class AddVessels(wx.Frame):
  def __init__(self,id=-1,title='ADD VESSEL'):
    wx.Frame.__init__(self, None, title=title, size=(300,230))
    #Vessels LIST frame manager
    self.x = 0
    self._mgr = aui.AuiManager()
    self._mgr.SetManagedWindow(self)
    self._mgr.Update()
    self.Bind(wx.EVT_CLOSE, self.OnClose)
    #Vessels LIST frame manager END
    self.panel = wx.Panel(self)
    addVessel = wx.Button(self.panel, -1, "ADD Vessel")
    showVessels = wx.Button(self.panel, -1, "Show Vessels")
    self.Bind(wx.EVT_BUTTON, self.AddVesselButton, addVessel)
    self.Bind(wx.EVT_BUTTON, self.OnCreateGrid, showVessels )
    sizer = wx.BoxSizer(wx.VERTICAL)

    labelText1 = wx.BoxSizer(wx.HORIZONTAL)
    label1 = wx.StaticText(self.panel, -1, "Vessel name:")
    text1 = wx.TextCtrl(self.panel, -1, "")
    self.vessel = text1
    labelText1.Add(label1, 0, wx.ALL, 5)
    labelText1.Add(text1, 1, wx.ALL, 5)

    labelText2 = wx.BoxSizer(wx.HORIZONTAL)
    label2 = wx.StaticText(self.panel, -1, "IMO:")
    text2 = wx.TextCtrl(self.panel, -1, "")
    self.imo = text2  
    labelText2.Add(label2, 0, wx.ALL, 5)
    labelText2.Add(text2, 1, wx.ALL, 5)

    labelText3 = wx.BoxSizer(wx.HORIZONTAL)
    sampleList = ['','1','2','3','4','5','7','8','9']
    label3 = wx.StaticText(self.panel, -1, "Group number:")
    comboBox3 = wx.ComboBox(self.panel, value='',size=wx.DefaultSize, choices=sampleList,style=wx.CB_DROPDOWN|wx.CB_READONLY)
    self.groupNumber = comboBox3  
    labelText3.Add(label3, 0, wx.ALL, 5)
    labelText3.Add(comboBox3, 1, wx.ALL, 5)

    buttonGroup = wx.BoxSizer(wx.HORIZONTAL)
    buttonGroup.Add(addVessel, 0, wx.ALL, 5)
    buttonGroup.Add(showVessels, 0, wx.ALL, 5)
    
    sizer.Add(labelText1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    sizer.Add(labelText2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    sizer.Add(labelText3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    sizer.Add(buttonGroup, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

    self.panel.SetSizer(sizer)
    self.panel.SetAutoLayout(True)

  def AddVesselButton(self, evt):
    data ={
      'name' : self.vessel.GetValue(),
      'imo' : self.imo.GetValue(),
      'groupNumber':self.groupNumber.GetValue()
    }
    db_connect(data)
    self.groupNumber.Remove(0,-1)
    self.vessel.Remove(0,-1)
    self.imo.Remove(0,-1)
  
  def ShowVesselsButton(self,evt):
    grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250), wx.NO_BORDER | wx.WANTS_CHARS)
    grid.CreateGrid(50, 20)
    return grid
#Vessels LIST
  def OnClose(self,event):
    self._mgr.UnInit()
    del self._mgr
    self.Destroy()

  def GetStartPosition(self):
    self.x = self.x + 20
    x = self.x
    pt = self.ClientToScreen(wx.Point(0, 0))
    return wx.Point(pt.x + x, pt.y + x)


  def OnCreateGrid(self, event):
    self._mgr.AddPane(self.CreateGrid(), aui.AuiPaneInfo().
                      Caption("Vessels").
                      Float().FloatingPosition(self.GetStartPosition()).
                      FloatingSize(wx.Size(300, 200)).CloseButton(True).MaximizeButton(True))
    self._mgr.Update()
  
  def CreateGrid(self):
    grid = wx.grid.Grid(self, -1, wx.Point(0, 0), wx.Size(150, 250),wx.NO_BORDER | wx.WANTS_CHARS)
    grid.CreateGrid(50, 20)
    return grid
#Vessels LIST END
   
if __name__ == '__main__':
  app = wx.App(False)
  frame = AddVessels()
  frame.Show()
  app.MainLoop()