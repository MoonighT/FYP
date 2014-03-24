import wx
import sys
from subprocess import call
import active_learning
import generate_training_file

APP_EXIT = 1

class RedirectText:
    def __init__(self, aWxTextCtrl):
        self.out = aWxTextCtrl

    def write(self, string):
        self.out.WriteText(string)


class Page_demo(wx.Panel):
    def __init__(self, parent):
        self.dirname = ''
        self.demo_data = {}

        wx.Panel.__init__(self, parent)

        panel = self
        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(panel, label="Demo Phase")
        sizer.Add(text1, pos=(0,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1,0), span=(1,5), flag=wx.EXPAND|wx.BOTTOM, border=10)

    
        text3 = wx.StaticText(panel, label="Test File")
        sizer.Add(text3, pos=(2,0), flag=wx.LEFT|wx.TOP,border=10)

        self.tc_demofile = wx.TextCtrl(panel)
        sizer.Add(self.tc_demofile, pos=(2,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_browse1 = wx.Button(panel, label="Browse...")
        sizer.Add(button_browse1, pos=(2,4), flag=wx.TOP|wx.RIGHT, border=5)
        button_browse1.Bind(wx.EVT_BUTTON, self.OnOpen_demo)


        text_4 = wx.StaticText(panel, label="Output")
        sizer.Add(text_4, pos=(3,0), flag=wx.LEFT|wx.TOP, border=10)

        self.tc_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.tc_output, pos=(3,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_test = wx.Button(panel, label="Demo!")
        sizer.Add(button_test, pos=(4,5), flag=wx.RIGHT|wx.BOTTOM, border=10)
        button_test.Bind(wx.EVT_BUTTON, self.Demo)

        sizer.AddGrowableRow(3)
        sizer.AddGrowableCol(1,2)
        panel.SetSizer(sizer)

        redir = RedirectText(self.tc_output)
        sys.stdout = redir


    def OnOpen_demo(self, e):
        self.file_open()
        e.Skip()

    def file_open(self):
        with wx.FileDialog(self, "Choose a file to open", self.dirname,
                           "", "*.*", wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.tc_output.LoadFile('/'.join((directory, filename)))
                self.demo_data["directory"] = directory
                self.demo_data["filename"] = filename
                self.tc_demofile.SetValue(filename)

    def Demo(self, e):
        demo_directory = '/'.join(self.demo_data.values())
        self.tc_output.SetValue("")
        active_learning.runDemo(demo_directory)

class Page_test(wx.Panel):
    def __init__(self, parent):
        self.dirname = ''
        self.test_data = {}

        wx.Panel.__init__(self, parent)

        panel = self
        sizer = wx.GridBagSizer(5, 5)

        text1 = wx.StaticText(panel, label="Testing Phase")
        sizer.Add(text1, pos=(0,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1,0), span=(1,5), flag=wx.EXPAND|wx.BOTTOM, border=10)

        text_2 = wx.StaticText(panel, label="Test Command")
        sizer.Add(text_2, pos=(2,0), flag=wx.LEFT, border=10)

        self.tc_command = wx.TextCtrl(panel)
        sizer.Add(self.tc_command, pos=(2,1), span=(1,2), flag=wx.TOP|wx.EXPAND)
    
        text3 = wx.StaticText(panel, label="Test File")
        sizer.Add(text3, pos=(3,0), flag=wx.LEFT|wx.TOP,border=10)

        self.tc_testfile = wx.TextCtrl(panel)
        sizer.Add(self.tc_testfile, pos=(3,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_browse1 = wx.Button(panel, label="Browse...")
        sizer.Add(button_browse1, pos=(3,4), flag=wx.TOP|wx.RIGHT, border=5)
        button_browse1.Bind(wx.EVT_BUTTON, self.OnOpen_test)


        text_4 = wx.StaticText(panel, label="Output")
        sizer.Add(text_4, pos=(4,0), flag=wx.LEFT|wx.TOP, border=10)

        self.tc_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.tc_output, pos=(4,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_test = wx.Button(panel, label="Test!")
        sizer.Add(button_test, pos=(5,5), flag=wx.RIGHT|wx.BOTTOM, border=10)
        button_test.Bind(wx.EVT_BUTTON, self.Test)

        sizer.AddGrowableRow(4)
        sizer.AddGrowableCol(1,2)
        panel.SetSizer(sizer)

        redir = RedirectText(self.tc_output)
        sys.stdout = redir


    def Test(self, e):
        test_command = self.tc_command.GetValue()
        test_directory = '/'.join(self.test_data.values())
        self.tc_output.SetValue("")
        active_learning.runActiveLearning(test_directory, True)

    def OnOpen_test(self, e):
        self.file_open()
        e.Skip()
    

    def file_open(self):
        with wx.FileDialog(self, "Choose a file to open", self.dirname,
                           "", "*.*", wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.tc_output.LoadFile('/'.join((directory, filename)))
                self.test_data["directory"] = directory
                self.test_data["filename"] = filename
                self.tc_testfile.SetValue(filename)


class Page_dev(wx.Panel):
    def __init__(self, parent):
        self.dirname = ''
        self.dev_data = {}
        self.parent = parent

        wx.Panel.__init__(self, parent)

        panel = self
        sizer = wx.GridBagSizer(6, 5)

        text1 = wx.StaticText(panel, label="Developing Phase")
        sizer.Add(text1, pos=(0,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1,0), span=(1,5), flag=wx.EXPAND|wx.BOTTOM, border=10)

        text_2 = wx.StaticText(panel, label="Dev Command")
        sizer.Add(text_2, pos=(2,0), flag=wx.LEFT, border=10)

        self.tc_command = wx.TextCtrl(panel)
        sizer.Add(self.tc_command, pos=(2,1), span=(1,2), flag=wx.TOP|wx.EXPAND)
    
        text3 = wx.StaticText(panel, label="Develop File")
        sizer.Add(text3, pos=(3,0), flag=wx.LEFT|wx.TOP,border=10)

        self.tc_devfile = wx.TextCtrl(panel)
        sizer.Add(self.tc_devfile, pos=(3,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_browse1 = wx.Button(panel, label="Browse...")
        sizer.Add(button_browse1, pos=(3,4), flag=wx.TOP|wx.RIGHT, border=5)
        button_browse1.Bind(wx.EVT_BUTTON, self.OnOpen_dev)


        text_4 = wx.StaticText(panel, label="Output")
        sizer.Add(text_4, pos=(4,0), flag=wx.LEFT|wx.TOP, border=10)

        self.tc_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.tc_output, pos=(4,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)


        text_5 = wx.StaticText(panel, label="Conditional Probability")
        sizer.Add(text_5, pos=(5,0), flag=wx.LEFT|wx.TOP, border=10)

        self.tc_prob = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.tc_prob, pos=(5,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)



        button_dev = wx.Button(panel, label="Train!")
        sizer.Add(button_dev, pos=(6,4), flag=wx.RIGHT|wx.BOTTOM, border=10)
        button_dev.Bind(wx.EVT_BUTTON, self.Dev)


        button_dev = wx.Button(panel, label="Update!")
        sizer.Add(button_dev, pos=(6,5), flag=wx.RIGHT|wx.BOTTOM, border=10)
        button_dev.Bind(wx.EVT_BUTTON, self.Update)

        sizer.AddGrowableRow(4)
        sizer.AddGrowableCol(1,2)
        panel.SetSizer(sizer)

        redir = RedirectText(self.tc_output)
        sys.stdout = redir


    def Dev(self, e):
        dev_command = self.tc_command.GetValue()
        dev_directory = '/'.join(self.dev_data.values())
        self.tc_output.SetValue("")
        least_con = active_learning.runActiveLearning(dev_directory)
        value = ''
        for w, t in least_con['content']:
            value += w + '\\' + t + ' '

        self.tc_output.SetValue(str(value))
        self.tc_prob.SetValue(str(least_con['prob']))

    def Update(self, e):
        new_label = self.tc_output.GetValue()
        self.tc_output.SetValue('')
        train_directory = '/'.join(self.parent.GetPage(0).train_data.values())
        template_directory = '/'.join(self.parent.GetPage(0).template.values())
        generate_training_file.activeUpdate(new_label, train_directory)
        call("crf_learn -f 2 -c 1.5 "+template_directory+" "+train_directory+" model",shell=True)
        self.Dev(e)

    def OnOpen_dev(self, e):
        self.file_open()
        e.Skip()
    

    def file_open(self):
        with wx.FileDialog(self, "Choose a file to open", self.dirname,
                           "", "*.*", wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.tc_output.LoadFile('/'.join((directory, filename)))
                self.dev_data["directory"] = directory
                self.dev_data["filename"] = filename
                self.tc_devfile.SetValue(filename)

class Page_train(wx.Panel):

    def __init__(self, parent):

        self.dirname = ''
        self.train_data = {}
        self.template = {}

        #layout

        wx.Panel.__init__(self, parent)

        panel = self
        sizer = wx.GridBagSizer(6, 5)


        text1 = wx.StaticText(panel, label="Trainning Phase")
        sizer.Add(text1, pos=(0,0), flag=wx.TOP|wx.LEFT|wx.BOTTOM, border=15)

        line = wx.StaticLine(panel)
        sizer.Add(line, pos=(1,0), span=(1,5), flag=wx.EXPAND|wx.BOTTOM, border=10)

        text_2 = wx.StaticText(panel, label="Train Command")
        sizer.Add(text_2, pos=(2,0), flag=wx.LEFT, border=10)

        self.tc_command = wx.TextCtrl(panel)
        sizer.Add(self.tc_command, pos=(2,1), span=(1,2), flag=wx.TOP|wx.EXPAND)
    
        text3 = wx.StaticText(panel, label="Train File")
        sizer.Add(text3, pos=(3,0), flag=wx.LEFT|wx.TOP,border=10)

        self.tc_trainfile = wx.TextCtrl(panel)
        sizer.Add(self.tc_trainfile, pos=(3,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_browse1 = wx.Button(panel, label="Browse...")
        sizer.Add(button_browse1, pos=(3,4), flag=wx.TOP|wx.RIGHT, border=5)
        button_browse1.Bind(wx.EVT_BUTTON, self.OnOpen_train)

        text4 = wx.StaticText(panel, label="Template File")
        sizer.Add(text4, pos=(4,0), flag=wx.LEFT|wx.TOP,border=10)

        self.tc_template = wx.TextCtrl(panel)
        sizer.Add(self.tc_template, pos=(4,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_browse2 = wx.Button(panel, label="Browse...")
        sizer.Add(button_browse2, pos=(4,4), flag=wx.TOP|wx.RIGHT, border=5)
        button_browse2.Bind(wx.EVT_BUTTON, self.OnOpen_template)

        text_5 = wx.StaticText(panel, label="Output")
        sizer.Add(text_5, pos=(5,0), flag=wx.LEFT|wx.TOP, border=10)

        self.tc_output = wx.TextCtrl(panel, style=wx.TE_MULTILINE)
        sizer.Add(self.tc_output, pos=(5,1), span=(1,2), flag=wx.TOP|wx.EXPAND, border=5)

        button_train = wx.Button(panel, label="Train!")
        sizer.Add(button_train, pos=(6,5), flag=wx.RIGHT|wx.BOTTOM, border=10)
        button_train.Bind(wx.EVT_BUTTON, self.Train)

        sizer.AddGrowableRow(5)
        sizer.AddGrowableCol(1,2)
        panel.SetSizer(sizer)

        redir = RedirectText(self.tc_output)
        sys.stdout = redir

    #event
    def Train(self, e):
        train_command = self.tc_command.GetValue()
        train_directory = '/'.join(self.train_data.values())
        template_directory = '/'.join(self.template.values())
        result = call("crf_learn -f 2 -c 1.5 "+template_directory+" "+train_directory+" model",shell=True)
        self.tc_output.SetValue("done")


    def OnOpen_train(self, e):
        self.file_open("train")
        e.Skip()

    def OnOpen_template(self, e):
        self.file_open("template")
        e.Skip()        

    def file_open(self, type):
        with wx.FileDialog(self, "Choose a file to open", self.dirname,
                           "", "*.*", wx.OPEN) as dlg:
            if dlg.ShowModal() == wx.ID_OK:
                directory, filename = dlg.GetDirectory(), dlg.GetFilename()
                self.tc_output.LoadFile('/'.join((directory, filename)))
                if type == "train":
                    self.train_data["directory"] = directory
                    self.train_data["filename"] = filename
                    self.tc_trainfile.SetValue(filename)
                elif type == "template":
                    self.tc_template.SetValue(filename)
                    self.template["directory"] = directory
                    self.template["filename"] = filename

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super(MyFrame,self).__init__(parent, title=title,size=(800,600))
        self.InitUI()
        self.Centre()
        self.Show()

    def InitUI(self):

        #manubar
        menubar = wx.MenuBar()
        fileMenu = wx.Menu()
        viewMenu = wx.Menu()

        #manu file items
        fileMenu.Append(wx.ID_NEW, '&New')
        fileMenu.Append(wx.ID_OPEN,'&Open')
        fileMenu.Append(wx.ID_SAVE, '&Save')
        fileMenu.AppendSeparator()


        qmi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        fileMenu.AppendItem(qmi)

        self.Bind(wx.EVT_MENU, self.onQuit, id=APP_EXIT)
        
        #manu view items
        self.shst = viewMenu.Append(wx.ID_ANY, 'Show statubar',
                'Show Statusbar', kind=wx.ITEM_CHECK)
        self.shtl = viewMenu.Append(wx.ID_ANY, 'Show toolbar',
                'Show Toolbar', kind=wx.ITEM_CHECK)
        viewMenu.Check(self.shst.GetId(), True)
        viewMenu.Check(self.shtl.GetId(), True)

        self.Bind(wx.EVT_MENU, self.ToggleStatusBar, self.shst)
        self.Bind(wx.EVT_MENU, self.ToggleToolBar, self.shtl)

        #menubar append
        menubar.Append(fileMenu, '&File')
        menubar.Append(viewMenu, '&View')
        self.SetMenuBar(menubar)
        
        #tool bar
        self.toolbar = self.CreateToolBar()
        self.toolbar.Realize()

        #status bar
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')

        #size title position
        self.SetTitle('Active labelling')
  
        #add pages
        p = wx.Panel(self)
        nb = wx.Notebook(p)

        # create the page windows as children of the notebook
        page_train = Page_train(nb)
        page_dev = Page_dev(nb)
        page_test = Page_test(nb)
        page_demo = Page_demo(nb)
        # add the pages to the notebook with the label to show on the tab
        nb.AddPage(page_train, "Train")
        nb.AddPage(page_dev, "Development")
        nb.AddPage(page_test, "Test")
        nb.AddPage(page_demo, "Demo")

        sizer = wx.BoxSizer()
        sizer.Add(nb, 1, wx.EXPAND)
        p.SetSizer(sizer)
        

    #event
    

    def ToggleStatusBar(self, e):
        if self.shst.IsChecked():
            self.statusbar.Show()
        else:
            self.statusbar.Hide()

    def ToggleToolBar(self,e):
        if self.shtl.IsChecked():
            self.toolbar.Show()
        else:
            self.toolbar.Hide()

    def onQuit(self,e):
        self.Close()

def main():
    ex = wx.App()
    MyFrame(None,title="active labelling")
    ex.MainLoop()

if __name__=='__main__':
    main()
