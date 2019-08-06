import wx
from addVessels import db_connect

class AddVessels(wx.Frame):
  def __init__(self, title='ADD VESSEL'):
    wx.Frame.__init__(self, None, title=title, size=(300,200))
    self.panel = wx.Panel(self)
    addVessel = wx.Button(self.panel, -1, "ADD Vessel", (10,130))
    self.Bind(wx.EVT_BUTTON, self.AddVesselButton, addVessel)
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

    sizer.Add(labelText1, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    sizer.Add(labelText2, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
    sizer.Add(labelText3, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

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
    
   
if __name__ == '__main__':
  app = wx.App(False)
  frame = AddVessels()
  frame.Show()
  app.MainLoop()